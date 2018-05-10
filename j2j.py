import sublime
import sublime_plugin
import re

regexp = '^\s*((private|protected|public|final|static|volatile)*\s+){0,3}(?P<type>[a-zA-Z_$][a-zA-Z\d_$<> ,\.\[\]]*)\s+(?P<field>[a-zA-Z_$][\w$]*)([\s=\'\"]?(?P<value>([a-zA-Z0-9_$\(\) ]+)))*[\'\"]?;'
default_values = {
		'boolean': 'true',
		'byte': '1',
		'char': '"d"',
		'double': '5.0',
		'float': '12.0',
		'int': '123',
		'integer': '123',
		'long': '9999999',
		'short': '12',
		'string': '"test_value"',
		'date': '"01-01-2010"'
}
rejected_regexps = [
		'^\s*{',
		'^\s*}',
		'^\s*package',
		'^\s*import',
		'^\s*(public|private|protected|final|asbtract|static| )*class',
		'^\s*(return|this|\.|")',
		'^\s*@',
		'^\s*/.*',
		'^\s*\\*',
		'^\s*$'
]

class J2jCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		allcontent = sublime.Region(0, self.view.size())
		content = self.view.substr(allcontent)
		lines = content.split('\n')

		filtered = filter(lambda entry: filter_out(entry), lines)

		fields = list(map(lambda entry: (regex_search(entry, 'type'), 
										 regex_search(entry, 'field'), 
										 regex_search(entry, 'value')), filtered))

		formatted_fields  = list(map(lambda entry: format_field(entry), fields))
		builtContent = '\n'.join(formatted_fields)[:-1]
		finalContent = '{' + builtContent + '}'

		self.view.replace(edit, allcontent, finalContent)
		self.view.run_command('pretty_json_and_sort')

def regex_search(source, field):
	try:
		return re.search(regexp, source).group(field)
	except AttributeError:
		print('Couldn\'t parse ' + source + ' for field ' + field)



def format_field(field_tuple):
	fieldType = field_tuple[0].replace('java.lang.', '').replace('java.util.', '')
	fieldName = field_tuple[1]
	fieldValue = field_tuple[2]

	if fieldValue:
		return ('"{}" : "{}",'.format(fieldName, fieldValue))

	return ('"{}" : {},'.format(fieldName, value_for_type(fieldType)))

def value_for_type(fieldType):
	if fieldType.endswith('[]'):
		return 	"[{}]".format(value_for_type(fieldType[:-2]))
	try:
		return default_values[fieldType.lower()]
	except KeyError:
		print('key not found:' + fieldType)
		return '{}'
		

def filter_out(entry):
	for rx in rejected_regexps:
		if re.match(rx, entry) != None:
			return False
	if re.match('.*\(.*\)', entry) != None:
		return '=' in entry and entry.index('=') < entry.index('(')
	return True



