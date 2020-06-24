from p0 import *

Restart = {
    "File" : "p0_final.pkl",
    "StartFromFileTime" : True
}

TimeStepping.update({
    "EndTime" : 48.,
    "nTimeStep" : 1000,
})

Numerics["InterpOrder"] = 1
Output["Prefix"] = "p1"
