import os, sys
for l in range(10) :
	for c in range(10) :
		c = str(c)
		l = str(l)
#		try : 
		os.rename("D:/Python/Projet_Jeux_video/Programme/Gros_projet/exploration/(" + l + ", " + c + ").txt", "D:/Python/Projet_Jeux_video/Programme/Gros_projet/explo/(" + c + ", " + l + ").txt" )
#		except :
#			print("a")
		c = int(c)
		l = int(l)