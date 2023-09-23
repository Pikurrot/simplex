import numpy as np
import re
import utils
from typing import Iterable

class Simplex:
	def __init__(self, objective: str, constraints: Iterable):
		# Parse objective and constraints
		self.objective = utils.parse_polynomial(objective)
		self.constraints = [utils.parse_linear_equation(constraint) for constraint in constraints]

		# Convert to equalities
		self.objective = utils.convert_to_equality(*self.objective, -1, 't')
		self.basic_vars = [f's{i}' for i in range(len(self.constraints))]
		self.constraints = [utils.convert_to_equality(*constraint, self.basic_vars[i]) for i, constraint in enumerate(self.constraints)]

		# Build tableau
		self.tableau, self.vars = self.build_tableau()

	def build_tableau(self):
		'''Build the tableau for the current equations. Returns the matrix and the variables corresponding to the columns'''
		# Extract unique variables
		all_vars = set(self.objective[0])
		for eq in self.constraints:
			all_vars.update(eq[0])
		all_vars = sorted(list(all_vars))
		
		# Build the matrix
		matrix = np.array([
			[eq[1][eq[0].index(var)] if var in eq[0] else 0. for var in all_vars] + [eq[2]]
			for eq in [self.objective] + self.constraints
		], dtype=np.float64)

		return matrix, all_vars + ['const']
	
	def solution(self):
		'''Get the solutions for the current tableau as a dict'''
		return dict(zip(['t'] + self.basic_vars, self.tableau[:, -1]))

def main():
	objective = 'x + y' # for now just maximize
	constraints = (
		'x <= 4',
		'x + 2y <= 10',
		'x + y <= 6'
	)

	simplex = Simplex(objective, constraints)
	print(simplex.solution())

if __name__ == '__main__':
	main()