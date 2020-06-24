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
import logging
import unittest

from PyFastNER import FastCNER
from PyFastNER import Rule
import os


class TestFastCNER(unittest.TestCase):

    def setUp(self):
        pwd = os.path.dirname(os.path.abspath(__file__))
        self.fastcner = FastCNER(str(os.path.join(pwd,'crule_test.tsv')))

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
        self.fastcner.initiate('ab[c|d]\t0.5\tPROBLEM')
        rule_map = self.fastcner.rule_map
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
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString('a ab abc.a ab bc.')
        assert (len(res) == 2)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].begin == 14 and res['R1'][0].end == 16)
        assert (len(res['R2']) == 4)
        for span in res['R2']:
            assert (span.text == 'b')

    def test_wildcard_match(self):
        rule_str = ''' \c\c\c\t1.5\tR1\tPSEUDO
 (\c\c\t1\tR1'''
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString('a ab abc.a db bc.')
        assert (len(res) == 1)
        assert (len(res['R1']) == 3)
        assert (res['R1'][0].text == 'ab')
        assert (res['R1'][1].text == 'db')
        assert (res['R1'][2].text == 'bc')

    def test_replicate_match(self):
        rule_str = '''\c+\t1.5\tR1\tPSEUDO
\c\c\t1\tR1'''
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString('a ab afc.a eg bc.')
        assert (len(res) == 1)
        assert (len(res['R1']) == 3)
        assert (res['R1'][0].text == 'ab')
        assert (res['R1'][1].text == 'eg')
        assert (res['R1'][2].text == 'bc')

    def test_b(self):
        rule_str = r"\ba	1.5	R1"
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString('a ab afc.a eg bc.')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == 'a')

    def test_e(self):
        rule_str = r"c\e	1.5	R1"
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString('cbc')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == 'c' and res['R1'][0].begin == 2 and res['R1'][0].end == 3)

    def test_d(self):
        rule_str = r"T\d+	1.5	R1"
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString('T37.3')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == 'T37')

    def test_d2(self):
        rule_str = r"T\d+[|.\d+]	1.5	R1"
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString('T37.3')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == 'T37.3')

    def test_C(self):
        rule_str = r"\C\d+[|.\d+]	1.5	R1"
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString('T37.3')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == 'T37.3')
        pass

    def test_w(self):
        rule_str = r"\w+(\C\d+[|.\d+]	1.5	R1"
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString('''\r\n\t\t T37.3''')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == 'T37.3')
        pass

    def test_u(self):
        rule_str = r"\u+(\C\d+[|.\d+]	1.5	R1"
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString(chr(235) + chr(187) + chr(195) + '''T37.3''')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == 'T37.3')
        pass

    def test_s(self):
        rule_str = r"\s+(\C\d+[|.\d+]	1.5	R1"
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString('''\t \t \tT37.3''')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == 'T37.3')
        res = self.fastcner.processString('''\t \t \nT37.3''')
        assert (len(res) == 0)
        pass

    def test_n(self):
        rule_str = r"\n+(\C\d+[|.\d+]	1.5	R1"
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString('''\n\n\nT37.3''')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == 'T37.3')
        res = self.fastcner.processString('''\t \t T37.3''')
        assert (len(res) == 0)
        pass

    def test_p(self):
        rule_str = r"\p+(\C\d+[|.\d+]	1.5	R1"
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString(''':(T37.3''')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == 'T37.3')
        res = self.fastcner.processString('''\t \t \nT37.3''')
        assert (len(res) == 0)
        pass

    def test_a(self):
        # FastCNER.logger.setLevel(logging.DEBUG)
        rule_str = r"\w+(\a+[|.\d+]	1.5	R1"
        text = ''' T37.3'''
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString(text)
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == 'T37.3')
        res = self.fastcner.processString(''' !T37.3''')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == '!T37.3')
        pass

    def test_back_slash(self):
        rule_str = r"\w+\\\d+	1.5	R1"
        self.fastcner.initiate(rule_str)
        res = self.fastcner.processString(''' \\37.3''')
        assert (len(res) == 1)
        assert (len(res['R1']) == 1)
        assert (res['R1'][0].text == " \\37")
        res = self.fastcner.processString(''' !T37.3''')
        assert (len(res) == 0)
        pass


if __name__ == '__main__':
    unittest.main()
