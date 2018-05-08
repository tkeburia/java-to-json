import sublime
import sublime_plugin
import re

class J2jCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		allcontent = sublime.Region(0, self.view.size())
		content = self.view.substr(allcontent)
		lines = content.split('\n')

		regexp = '^\s*((private|protected|public|final|static|volatile)*\s+){0,3}(?P<type>[a-zA-Z_$][a-zA-Z\d_$<> ,]*)\s+(?P<field>[a-zA-Z_$][\w$]+)(?P<value>(\s?=\s?\w+))?;'

		filtered = filter(lambda entry: filter_out(entry), lines)
		fields = list(map(lambda entry: (re.search(regexp, entry).group('type'), 
										re.search(regexp, entry).group('field'), 
										re.search(regexp, entry).group('value')), filtered))
		formatted_fields  = list(map(lambda entry: format_field(entry), fields))
		builtContent = '\n'.join(formatted_fields)[:-1]
		finalContent = '{' + builtContent + '}'

		self.view.replace(edit, allcontent, finalContent)

		self.view.run_command('pretty_json_and_sort')


def format_field(field_tuple):

	fieldType = field_tuple[0]
	fieldName = field_tuple[1]

	if field_tuple[2]:
		return ('"{}" : "{}",'.format(fieldName, field_tuple[2]))

	if fieldType.lower() == 'boolean':
		return ('"{}" : {},'.format(fieldName, 'true'))
	if fieldType == 'byte':
		return ('"{}" : {},'.format(fieldName, '1'))
	if fieldType == 'char':
		return ('"{}" : "{}",'.format(fieldName, 'd'))
	if fieldType == 'double':
		return ('"{}" : {},'.format(fieldName, '5.0'))
	if fieldType == 'float':
		return ('"{}" : {},'.format(fieldName, '12.0'))
	if fieldType == 'int':
		return ('"{}" : {},'.format(fieldName, '123'))
	if fieldType == 'long':
		return ('"{}" : {},'.format(fieldName, '9999999'))
	if fieldType == 'short':
		return ('"{}" : {},'.format(fieldName, '12'))
	if fieldType == 'String':
		return ('"{}" : "{}",'.format(fieldName, fieldName))


	return ('"{}" : "{}",'.format(fieldName, '{}'))


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