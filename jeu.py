
import pygame
from pygame.locals import *
from exploration import *
from ville import *
from donjon import *
from classes import*
from multijoueur import *
import socket

pygame.init()
fenetre = pygame.display.set_mode((500,500))
jouer = 1
accueil = 1
monstre = Monstre()
player = Player()
info_item = Item()
serveur = Serveur()
list_coordonnee = Coordonnee()
boss1 = Boss()
sauvegarde = []
player_existant = False

police=pygame.font.Font(None, 20)
text=police.render("PSEUDO :", True, (255,255,255))
entree= True
nom_player=""
while entree :
	fenetre.fill((0,0,0))
	fenetre.blit(text, (170, 240))
	background = pygame.draw.rect(fenetre, (255,255,255), (245, 235, 200, 20))
	for event in pygame.event.get() :
		if event.type==QUIT :
			entree = False
			jouer = False
		if event.type == KEYDOWN :
			if event.key == 13 :
				entree = False
			if event.key == 8 : #Supprimer
				nom_player = nom_player[:-1]
			if event.unicode in "azertyuiopqsdfghjklmwxcvbn" :
				nom_player = str(nom_player)+str(event.unicode)

	entree_utilisateur = police.render(str(nom_player), True, (0,0,0))
	fenetre.blit(entree_utilisateur, (250, 240))
	pygame.display.flip()

player.name = nom_player

try :
	save = open("save_"+str(player.name)+".txt", "r")
	player.item = []
	player.item_equip = "Pioche Pierre"
	player.item_possess = []
	player.item_quantite = {}
	for ligne in save :
		sauvegarde.append(ligne)
	player.money = int(sauvegarde[0])
	player.exp = int(sauvegarde[1])
	player.lvl = int(sauvegarde[2])
	player.exp_require_lvl_up = 100*(2**player.lvl)
	if sauvegarde[6] == "False\n" :
		player.first_time_ville = False
	else :
		player.first_time_ville = True

	for element in sauvegarde[3].split("/") :
		if element!="" and element!="\n" :
			player.item_possess.append(element)
	for element in sauvegarde[4].split("/") :
		if element!="" and element!="\n" :
			player.item_spe_possess.append(element)
	for element in sauvegarde[5].split("/") :
		if element!="" and element!="\n":
			player.item_quantite[str(element.split(":")[0])]=int(element.split(":")[1])
	colonne, ligne = 0, 0
	for element in sauvegarde[7].split("/") :
		if element!="" and element!="\n" :
			for ligne in range(10) :
				for colonne in range(10) :
					if element == str((colonne, ligne)) :
						player.zone_explo_deja_explore.append((colonne, ligne))
	#######################################################
	#######Chargement des list_coordonnee.explo_...########
	#######################################################
	for position in player.zone_explo_deja_explore :
		with open("exploration/" + str(position) + ".txt", 'r') as fichier :
			numero_colonne = 0
			numero_ligne = 0
			explo_coal, explo_sol, explo_mur  = [], [], []
			for ligne in fichier :
				for caractere in ligne :
					coordonne_x = int(numero_colonne*25)
					coordonne_y = int(numero_ligne*25)
					if caractere == "0" :
						charbon = randrange(10)
						if charbon == 0 :
							explo_coal.append((coordonne_x, coordonne_y))
						else :
							explo_sol.append((coordonne_x, coordonne_y))
					if caractere == "m" :
						explo_mur.append((coordonne_x, coordonne_y))
					numero_colonne += 1
				numero_ligne+=1
				numero_colonne = 0
		list_coordonnee.explo_mur_zone_deja_explore[position] = explo_mur
		list_coordonnee.explo_sol_zone_deja_explore[position] = explo_sol
		list_coordonnee.explo_coal_zone_deja_explore[position] = explo_coal
		list_coordonnee.explo_lantern_zone_deja_explore[position] = []
except :
	pass
player.multijoueur = False

while jouer :
	fenetre = pygame.display.set_mode((500,500))
	hauteur = 1
	while accueil :
		fenetre.fill((0,0,0))
		police = pygame.font.Font("Police/SuperMario.ttf", 24)
		text_dungeon = police.render("DUNGEON", True, (255,255,255))
		text_dungeon_select = police.render("DUNGEON", True, (255,255,0))
		text_ville = police.render("VILLE", True, (255,255,255))
		text_ville_select = police.render("VILLE", True, (255,255,0))
		text_exploration = police.render("EXPLORATION", True, (255,255,255))
		text_exploration_select = police.render("EXPLORATION", True, (255,255,0))
		text_multijoueur = police.render("MULTIJOUEUR", True, (255,255,255))
		text_multijoueur_select = police.render("MULTIJOUEUR", True, (255,255,0))
		police_sword = pygame.font.Font("Police/Fantasy.ttf", 20)
		sword = police_sword.render("H", True, (255,255,255))
		ville, dungeon, explo, multi = False, False, False, False

		if hauteur%4 == 1 :
			fenetre.blit(text_dungeon, (180, 260))
			fenetre.blit(text_exploration, (150,230))
			fenetre.blit(text_ville_select, (200, 200))
			fenetre.blit(text_multijoueur, (140, 290))
			fenetre.blit(sword, (100, 200))
			ville = True

		if hauteur%4 == 2 :
			fenetre.blit(text_dungeon, (180, 260))
			fenetre.blit(text_exploration_select, (150,230))
			fenetre.blit(text_ville, (200, 200))
			fenetre.blit(text_multijoueur, (140, 290))
			fenetre.blit(sword, (50, 230))
			explo = True

		if hauteur%4 == 3 :
			fenetre.blit(text_dungeon_select, (180, 260))
			fenetre.blit(text_exploration, (150,230))
			fenetre.blit(text_ville, (200, 200))
			fenetre.blit(text_multijoueur, (140, 290))
			fenetre.blit(sword, (80, 260))
			dungeon = True

		if hauteur%4 == 0 :
			fenetre.blit(text_multijoueur_select, (140, 290))
			fenetre.blit(text_exploration, (150,230))
			fenetre.blit(text_ville, (200, 200))
			fenetre.blit(text_dungeon, (180, 260))
			fenetre.blit(sword, (40, 290))
			multi = True

		for event in pygame.event.get() :
			if event.type == KEYDOWN :
				if event.key == K_DOWN :
					hauteur+=1
				if event.key == K_UP :
					hauteur-=1
				if event.key == 13 : #si la touche ENTER est pressé 
					accueil = False

			if event.type == QUIT :
				jouer = False
				accueil = False
				explo = False
				ville = False
				donjon = False

		pygame.display.flip()

	if explo :
		chargement_explo(fenetre, player, list_coordonnee, monstre)
		item_equip_possess = False
		for item in player.item_possess :
			if item == player.item_equip :
				item_equip_possess = True
		if not item_equip_possess :
			player.item_equip = player.item_possess[0]
			player.change_stat()
		player.pos = (225, 75)
		player.pos_explo = (0,0)
		for coordonnee_marqueur in list_coordonnee.explo_marqueur :
			player.pos_explo = coordonnee_marqueur
			player.pos = list_coordonnee.explo_marqueur[coordonnee_marqueur]
			pygame.key.set_repeat(150, 150)

	while explo :
		element_return = exploration(fenetre, player, list_coordonnee, monstre)
		explo = element_return[1]
		jouer = element_return[0]
		accueil = element_return[2]

	player.pos = (250,250)

	if ville :
		ville_arrivee = True
	while ville :
		element_return = ville_prog(fenetre, player, list_coordonnee, info_item, ville_arrivee)
		ville = element_return[0]
		jouer = element_return[1]
		accueil = element_return[2]
		dungeon = element_return[3]
		explo = element_return[4]
		ville_arrivee = element_return[5]

	if dungeon :
		donjon_arrivee_chargement(list_coordonnee, player)
		pygame.key.set_repeat(30, 30)
		liste_fleche = []
	while dungeon :
		dungeon, jouer, accueil = donjon_prog(fenetre, player, list_coordonnee, boss1, liste_fleche)

	if multi :
		jouer, acceuil = multiplayer(fenetre, player, serveur)


fichier_sauvegarde = open("save_"+str(player.name)+".txt", "w")
fichier_sauvegarde.write(str(player.money)+"\n"+str(player.exp)+"\n"+str(player.lvl)+"\n")
for element in player.item_possess :
	fichier_sauvegarde.write(str(element)+"/")
fichier_sauvegarde.write("\n")
for element in player.item_spe_possess :
	fichier_sauvegarde.write(str(element)+"/")
fichier_sauvegarde.write("\n")
for element in player.item_quantite :
	fichier_sauvegarde.write(str(element)+":"+str(player.item_quantite[str(element)])+"/")
fichier_sauvegarde.write("\n"+str(player.first_time_ville)+"\n")
for element in player.zone_explo_deja_explore :
	fichier_sauvegarde.write(str(element)+"/")

fichier_sauvegarde.close()