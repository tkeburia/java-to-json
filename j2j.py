import sublime
import sublime_plugin
import re

class J2jCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		allcontent = sublime.Region(0, self.view.size())
		content = self.view.substr(allcontent)
		lines = content.split('\n')

		filtered = filter(lambda entry: filter_out(entry), lines)
		fields = list(map(lambda entry: re.search('^\s*([a-zA-z<>]*\s){1,3}(?P<field>\w+)(\s?=\s?.*);', entry).group('field'), filtered))
		formatted_fields  = list(map(lambda entry: format_field(entry), fields))
		builtContent = '\n'.join(formatted_fields)[:-1]
		finalContent = '{' + builtContent + '}'

		self.view.replace(edit, allcontent, finalContent)

		self.view.run_command('pretty_json_and_sort')


def format_field(field):
	return ('"{}" : "{}",'.format(field, field))


def filter_out(entry):
	if re.match('^\s*@', entry) != None:
		return False
	if re.match('^\s*/.*', entry) != None:
		return False
	if re.match('^\s*\\*', entry) != None:
		return False				
	if re.match('^\s*$', entry) != None:
		return False
	return True