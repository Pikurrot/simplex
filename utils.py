import numpy as np
import re

def parse_linear_equation(equation: str):
	'''Parse a linear equation and return the variables, coefficients, constant, and operator of a linear equation'''
	# Adjusted regex patterns
	term_pattern = r'([\+-]?\s*\d*\.?\d*)\s*([a-zA-Z])'
	operator_pattern = r'([<=>]+)'
	constant_pattern = r'([\+-]?\s*\d+\.?\d*)$'  # The constant is expected to be at the end

	# Extract terms, operator, and constant
	terms = re.findall(term_pattern, equation)
	operator_str = re.search(operator_pattern, equation).group(1)
	constant = float(re.search(constant_pattern, equation).group(1).strip())

	# Convert operator to integer representation
	operator_map = {'<=': -1, '=': 0, '>=': 1}
	operator = operator_map.get(operator_str, None)
	if operator is None:
		raise ValueError(f"Unsupported operator: {operator_str}")

	# Extract variables and coefficients
	variables = []
	coefficients = []
	for term in terms:
		coefficient, variable = term
		coefficient = coefficient.strip().replace(' ', '')
		
		coefficient = float(coefficient) if coefficient and coefficient not in ['+', '-'] else (1.0 if coefficient in ['', '+'] else -1.0)
		variables.append(variable)
		coefficients.append(coefficient)
	
	return np.array(variables), np.array(coefficients), constant, operator


def parse_polynomial(expression: str):
	'''Parse a polynomial and return the variables, coefficients, and constant of a polynomial'''
	# Adjusted regex patterns for terms and constant
	term_pattern = r'([\+-]?\s*\d*\.?\d*)\s*([a-zA-Z])'
	constant_pattern = r'([\+-]?\s*\d+\.?\d*)$'  # The constant is expected to be at the end

	# Extract terms and constant
	terms = re.findall(term_pattern, expression)
	constant_match = re.search(constant_pattern, expression)
	constant = float(constant_match.group(1).replace(' ', '')) if constant_match else 0.0

	# Extract variables and coefficients
	variables = []
	coefficients = []
	for term in terms:
		coefficient, variable = term
		coefficient = coefficient.strip().replace(' ', '')
		
		coefficient = float(coefficient) if coefficient and coefficient not in ['+', '-'] else (1.0 if coefficient in ['', '+'] else -1.0)
		variables.append(variable)
		coefficients.append(coefficient)
	
	return np.array(variables), np.array(coefficients), constant
