# Copyright  2017  Department of Biomedical Informatics, University of Utah
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import unittest

from PyFastNER.FastCNER import FastCNER
from PyFastNER.IOUtils import Rule


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
		res = fastcner.processString('a ab abc.a ab bc.')
		assert (len(res) == 2)
		assert (len(res['R1']) == 1)
		assert (res['R1'][0].begin == 14 and res['R1'][0].end == 16)
		assert (len(res['R2']) == 4)
		for span in res['R2']:
			assert (span.text == 'b')

	def test_wildcard_match(self):
		rule_str = ''' \c\c\c\t1.5\tR1\tPSEUDO
 (\c\c\t1\tR1'''
		fastcner = FastCNER(rule_str)
		res = fastcner.processString('a ab abc.a db bc.')
		assert (len(res) == 1)
		assert (len(res['R1']) == 3)
		assert (res['R1'][0].text == 'ab')
		assert (res['R1'][1].text == 'db')
		assert (res['R1'][2].text == 'bc')


	def test_replicate_match(self):
		rule_str = '''\c+\t1.5\tR1\tPSEUDO
\c\c\t1\tR1'''
		fastcner = FastCNER(rule_str)
		res = fastcner.processString('a ab afc.a eg bc.')
		assert (len(res) == 1)
		assert (len(res['R1']) == 3)
		assert (res['R1'][0].text == 'ab')
		assert (res['R1'][1].text == 'eg')
		assert (res['R1'][2].text == 'bc')


if __name__ == '__main__':
	unittest.main()
