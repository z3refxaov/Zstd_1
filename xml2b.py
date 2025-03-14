# -*- convert xml -> bytes        
import os
import xml.etree.ElementTree as ET

def byteint(num):
	return num.to_bytes(4, byteorder='little')

def bytestr(stri):
	outbyte = byteint(len(stri) + 4)
	outbyte += stri.encode()
	return outbyte

def byteattr(key, attr):
	if key == 'Var':
		if attr[key] == 'Array':
			stri = 'JTArr'
		elif attr[key] == 'String':
			stri = 'JTPri'
		else:
			stri = 'JT' + attr[key]
		aid = 6
	elif key == 'Var_Raw':
		stri = attr[key]
		aid = 6
	elif key == 'Type':
		stri = 'Type' + attr[key]
		aid = 8
	elif key == 'Type_Raw':
		stri = attr[key]
		aid = 8
	else:
		stri = attr[key]
		aid = int(key) if key.isdigit() else 0
	
	stripro = stri.encode()
	outbyte = byteint(len(stripro) + 8) + byteint(aid) + stripro
	return outbyte

def bytenode(node):
	iftex = False
	name1 = 'Element' if node.tag == 'Item' else node.tag
	name = bytestr(name1)
	attr1 = b''
	aindex = len(node.attrib)
	plus = 8

	for key in node.attrib:
		attr1 += byteattr(key, node.attrib)

	if node.text and node.text.strip():
		stri1 = node.text.strip()
		iftex = True
		stripro = ('V' + stri1).encode()
		attr1 += byteint(len(stripro) + 8) + byteint(5) + stripro + byteint(4)
		aindex += 1
		plus = 4

	attr1 = byteint(len(attr1) + plus) + byteint(aindex) + attr1 + byteint(4)
	alchild = b''

	if len(node):
		cindex = 0
		for child in node:
			alchild += bytenode(child)
			cindex += 1
		alchild = byteint(len(alchild) + 8) + byteint(cindex) + alchild
	else:
		if not iftex:
			alchild = byteint(4)

	bnode = name + attr1 + alchild
	bnode = byteint(len(bnode) + 4) + bnode
	return bnode

char_prefab_path = os.path.join("Prefab_Characters")
heroname_path = os.path.join(char_prefab_path, "Prefab_Hero")

if os.path.exists(heroname_path):
	for heroname in os.listdir(heroname_path):
		heroname_full_path = os.path.join(heroname_path, heroname)

		xml_files = []
		for filename in os.listdir(heroname_full_path):
			if filename.endswith(".xml"):
				new_filename = os.path.splitext(filename)[0] + ".bytes"
				new_filepath = os.path.join(heroname_full_path, new_filename)
				old_filepath = os.path.join(heroname_full_path, filename)
				os.rename(old_filepath, new_filepath)
				xml_files.append(new_filepath)  

		for xml_file in xml_files:
			with open(xml_file, "rb") as byt:
				tree = ET.parse(xml_file).getroot()
				with open(xml_file, "wb") as f:
					f.write(bytenode(tree))

			print(f"{xml_file}")