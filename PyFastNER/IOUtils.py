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
import csv
import logging
from decimal import Decimal
from typing import Union, List, Iterator, Generator


class IOUtils:

    def __init__(self, rules: Union[str, List]):
        self.rule_cells = {}
        self.initiations = {}
        self.full_definition = False
        if isinstance(rules, str):
            if rules.lower().endswith('csv'):
                self.read(rules, ',')
            elif rules.lower().endswith('tsv'):
                self.read(rules, '\t')
            else:
                self.readString(rules, '\t')
        elif isinstance(rules, List):
            if len(rules) > 0:
                if isinstance(rules[0], List):
                    self.parse_iterator(rules)
                elif isinstance(rules[0], str):
                    self.parse_iterator([line.split('\t') for line in rules])
            pass
        else:
            raise ValueError(
                "Rules can either be a List or a string. The input type: '{}' is not eligible.".format(type(rules)))
        pass

    def read(self, file_name, delimiter):
        with open(file_name, newline='') as csvfile:
            self.parse(csvfile, delimiter)
        pass

    def readString(self, input, delimiter):
        self.parse(input.splitlines(), delimiter)

    def parse(self, input, delimiter):
        spamreader = csv.reader(input, delimiter=delimiter)
        self.parse_iterator(spamreader)
        pass

    def parse_iterator(self, iterator: Union[Iterator, List]):
        row_num = 0
        for row in iterator:
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
                logging.info('Incorrect formated rule: ' + str(row))
        pass

    def buildRule(self, row_num, row):
        rule_type = 'ACTUAL'
        if len(row) == 4:
            rule_type = row[3].strip()
            self.full_definition = True
        return Rule(row_num, row[0], row[2].strip(), float(row[1].strip()), rule_type)


class Rule:
    def __init__(self, id, rule, rule_name, score=1.0, type='ACTUAL'):
        self.id = id
        self.rule = rule
        self.score = score
        self.rule_name = rule_name
        self.type = type

    def copy(self):
        return Rule(self.id, self.rule, self.rule_name, self.score, self.type)

    def __str__(self):
        return "Rule {0}:\n\trule content:\t{1}\n\trule score:\t{2}\n\trule name:\t{3}\n\trule type:\t{4}\n".format(
            self.id, self.rule, self.score, self.rule_name, self.type)

    def __repr__(self):
        return self.__str__()


class Span:
    def __init__(self, begin=-1, end=-1, text='', rule_id=-1, score=1.0):
        self.begin = begin
        self.end = end
        self.width = end - begin
        self.text = text
        self.rule_id = rule_id
        self.score = score

    def __str__(self):
        return "Span: \n\tbegin:\t{0}\n\tend:\t{1}\n\twidth:\t{2}\n\ttext:\t{3}\n\trule_id:\t{4}\n\tscore:\t{5}".format(
            self.begin, self.end, self.width, self.text, self.rule_id, self.score
        )
