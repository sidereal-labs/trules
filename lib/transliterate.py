#!/usr/local/bin/python
# coding: utf-8

import json
import re
import unicodedata
import sys

transforms = {}

with open("json/transforms.json") as fh:
	transforms = json.load(fh)

def transliterate(words, source=None, target="Latin", variant=None, this=None, doprint=True):
	allreturns = []
	if type(words) is not list:
		words = [words]
	for word in words:
		if type(word) is not unicode:
			try:
				word = word.decode("utf-8")
			except KeyboardInterrupt:
				sys.exit(0)
			except:
				word = word.decode("utf-16")
		# print key, len(transform["phases"])
		origword = word
		wordreturns = []
		for key, transform in transforms.iteritems():
			good = False
			dxn = 0
			# print source, transform["source"], target, transform["target"]
			if (source is None or source.lower() == transform["source"].lower()) and (transform["target"].lower() == target.lower()) and (variant is None or variant == transform["variant"] or transform["variant"] is None) and (this != transform["variant"] or this is None):
				good = True
				dxn = 1
			elif (source is None or source.lower() == transform["target"].lower()) and (transform["source"].lower() == target.lower()) and (variant is None or variant == transform["variant"] or transform["variant"] is None) and (this != transform["variant"] or this is None):
				good = True
				dxn = -1
			if good:
				word = origword
				p = 0
				for phase in transform["phases"]:
					# print "phase", p, (type(phase) is list) * len(phase)
					p += 1
					if type(phase) is list:
						i = 0
						while i < len(word): 
							# print i, word[i]
							r = 0
							for rule in phase:
								# print rule[0]
								orig = word
								# print i, len(word), rule[4]
								if dxn == 1 and rule[8] >= 0:
									try:
										word = re.sub("(^.{" + str(i) + "}" + rule[2] + ")(" + rule[0] + ")(" + rule[3] + ".*)$", "\\1" + rule[1] + "\\3", word)
									except KeyboardInterrupt:
										sys.exit(0)
									except:
										# print "Rule",r,"broken"
										pass
									r += 1
									if orig != word:
										# print i, word[i], rule[0] + " -> " + rule[1]
										# print orig, rule[0], word
										i += len(word) - len(orig) + rule[4]
										# print orig, word, i
										changed = True
										break
								elif dxn == -1 and rule[8] <= 0:
									try:
										word = re.sub("(^.{" + str(i) + "}" + rule[5] + ")(" + rule[1] + ")(" + rule[6] + ".*)$", "\\1" + rule[0] + "\\3", word)
									except KeyboardInterrupt:
										sys.exit(0)
									except:
										# print "Rule",r,"broken"
										pass
									r += 1
									if orig != word:
										# print i, word[i], rule[0] + " -> " + rule[1]
										# print orig, rule[0], word
										i += len(word) - len(orig) + rule[7]
										# print orig, word, i
										changed = True
										break									

							i += 1
							#print rule[2] + rule[0] + rule[3], " -> ", rule[1], " = ", word
					elif type(phase) is str or type(phase) is unicode:
						# print phase
						if phase.startswith("::"):
							newtrans = phase[2:].split("(")[0].strip()
							if newtrans.find("[") > -1:
								pass
								# if re.match(newtrans,word) is None:
								# 	break
							elif newtrans.find("-") > -1:
								newtrans = newtrans.encode("utf-8")
								v = None
								if len(newtrans.split("-")) > 2:
									v = newtrans.split("-")[2]
								newreturns = transliterate(word, source=newtrans.split("-")[0], target=newtrans.split("-")[1], variant=v, this=transform["variant"], doprint=False)
								if len(newreturns) > 0 and len(newreturns[0]["returns"]) > 0:
									word = newreturns[0]["returns"][0]["transliteration"]
							elif newtrans.startswith("NF"):
								word = unicodedata.normalize(newtrans,word)
							else:
								# print newtrans
								pass
				if word != origword:
					wordreturns.append({"transliteration": word, "variant": key})
		allreturns.append({"word": origword, "returns": wordreturns})
	if doprint:
		for x in allreturns:
			print x["word"]
			for y in x["returns"]:
				print "\t" + y["variant"]
				print "\t\t" + y["transliteration"]
	return allreturns