TimeStepping = {
	"FinalTime" : .01,
	"TimeStepSize" : .01,
	"TimeStepper" : "RK4",
}

Numerics = {
	"SolutionOrder" : 2,
	"SolutionBasis" : "LagrangeTri",
	"ElementQuadrature" : "Dunavant",
	"FaceQuadrature" : "GaussLegendre",
}

Mesh = {
	"ElementShape" : "Triangle",
	"NumElemsX" : 1,
	"NumElemsY" : 1,
	"xmin" : -5.,
	"xmax" : 5.,
	"ymin" : -5.,
	"ymax" : 5.,
	#"PeriodicBoundariesX" : ["x2", "x1"],
}

Physics = {
	"Type" : "Euler",
	"ConvFluxNumerical" : "LaxFriedrichs",
	"GasConstant" : 1.,
}

InitialCondition = {
	"Function" : "IsentropicVortex",
}

ExactSolution = InitialCondition.copy()

d = {
	"BCType" : "StateAll",
	"Function" : "IsentropicVortex",
}

BoundaryConditions = {
	"x1" : d,
	"x2" : d,
	"y1" : d,
	"y2" : d,
}

Output = {
	"WriteInterval" : 10,
	"Prefix" : "Data",
	"AutoPostProcess" : False,
	"WriteInitialSolution" : True,
	"WriteFinalSolution" : True,
	"Verbose" : True,
}