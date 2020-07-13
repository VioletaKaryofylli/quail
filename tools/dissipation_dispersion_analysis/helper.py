import numpy as np

import general
# from Basis import GetInvMassMatrix, get_stiffness_matrix, BasisData
import numerics.basis.tools as basis_tools
# from Quadrature import get_gaussian_quadrature_elem, QuadData
import code


### Function to calculate mass matrix, stiffness matrix, basis polynomials
def CalculateBasisAndMatrices(solver, mesh, order):
	## Mass, stiffness matrix
	# MMinv, _ = basis_defs.get_elem_inv_mass_matrix(mesh, basis=basis, Order=Order, elem=0, PhysicalSpace=True)
	MMinv = solver.elem_operators.iMM_elems[0]
	SM = basis_tools.get_stiffness_matrix(solver, mesh, order=order, elem=0)

	# _ = basis.eval_basis_on_face(mesh, f, quad_pts, None, Get_Phi=True)
	# 		self.faces_to_basisL[f] = basis.basis_val
	PhiLeft = solver.iface_operators.faces_to_basisL[0].transpose()
	PhiRight = solver.iface_operators.faces_to_basisL[1].transpose()
	nn = solver.basis.get_num_basis_coeff(order)

	## Evaluate basis polynomials
	# Quadrature
	# quad_order = basis.get_quadrature(mesh, order)
	# xq, _ = basis.get_quad_data(quad_order)

	# # Basis on left face
	# PhiDataLeft = BasisData(basis,order,mesh)
	# PhiDataLeft.eval_basis_on_face(mesh, egrp=0, face=0, xq=xq, xelem=None, Get_Phi=True)
	# PhiLeft = PhiDataLeft.Phi.transpose() # [nn,1]
	# # Basis on right face
	# PhiDataRight = BasisData(basis,order,mesh)
	# PhiDataRight.eval_basis_on_face(mesh, egrp=0, face=1, xq=xq, xelem=None, Get_Phi=True)
	# PhiRight = PhiDataRight.Phi.transpose() # [nn,1]
	# nn = PhiDataLeft.Phi.shape[1]

	# code.interact(local=locals())

	return MMinv, SM, PhiLeft, PhiRight, nn


### Function to calculate eigenvalues
def GetEigValues(MMinv, SM, PhiLeft, PhiRight, L, p, h, alpha, solver=None):
	# A = np.matmul(-MMinv, SM + np.matmul(PhiLeft, PhiRight.transpose())*np.exp(-1.j*L*(p+1)) \
	# 		- np.matmul(PhiRight, PhiRight.transpose()))

	# # Eigenvalues
	# eigs,_ = np.linalg.eig(A) 
	# Omega = h*eigs/1.j

	A = np.matmul(-h/1.j*MMinv, SM + np.matmul(0.5*PhiLeft, alpha*PhiLeft.transpose() + \
		(2. - alpha)*PhiRight.transpose()*np.exp(-1.j*L*(p+1))) \
		- np.matmul(0.5*PhiRight, (2.-alpha)*PhiRight.transpose() + \
		alpha*np.exp(1.j*L*(p+1))*PhiLeft.transpose()))

	# Eigenvalues
	Omega,v = np.linalg.eig(A) 

	Omega_r = np.real(Omega)
	Omega_i = np.imag(Omega)

	# if solver is not None:
	# 	EqnSet = solver.EqnSet
	# 	EqnSet.IC.Set(theta = 1.j*L*(p+1))
	# 	solver.init_state()
	# 	U = EqnSet.U.Arrays
	# 	Unorm = U/np.linalg.norm(U)

	return Omega_r, Omega_i