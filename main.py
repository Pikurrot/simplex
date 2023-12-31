import numpy as np
import utils
from typing import Union
import gradio as gr

class Simplex:
	def __init__(self, objective: str, constraints: Union[str, tuple, list]):
		# Parse objective and constraints
		self.objective = utils.parse_polynomial(objective)
		self.obj_vars = self.objective[0]
		if isinstance(constraints, str):
			self.constraints = [constraint.strip() for constraint in constraints.split('\n') if constraint.strip()]
		self.constraints = [utils.parse_linear_equation(constraint) for constraint in self.constraints]

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
		return {var: val for var, val in zip(['t'] + self.basic_vars, self.tableau[:, -1]) if var in self.obj_vars + ['t']}
	
	def choose_entering(self):
		'''Choose the entering variable. Returns its column position in the tableau'''
		# Choose the variable with the most negative coefficient in the objective function row
		return np.argmin(self.tableau[0, :-1])
	
	def choose_leaving(self, entering: np.intp):
		'''Choose the leaving variable. Returns its row position in the tableau'''
		# Choose the variable with the smallest ratio: constant / entering variable coefficient
		entering_col = np.copy(self.tableau[:, entering])
		entering_col[0] = 0 # ignore the objective function row
		with np.errstate(divide='ignore', invalid='ignore'):
			ratios = np.where(entering_col != 0, self.tableau[:, -1] / entering_col, np.inf)
		return np.argmin(ratios)
	
	def pivot_operation(self, entering: np.intp, leaving: np.intp):
		'''Perform the pivot operation on the tableau'''
		# Get the pivot row and column
		pivot_row = self.tableau[leaving]
		pivot_col = self.tableau[:, entering]

		# Perform the pivot operation
		self.tableau = self.tableau - np.outer(pivot_col, pivot_row) / pivot_row[entering]
		self.tableau[leaving] = pivot_row / pivot_row[entering]
		self.basic_vars[leaving - 1] = self.vars[entering]

	def solve(self, as_str: bool = False):
		'''Solve the linear program. Returns the solution as a dict'''
		while True:
			entering = self.choose_entering()
			if self.tableau[0, entering] >= 0:
				break
			leaving = self.choose_leaving(entering)
			self.pivot_operation(entering, leaving)
		if as_str:
			string = 'Optimal solution:'
			for var, val in self.solution().items():
				string += f'\n{var} = {val}'
			return string
		return self.solution()

	def __str__(self):
		'''Return a string representation of the tableau'''
		row_names = ['t'] + self.basic_vars
		col_names = self.vars
		max_row_name_width = max(map(len, row_names))
		max_col_name_width = max(map(len, col_names))
		max_val_width = max(map(len, map(str, self.tableau.ravel())))
		cell_width = max(max_col_name_width, max_val_width)
		string = ' ' * (max_row_name_width + 1) + ' '.join([col.center(cell_width) for col in col_names])
		for row_name, row in zip(row_names, self.tableau):
			row_str = row_name.ljust(max_row_name_width) + ' ' + ' '.join([str(val).rjust(cell_width) for val in row])
			string += '\n' + row_str
		return string

def main():
	iface = gr.Interface(
		fn = lambda objective, constraints: Simplex(objective, constraints).solve(as_str=True),
		inputs = [gr.Textbox(lines=1, placeholder='Enter objective function. eg.\nx + y'),
				gr.Textbox(lines=5, placeholder='Enter constraints (one per line). eg.\nx + y <= 4\nx + 2y <= 10\nx + y <= 6\n')],
		outputs = gr.Textbox(),
		title = 'Simplex',
		description = 'A simple linear programming solver. Only for maximization problems. Only supports = and <= constraints.',
		examples=[
			['x + y', 'x <= 4\nx + 2y <= 10\nx + y <= 6'],
		],
		allow_flagging='never'
	)

	iface.launch(inbrowser=True)

if __name__ == '__main__':
	main()