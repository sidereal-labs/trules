import json
import re
import unicodedata
import sys
import codecs

with open("../json/transforms.json") as fh:
	transforms = json.load(fh)	
	i = 1
	k = 1
	j = 1
	with codecs.open("../tsv/sets.tsv","w","utf-8") as setfile:
		setfile.write(u'\ufeff')
		setfile.write("\t".join(["id","name","source","target","variant","direction"]) + "\n")
		with codecs.open("../tsv/phases.tsv","w","utf-8") as phasefile:
			phasefile.write(u'\ufeff')
			phasefile.write("\t".join(["set_id","phase_id","forward_transform_source","forward_transform_target","forward_transform_variant","forward_filter","forward_function","reverse_transform_source","reverse_transform_target","reverse_transform_variant","reverse_filter","reverse_function"]) + "\n")
			with codecs.open("../tsv/rules.tsv","w","utf-8") as rulesfile:
				rulesfile.write(u'\ufeff')
				rulesfile.write("\t".join(["id","set_id","phase_id","source","target","source_context_left","source_context_right", "target_context_left", "target_context_right","source_revisit", "target_revisit", "direction"]) + "\n")
				for key, value in transforms.iteritems():
					setfile.write("\t".join([str(x) for x in [i, key, value["source"], value["target"], value["variant"], value["direction"]]]) + "\n")
					for phase in value["phases"]:
						if type(phase) is list:
							if len(phase) > 0:
								for rule in phase:
									rulesfile.write(str(k) + "\t" + str(i) + "\t" + str(j) + "\t")
									for step in rule:
										if step is None:
											rulesfile
										elif type(step) is int:
											rulesfile.write(str(step))
										else:
											rulesfile.write(step)
										rulesfile.write("\t")
									rulesfile.write("\n")
									k += 1
								phasefile.write("\t".join([str(i),str(j),"","","","","","","","","",""]) + "\n")
								j += 1

						elif phase.startswith("::"):
							forward = phase[2:].split("(")[0].strip()
							reverse = phase[2:].split("(")[-1].split(")")[0].strip()
							forward_transform = ['','','']
							reverse_transform = ['','','']
							forward_filter = ''
							reverse_filter = ''
							forward_function = ''
							reverse_function = ''
							
							if forward.find("[") > -1:
								forward_filter = forward
							elif forward.find("-") > -1:
								trans = forward.split("-")
								for a in range(len(trans)):
									forward_transform[a] = trans[a]
							else:
								forward_function = forward
							
							if reverse != forward:	
								if reverse.find("[") > -1:
									reverse_filter = reverse							
								elif reverse.find("-") > -1:
									trans = reverse.split("-")
									for a in range(len(trans)):
										reverse_transform[a] = trans[a]
								else:
									reverse_function = reverse
							else:
								reverse_transform = [forward_transform[1], forward_transform[0], forward_transform[2]]
								reverse_filter = forward_filter
								reverse_function = forward_function
							
							phasefile.write(str(i) + "\t" + str(j) + "\t" + "\t".join(["\t".join(forward_transform), forward_filter, forward_function, "\t".join(reverse_transform), reverse_filter, reverse_function]) + "\n")
					i += 1
					j += 1