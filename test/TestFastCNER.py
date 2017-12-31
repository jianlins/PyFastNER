import json
import unittest
from pprint import pprint

from nlp.FastCNER import FastCNER
from nlp.IOUtils import Rule


class TestFastCNER(unittest.TestCase):
	def setUp(self):
		self.fastcner = FastCNER('../conf/crule_test.tsv')

	def test_expand(self):
		expanded = self.fastcner.expandSquareBracket(Rule(-1, 'ab[c|d]e[f|g]', 'R1', 1.5))
		assert (len(expanded) == 4)
		assert (expanded[0].rule == 'abcef' and expanded[0].id == -1)
		assert (expanded[1].rule == 'abdef' and expanded[0].id == -1)
		assert (expanded[2].rule == 'abceg' and expanded[0].id == -1)
		assert (expanded[3].rule == 'abdeg' and expanded[0].id == -1)

	def test_expand(self):
		expanded = self.fastcner.expandSquareBracket(Rule(-1, 'ab\[c|d\]e[f|g]', 'R1', 1.5))
		assert (len(expanded) == 2)
		assert (expanded[0].rule == 'ab[c|d]ef' and expanded[0].id == -1)
		assert (expanded[1].rule == 'ab[c|d]eg' and expanded[0].id == -1)

	def test_rule_map(self):
		fastcner = FastCNER('ab[c|d]\t0.5\tPROBLEM')
		rule_map = fastcner.rule_map
		# print(json.dumps(rule_map, indent=2))
		# print(json.dumps(fastcner.scores, indent=2))
		assert (len(rule_map) == 1)
		assert (len(rule_map['a']) == 1)
		assert (len(rule_map['a']['b']) == 2)
		assert (len(rule_map['a']['b']['c']) == 1)
		assert (len(rule_map['a']['b']['d']) == 1)
		assert (len(rule_map['a']['b']['c']['<END>']) == 1)
		assert (len(rule_map['a']['b']['d']['<END>']) == 1)
		assert (rule_map['a']['b']['c']['<END>']['PROBLEM'] == 1)
		assert (rule_map['a']['b']['d']['<END>']['PROBLEM'] == 1)
		pass

	def test_overlap_match(self):
		rule_str = '''abc\t1.5\tR1\tPSEUDO
bc\t1\tR1
b\t1\tR2'''
		fastcner = FastCNER(rule_str)
		res=fastcner.processString('a ab abc.a ab bc.')
		print(res)


if __name__ == '__main__':
	unittest.main()
