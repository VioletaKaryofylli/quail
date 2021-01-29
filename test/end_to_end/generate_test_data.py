import os
import pickle
import subprocess
import sys
sys.path.append('../../src')
import numpy as np

import list_of_cases
import physics.euler.euler as euler
import physics.scalar.scalar as scalar
import physics.chemistry.chemistry as chemistry
import solver.DG as DG
import solver.ADERDG as ADERDG


def generate_regression_test_data():
	"""
	This function runs Quail for each regression test and saves the final
	solution array into a binary Numpy data file. In general, this function
	should only be executed if 1) there are changes made to the test cases, or
	2) there are changes to Quail which affect the solution (for example, a
	bug being discovered and fixed).
	"""

	# Get script directory
	script_dir = sys.path[0]

	# Add full path to case directories
	case_dirs = [f'{script_dir}/cases/{case_dir}' for case_dir in
			list_of_cases.case_dirs]
	n_cases = len(case_dirs)

	# Name and path of data file which stores the regression test data
	datafile_name = f'{script_dir}/regression_data.npy'

	# Loop over all case directories
	results = []
	for case_dir in case_dirs:
		# Move to the test case directory
		os.chdir(case_dir)
		# Call the Quail executable
		text_output = subprocess.check_output([
				f'{script_dir}/../../src/quail', 'input_file.py',
				], stderr=subprocess.STDOUT)
		# Print text output of Quail
		print(text_output.decode('utf-8'))

		# Open resulting solution file
		with open('Data_final.pkl', 'rb') as solutionfile:
			# Load data
			solver = pickle.load(solutionfile)
			# Save final solution
			results.append(solver.state_coeffs)

	# Save results to the regression test datafile
	with open(datafile_name, 'wb') as datafile:
		for data in results: np.save(datafile, data)


if __name__ == "__main__":
	generate_regression_test_data()
