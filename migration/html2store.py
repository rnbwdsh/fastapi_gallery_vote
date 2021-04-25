import re
import os
import yaml
import sys
sys.path.insert(0,"..")
from voteable import Voteable

h = open("IconLogoIdeenfrInformatikAI.html").read()
img = h.split('img alt="" src="')[1:]

def find(i, word):
	i = re.findall(word+":(.+?)</", i)[0]
	i = i.replace("</span>", "")
	return len(i.strip())

vs = {}
for nr, i in enumerate(img):
	try:
		name = i[0:i.find('"')].replace("images/", "")
		i = i.replace("\n", "").replace("&nbsp;", "")
		gut = find(i,"Gut")
		schl = find(i,"Schlecht")
		neut = find(i,"neutral")
		v = Voteable(name)
		v.plus = set(range(gut))
		v.neutral = set(range(neut))
		v.minus = set(range(schl))
		vs[name] = v
	except Exception as e:
		print(e)

with open("../store.yml", "w") as p:
	yaml.dump(vs, p)
