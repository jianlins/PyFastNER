import csv
from decimal import Decimal


class IOUtils:
	initiations = {}
	rule_cells = {}

	def __init__(self, file_name):
		if file_name.lower().endswith('csv'):
			self.read(file_name, ',')
		elif file_name.lower().endswith('tsv'):
			self.read(file_name, '\t')
		pass

	def read(self, file_name, delimiter):
		with open('../conf/crule_test.tsv', newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=delimiter)
			row_num = 0
			for row in spamreader:
				row_num += 1
				if len(row) < 2:
					continue
				if row[0].startswith('#'):
					continue
				if row[0].startswith('@'):
					if row[0][1].isupper():
						self.initiations[row_num] = row
				elif len(row) >= 3:
					self.rule_cells[row_num] = self.buildRule(row_num, row)
				else:
					print('Incorrect formated rule: ' + str(row))
		pass

	def buildRule(self, row_num, row):
		rule_type = 'ACTUAL'
		if len(row) == 4:
			rule_type = row[3].strip()
		return Rule(row_num, row[0], Decimal(row[1].strip()), row[2].strip(), rule_type)


class Rule:
	id = -1
	rule_name = ''
	type = 'ACTUAL'
	rule = ''
	score = 1.0

	def __init__(self, id, rule, score, rule_name, type):
		self.id = id
		self.rule = rule
		self.score = score
		self.rule_name = rule_name
		self.type = type

	def copy(self):
		return Rule(self.id, self.rule, self.score, self.rule_name, self.type)

	def __str__(self):
		return "Rule {0}:\n\trule content:\t{1}\n\trule score:\t{2}\n\trule name:\t{3}\n\trule type:\t{4}\n".format(
			self.id, self.rule, self.score, self.rule_name, self.type)
