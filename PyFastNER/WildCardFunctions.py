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
import string


class WildCardFunctions:
    def __init__(self, processRulesFunc):
        self.wildcard_funcs = dict()
        self.initWildCardFuncs(self.wildcard_funcs)
        self.processRules = processRulesFunc
        pass

    def initWildCardFuncs(self, wildcard_funs):
        wildcard_funs['s'] = self.processWildCard_s
        wildcard_funs['n'] = self.processWildCard_n
        wildcard_funs['('] = self.processWildCard_openParan
        wildcard_funs[')'] = self.processWildCard_closeParan
        wildcard_funs['d'] = self.processWildCard_d
        wildcard_funs['C'] = self.processWildCard_C
        wildcard_funs['c'] = self.processWildCard_c
        wildcard_funs['p'] = self.processWildCard_p
        wildcard_funs['+'] = self.processWildCard_plus
        wildcard_funs['\\'] = self.processWildCard_backSlash
        wildcard_funs['b'] = self.processWildCard_b
        wildcard_funs['a'] = self.processWildCard_a
        wildcard_funs['u'] = self.processWildCard_u
        wildcard_funs['w'] = self.processWildCard_w
        wildcard_funs['e'] = self.processWildCard_e
        pass

    def processWildCard_s(self, text, rule_map, match_begin, match_end, current_position, matches,
                          this_char):
        if this_char == ' ' or this_char == '\t' or ord(this_char) == 160:
            self.processRules(text, rule_map['s'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, 's')
        pass

    def processWildCard_n(self, text, rule_map, match_begin, match_end, current_position, matches,
                          this_char):
        if this_char == '\n' or this_char == '\r':
            self.processRules(text, rule_map['n'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, 'n')
        pass

    def processWildCard_openParan(self, text, rule_map, match_begin, match_end, current_position, matches,
                                  this_char):
        if this_char == '(':
            self.processRules(text, rule_map['('], match_begin, match_end, current_position + 1, matches,
                              this_char, True, '(')
        pass

    def processWildCard_closeParan(self, text, rule_map, match_begin, match_end, current_position, matches,
                                   this_char):
        if this_char == ')':
            self.processRules(text, rule_map[')'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, ')')
        pass

    def processWildCard_d(self, text, rule_map, match_begin, match_end, current_position, matches,
                          this_char):
        if this_char.isdigit():
            self.processRules(text, rule_map['d'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, 'd')
        pass

    def processWildCard_C(self, text, rule_map, match_begin, match_end, current_position, matches,
                          this_char):
        if this_char.isupper():
            self.processRules(text, rule_map['C'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, 'C')
        pass

    def processWildCard_c(self, text, rule_map, match_begin, match_end, current_position, matches,
                          this_char):
        if this_char.islower():
            self.processRules(text, rule_map['c'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, 'c')
        pass

    def processWildCard_p(self, text, rule_map, match_begin, match_end, current_position, matches,
                          this_char):
        if this_char in string.punctuation:
            self.processRules(text, rule_map['p'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, 'p')
        pass

    def processWildCard_plus(self, text, rule_map, match_begin, match_end, current_position, matches,
                             this_char):
        if this_char.islower():
            self.processRules(text, rule_map['c'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, 'c')
        pass

    def processWildCard_backSlash(self, text, rule_map, match_begin, match_end, current_position, matches,
                                  this_char):
        if this_char == '\\':
            self.processRules(text, rule_map['\\'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, '\\')

    def processWildCard_a(self, text, rule_map, match_begin, match_end, current_position, matches,
                          this_char):
        if not this_char.isspace():
            self.processRules(text, rule_map['a'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, 'a')
            pass

    def processWildCard_u(self, text, rule_map, match_begin, match_end, current_position, matches,
                          this_char):
        if this_char > '~' and ord(this_char) != 160:
            self.processRules(text, rule_map['u'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, 'u')
            pass

    def processWildCard_w(self, text, rule_map, match_begin, match_end, current_position, matches,
                          this_char):
        if this_char > '~' or this_char.isspace():
            self.processRules(text, rule_map['w'], match_begin, match_end, current_position + 1, matches,
                              this_char, True, 'w')
            pass

    def processWildCard_b(self, text, rule_map, match_begin, match_end, current_position, matches,
                          this_char):
        if current_position == 0:
            self.processRules(text, rule_map['b'], match_begin, match_end, current_position, matches,
                              this_char, True, 'b')
            pass

    def processWildCard_e(self, text, rule_map, match_begin, match_end, current_position, matches,
                          this_char):
        if current_position == len(text):
            self.processRules(text, rule_map['e'], match_begin, match_end, current_position, matches,
                              this_char, True, 'e')
            pass