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


def processReplicationCommon(evalFunc, processRulesFunc, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
	current_repeats = 0
	text_length = len(text)
	while evalFunc(this_char) and current_repeats < ReplicationFunctions.max_repeat and current_position < text_length:
		current_repeats += 1
		current_position += 1
		if current_position == text_length:
			break
		this_char = text[current_position]
	processRulesFunc(text, rule_map, match_begin, match_end, current_position, matches, previous_char, False, '+')
	pass


class ReplicationFunctions:

	def __init__(self, processRulesFunc, max_repeat=50):
		self.replication_funcs = dict()
		self.processRules = processRulesFunc
		ReplicationFunctions.max_repeat = max_repeat
		self.initReplicationFunctions(self.replication_funcs)
		pass

	def initReplicationFunctions(self, replication_funcs):
		replication_funcs['s'] = self.processReplication_s
		replication_funcs['n'] = self.processReplication_n
		replication_funcs['d'] = self.processReplication_d
		replication_funcs['C'] = self.processReplication_C
		replication_funcs['c'] = self.processReplication_c
		replication_funcs['p'] = self.processReplication_p
		replication_funcs['a'] = self.processReplication_a
		replication_funcs['u'] = self.processReplication_u
		replication_funcs['w'] = self.processReplication_w
		pass

	def processReplication_s(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		evalFunc = lambda char: (char == ' ' or char == '\t' or ord(char) == 160)
		processReplicationCommon(evalFunc, self.processRules, text, rule_map, match_begin, match_end, current_position, matches,
								 this_char, previous_char)
		pass

	def processReplication_n(self, text, rule_map, match_begin, match_end, current_position, matches, this_char, previous_char):
		evalFunc = lambda char: (char == '\n' or char == '\r')
		processReplicationCommon(evalFunc, self.processRules, text, rule_map, match_begin, match_end, current_position, matches,
								 this_char, previous_char)
		pass

	def processReplication_d(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		evalFunc = lambda char: char.isdigit()
		processReplicationCommon(evalFunc, self.processRules, text, rule_map, match_begin, match_end, current_position, matches,
								 this_char, previous_char)
		pass

	def processReplication_C(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		evalFunc = lambda char: char.isupper()
		processReplicationCommon(evalFunc, self.processRules, text, rule_map, match_begin, match_end, current_position, matches,
								 this_char, previous_char)
		pass

	def processReplication_c(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		evalFunc = lambda char: char.islower()
		processReplicationCommon(evalFunc, self.processRules, text, rule_map, match_begin, match_end, current_position, matches,
								 this_char, previous_char)
		pass

	def processReplication_p(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		evalFunc = lambda char: char in string.punctuation
		processReplicationCommon(evalFunc, self.processRules, text, rule_map, match_begin, match_end, current_position, matches,
								 this_char, previous_char)
		pass

	def processReplication_a(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		evalFunc = lambda char: not char.isspace()
		processReplicationCommon(evalFunc, self.processRules, text, rule_map, match_begin, match_end, current_position, matches,
								 this_char, previous_char)
		pass

	def processReplication_u(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		evalFunc = lambda char: (char > '~' and ord(char) != 160)
		processReplicationCommon(evalFunc, self.processRules, text, rule_map, match_begin, match_end, current_position, matches,
								 this_char, previous_char)
		pass

	def processReplication_w(self, text, rule_map, match_begin, match_end, current_position, matches,
							 this_char, previous_char):
		evalFunc = lambda char: (char > '~' or char.isspace())
		processReplicationCommon(evalFunc, self.processRules, text, rule_map, match_begin, match_end, current_position, matches,
								 this_char, previous_char)
		pass
