import numpy as np
import re
import utils

class Simplex:
	def __init__(self, objective: str, constraints: iter):
		self.objective = utils.parse_polynomial(objective)
		self.constraints = [utils.parse_linear_equation(constraint) for constraint in constraints]

def main():
	objective = 'x + y' # for not just maximize
	constraints = (
		'x <= 4',
		'x + 2y <= 10',
		'x + y <= 6'
	)

	simplex = Simplex(objective, constraints)

if __name__ == '__main__':
	main()