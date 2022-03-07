import numpy as np


# x = np.linspace(0., 3., 30)
# indOne = (x<=0.5)
# indTwo = ((x>0.5) & (x<=1.5))
# indThree = (x>1.5)
# Area = 1.0 + 2.2 * (x - 1.5)**2.
# AreaGradient = 4.4 * x

# rho = np.zeros(x.shape)
# rho[indOne] = 1.
# rho[indTwo] = 1. - 0.3146 * (x[indTwo] - 0.5)
# rho[indThree] = 0.634 - 0.3879 * (x[indThree] - 1.5)


# T = np.zeros(x.shape)
# T[indOne] = 1.
# T[indTwo] = 1. - 0.167 * (x[indTwo] - 0.5)
# T[indThree] = 0.833 - 0.3507 * (x[indThree] - 1.5)

# u = 0.59 / rho / Area

# dx = 3. / 30
# dt = np.min(0.5 * dx / (np.sqrt(T) + u))
# print(dt)


TimeStepping = {
	"InitialTime" : 0.,
	"FinalTime" : 10.0,
# 	"TimeStepSize" : dt,
    "CFL" : 0.5,
	"TimeStepper" : "SSPRK3",
}

Numerics = {
    "SolutionOrder" : 1,
    "SolutionBasis" : "LagrangeSeg",
    "Solver" : "DG",
    "ApplyLimiters" : "PositivityPreserving",
    "L2InitialCondition" : False,
    "ArtificialViscosity" : True,
    "Quasi1D" : True,
    "AVParameter" : 50.,
    "NodeType" : "Equidistant",
    # "ElementQuadrature" : "GaussLegendre",
    # "FaceQuadrature" : "GaussLegendre",
}

Output = {
	"AutoPostProcess" : True,
}

Mesh = {
	"File" : None,
	"ElementShape" : "Segment",
	"NumElemsX" : 50,
	"xmin" : 0.,
	"xmax" : 1.,
}

Physics = {
	"Type" : "Euler",
	"ConvFluxNumerical" : "LaxFriedrichs",
	"GasConstant" : 1,
	"SpecificHeatRatio" : 1.4,
}

InitialCondition = {
	"Function" : "Quasi1DNozzleSupersonic",
	"Area": 1.0,
	"AreaGradient": 0.0,
}

BoundaryConditions = {
	"x1" : {
		"BCType" : "StateAll",
		"Function" : "Quasi1DNozzleSupersonic",
	},
# 	"x1" : {
# 		"BCType" : "SubsonicInflow",
# 		"rho" : 1,
# 		"T" : 1,
# 	},
	"x2" : {
		"BCType" : "Extrapolate",
		"Function" : "Quasi1DNozzleSupersonic",
	},
# 	"x2" : {
# 		"BCType" : "PressureOutlet",
# 		"p" : 0.2842,
# 	},
}

SourceTerms = {
 	"source1" : {
		"Function" : "Quasi1DNozzleSource",
 	},
}