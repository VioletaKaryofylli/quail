import numpy as np 
from Basis import *
from Quadrature import *
from Mesh import *
import code
import copy
from Data import ArrayList, GenericData
from SolverTools import *
from Stepper import *
import time
import MeshTools
import Post
import Errors
from scipy.optimize import fsolve, root

import Limiter

global echeck
echeck = -1


class ElemOperators(object):
	def __init__(self):
		self.quad_pts = None
		self.quad_wts = None
		self.basis_val = None 
		self.basis_grad = None 
		self.basis_pgrad_elems = None 
		self.gbasis_val = None 
		self.jac_elems = None 
		self.ijac_elems = None 
		self.djac_elems = None 
		self.x_elems = None
		self.Uq = None 
		self.Fq = None 
		self.Sq = None 

	def get_gaussian_quadrature(self, mesh, EqnSet, basis, order):

		QuadOrder, _ = get_gaussian_quadrature_elem(mesh, mesh.gbasis, order, EqnSet, None)
		quadData = QuadData(mesh, basis, EntityType.Element, QuadOrder)
		self.quad_pts = quadData.quad_pts
		self.quad_wts = quadData.quad_wts

	def get_basis_and_geom_data(self, mesh, basis, order):
		# separate these later

		# Unpack
		dim = mesh.Dim 
		nElem = mesh.nElem 
		quad_pts = self.quad_pts 
		nq = quad_pts.shape[0]
		nb = basis.nb

		# Allocate
		self.jac_elems = np.zeros([nElem,nq,dim,dim])
		self.ijac_elems = np.zeros([nElem,nq,dim,dim])
		self.djac_elems = np.zeros([nElem,nq,1])
		self.x_elems = np.zeros([nElem,nq,dim])
		self.basis_pgrad_elems = np.zeros([nElem,nq,nb,dim])

		GeomPhiData = None

		# basis data
		basis.eval_basis(self.quad_pts, Get_Phi=True, Get_GPhi=True)

		self.basis_val = basis.basis_val 
		self.basis_grad = basis.basis_grad 

		for elem in range(mesh.nElem):
			# Jacobian
			djac, jac, ijac = element_jacobian(mesh, elem, quad_pts, get_djac=True, get_jac=True, get_ijac=True)
			# Store
			self.jac_elems[elem] = jac
			self.ijac_elems[elem] = ijac
			self.djac_elems[elem] = djac

			# Physical coordinates of quadrature points
			x, GeomPhiData = ref_to_phys(mesh, elem, GeomPhiData, quad_pts)
			# Store
			self.x_elems[elem] = x
			# Physical gradient
			basis.eval_basis(quad_pts, Get_gPhi=True, ijac=ijac) # gPhi is [nq,nb,dim]
			self.basis_pgrad_elems[elem] = basis.basis_pgrad

	def alloc_other_arrays(self, EqnSet, basis, order):
		quad_pts = self.quad_pts 
		nq = quad_pts.shape[0]
		nb = basis.nb
		ns = EqnSet.StateRank
		dim = EqnSet.Dim

		self.Uq = np.zeros([nq, ns]) 
		self.Fq = np.zeros([nq, ns, dim])
		self.Sq = np.zeros([nq, ns])  

	def compute_operators(self, mesh, EqnSet, basis, order):
		self.get_gaussian_quadrature(mesh, EqnSet, basis, order)
		self.get_basis_and_geom_data(mesh, basis, order)
		self.alloc_other_arrays(EqnSet, basis, order)


class IFaceOperators(ElemOperators):
	def __init__(self):
		self.quad_pts = None
		self.quad_wts = None
		self.faces_to_basisL = None
		self.faces_to_basisR = None
		self.normals_ifaces = None
		self.UqL = None 
		self.UqR = None 
		self.Fq = None 

	def get_gaussian_quadrature(self, mesh, EqnSet, basis, order):

		QuadOrder, _ = get_gaussian_quadrature_face(mesh, None, mesh.gbasis, order, EqnSet, None)
		quadData = QuadData(mesh, basis, EntityType.IFace, QuadOrder)
		self.quad_pts = quadData.quad_pts
		self.quad_wts = quadData.quad_wts

	def get_basis_and_geom_data(self, mesh, basis, order):
		# separate these later

		# Unpack
		dim = mesh.Dim
		quad_pts = self.quad_pts 
		nq = quad_pts.shape[0]
		nb = basis.nb
		nFacePerElem = mesh.nFacePerElem

		# Allocate
		self.faces_to_basisL = np.zeros([nFacePerElem,nq,nb])
		self.faces_to_basisR = np.zeros([nFacePerElem,nq,nb])
		self.normals_ifaces = np.zeros([mesh.nIFace,nq,dim])

		# basis data
		#PhiData = BasisData(basis, order, mesh)

		for f in range(nFacePerElem):
			# Left
			_ = basis.eval_basis_on_face(mesh, f, quad_pts, None, Get_Phi=True)
			self.faces_to_basisL[f] = basis.basis_val
			# Right
			_ = basis.eval_basis_on_face(mesh, f, quad_pts[::-1], None, Get_Phi=True)
			self.faces_to_basisR[f] = basis.basis_val

		i = 0
		for IFace in mesh.IFaces:
			# Normals
			nvec = iface_normal(mesh, IFace, quad_pts)
			self.normals_ifaces[i] = nvec
			i += 1

	def alloc_other_arrays(self, EqnSet, basis, order):
		quad_pts = self.quad_pts 
		nq = quad_pts.shape[0]
		ns = EqnSet.StateRank

		self.UqL = np.zeros([nq, ns])
		self.UqR = np.zeros([nq, ns])
		self.Fq = np.zeros([nq, ns])

	def compute_operators(self, mesh, EqnSet, basis, order):
		self.get_gaussian_quadrature(mesh, EqnSet, basis, order)
		self.get_basis_and_geom_data(mesh, basis, order)
		self.alloc_other_arrays(EqnSet, basis, order)


class BFaceOperators(IFaceOperators):
	def __init__(self):
		self.quad_pts = None
		self.quad_wts = None
		self.faces_to_basis = None
		self.faces_to_xref = None
		self.normals_bfgroups = None
		self.x = None
		self.UqI = None 
		self.UqB = None 
		self.Fq = None 

	def get_basis_and_geom_data(self, mesh, basis, order):
		# separate these later

		# Unpack
		dim = mesh.Dim
		quad_pts = self.quad_pts 
		nq = quad_pts.shape[0]
		nb = basis.nb
		nFacePerElem = mesh.nFacePerElem

		# Allocate
		self.faces_to_basis = np.zeros([nFacePerElem,nq,nb])
		self.faces_to_xref = np.zeros([nFacePerElem,nq,dim])
		self.normals_bfgroups = []
		self.x_bfgroups = []

		# basis data
		# PhiData = BasisData(basis, order, mesh)
		GeomPhiData = None

		for f in range(nFacePerElem):
			# Left
			self.faces_to_xref[f] = xref = basis.eval_basis_on_face(mesh, f, quad_pts, None, Get_Phi=True)
			self.faces_to_basis[f] = basis.basis_val

		i = 0
		for BFG in mesh.BFaceGroups:
			self.normals_bfgroups.append(np.zeros([BFG.nBFace,nq,dim]))
			self.x_bfgroups.append(np.zeros([BFG.nBFace,nq,dim]))
			normal_bfgroup = self.normals_bfgroups[i]
			x_bfgroup = self.x_bfgroups[i]
			j = 0
			for BFace in BFG.BFaces:
				# Normals
				nvec = bface_normal(mesh, BFace, quad_pts)
				normal_bfgroup[j] = nvec

				# Physical coordinates of quadrature points
				x, GeomPhiData = ref_to_phys(mesh, BFace.Elem, GeomPhiData, self.faces_to_xref[BFace.face], None, True)
				# Store
				x_bfgroup[j] = x

				# Increment
				j += 1
			i += 1

	def alloc_other_arrays(self, EqnSet, basis, order):
		quad_pts = self.quad_pts 
		nq = quad_pts.shape[0]
		ns = EqnSet.StateRank

		self.UqI = np.zeros([nq, ns])
		self.UqB = np.zeros([nq, ns])
		self.Fq = np.zeros([nq, ns])

	def compute_operators(self, mesh, EqnSet, basis, order):
		self.get_gaussian_quadrature(mesh, EqnSet, basis, order)
		self.get_basis_and_geom_data(mesh, basis, order)
		self.alloc_other_arrays(EqnSet, basis, order)
		
#class ADEROperators(object):



class DG_Solver(object):
	'''
	Class: DG_Solver
	--------------------------------------------------------------------------
	Discontinuous Galerkin method designed to solve a given set of PDEs

	ATTRIBUTES:
		Params: list of parameters for the solver
		EqnSet: solver object (current implementation supports Scalar and Euler equations)
		mesh: mesh object
		DataSet: location to store generic data
		Time: current time in the simulation
		nTimeStep: number of time steps
	'''
	def __init__(self,Params,EqnSet,mesh):
		'''
		Method: __init__
		--------------------------------------------------------------------------
		Initializes the DG_Solver object, verifies parameters, and initializes the state

		INPUTS:
			Params: list of parameters for the solver
			EqnSet: solver object (current implementation supports Scalar and Euler equations)
			mesh: mesh object
		'''

		self.Params = Params
		self.EqnSet = EqnSet
		self.mesh = mesh
		self.DataSet = GenericData()

		self.Time = Params["StartTime"]
		self.nTimeStep = 0 # will be set later

		TimeScheme = Params["TimeScheme"]
		if TimeScheme is "FE":
			Stepper = FE()
		elif TimeScheme is "RK4":
			Stepper = RK4()
		elif TimeScheme is "LSRK4":
			Stepper = LSRK4()
		elif TimeScheme is "SSPRK3":
			Stepper = SSPRK3()
		elif TimeScheme is "ADER":
			Stepper = ADER()
		else:
			raise NotImplementedError("Time scheme not supported")
		# if Params["nTimeStep"] > 0:
		# 	Stepper.dt = Params["EndTime"]/Params["nTimeStep"]
		self.Stepper = Stepper

		# Set the basis functions for the solver
		BasisFunction  = Params["InterpBasis"]
		if BasisFunction is "LagrangeSeg":
			basis = LagrangeSeg(EqnSet.Order, mesh)
		elif BasisFunction is "LegendreSeg":
			basis = LegendreSeg(EqnSet.Order, mesh)
		elif BasisFunction is "LagrangeQuad":
			basis = LagrangeQuad(EqnSet.Order, mesh)
		elif BasisFunction is "LegendreQuad":
			basis = LegendreQuad(EqnSet.Order, mesh)
		elif BasisFunction is "LagrangeTri":
			basis = LagrangeTri(EqnSet.Order, mesh)
		else:
			raise NotImplementedError
		self.basis = basis

		# Set the space-time basis if using the ADER-DG solver
		if TimeScheme is "ADER":
			if BasisFunction is "LagrangeSeg":
				basis_st = LagrangeQuad(EqnSet.Order, mesh)
			elif BasisFunction is "LegendreSeg":
				basis_st = LegendreQuad(EqnSet.Order, mesh)
			else:
				raise NotImplementedError

			self.basis_st = basis_st

		# Limiter
		limiterType = Params["ApplyLimiter"]
		self.Limiter = Limiter.set_limiter(limiterType)

		# Check validity of parameters
		self.check_solver_params()

		# Initialize state
		self.init_state()

		# Precompute operators
		self.precompute_matrix_operators()

	def check_solver_params(self):
		'''
		Method: check_solver_params
		--------------------------------------------------------------------------
		Checks the validity of the solver parameters

		'''
		Params = self.Params
		mesh = self.mesh
		EqnSet = self.EqnSet
		### Check interp basis validity
		if BasisType[Params["InterpBasis"]] == BasisType.LagrangeSeg or BasisType[Params["InterpBasis"]] == BasisType.LegendreSeg:
		    if mesh.Dim != 1:
		        raise Errors.IncompatibleError
		else:
		    if mesh.Dim != 2:
		        raise Errors.IncompatibleError

		### Check uniform mesh
		if Params["UniformMesh"] is True:
		    ''' 
		    Check that element volumes are the same
		    Note that this is a necessary but not sufficient requirement
		    '''
		    TotVol, ElemVols = MeshTools.element_volumes(mesh)
		    if (ElemVols.Max - ElemVols.Min)/TotVol > 1.e-8:
		        raise ValueError

		### Check linear geometric mapping
		if Params["LinearGeomMapping"] is True:
			if mesh.QOrder != 1:
			    raise Errors.IncompatibleError
			if mesh.QBasis == BasisType.LagrangeQuad \
			    and Params["UniformMesh"] is False:
			    raise Errors.IncompatibleError

		### Check limiter ###
		if Params["ApplyLimiter"] is 'ScalarPositivityPreserving' \
			and EqnSet.StateRank > 1:
				raise IncompatibleError
		if Params["ApplyLimiter"] is 'PositivityPreserving' \
			and EqnSet.StateRank == 1:
				raise IncompatibleError

		### Check time integration scheme ###
		TimeScheme = Params["TimeScheme"]		
		if TimeScheme is "ADER":
			raise Errors.IncompatibleError

		### Force the BasisADER to be None ###
		EqnSet.BasisADER = 0 #dummy


	def precompute_matrix_operators(self):
		mesh = self.mesh 
		EqnSet = self.EqnSet
		basis = self.basis

		self.elem_operators = ElemOperators()
		self.elem_operators.compute_operators(mesh, EqnSet, basis, EqnSet.Order)
		self.iface_operators = IFaceOperators()
		self.iface_operators.compute_operators(mesh, EqnSet, basis, EqnSet.Order)
		self.bface_operators = BFaceOperators()
		self.bface_operators.compute_operators(mesh, EqnSet, basis, EqnSet.Order)

	def init_state(self):
		'''
		Method: init_state
		-------------------------
		Initializes the state based on prescribed initial conditions
		
		'''
		mesh = self.mesh
		EqnSet = self.EqnSet
		basis = self.basis

		nb = basis.nb

		U = EqnSet.U
		ns = EqnSet.StateRank
		Params = self.Params

		# Get mass matrices
		try:
			iMM = self.DataSet.iMM_all
		except AttributeError:
			# not found; need to compute
			iMM_all = get_inv_mass_matrices(mesh, EqnSet, solver=self)

		InterpolateIC = Params["InterpolateIC"]
		quadData = None
		# JData = JacobianData(mesh)
		GeomPhiData = None
		quad_pts = None
		xphys = None

		#basis = EqnSet.Basis
		order = EqnSet.Order
		rhs = np.zeros([nb,ns],dtype=U.dtype)

		# Precompute basis and quadrature
		if not InterpolateIC:
			QuadOrder,_ = get_gaussian_quadrature_elem(mesh, basis,
				2*np.amax([order,1]), EqnSet, quadData)

			quadData = QuadData(mesh, mesh.gbasis, EntityType.Element, QuadOrder)

			quad_pts = quadData.quad_pts
			quad_wts = quadData.quad_wts
			nq = quad_pts.shape[0]

			#PhiData = BasisData(basis,order,mesh)
			basis.eval_basis(quad_pts, Get_Phi=True)
			xphys = np.zeros([nq, mesh.Dim])
		
		else:
			quad_pts, nq = basis.equidistant_nodes(order, quad_pts)
			#nb = nq

		for elem in range(mesh.nElem):

			xphys, GeomPhiData = ref_to_phys(mesh, elem, GeomPhiData, quad_pts, xphys)

			f = EqnSet.CallFunction(EqnSet.IC, x=xphys, Time=self.Time)
			f.shape = nq,ns

			if not InterpolateIC:

				djac,_,_ = element_jacobian(mesh,elem,quad_pts,get_djac=True)

				iMM = iMM_all[elem]

				# rhs *= 0.
				# for n in range(nn):
				# 	for iq in range(nq):
				# 		rhs[n,:] += f[iq,:]*PhiData.Phi[iq,n]*quad_wts[iq]*JData.djac[iq*(JData.nq != 1)]

				rhs[:] = np.matmul(basis.basis_val.transpose(), f*quad_wts*djac) # [nb, ns]

				U[elem,:,:] = np.matmul(iMM,rhs)
			else:
				U[elem] = f

	def apply_limiter(self, U):
		'''
		Method: apply_limiter
		-------------------------
		Applies the limiter to the solution array, U.
		
		INPUTS:
			U: solution array

		OUTPUTS:
			U: limited solution array

		Notes: See Limiter.py for details
		'''
		if self.Limiter is not None:
			self.Limiter.limit_solution(self, U)


	def calculate_residual_elem(self, elem, Up, ER, StaticData):
		'''
		Method: calculate_residual_elem
		---------------------------------
		Calculates the volume integral for a specified element
		
		INPUTS:
			elem: element index
			U: solution array
			
		OUTPUTS:
			ER: calculated residiual array (for volume integral of specified element)
		'''
		EqnSet = self.EqnSet
		ns = EqnSet.StateRank
		dim = EqnSet.Dim

		elem_ops = self.elem_operators
		quad_wts = elem_ops.quad_wts
		basis_val = elem_ops.basis_val 
		basis_pgrad_elems = elem_ops.basis_pgrad_elems
		djac_elems = elem_ops.djac_elems 
		x_elems = elem_ops.x_elems
		Sq = elem_ops.Sq

		# Unpack
		basis_pgrad = basis_pgrad_elems[elem]
		djac = djac_elems[elem]
		nq = quad_wts.shape[0]
		x = x_elems[elem]

		# interpolate state and gradient at quad points
		Uq = np.matmul(basis_val, Up)

		Fq = EqnSet.ConvFluxInterior(Uq, F=None) # [nq,ns,dim]

		# for ir in range(ns):
		# 	for jn in range(nb):
		# 		for iq in range(nq):
		# 			gPhi = PhiData.gPhi[iq,jn] # dim
		# 			ER[jn,ir] += np.dot(gPhi, F[iq,ir,:])*wq[iq]*JData.djac[iq*(JData.nq!=1)]

		ER += np.tensordot(basis_pgrad, Fq*(quad_wts*djac).reshape(nq,1,1), axes=([0,2],[0,2])) # [nb, ns]

		Sq[:] = 0. # SourceState is an additive function so source needs to be initialized to zero for each time step
		Sq = EqnSet.SourceState(nq, x, self.Time, Uq, Sq) # [nq,ns]

		# Calculate source term integral
		# for ir in range(sr):
		# 	for jn in range(nn):
		# 		for iq in range(nq):
		# 			Phi = PhiData.Phi[iq,jn]
		# 			ER[jn,ir] += Phi*s[iq,ir]*wq[iq]*JData.djac[iq*(JData.nq!=1)]

		ER += np.matmul(basis_val.transpose(), Sq*quad_wts*djac) # [nb, ns]

		if elem == echeck:
			code.interact(local=locals())

		return ER, StaticData

	def calculate_residual_elems(self, U, R):
		'''
		Method: calculate_residual_elems
		---------------------------------
		Calculates the volume integral across the entire domain
		
		INPUTS:
			U: solution array
			
		OUTPUTS:
			R: calculated residiual array
		'''
		mesh = self.mesh
		EqnSet = self.EqnSet
		StaticData = None

		for elem in range(mesh.nElem):
			R[elem], StaticData = self.calculate_residual_elem(elem, U[elem], R[elem], StaticData)


	def calculate_residual_iface(self, iiface, UpL, UpR, RL, RR, StaticData):
		'''
		Method: calculate_residual_iface
		---------------------------------
		Calculates the boundary integral for the internal faces
		
		INPUTS:
			iiface: internal face index
			UL: solution array from left neighboring element
			UR: solution array from right neighboring element
			
		OUTPUTS:
			RL: calculated residual array (left neighboring element contribution)
			RR: calculated residual array (right neighboring element contribution)
		'''
		mesh = self.mesh
		EqnSet = self.EqnSet
		IFace = mesh.IFaces[iiface]
		elemL = IFace.ElemL
		elemR = IFace.ElemR
		faceL = IFace.faceL
		faceR = IFace.faceR

		iface_ops = self.iface_operators
		quad_pts = iface_ops.quad_pts
		quad_wts = iface_ops.quad_wts
		faces_to_basisL = iface_ops.faces_to_basisL
		faces_to_basisR = iface_ops.faces_to_basisR
		normals_ifaces = iface_ops.normals_ifaces
		UqL = iface_ops.UqL
		UqR = iface_ops.UqR
		Fq = iface_ops.Fq

		nq = quad_wts.shape[0]
		basis_valL = faces_to_basisL[faceL]
		basis_valR = faces_to_basisR[faceR]

		# interpolate state and gradient at quad points
		UqL = np.matmul(basis_valL, UpL)
		UqR = np.matmul(basis_valR, UpR)

		normals = normals_ifaces[iiface]

		if StaticData is None:
			StaticData = GenericData()

		Fq = EqnSet.ConvFluxNumerical(UqL, UqR, normals, nq, StaticData) # [nq,ns]

		RL -= np.matmul(basis_valL.transpose(), Fq*quad_wts) # [nb,sr]
		RR += np.matmul(basis_valR.transpose(), Fq*quad_wts) # [nb,sr]

		if elemL == echeck or elemR == echeck:
			if elemL == echeck: print("Left!")
			else: print("Right!")
			code.interact(local=locals())

		return RL, RR, StaticData



	def calculate_residual_ifaces(self, U, R):
		'''
		Method: calculate_residual_ifaces
		-----------------------------------
		Calculates the boundary integral for all internal faces
		
		INPUTS:
			U: solution array
			
		OUTPUTS:
			R: calculated residual array (includes all face contributions)
		'''
		mesh = self.mesh
		EqnSet = self.EqnSet
		StaticData = None

		for iiface in range(mesh.nIFace):
			IFace = mesh.IFaces[iiface]
			elemL = IFace.ElemL
			elemR = IFace.ElemR
			faceL = IFace.faceL
			faceR = IFace.faceR

			UL = U[elemL]
			UR = U[elemR]
			RL = R[elemL]
			RR = R[elemR]

			RL, RR, StaticData = self.calculate_residual_iface(iiface, UL, UR, RL, RR, StaticData)

	def calculate_residual_bface(self, ibfgrp, ibface, U, R, StaticData):
		'''
		Method: calculate_residual_bface
		---------------------------------
		Calculates the boundary integral for the boundary faces
		
		INPUTS:
			ibfgrp: index of boundary face groups (groups indicate different boundary conditions)
			ibface: boundary face index
			U: solution array from internal cell
			
		OUTPUTS:
			R: calculated residual array from boundary face
		'''
		mesh = self.mesh
		EqnSet = self.EqnSet
		BFG = mesh.BFaceGroups[ibfgrp]
		BFace = BFG.BFaces[ibface]
		elem = BFace.Elem
		face = BFace.face

		bface_ops = self.bface_operators
		quad_pts = bface_ops.quad_pts
		quad_wts = bface_ops.quad_wts
		faces_to_basis = bface_ops.faces_to_basis
		normals_bfgroups = bface_ops.normals_bfgroups
		x_bfgroups = bface_ops.x_bfgroups
		UqI = bface_ops.UqI
		UqB = bface_ops.UqB
		Fq = bface_ops.Fq

		nq = quad_wts.shape[0]
		basis_val = faces_to_basis[face]

		# interpolate state and gradient at quad points
		UqI = np.matmul(basis_val, U)

		normals = normals_bfgroups[ibfgrp][ibface]
		x = x_bfgroups[ibfgrp][ibface]

		# Get boundary state
		BC = EqnSet.BCs[ibfgrp]
		UqB = EqnSet.BoundaryState(BC, nq, x, self.Time, normals, UqI, UqB)

		if StaticData is None:
			StaticData = GenericData()

		Fq = EqnSet.ConvFluxBoundary(BC, UqI, UqB, normals, nq, StaticData) # [nq,sr]

		R -= np.matmul(basis_val.transpose(), Fq*quad_wts) # [nn,sr]

		if elem == echeck:
			code.interact(local=locals())

		return R, StaticData


	def calculate_residual_bfaces(self, U, R):
		'''
		Method: calculate_residual_bfaces
		-----------------------------------
		Calculates the boundary integral for all the boundary faces
		
		INPUTS:
			U: solution array from internal cell
			
		OUTPUTS:
			R: calculated residual array from boundary face
		'''
		mesh = self.mesh
		EqnSet = self.EqnSet
		StaticData = None

		for ibfgrp in range(mesh.nBFaceGroup):
			BFG = mesh.BFaceGroups[ibfgrp]

			for ibface in range(BFG.nBFace):
				BFace = BFG.BFaces[ibface]
				elem = BFace.Elem
				face = BFace.face

				R[elem], StaticData = self.calculate_residual_bface(ibfgrp, ibface, U[elem], R[elem], StaticData)


	def calculate_residual(self, U, R):
		'''
		Method: calculate_residual
		-----------------------------------
		Calculates the boundary + volume integral for the DG formulation
		
		INPUTS:
			U: solution array
			
		OUTPUTS:
			R: residual array
		'''

		mesh = self.mesh
		EqnSet = self.EqnSet

		if R is None:
			# R = ArrayList(SimilarArray=U)
			R = np.copy(U)
		# Initialize residual to zero
		# R.SetUniformValue(0.)
		R[:] = 0.

		self.calculate_residual_bfaces(U, R)
		self.calculate_residual_elems(U, R)
		self.calculate_residual_ifaces(U, R)

		return R


	def apply_time_scheme(self, fhistory=None):
		'''
		Method: apply_time_scheme
		-----------------------------
		Applies the specified time scheme to update the solution

		'''
		EqnSet = self.EqnSet
		mesh = self.mesh
		Order = self.Params["InterpOrder"]
		Stepper = self.Stepper
		Time = self.Time

		# Parameters
		TrackOutput = self.Params["TrackOutput"]

		t0 = time.time()
		for iStep in range(self.nTimeStep):

			# Integrate in time
			# self.Time is used for local time
			R = Stepper.TakeTimeStep(self)

			# Increment time
			Time += Stepper.dt
			self.Time = Time

			# Info to print
			# PrintInfo = (iStep+1, self.Time, R.VectorNorm(ord=1))
			PrintInfo = (iStep+1, self.Time, np.linalg.norm(np.reshape(R,-1), ord=1))
			PrintString = "%d: Time = %g, Residual norm = %g" % (PrintInfo)

			# Output
			if TrackOutput:
				output,_ = Post.L2_error(mesh,EqnSet,Time,"Entropy",False)
				OutputString = ", Output = %g" % (output)
				PrintString += OutputString

			# Print info
			print(PrintString)

			# Write to file if requested
			if fhistory is not None:
				fhistory.write("%d %g %g" % (PrintInfo))
				if TrackOutput:
					fhistory.write(" %g" % (output))
				fhistory.write("\n")


		t1 = time.time()
		print("Wall clock time = %g seconds" % (t1-t0))


	def solve(self):
		'''
		Method: solve
		-----------------------------
		Performs the main solve of the DG method. Initializes the temporal loop. 

		'''
		mesh = self.mesh
		EqnSet = self.EqnSet
		basis = self.basis

		OrderSequencing = self.Params["OrderSequencing"]
		InterpOrder = self.Params["InterpOrder"]
		nTimeStep = self.Params["nTimeStep"]
		EndTime = self.Params["EndTime"]
		WriteTimeHistory = self.Params["WriteTimeHistory"]
		if WriteTimeHistory:
			fhistory = open("TimeHistory.txt", "w")
		else:
			fhistory = None


		''' Convert to lists '''
		# InterpOrder
		if np.issubdtype(type(InterpOrder), np.integer):
			InterpOrders = [InterpOrder]
		elif type(InterpOrder) is list:
			InterpOrders = InterpOrder 
		else:
			raise TypeError
		nOrder = len(InterpOrders)
		# nTimeStep
		if np.issubdtype(type(nTimeStep), np.integer):
			nTimeSteps = [nTimeStep]*nOrder
		elif type(nTimeStep) is list:
			nTimeSteps = nTimeStep 
		else:
			raise TypeError
		# EndTime
		if np.issubdtype(type(EndTime), np.floating):
			EndTimes = []
			for i in range(nOrder):
				EndTimes.append(EndTime*(i+1))
		elif type(EndTime) is list:
			EndTimes = EndTime 
		else:
			raise TypeError


		''' Check compatibility '''
		if nOrder != len(nTimeSteps) or nOrder != len(EndTimes):
			raise ValueError

		if np.any(np.diff(EndTimes) < 0.):
			raise ValueError

		if not OrderSequencing:
			if len(InterpOrders) != 1:
				raise ValueError

		''' Loop through Orders '''
		Time = 0.
		for iOrder in range(nOrder):
			Order = InterpOrders[iOrder]
			''' Compute time step '''
			self.Stepper.dt = (EndTimes[iOrder]-Time)/nTimeSteps[iOrder]
			self.nTimeStep = nTimeSteps[iOrder]

			''' After first iteration, project solution to next Order '''
			if iOrder > 0:
				# Clear DataSet
				delattr(self, "DataSet")
				self.DataSet = GenericData()
				# Increment Order
				Order_old = EqnSet.Order
				EqnSet.Order = Order
				# Project
				project_state_to_new_basis(self, mesh, EqnSet, basis, Order_old)

				basis.order = Order
				basis.nb = basis.get_num_basis_coeff(Order)				

				self.precompute_matrix_operators()

			''' Apply time scheme '''
			self.apply_time_scheme(fhistory)

			Time = EndTimes[iOrder]


		if WriteTimeHistory:
			fhistory.close()


class ElemOperatorsADER(ElemOperators):

	def get_basis_and_geom_data(self, mesh, basis, order):
		# separate these later

		# Unpack
		quad_pts = self.quad_pts 
		basis.eval_basis(quad_pts, Get_Phi=True, Get_GPhi=False)

		self.basis_val = basis.basis_val

class IFaceOperatorsADER(IFaceOperators):

	def get_gaussian_quadrature(self, mesh, EqnSet, basis, order):

		QuadOrder, _ = get_gaussian_quadrature_face(mesh, None, mesh.gbasis, order, EqnSet, None)
		quadData = QuadDataADER(mesh, basis, EntityType.IFace, QuadOrder)
		self.quad_pts = quadData.quad_pts
		self.quad_wts = quadData.quad_wts

	def get_basis_and_geom_data(self, mesh, basis, order):
		# separate these later

		# Unpack
		dim = mesh.Dim
		quad_pts = self.quad_pts 
		nq = quad_pts.shape[0]
		nb = basis.get_num_basis_coeff(order)
		nFacePerElem = mesh.nFacePerElem + 2

		# Allocate
		self.faces_to_basisL = np.zeros([nFacePerElem,nq,nb])
		self.faces_to_basisR = np.zeros([nFacePerElem,nq,nb])
		self.normals_ifaces = np.zeros([mesh.nIFace,nq,dim])

		for f in range(nFacePerElem):
			# Left
			#eval_basis_on_face_ader(mesh, basis_st, face_stL, quad_pts_st, xelemLPhi, Get_Phi=True)
			_ = basis.eval_basis_on_face_ader(mesh, basis, f, quad_pts, None, Get_Phi=True)
			self.faces_to_basisL[f] = basis.basis_val
			# Right
			_ = basis.eval_basis_on_face_ader(mesh, basis, f, quad_pts[::-1], None, Get_Phi=True)
			self.faces_to_basisR[f] = basis.basis_val

		i = 0
		for IFace in mesh.IFaces:
			# Normals
			nvec = iface_normal(mesh, IFace, quad_pts)
			self.normals_ifaces[i] = nvec
			i += 1

class BFaceOperatorsADER(IFaceOperatorsADER):

	def get_basis_and_geom_data(self, mesh, basis, order):
		# separate these later

		# Unpack
		dim = mesh.Dim
		quad_pts = self.quad_pts 
		nq = quad_pts.shape[0]
		nb = basis.get_num_basis_coeff(order)
		nFacePerElem = mesh.nFacePerElem + 2

		# Allocate
		self.faces_to_basis = np.zeros([nFacePerElem,nq,nb])
		self.faces_to_xref = np.zeros([nFacePerElem,nq,dim+1])
		self.normals_bfgroups = []
		self.x_bfgroups = []

		GeomPhiData = None

		for f in range(nFacePerElem):
			# Left
			self.faces_to_xref[f] = xref = basis.eval_basis_on_face_ader(mesh, basis, f, quad_pts, None, Get_Phi=True)
			self.faces_to_basis[f] = basis.basis_val

		i = 0
		for BFG in mesh.BFaceGroups:
			self.normals_bfgroups.append(np.zeros([BFG.nBFace,nq,dim]))
			self.x_bfgroups.append(np.zeros([BFG.nBFace,nq,dim]))
			normal_bfgroup = self.normals_bfgroups[i]
			x_bfgroup = self.x_bfgroups[i]
			j = 0
			for BFace in BFG.BFaces:
				# Normals
				nvec = bface_normal(mesh, BFace, quad_pts)
				normal_bfgroup[j] = nvec

				# Physical coordinates of quadrature points
				x, GeomPhiData = ref_to_phys(mesh, BFace.Elem, GeomPhiData, self.faces_to_xref[BFace.face], None, True)
				# Store
				x_bfgroup[j] = x

				# Increment
				j += 1
			i += 1

	def alloc_other_arrays(self, EqnSet, basis, order):
		quad_pts = self.quad_pts 
		nq = quad_pts.shape[0]
		ns = EqnSet.StateRank

		self.UqI = np.zeros([nq, ns])
		self.UqB = np.zeros([nq, ns])
		self.Fq = np.zeros([nq, ns])


class ADEROperators(object):
	def __init__(self):
		self.MM = None
		self.iMM = None
		self.K = None
		self.iK = None 
		self.FTL = None 
		self.FTR = None
		self.SMT = None
		self.SMS = None		

	def calc_ader_matrices(self, mesh, basis, basis_st, order):

		# Get flux matrices in time
		FTL,_ = get_temporal_flux_ader(mesh, basis_st, basis_st, order, elem=0, PhysicalSpace=False, StaticData=None)
		FTR,_ = get_temporal_flux_ader(mesh, basis_st, basis, order, elem=0, PhysicalSpace=False, StaticData=None)

		# Get stiffness matrix in time
		SMT,_ = get_stiffness_matrix_ader(mesh, basis_st, order, elem=0, gradDir=1)

		# Get stiffness matrix in space
		SMS,_ = get_stiffness_matrix_ader(mesh, basis_st, order, elem=0, gradDir=0)

		# Get mass matrix in space-time
		MM,_ =  get_elem_mass_matrix_ader(mesh, basis_st, order, elem=-1, PhysicalSpace=False, StaticData=None)
		iMM,_ =  get_elem_inv_mass_matrix_ader(mesh, basis_st, order, elem=-1, PhysicalSpace=True, StaticData=None)


		self.FTL = FTL
		self.FTR = FTR
		self.SMT = SMT
		self.SMS = np.transpose(SMS)
		self.MM = MM
		self.iMM = iMM
		self.K = FTL - SMT
		self.iK = np.linalg.inv(self.K) 

	def compute_operators(self, mesh, EqnSet, basis, basis_st, order):
		self.calc_ader_matrices(mesh, basis, basis_st, order)


class ADERDG_Solver(DG_Solver):
	'''
	Class: ADERDG_Solver
	--------------------------------------------------------------------------
	Use the ADER-DG method to solve a given set of PDEs
	'''
	
	def check_solver_params(self):
		'''
		Method: check_solver_params
		--------------------------------------------------------------------------
		Checks the validity of the solver parameters

		'''
		Params = self.Params
		mesh = self.mesh
		EqnSet = self.EqnSet
		### Check interp basis validity
		if BasisType[Params["InterpBasis"]] == BasisType.LagrangeSeg or BasisType[Params["InterpBasis"]] == BasisType.LegendreSeg:
		    if mesh.Dim != 1:
		        raise Errors.IncompatibleError
		else:
		    if mesh.Dim != 2:
		        raise Errors.IncompatibleError

		### Check uniform mesh
		if Params["UniformMesh"] is True:
		    ''' 
		    Check that element volumes are the same
		    Note that this is a necessary but not sufficient requirement
		    '''
		    TotVol, ElemVols = MeshTools.element_volumes(mesh)
		    if (ElemVols.Max - ElemVols.Min)/TotVol > 1.e-8:
		        raise ValueError

		### Check linear geometric mapping
		if Params["LinearGeomMapping"] is True:
			if mesh.QOrder != 1:
			    raise Errors.IncompatibleError
			if mesh.QBasis == BasisType.LagrangeQuad \
			    and Params["UniformMesh"] is False:
			    raise Errors.IncompatibleError

		### Check limiter ###
		if Params["ApplyLimiter"] is 'ScalarPositivityPreserving' \
			and EqnSet.StateRank > 1:
				raise IncompatibleError
		if Params["ApplyLimiter"] is 'PositivityPreserving' \
			and EqnSet.StateRank == 1:
				raise IncompatibleError

		### Check time integration scheme ###
		TimeScheme = Params["TimeScheme"]
		if TimeScheme is not "ADER":
			raise Errors.IncompatibleError

		### Check flux/source coefficient interpolation compatability with basis functions.
		if Params["InterpolateFlux"] is True and BasisType[Params["InterpBasis"]] == BasisType.LegendreSeg:
			raise Errors.IncompatibleError


	def precompute_matrix_operators(self):
		mesh = self.mesh 
		EqnSet = self.EqnSet

		basis = self.basis
		basis_st = self.basis_st


		self.elem_operators = ElemOperators()
		self.elem_operators.compute_operators(mesh, EqnSet, basis, EqnSet.Order)
		self.iface_operators = IFaceOperators()
		self.iface_operators.compute_operators(mesh, EqnSet, basis, EqnSet.Order)
		self.bface_operators = BFaceOperators()
		self.bface_operators.compute_operators(mesh, EqnSet, basis, EqnSet.Order)

		# Calculate ADER specific space-time operators
		self.elem_operators_st = ElemOperatorsADER()
		self.elem_operators_st.compute_operators(mesh, EqnSet, basis_st, EqnSet.Order)
		self.iface_operators_st = IFaceOperatorsADER()
		self.iface_operators_st.compute_operators(mesh, EqnSet, basis_st, EqnSet.Order)
		self.bface_operators_st = BFaceOperatorsADER()
		self.bface_operators_st.compute_operators(mesh, EqnSet, basis_st, EqnSet.Order)

		self.ader_operators = ADEROperators()
		self.ader_operators.compute_operators(mesh, EqnSet, basis, basis_st, EqnSet.Order)

	def calculate_predictor_step(self, dt, W, Up):
		'''
		Method: calculate_predictor_step
		-------------------------------------------
		Calls the predictor step for each element

		INPUTS:
			dt: time step 
			W: previous time step solution in space only

		OUTPUTS:
			Up: predicted solution in space-time
		'''
		mesh = self.mesh
		EqnSet = self.EqnSet
		StaticData = None

		for elem in range(mesh.nElem):
			Up[elem], StaticData = self.calculate_predictor_elem(elem, dt, W[elem], Up[elem], StaticData)

		return Up

	def calculate_predictor_elem(self, elem, dt, Wp, Up, StaticData):
		'''
		Method: calculate_predictor_elem
		-------------------------------------------
		Calculates the predicted solution state for the ADER-DG method using a nonlinear solve of the
		weak form of the DG discretization in time.

		INPUTS:
			elem: element index
			dt: time step 
			W: previous time step solution in space only

		OUTPUTS:
			Up: predicted solution in space-time
		'''
		EqnSet = self.EqnSet
		ns = EqnSet.StateRank
		mesh = self.mesh

		basis = EqnSet.Basis #basis2
		basis_st = EqnSet.BasisADER #basis1
		order = EqnSet.Order
		
		elem_ops = self.elem_operators
		ader_ops = self.ader_operators
		
		quad_wts = elem_ops.quad_wts
		basis_val = elem_ops.basis_val 
		djac_elems = elem_ops.djac_elems 
		
		djac = djac_elems[elem]
		# _, ElemVols = MeshTools.element_volumes(mesh, self)

		FTR = ader_ops.FTR
		MM = ader_ops.MM
		SMS = ader_ops.SMS
		# K = ader_ops.K
		iK = ader_ops.iK
		# W_bar = np.zeros([1,ns])
		# Wq = np.matmul(basis_val, Wp)
		# vol = ElemVols[elem]

		# W_bar[:] = np.matmul(Wq.transpose(),quad_wts*djac).T/vol

		# Wh = np.average(W)

		# def F(u):
		# 	S = 0.
		# 	S = EqnSet.SourceState(1, 0., 0., u, S)
		# 	F = u - S[0,0] - W_bar[0,0]
		# 	return F

		#U_bar = fsolve(F, W_bar)
		# nu= -100000.
		# dsdu = nu
		# Up[:] = U_bar
		#code.interact(local=locals())
		#dsdu = (1./nu)*(2.*U_bar-3.*U_bar**2 - 0.5 +2.*U_bar*0.5)
		#dsdu = (1./nu)*(2.*Up-3.*Up**2 - 0.5 +2.*Up*0.5)
		#code.interact(local=locals())

		### Hacky implementation of implicit source term
		# Kp = K-MM*dt*dsdu

		# iK = np.linalg.inv(Kp)

		srcpoly = self.source_coefficients(elem, dt, order, basis_st, Up)
		fluxpoly = self.flux_coefficients(elem, dt, order, basis_st, Up)
		ntest = 10
		for i in range(ntest):

			# Up_new = np.matmul(iK,(np.matmul(MM,srcpoly)-np.matmul(SMS,fluxpoly)+np.matmul(FTR,Wp)-np.matmul(MM,dt*dsdu*Up)))
			Up_new = np.matmul(iK,(np.matmul(MM,srcpoly)-np.matmul(SMS,fluxpoly)+np.matmul(FTR,Wp)))
			err = Up_new - Up

			if np.amax(np.abs(err))<1e-9:
				Up = Up_new
				break

			Up = Up_new
			
			srcpoly = self.source_coefficients(elem, dt, order, basis_st, Up)
			fluxpoly = self.flux_coefficients(elem, dt, order, basis_st, Up)


		return Up, StaticData

	def calculate_residual_elem(self, elem, Up, ER, StaticData):
		'''
		Method: calculate_residual_elem
		-------------------------------------------
		Calculates the residual from the volume integral for each element

		INPUTS:
			elem: element index
			U: solution state

		OUTPUTS:
		ER: calculated residiual array (for volume integral of specified element)
		'''
		EqnSet = self.EqnSet
		mesh = self.mesh
		ns = EqnSet.StateRank
		dim = EqnSet.Dim

		elem_ops = self.elem_operators
		elem_ops_st = self.elem_operators_st
		quad_wts = elem_ops.quad_wts
		quad_wts_st = elem_ops_st.quad_wts
		quad_pts_st = elem_ops_st.quad_pts
		basis_val = elem_ops.basis_val 
		basis_val_st = elem_ops_st.basis_val
		basis_pgrad_elems = elem_ops.basis_pgrad_elems
		djac_elems = elem_ops.djac_elems 
		x_elems = elem_ops.x_elems
		Sq = elem_ops_st.Sq

		TimePhiData = None

		# Unpack
		basis_pgrad = basis_pgrad_elems[elem]
		djac = djac_elems[elem]
		nq = quad_wts.shape[0]
		nq_st = quad_wts_st.shape[0]
		nb = basis_val.shape[1]
		x = x_elems[elem]

		# interpolate state and gradient at quad points
		Uq = np.matmul(basis_val_st, Up)

		Fq = EqnSet.ConvFluxInterior(Uq, F=None) # [nq,sr,dim]

		# for ir in range(sr):
		# 	for k in range(nn): # Loop over basis function in space
		# 		for i in range(nq): # Loop over time
		# 			for j in range(nq): # Loop over space
		# 				gPsi = PsiData.gPhi[j,k]
		# 				ER[k,ir] += wq[i]*wq[j]*JData.djac[j*(JData.nq!=1)]*F[i,j,ir]*gPsi

		# F = np.reshape(F,(nqST,sr,dim))
		
		ER += np.tensordot(np.tile(basis_pgrad,(nb,1,1)), Fq*(quad_wts_st.reshape(nq,nq)*djac).reshape(nq_st,1,1), axes=([0,2],[0,2])) # [nb, ns]
		
		t = np.zeros([nq_st,dim])
		t, TimePhiData = ref_to_phys_time(mesh, elem, self.Time, self.Stepper.dt, TimePhiData, quad_pts_st, t, None)
		
		Sq[:] = 0.
		Sq = EqnSet.SourceState(nq_st, x, t, Uq, Sq) # [nq,sr,dim]

		# s = np.reshape(s,(nq,nq,sr))
		# #Calculate source term integral
		# for ir in range(sr):
		# 	for k in range(nn):
		# 		for i in range(nq): # Loop over time
		# 			for j in range(nq): # Loop over space
		# 				Psi = PsiData.Phi[j,k]
		# 				ER[k,ir] += wq[i]*wq[j]*s[i,j,ir]*JData.djac[j*(JData.nq!=1)]*Psi
		# s = np.reshape(s,(nqST,sr))

		ER += np.matmul(np.tile(basis_val,(nb,1)).transpose(),Sq*(quad_wts_st.reshape(nq,nq)*djac).reshape(nq_st,1)) # [nb, ns]

		if elem == echeck:
			code.interact(local=locals())

		return ER, StaticData

	def calculate_residual_iface(self, iiface, UpL, UpR, RL, RR, StaticData):
		'''
		Method: calculate_residual_iface
		-------------------------------------------
		Calculates the residual from the boundary integral for each internal face

		INPUTS:
			iiface: internal face index
			UL: solution array from left neighboring element
			UR: solution array from right neighboring element
			
		OUTPUTS:
			RL: calculated residual array (left neighboring element contribution)
			RR: calculated residual array (right neighboring element contribution)
		'''
		mesh = self.mesh
		EqnSet = self.EqnSet
		IFace = mesh.IFaces[iiface]
		elemL = IFace.ElemL
		elemR = IFace.ElemR
		faceL = IFace.faceL
		faceR = IFace.faceR

		if faceL == 0:
			faceL_st = 3
		elif faceL == 1:
			faceL_st = 1
		else:
			return IncompatibleError
		if faceR == 0:
			faceR_st = 3
		elif faceR == 1:
			faceR_st = 1
		else:
			return IncompatibleError

		iface_ops = self.iface_operators
		iface_ops_st = self.iface_operators_st
		quad_pts = iface_ops.quad_pts
		quad_wts = iface_ops.quad_wts
		quad_wts_st = iface_ops_st.quad_wts
		faces_to_basisL = iface_ops.faces_to_basisL
		faces_to_basisR = iface_ops.faces_to_basisR
		faces_to_basisL_st = iface_ops_st.faces_to_basisL
		faces_to_basisR_st = iface_ops_st.faces_to_basisR

		normals_ifaces = iface_ops.normals_ifaces
		UqL = iface_ops.UqL
		UqR = iface_ops.UqR
		Fq = iface_ops.Fq

		nq = quad_wts.shape[0]
		nq_st = quad_wts_st.shape[0]

		basis_valL = faces_to_basisL[faceL]
		basis_valR = faces_to_basisR[faceR]

		basis_valL_st = faces_to_basisL_st[faceL_st]
		basis_valR_st = faces_to_basisR_st[faceR_st]

		nbL = basis_valL.shape[1]
		nbR = basis_valR.shape[1]
		nb = np.amax([nbL,nbR])

		UqL = np.matmul(basis_valL_st, UpL)
		UqR = np.matmul(basis_valR_st, UpR)

		normals = normals_ifaces[iiface]

		if StaticData is None:
			StaticData = GenericData()

		Fq = EqnSet.ConvFluxNumerical(UqL, UqR, normals, nq_st, StaticData) # [nq_st,ns]

		# F = np.reshape(F,(nq,nqST,sr))
		
		# for ir in range(sr):
		# 	#for k in range(nn): # Loop over basis function in space
		# 	for i in range(nqST): # Loop over time
		# 		for j in range(nq): # Loop over space
		# 			PsiL = PsiDataL.Phi[j,:]
		# 			PsiR = PsiDataR.Phi[j,:]
		# 			RL[:,ir] -= wqST[i]*wq[j]*F[j,i,ir]*PsiL
		# 			RR[:,ir] += wqST[i]*wq[j]*F[j,i,ir]*PsiR

		# F = np.reshape(F,(nqST,sr))


		RL -= np.matmul(np.tile(basis_valL,(nb,1)).transpose(), Fq*quad_wts_st*quad_wts) # [nb, ns]
		RR += np.matmul(np.tile(basis_valR,(nb,1)).transpose(), Fq*quad_wts_st*quad_wts) # [nb, ns]

		if elemL == echeck or elemR == echeck:
			if elemL == echeck: print("Left!")
			else: print("Right!")
			code.interact(local=locals())

		return RL, RR, StaticData

	def calculate_residual_bface(self, ibfgrp, ibface, U, R, StaticData):
		'''
		Method: calculate_residual_bface
		-------------------------------------------
		Calculates the residual from the boundary integral for each boundary face

		INPUTS:
			ibfgrp: index of BC group
			ibface: index of boundary face
			U: solution array from internal element
			
		OUTPUTS:
			R: calculated residual array (from boundary face)
		'''
		mesh = self.mesh
		dim = mesh.Dim
		EqnSet = self.EqnSet
		BFG = mesh.BFaceGroups[ibfgrp]
		BFace = BFG.BFaces[ibface]
		elem = BFace.Elem
		face = BFace.face

		bface_ops = self.bface_operators
		bface_ops_st = self.bface_operators_st
		quad_pts = bface_ops.quad_pts
		quad_wts = bface_ops.quad_wts
		quad_pts_st = bface_ops_st.quad_pts
		quad_wts_st = bface_ops_st.quad_wts
		faces_to_xref_st = bface_ops_st.faces_to_xref

		faces_to_basis = bface_ops.faces_to_basis
		faces_to_basis_st = bface_ops_st.faces_to_basis
		normals_bfgroups = bface_ops.normals_bfgroups
		x_bfgroups = bface_ops.x_bfgroups
		UqI = bface_ops_st.UqI
		UqB = bface_ops_st.UqB
		Fq = bface_ops.Fq


		if face == 0:
			face_st = 3
		elif face == 1:
			face_st = 1
		else:
			return IncompatibleError
	
		basis_val = faces_to_basis[face]
		basis_val_st = faces_to_basis_st[face_st]
		xref_st = faces_to_xref_st[face_st]

		nq_st = quad_wts_st.shape[0]
		nb = basis_val.shape[1]

		TimePhiData = None

		t = np.zeros([nq_st,dim])
		t, TimePhiData = ref_to_phys_time(mesh, elem, self.Time, self.Stepper.dt, TimePhiData, xref_st, t, None)

		# interpolate state and gradient at quad points
		UqI = np.matmul(basis_val_st, U)

		normals = normals_bfgroups[ibfgrp][ibface]
		x = x_bfgroups[ibfgrp][ibface]

		# Get boundary state
		BC = EqnSet.BCs[ibfgrp]
		UqB = EqnSet.BoundaryState(BC, nq_st, x, t, normals, UqI, UqB)

		if StaticData is None:
			StaticData = GenericData()

		Fq = EqnSet.ConvFluxBoundary(BC, UqI, UqB, normals, nq_st, StaticData) # [nq_st,ns]

		# F = np.reshape(F,(nq,nqST,sr))

		# for ir in range(sr):
		# 	for i in range(nqST): # Loop over time
		# 		for j in range(nq): # Loop over space
		# 			Psi = PsiData.Phi[j,:]
		# 			R[:,ir] -= wqST[i]*wq[j]*F[j,i,ir]*Psi
	
		# F = np.reshape(F,(nqST,sr))

		R -= np.matmul(np.tile(basis_val,(nb,1)).transpose(),Fq*quad_wts_st*quad_wts)

		if elem == echeck:
			code.interact(local=locals())

		return R, StaticData

	def flux_coefficients(self, elem, dt, order, basis, Up):
		'''
		Method: flux_coefficients
		-------------------------------------------
		Calculates the polynomial coefficients for the flux functions in ADER-DG

		INPUTS:
			elem: element index
			dt: time step size
			order: solution order
			U: solution array
			
		OUTPUTS:
			F: polynomical coefficients of the flux function
		'''

		EqnSet = self.EqnSet
		mesh = self.mesh
		ns = EqnSet.StateRank
		dim = EqnSet.Dim
		Params = self.Params

		InterpolateFlux = Params["InterpolateFlux"]

		elem_ops = self.elem_operators
		djac_elems = elem_ops.djac_elems 
		djac = djac_elems[elem]

		rhs = np.zeros([order_to_num_basis_coeff(basis,order),ns],dtype=Up.dtype)

		if not InterpolateFlux:
			ader_ops = self.ader_operators
			elem_ops_st = self.elem_operators_st
			basis_val_st = elem_ops_st.basis_val
			quad_wts_st = elem_ops_st.quad_wts
			nq_st = quad_wts_st.shape[0]
			quad_pts = elem_ops.quad_pts
			nq = quad_pts.shape[0]
			Uq = np.matmul(basis_val_st, Up)
			Fq = EqnSet.ConvFluxInterior(Uq, F=None) # [nq_st,ns,dim]
			Fq = Fq.reshape(nq_st,ns)
			iMM = ader_ops.iMM
			
			rhs *=0.

			# for ir in range(ns):
			# 	for k in range(nb): # Loop over basis function in space
			# 		for i in range(nq): # Loop over time
			# 			for j in range(nq): # Loop over space
			# 				#Phi = PhiData.Phi[j,k]
			# 				rhs[k,ir] += wq[i]*wq[j]*JData.djac[j*(JData.nq!=1)]*f[i,j,ir]*Phi[i,j,k]

			rhs = np.matmul(basis_val_st.transpose(), Fq*(quad_wts_st*(np.tile(djac,(nq,1))))) # [nb, ns]

			F = np.dot(iMM,rhs)*(1.0/(np.tile(djac,(nq,1))))*dt/2.0

		else:
			quad_pts = elem_ops.quad_pts
			nq = quad_pts.shape[0]

			Fq = EqnSet.ConvFluxInterior(Up,F=None)
			F = Fq[:,:,0]*(1.0/(np.tile(djac,(nq,1))))*dt/2.0

		return F

	def source_coefficients(self, elem, dt, order, basis, Up):
		'''
		Method: source_coefficients
		-------------------------------------------
		Calculates the polynomial coefficients for the source functions in ADER-DG

		INPUTS:
			elem: element index
			dt: time step size
			order: solution order
			U: solution array
			
		OUTPUTS:
			S: polynomical coefficients of the flux function
		'''
		mesh = self.mesh
		dim = mesh.Dim
		EqnSet = self.EqnSet
		ns = EqnSet.StateRank
		Params = self.Params
		entity = EntityType.Element
		InterpolateFlux = Params["InterpolateFlux"]

		elem_ops = self.elem_operators
		elem_ops_st = self.elem_operators_st
		djac_elems = elem_ops.djac_elems 
		djac = djac_elems[elem]
		Sq = elem_ops_st.Sq

		x_elems = elem_ops.x_elems
		x = x_elems[elem]

		TimePhiData = None

		if not InterpolateFlux:
			rhs = np.zeros([order_to_num_basis_coeff(basis,order),ns],dtype=Up.dtype)

			ader_ops = self.ader_operators
			basis_val_st = elem_ops_st.basis_val
			quad_wts_st = elem_ops_st.quad_wts
			nq_st = quad_wts_st.shape[0]
			quad_pts_st = elem_ops_st.quad_pts
			quad_pts = elem_ops.quad_pts
			nq = quad_pts.shape[0]
			Uq = np.matmul(basis_val_st, Up)
			Fq = EqnSet.ConvFluxInterior(Uq, F=None) # [nq_st,ns,dim]
			Fq = Fq.reshape(nq_st,ns)
			iMM = ader_ops.iMM


			t = np.zeros([nq_st,dim])
			t, TimePhiData = ref_to_phys_time(mesh, elem, self.Time, self.Stepper.dt, TimePhiData, quad_pts_st, t, None)

			Uq = np.matmul(basis_val_st,Up)
		
			Sq[:] = 0.
			Sq = EqnSet.SourceState(nq_st, x, t, Uq, Sq) # [nq,sr,dim]

			rhs *=0.

			rhs[:] = np.matmul(basis_val_st.transpose(),Sq*quad_wts_st*(np.tile(djac,(nq,1)))) # [nb, ns]
			S = np.dot(iMM,rhs)*dt/2.0

		else:

			quad_pts_st = elem_ops_st.quad_pts
			nq_st = quad_pts_st.shape[0]
			t = np.zeros([nq_st,dim])
			t, TimePhiData = ref_to_phys_time(mesh, elem, self.Time, self.Stepper.dt, TimePhiData, quad_pts_st, t, None)

			Sq[:] = 0.
			Sq = EqnSet.SourceState(nq_st, x, t, Up, Sq)
			S = Sq*dt/2.0

		return S
