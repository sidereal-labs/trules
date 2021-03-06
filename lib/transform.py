#!/usr/local/bin/python
# coding: utf-8

import xml.etree.ElementTree as et
import re
import os
import json

transforms = {}

files = ["transforms/" + file for file in os.listdir("transforms/") if file[-3:] == "xml"] + ["transforms/cldr/" + file for file in os.listdir("transforms/cldr") if file[-3:] == "xml"]

for file in files:
	tree = et.parse(file)
	print "Rebuilding from", file, "                                                             \r",
	for transform in tree.findall("transforms/transform"):
		phases = [[]]
		definitions = []
		source = transform.attrib["source"]
		target = transform.attrib["target"]
		direction = transform.attrib["direction"]
		variant = None
		if "variant" in transform.attrib:
			variant = transform.attrib["variant"]
		# print source, target, direction
		for trule in transform.findall("tRule"):
			if trule.text and len(trule.text.strip()) > 0:
				rule = trule.text.split(";")[0].strip()
				try:
					while rule.find("""\u""") > -1:
						idx = rule.find("""\u""")
						rule = rule[:idx] + unicode(str(rule[idx:idx+6]),"unicode-escape") + rule[idx+6:]
					while rule.find("""\U""") > -1:
						idx = rule.find("""\U""")
						rule = rule[:idx] + unicode(str(rule[idx:idx+10]),"unicode-escape") + rule[idx+10:]
				except UnicodeError as e:
					print e
					print file
					print trule.text
				rule = rule.encode("utf-8")
				if rule.find("=") > -1 and rule.startswith("$"):
					for definition in definitions:
						rule = rule.replace(definition[0], definition[1])
					definitions.append([x.strip() for x in rule.split("=")])
				elif rule.find("→") > -1 or rule.find("↔") > -1 or rule.find("←") > -1:
					for definition in definitions:
						rule = rule.replace(definition[0], definition[1])
					rule = rule.replace("' '", "$space").replace("\ ", "$space")
					dxn = 0
					if rule.find("→") > -1:
						dxn = 1
						pre = rule.split("→")[0].strip().decode("utf-8").replace(" ","")
						post = rule.split("→")[1].strip().decode("utf-8").replace(" ","")
					elif rule.find("↔") > -1:
						dxn = 0
						pre = rule.split("↔")[0].strip().decode("utf-8").replace(" ","")
						post = rule.split("↔")[1].strip().decode("utf-8").replace(" ","")
					elif rule.find("←") > -1:
						dxn = -1
						pre = rule.split("←")[0].strip().decode("utf-8").replace(" ","")
						post = rule.split("←")[1].strip().decode("utf-8").replace(" ","")
						# if post.find("{") > -1:
						# 	post = post.split("{")[1]
						# if post.find("}") > -1:
						# 	post = post.split("}")[0]
					prectxtleft = u""
					prectxtright = u""
					postrevisit = 0;
					postctxtleft = u""
					postctxtright = u""
					prerevisit = 0;

					if "|" in post:
						postrevisit = -1 * len(post.split("|")[1])
						post = "".join(post.split("|")).replace("@","")
					if "{" in pre:
						prectxtleft = pre.split("{")[0].strip()
						pre = pre.split("{")[1].strip()
					if "}" in pre:
						prectxtright = pre.split("}")[1].strip()
						pre = pre.split("}")[0].strip()

					if "|" in pre:
						prerevisit = -1 * len(pre.split("|")[1])
						pre = "".join(pre.split("|")).replace("@","")
					if "{" in post:
						postctxtleft = post.split("{")[0].strip()
						post = post.split("{")[1].strip()
					if "}" in post:
						postctxtright = post.split("}")[1].strip()
						post = post.split("}")[0].strip()

					phases[-1].append([re.sub("\[\:([^\]]*)\:\]", "\\p{\\1}",x.encode("utf-8").replace("$space", " ").replace("'.'","\\.")) for x in [pre, post, prectxtleft, prectxtright, postctxtleft, postctxtright]] + [postrevisit, prerevisit, dxn])
				elif rule is not None and len(rule) > 0:
					if type(phases[-1]) is "list" and len(phases[-1]) == 0:
						phases[-1] = re.sub("\[\:([^\]]*)\:\]", "\\p{\\1}", rule)
					else:
						phases.append(re.sub("\[\:([^\]]*)\:\]", "\\p{\\1}", rule))
					phases.append([])
		#print phases
		transforms[file[:-4]] = {"source": source, "target": target, "direction": direction, "phases": phases, "variant": variant}

print "\nParsed", len(files), "files"
print "Writing results to json/transforms.json"

with open("./json/transforms.json","w") as fh:
	json.dump(transforms, fh)

print "Done\n"

