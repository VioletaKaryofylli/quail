import processing.post as post
import processing.plot as plot
import processing.readwritedatafiles as readwritedatafiles

# Read data file
fname = "/Users/violetakaryofylli/quail/examples/euler/1D/quasi_1D_nozzle/Data_final.pkl"
solver = readwritedatafiles.read_data_file(fname)

# Unpack
mesh = solver.mesh
physics = solver.physics

# Compute L2 error
# post.get_error(mesh, physics, solver, "Density")

''' Plot '''
### Total energy profile ###
plot.prepare_plot()
# DG solution
plot.plot_solution(mesh, physics, solver, "Temperature", plot_numerical=True, 
		plot_exact=False, plot_IC=False, create_new_figure=True, fmt='bo',
		legend_label="DG")
# Exact solution
# plot.plot_solution(mesh, physics, solver, "Energy", plot_exact=True, 
# 		plot_numerical=False, create_new_figure=False, fmt='k-')
# Initial condition
plot.plot_solution(mesh, physics, solver, "Temperature", plot_IC=True, 
		plot_numerical=False, create_new_figure=False, fmt='k--')
# Save figure
plot.save_figure(file_name='Temperature', file_type='pdf', crop_level=2)

plot.show_plot()

### Total energy profile ###
plot.prepare_plot()
# DG solution
plot.plot_solution(mesh, physics, solver, "Density", plot_numerical=True, 
		plot_exact=False, plot_IC=False, create_new_figure=True, fmt='bo',
		legend_label="DG")
# Exact solution
# plot.plot_solution(mesh, physics, solver, "Energy", plot_exact=True, 
# 		plot_numerical=False, create_new_figure=False, fmt='k-')
# Initial condition
plot.plot_solution(mesh, physics, solver, "Density", plot_IC=True, 
		plot_numerical=False, create_new_figure=False, fmt='k--')
# Save figure
plot.save_figure(file_name='Density', file_type='pdf', crop_level=2)

plot.show_plot()

plot.prepare_plot()
# DG solution
plot.plot_solution(mesh, physics, solver, "Pressure", plot_numerical=True, 
		plot_exact=False, plot_IC=False, create_new_figure=True, fmt='bo',
		legend_label="DG")
# Exact solution
# plot.plot_solution(mesh, physics, solver, "Energy", plot_exact=True, 
# 		plot_numerical=False, create_new_figure=False, fmt='k-')
# Initial condition
plot.plot_solution(mesh, physics, solver, "Pressure", plot_IC=True, 
		plot_numerical=False, create_new_figure=False, fmt='k--')
# Save figure
plot.save_figure(file_name='Pressure', file_type='pdf', crop_level=2)

plot.show_plot()

plot.prepare_plot()
# DG solution
plot.plot_solution(mesh, physics, solver, "Velocity", plot_numerical=True, 
		plot_exact=False, plot_IC=False, create_new_figure=True, fmt='bo',
		legend_label="DG")
# Exact solution
# plot.plot_solution(mesh, physics, solver, "Energy", plot_exact=True, 
# 		plot_numerical=False, create_new_figure=False, fmt='k-')
# Initial condition
plot.plot_solution(mesh, physics, solver, "Velocity", plot_IC=True, 
		plot_numerical=False, create_new_figure=False, fmt='k--')
# Save figure
plot.save_figure(file_name='Velocity', file_type='pdf', crop_level=2)

plot.show_plot()