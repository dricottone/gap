#!/usr/bin/env python3

import re

def main(arguments):
	config=dict()
	positional=[]
	pattern=re.compile(r"(?:-(?:f|o|h|x|V|v|q)|--(?:format|output|help|version|verbose|quiet|attached-values|no-attached-values|debug-mode|no-debug-mode|executable|no-executable|raise-on-overfull|no-raise-on-overfull))(?:=.*)?$")
	consuming,needing,wanting=None,0,0
	attached_value=None
	while len(arguments) and arguments[0]!="--":
		if consuming is not None:
			if config[consuming] is None:
				config[consuming]=arguments.pop(0)
			else:
				config[consuming].append(arguments.pop(0))
			needing-=1
			wanting-=1
			if wanting==0:
				consuming,needing,wanting=None,0,0
		elif pattern.match(arguments[0]):
			option = arguments.pop(0).lstrip('-')
			if '=' in option:
				option,attached_value=option.split('=',1)
			if option=="format":
				if attached_value is not None:
					config["format"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["format"]=None
					consuming,needing,wanting="format",1,1
			elif option=="output":
				if attached_value is not None:
					config["output"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["output"]=None
					consuming,needing,wanting="output",1,1
			elif option=="help":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "help"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["help"]=True
			elif option=="version":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "version"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["version"]=True
			elif option=="verbose":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "verbose"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["verbose"]=True
			elif option=="quiet":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "quiet"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["quiet"]=True
			elif option=="attached-values":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "attached-values"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["attached-values"]=True
			elif option=="no-attached-values":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "no-attached-values"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["no-attached-values"]=True
			elif option=="debug-mode":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "debug-mode"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["debug-mode"]=True
			elif option=="no-debug-mode":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "no-debug-mode"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["no-debug-mode"]=True
			elif option=="executable":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "executable"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["executable"]=True
			elif option=="no-executable":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "no-executable"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["no-executable"]=True
			elif option=="raise-on-overfull":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "raise-on-overfull"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["raise-on-overfull"]=True
			elif option=="no-raise-on-overfull":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "no-raise-on-overfull"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["no-raise-on-overfull"]=True
			elif option=="f":
				if attached_value is not None:
					config["format"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["format"]=None
					consuming,needing,wanting="format",1,1
			elif option=="o":
				if attached_value is not None:
					config["output"]=attached_value
					attached_value=None
					consuming,needing,wanting=None,0,0
				else:
					config["output"]=None
					consuming,needing,wanting="output",1,1
			elif option=="h":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "help"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["help"]=True
			elif option=="x":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "help"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["help"]=True
			elif option=="V":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "version"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["version"]=True
			elif option=="v":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "verbose"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["verbose"]=True
			elif option=="q":
				if attached_value is not None:
					message=(
						'unexpected value while parsing "quiet"'
						' (expected 0 values)'
					)
					raise ValueError(message) from None
				config["quiet"]=True
		else:
			positional.append(arguments.pop(0))
	if needing>0:
		message=(
			f'unexpected end while parsing "{consuming}"'
			f' (expected {needing} values)'
		)
		raise ValueError(message) from None
	for argument in arguments[1:]:
		positional.append(argument)
	return config,positional

