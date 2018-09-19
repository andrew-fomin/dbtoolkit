#!usr/bin/env python
#
# Script to automatically update an RPD with new connection pool details
# Author: Minesh Patel (Rittman Mead)


# Standard Python distribution libraries
import os
import re
import sys
import json
import argparse

from lxml import etree

# Custom python libraries:
import rm_sys

try:
	rm_sys.os.chdir(rm_sys.SCRIPT_DIR)  # Change to script directory

	# ArgumentParser to parse arguments and options
	parser = argparse.ArgumentParser(description="Rittman Mead - Updates RPD with connection pool values and variables "
	                                             "from an input file. Also can generate templates for you.")
	parser.add_argument('rpd', action="store", help='Provide input rpd path, rpd password.')
	parser.add_argument('json', help='Provide input JSON file with static variables and connection pool values. If the '
	                                 '--generate flag is passed, this specifies the name for the XML output')
	parser.add_argument('-g', '--generate', action='store_true', default=False,
	                    help='Generates the XUDML for connection pools only.')
	parser.add_argument('-o', '--output', action='store', default='patched_rpd.rpd',
	                    help='Specify filename for the RPD created once patched with the XUDML.')
	parser.add_argument('-u', '--userdsn', action='store_true', default=False,
	                    help='Changes the system to use user/DSN combinations instead of connection pools. Useful when'
	                         'the same combination is used for multiple connection pools.')
	parser.add_argument('-p', '--password', action='store', default=None,
	                    help='Specify the RPD password if it is different to the configured variable, RPD_PW')
	parser.add_argument("-c", "--configfile", action="store", default="config.ini",
	                    help="Config file to be used. Note that this is expected in the script directory.")
	parser.add_argument("-d", "--debug", action="store_true", default=False,
	                    help="Enables debugging mode, with enhanced error messages.")

	args = parser.parse_args()
	CONFIG_FILE = args.configfile

	rm_sys.parse_config(CONFIG_FILE, ['OBIEE'])
	if args.debug:
		rm_sys.DEBUG = True

	RPD = os.path.join(rm_sys.CURRENT_DIR, args.rpd)
	if not RPD.endswith('.rpd'):
		RPD = RPD + '.rpd'
	INPUT_JSON = os.path.join(rm_sys.CURRENT_DIR, args.json)
	OUTPUT_XML = os.path.join(rm_sys.CURRENT_DIR, 'gen-cp-vars.xml')
	OUTPUT_RPD = os.path.join(rm_sys.CURRENT_DIR, args.output)
	USER_DSN = args.userdsn
	GENERATE = args.generate
	#GENERATE = True
	if GENERATE:
		OUTPUT_JSON = INPUT_JSON
	else:
		if not USER_DSN:  # Infer this from the format of the file if unspecified. Can save potential mistakes in application.
			with open(INPUT_JSON) as f:
				inp = json.load(f)
				if 'user_dsns' in inp and 'connection_pool' not in inp:
					USER_DSN = True
				del inp

	XML_HEADER = """<?xml version="1.0" encoding="ISO-8859-1" ?>"""
	XML_HEADER += """<Repository xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><DECLARE>\n\n"""
	XML_FOOTER = """</DECLARE></Repository>"""

	RPD_PW = args.password
	if RPD_PW is None:
		RPD_PW = rm_sys.RPD_PW

except Exception as err:
	print '\n\nException caught:\n\n%s ' % err
	print '\n\tError: Failed to get command line arguments. Exiting.'
	sys.exit(1)


def add_variable(txt, arr):
	"""Checks text string to see if it is a repository variable and then adds it to the given set"""

	#print 'add_variable: %s' % txt

	var = re.search('VALUEOF\((.*?)\)', txt)
	if var:
		arr.add(var.group(1))


def filter_userdsns(dsn, user, udsns):
	"""Filters a list of User/DSN combinations and returns the relevant element"""
	indices = [i for i, x in enumerate(udsns) if x['dsn'] == dsn and x['user'] == user]
	if len(indices) == 1:
		return udsns[indices[0]]
	else:
		return None


def strip_str(in_str):
	"""Strips the first and last characters of a string."""
	return in_str[1:len(in_str) - 1]


def generate():
	"""Generates XUDML from an RPD file and filters for only connection pools and variables"""
	if rm_sys.obi.rpd_to_xudml(RPD, OUTPUT_XML, skip_open=True, pw=RPD_PW):
		xml = XML_HEADER
		vars_to_update = set()

		for ev, element in etree.iterparse(OUTPUT_XML, tag="ConnectionPool"):

			try:
				add_variable(element.attrib['user'], vars_to_update)
			except Exception as err:
				print 'Warning! In update_rpd.py -> generate(): no attribute "user" for parent %s' % element.attrib['parentName']

			try:
				add_variable(element.attrib['dataSource'], vars_to_update)
			except Exception as err:
				print 'Warning! In update_rpd.py -> generate(): no attribute "dataSource" for parent %s' % element.attrib['parentName']


			xml += etree.tostring(element)
			element.clear()

		for ev, element in etree.iterparse(OUTPUT_XML, tag="Variable"):
			if element.attrib['name'] in vars_to_update:
				xml += etree.tostring(element)

		xml += XML_FOOTER  # Standard XML footer
		rm_sys.write_output(xml, OUTPUT_XML, 'w')
		return xml
	else:
		print 'NOTHING'
		sys.exit(1)  # Exit on failure


def apply_cp_vars():
	"""Gets the original XUDML from an RPD and updates specific values based on the input JSON"""
	print('Extracting the original XUDML from the RPD...')

	rm_sys.check_file_exists(INPUT_JSON)  # Error if there is no input file
	generate()  # Generate XUDML from the existing RPD
	override = None

	cp_vars = rm_sys.read_json(INPUT_JSON)

	if not USER_DSN:
		print('Using connection pool based configuration format...')
	else:
		print('Using user/dsn based configuration format...')

	xml = XML_HEADER
	for ev, element in etree.iterparse(OUTPUT_XML, tag="ConnectionPool"):
		if not USER_DSN:
			if cp_name(element) in cp_vars['connection_pools']:
				override = cp_vars['connection_pools'][cp_name(element)]
		else:
			override = filter_userdsns(element.attrib['dataSource'], element.attrib['user'], cp_vars['user_dsns'])

		if override is not None:
			if not USER_DSN:

				try:
					element.attrib['dataSource'] = override['dsn']
				except Exception as err:
					print 'Error: dataSource key!!!'
					element.set('dataSource', override['dsn'])


				try:
					element.attrib['user'] = override['user']
				except Exception as err:
					print 'Error! user key!!!'
					element.set('user', override['user'])


			if override['password']:
				print('Encrypting password...')
				new_password = rm_sys.obi.encrypt_str(override['password'])
				element.attrib['password'] = new_password
			xml += etree.tostring(element)
		else:
			print('\nWarning: could not find entry in the input file for:\n\tConnection Pool: %s\n\tDSN: %s\n\tUser: %s\n' %
			      (cp_name(element), element.attrib['dataSource'], element.attrib['user']))
		element.clear()

	for ev, element in etree.iterparse(OUTPUT_XML, tag="Variable"):
		if element.attrib['name'] in cp_vars['variables']:
			element.find('./Expr').text = "'%s'" % cp_vars['variables'][element.attrib['name']]
		xml += etree.tostring(element)

	xml += XML_FOOTER
	rm_sys.write_output(xml, OUTPUT_XML, 'w')

	print('\nApplying XUDML patch to the RPD...')
	rm_sys.obi.xudml_to_rpd(OUTPUT_XML, RPD, OUTPUT_RPD, pw=RPD_PW)


def cp_name(element):
	"""Returns a clean, qualified Connection Pool name from a raw UDML CP node"""
	return strip_str(element.attrib['parentName']) + '.' + element.attrib['name']


def get_cps_vars():
	"""Generates a dictionary describing the connection pool details and variables of an RPD"""
	print('Converting RPD to XUDML...')
	if rm_sys.obi.rpd_to_xudml(RPD, OUTPUT_XML, skip_open=True, pw=RPD_PW):
		vars_to_update = set()

		print('Stripping XUDML to only required elements...')
		if not USER_DSN:
			cp_vars = {
				"connection_pools": {},
				"variables": {}
			}
		else:
			cp_vars = {
				"user_dsns": [],
				"variables": {}
			}

		for ev, element in etree.iterparse(OUTPUT_XML, tag="ConnectionPool"):

			#print 'XML elements: %s' % element.attrib

			try:
				user = element.attrib['user']
			except Exception as err:
				print 'Warning! Missing Connection Pool "user" key in XML! Substituted with a blank. Type: ConnectionPool, UID: %s, parent name: %s' % (element.attrib['uid'], element.attrib['parentName'])
				user = ''

			try:
				dsn = element.attrib['dataSource']
			except Exception as err:
				print 'Warning! Missing Connection Pool "dataSource" key in XML! Substituted with a blank. Type: ConnectionPool, UID: %s, parent name: %s' % (element.attrib['uid'], element.attrib['parentName'])
				dsn = ''

			add_variable(dsn, vars_to_update)
			add_variable(user, vars_to_update)

			if not USER_DSN:
				new_cp = {
					'dsn': dsn,
					'user': user,
					'password': ''
				}
				cp_vars['connection_pools'][cp_name(element)] = new_cp
			else:
				udsn = filter_userdsns(dsn, user, cp_vars['user_dsns'])
				if udsn is None:  # Add the User DSN combination if it doesn't exist
					cp_vars['user_dsns'].append({'dsn': dsn, 'user': user, 'password': ''})
			element.clear()

		for ev, element in etree.iterparse(OUTPUT_XML, tag="Variable"):
			if element.attrib['name'] in vars_to_update:
				cp_vars['variables'][element.attrib['name']] = strip_str(element.find('./Expr').text)

		print '\nXML extract done!'

		return cp_vars


def main():
	rm_sys.check_file_exists(RPD)
	if GENERATE:
		print('Generating passwords JSON file from the RPD...')
		rm_sys.write_output(json.dumps(get_cps_vars(), indent=4), OUTPUT_JSON, 'w')
	else:
		print 'Applying...'
		apply_cp_vars()
	rm_sys.delete_file(OUTPUT_XML)
if __name__ == "__main__":
	main()
