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
# from quicksect import IntervalTree
import logging
import logging.config
import os
from typing import Union, List, Dict

from quicksectx import IntervalTree, Interval

from .IOUtils import IOUtils, Rule, Span
from .ReplicationFunctionsLambda import ReplicationFunctions
from .ReplicationFunctionsLambda import processReplicationCommon
from .WildCardFunctions import WildCardFunctions


def initLogger():
    config_files = ['../../../conf/logging.ini', '../../conf/logging.ini', '../conf/logging.ini', 'conf/logging.ini',
                    'logging.ini']
    config_file = None
    for f in config_files:
        if os.path.isfile(f):
            config_file = f
            break
    if config_file is None:
        config_file = config_files[-1]
        with open(config_file, 'w') as f:
            f.write('''[loggers]
keys=root

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=WARNING
handlers=consoleHandler

[handler_consoleHandler]
class=StreamHandler
level=WARNING
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=
''')
    logging.config.fileConfig(config_file)


# initLogger()


class FastCNER:
    END = ('<END>')

    def __init__(self, rules: Union[str, List] = '', max_repeat: int = 50, enable_logger: bool = False):
        self.span_compare_method = 'width'
        self.support_replication = False
        self.offset = 0
        self.max_repeat = max_repeat
        self.overlap_checkers = dict()
        self.wildcard_funcs = WildCardFunctions(self.processRules).wildcard_funcs
        self.replication_funcs = ReplicationFunctions(self.processRules, self.max_repeat).replication_funcs
        self.rule_str = rules
        self.rule_map = dict()
        self.scores = dict()
        self.full_definition = False
        self.rule_store = {}
        self.initiate(rules)
        if enable_logger:
            initLogger()
            self.logger == logging.getLogger(__name__)
        else:
            self.logger = None

    def initiate(self, rule_str):
        self.rule_str = rule_str
        self.rule_map.clear()
        self.rule_store.clear()
        self.scores.clear()
        io_utils = IOUtils(rule_str)
        self.full_definition = io_utils.full_definition
        self.rule_store = io_utils.rule_cells
        self.constructRuleMap(self.rule_store)
        pass

    def constructRuleMap(self, rule_store):
        # reset the variables in case reuse this function to re-initiate from rule_store
        self.rule_map.clear()
        self.rule_store = rule_store
        self.scores.clear()

        for id, rule in rule_store.items():
            if '[' in rule.rule:
                rules = self.expandSquareBracket(rule)
                for subrule in rules:
                    self.addRule(subrule)
            else:
                self.addRule(rule)
        pass

    def getType(self, span):
        return self.rule_store[span.rule_id].type

    # expand rules with square brackets
    def expandSquareBracket(self, rule):
        OUT = 0
        IN = 1
        expanded_rules = []
        rule_builder = []
        rule_builder.append([])
        rule_str = rule.rule
        # status: 0 for OUT, 1 for in
        status = OUT
        pre_char = ' '
        next_ch = ' '
        branches = []
        for i in range(0, len(rule_str)):
            ch = rule_str[i]
            if i > 0:
                pre_char = rule_str[i - 1]
            if i < len(rule_str) - 1:
                next_ch = rule_str[i + 1]
            else:
                next_ch = ' '
            if status == OUT and (ch != '[' or pre_char == '\\'):
                if ch == '\\' and (next_ch == '[' or next_ch == ']'):
                    pre_char = ch
                    continue
                for j in range(0, len(rule_builder)):
                    rule_builder[j].append(ch)
            elif status == OUT and ch == '[' and pre_char != '\\':
                status = IN
                branches = [[]]
                continue
            elif status == IN and (ch != ']' or (ch == ']' and pre_char == '\\')):
                if ch == '|':
                    branches.append([])
                elif ch == '\\' and (next_ch == '[' or next_ch == ']'):
                    pre_char = ch
                    continue
                else:
                    branches[-1].append(ch)
            elif status == IN and ch == ']' and pre_char != '\\':
                status = OUT
                previous_size = len(rule_builder)
                if ch == '\\' and (next_ch == '[' or next_ch == ']'):
                    pre_char = ch
                    continue
                for j in range(0, previous_size):
                    sb = list(rule_builder[j])
                    rule_builder[j].extend(branches[0])
                    for k in range(1, len(branches)):
                        rule_builder.append(list(sb))
                        rule_builder[-1].extend(branches[k])
        cleanSet = set()
        for sub_rule in rule_builder:
            rule_str = ''.join(sub_rule)
            if rule_str not in cleanSet:
                new_rule = Rule(rule.id, rule_str, rule.rule_name, rule.score, rule.type)
                expanded_rules.append(new_rule)
                cleanSet.add(rule_str)
        return expanded_rules

    def addRule(self, rule):
        determinant = rule.rule_name
        rule_map1 = self.rule_map
        rule_map2 = dict()
        length = len(rule.rule)
        rule_str = rule.rule
        if '+' in rule_str:
            self.support_replication = True
        i = 0
        while i < length and rule_map1 != None and rule_str[i] in rule_map1:
            rule_map1 = rule_map1.get(rule_str[i])
            i += 1
        # if the rule has been included
        if i == length and FastCNER.END in rule_map1 and rule_map1[FastCNER.END] == determinant:
            return False
        # 		start with the determinant, construct the last descendant dict
        if i == length:
            if FastCNER.END in rule_map1:
                rule_map1[FastCNER.END][determinant] = rule.id
            else:
                rule_map2[determinant] = rule.id
                rule_map1[FastCNER.END] = rule_map2.copy()
            self.scores[rule.id] = rule.score
            return True
        else:
            rule_map2[determinant] = rule.id
            rule_map2[FastCNER.END] = rule_map2.copy()
            rule_map2.pop(determinant, None)

            for j in range(length - 1, i, -1):
                rule_mapt = rule_map2.copy()
                rule_map2.clear()
                rule_map2[rule_str[j]] = rule_mapt
        self.scores[rule.id] = rule.score
        rule_map1[rule_str[i]] = rule_map2.copy()
        return True

    def processString(self, text: str, offset: int = 0):
        matches: Dict = dict()
        return self.process(text, offset, matches)

    def process(self, text: str, offset: int = 0, matches: Dict = dict()):
        """

        @param text: input text
        @param offset: start position to check matches
        @param matches: matches rules. You can redefine keys to ensure the order of the keys
        @return: A dictionary of matched Span grouped by types(keys)
        """
        self.offset = offset
        self.overlap_checkers.clear()
        for i in range(0, len(text)):
            pre_char = text[i - 1] if i > 0 else ' '
            self.processRules(text, self.rule_map, i, 0, i, matches, pre_char, False, ' ')
        self.removePseudo(matches)
        return matches

    def processRules(self, text, rule_map, match_begin, match_end, current_position,
                     matches, pre_char, wildcard_support, pre_key):
        length = len(text)
        if current_position < length:
            this_char = text[current_position]

            if '\\' in rule_map:
                self.processWildCards(text, rule_map['\\'], match_begin, match_end, current_position, matches, pre_char,
                                      True, '\\')
            if '(' in rule_map and pre_key != '\\':
                self.processRules(text, rule_map['('], current_position, match_end, current_position, matches, pre_char,
                                  False, '(')
            if ')' in rule_map and pre_key != '\\':
                self.processRules(text, rule_map[')'], match_begin, current_position, current_position, matches,
                                  pre_char, False, ')')

            if FastCNER.END in rule_map:
                self.addDeterminants(text, rule_map, matches, match_begin, match_end, current_position)
            if this_char in rule_map and this_char != ')' and this_char != '(':
                self.processRules(text, rule_map[this_char], match_begin, match_end, current_position + 1, matches,
                                  this_char, False, this_char)

            if self.support_replication and '+' in rule_map:
                self.processRules(text, rule_map['+'], match_begin, match_end, current_position, matches, this_char,
                                  False, '+')
                self.processReplication(text, rule_map['+'], match_begin, match_end, current_position, matches,
                                        this_char, wildcard_support, pre_key)
        elif current_position == length and FastCNER.END in rule_map:
            if match_end == 0:
                self.addDeterminants(text, rule_map, matches, match_begin, current_position, current_position)
            else:
                self.addDeterminants(text, rule_map, matches, match_begin, match_end, current_position)
        elif current_position == length and '\\' in rule_map and 'e' in rule_map['\\']:
            deter_rule = rule_map['\\']['e']
            if match_end == 0:
                self.addDeterminants(text, deter_rule, matches, match_begin, current_position, current_position)
            else:
                self.addDeterminants(text, deter_rule, matches, match_begin, match_end, current_position)
        elif current_position == length and ')' in rule_map:
            deter_rule = rule_map[')']
            if FastCNER.END in deter_rule:
                self.addDeterminants(text, deter_rule, matches, match_begin, current_position, current_position)
            elif '\\' in deter_rule and 'e' in deter_rule['\\']:
                self.processRules(text, deter_rule['\\'], match_begin, current_position, current_position, matches,
                                  pre_char, False, ' ')
        elif current_position == length and '+' in rule_map:
            self.processRules(text, rule_map['+'], match_begin, match_end, current_position, matches, pre_char,
                              wildcard_support, pre_key)
        pass

    def processReplication(self, text, rule_map, match_begin, match_end, current_position, matches,
                           pre_char, wildcard_support, pre_key):
        this_char = text[current_position]
        if wildcard_support:
            if pre_key in self.replication_funcs:
                self.replication_funcs[pre_key](text, rule_map, match_begin, match_end, current_position, matches,
                                                this_char, pre_char)
            else:
                logging.info('"\\' + pre_key + '+" is not a eligible syntax.')
        else:
            processReplicationCommon(lambda char: char == pre_key, self.processRules, text, rule_map, match_begin,
                                     match_end, current_position,
                                     matches,
                                     this_char, pre_char)
        pass

    def processWildCards(self, text, rule_map, match_begin, match_end, current_position, matches,
                         pre_char, wildcard_support, pre_key):
        this_char = text[current_position]
        for rule_char in rule_map.keys():
            if rule_char in self.wildcard_funcs:
                self.wildcard_funcs[rule_char](text, rule_map, match_begin, match_end, current_position, matches,
                                               this_char)
            else:
                logging.info('"\\' + rule_char + '" is not a eligible syntax.')
        pass

    def addDeterminants(self, text, deter_rule, matches, match_begin, match_end, current_position):
        deter_rule = deter_rule[FastCNER.END]
        end = current_position if match_end == 0 else match_end
        current_span = Span(match_begin + self.offset, end + self.offset,
                            text[match_begin:end])
        current_spans_list = []
        overlap_checkers = self.overlap_checkers
        for key in deter_rule.keys():
            rule_id = deter_rule[key]
            if self.logger is not None:
                self.logger.debug(
                    'try add matched rule ({}-{})\t{}'.format(match_begin, match_end, str(self.rule_store[rule_id])))
            current_span.rule_id = rule_id
            if key in matches:
                current_spans_list = matches[key]
                overlap_checker = overlap_checkers[key]
                overlapped_pos = overlap_checker.search(current_span.begin, current_span.end)
                if len(overlapped_pos) > 0:
                    pos = overlapped_pos.pop().data
                    overlapped_span = current_spans_list[pos]
                    if not self.compareSpan(current_span, overlapped_span):
                        continue
                    current_spans_list[pos] = current_span
                    overlap_checker.remove(Interval(current_span.begin, current_span.end))
                    overlap_checker.add(current_span.begin, current_span.end, pos)
                else:
                    overlap_checker.add(current_span.begin, current_span.end, len(current_spans_list))
                    current_spans_list.append(current_span)
            else:
                matches[key] = current_spans_list
                overlap_checker = IntervalTree()
                # quickset's search will include both lower and upper bounds, so minus one from the end.
                overlap_checker.add(current_span.begin, current_span.end - 1, len(current_spans_list))
                current_spans_list.append(current_span)
                overlap_checkers[key] = overlap_checker

        pass

    def compareSpan(self, a, b):
        if self.span_compare_method == 'score':
            return a.score < 0 or a.score > b.score
        elif self.span_compare_method == 'scorewidth':
            return a.score < 0 or a.score > b.score or (a.score == b.score and a.width > b.width)
        elif self.span_compare_method == 'widthscore':
            return a.width > b.width or (a.width == b.width and a.score > b.score)
        else:
            return a.width > b.width

    def removePseudo(self, matches):
        for key, span_list in matches.items():
            cleaned_list = [x for x in span_list if self.rule_store[x.rule_id].type == 'ACTUAL']
            matches[key] = cleaned_list
        pass
