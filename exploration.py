#! python3.2
import pygame
from pygame.locals import *
from fonction import *
from random import randrange
from classes import *

def exploration(fenetre, player, list_coordonnee, monstre) :
	pygame.key.set_repeat(150, 150)
	accueil = False
	list_coordonnee.chargement(fenetre, player, monstre)
	list_coordonnee.chargement_fleche(fenetre, player, monstre)
	pygame.display.flip()
	if player.invincible == 0 :
		player.toucher(fenetre, list_coordonnee, monstre)
	element_return = mouvement(fenetre, player, list_coordonnee, monstre)
	quitter = element_return[0]
	back_to_accueil = element_return[1]
	if player.exp >= player.exp_require_lvl_up :
		player.lvl_up(fenetre, list_coordonnee, monstre)
		player.exp_require_lvl_up*=2
	verif_change_zone(player, fenetre, list_coordonnee, monstre)
	jouer = True
	exploration = True
	if back_to_accueil :
		exploration = False
		accueil = True
	if quitter :
		exploration = False
		jouer = False
	event_return = [jouer, exploration, accueil]
	return event_return


def chargement_explo (fenetre, player, list_coordonnee, monstre) :
	list_coordonnee.explo_monstre = []
	monstre.nombre = 0
	position = str(player.pos_explo)
	monstre1_apparition = randrange(4)
	monstre2_apparition = randrange(4)
	monstre3_apparition = randrange(4)
	monstre4_apparition = randrange(4)
	if monstre1_apparition == 0 :
		monstre.nombre+=1
		monstre.vie.append(5)
	if monstre2_apparition == 0 :
		monstre.nombre+=1
		monstre.vie.append(5)
	if monstre3_apparition == 0 :
		monstre.nombre+=1
		monstre.vie.append(5)
	if monstre4_apparition == 0 :
		monstre.nombre+=1
		monstre.vie.append(5)

	zone_deja_explore = False
	if player.pos_explo in player.zone_explo_deja_explore :
		zone_deja_explore = True
		list_coordonnee.explo_mur = list_coordonnee.explo_mur_zone_deja_explore[player.pos_explo]
		list_coordonnee.explo_sol = list_coordonnee.explo_sol_zone_deja_explore[player.pos_explo]
		list_coordonnee.explo_coal = list_coordonnee.explo_coal_zone_deja_explore[player.pos_explo]
		list_coordonnee.explo_lantern = list_coordonnee.explo_lantern_zone_deja_explore[player.pos_explo]
		list_coordonnee.explo_case_eviter_monstre = list_coordonnee.explo_mur_zone_deja_explore[player.pos_explo]
		for coordonnee in list_coordonnee.explo_sol :
			list_coordonnee.explo_general_sol.append(coordonnee)
		for coordonnee in list_coordonnee.explo_coal :
			list_coordonnee.explo_general_sol.append(coordonnee)
		try :
			coordonnee_marqueur = list_coordonnee.explo_marqueur[player.pos_explo]
			image_marqueur = pygame.image.load("Image/balise.jpg").convert()
			image_marqueur.set_colorkey((0,255,0))
			fenetre.blit(image_marqueur, coordonnee_marqueur)
		except :
			pass


	if zone_deja_explore == False :
		with open("exploration/" + position + ".txt", 'r') as fichier :
			numero_colonne = 0
			numero_ligne = 0
			for ligne in fichier :
				for caractere in ligne :
					coordonne_x = int(numero_colonne*25)
					coordonne_y = int(numero_ligne*25)
					if caractere == "0" :
						charbon = randrange(10)
						if charbon == 0 :
							list_coordonnee.explo_coal.append((coordonne_x, coordonne_y))
							list_coordonnee.explo_general_sol.append((coordonne_x, coordonne_y))
						else :
							list_coordonnee.explo_sol.append((coordonne_x, coordonne_y))
							list_coordonnee.explo_general_sol.append((coordonne_x, coordonne_y))
					if caractere == "m" :
						list_coordonnee.explo_case_eviter_monstre.append((coordonne_x, coordonne_y))
						list_coordonnee.explo_mur.append((coordonne_x, coordonne_y))
					numero_colonne += 1
				numero_ligne+=1
				numero_colonne = 0
		list_coordonnee.explo_mur_zone_deja_explore[player.pos_explo] = list_coordonnee.explo_mur
		list_coordonnee.explo_sol_zone_deja_explore[player.pos_explo] = list_coordonnee.explo_sol
		list_coordonnee.explo_coal_zone_deja_explore[player.pos_explo] = list_coordonnee.explo_coal
		list_coordonnee.explo_lantern_zone_deja_explore[player.pos_explo] = list_coordonnee.explo_lantern
		player.zone_explo_deja_explore.append(player.pos_explo)

	for numero_monstre in range(monstre.nombre) :
		coordonnee_monstre = list_coordonnee.explo_general_sol[randrange(len(list_coordonnee.explo_general_sol))]
		list_coordonnee.explo_monstre.append(coordonnee_monstre)

def mouvement (fenetre, player, list_coordonnee, monstre) :
	back_to_accueil = False
	direction_initial = player.direction_explo
	quitter = False
	pos_initiale = player.pos
	pos_x = player.pos[0]
	pos_y = player.pos[1]
	for event in pygame.event.get() :
		if event.type == KEYDOWN and player.in_boucle == False :
			if event.key == K_UP :
				pos_y -= 25
				player.direction_explo = "UP"
				player.image_actuel = player.image_up
				if player.invincible == 0 :
					monstre.mouvement(fenetre, player, list_coordonnee)
				else :
					player.invincible -= 1
				
			if event.key == K_DOWN :
				pos_y += 25
				player.direction_explo = "DOWN"
				player.image_actuel = player.image_down
				if player.invincible == 0 :
					monstre.mouvement(fenetre, player, list_coordonnee)
				else :
					player.invincible -= 1
				
			if event.key == K_LEFT :
				pos_x -= 25
				player.direction_explo = "LEFT"
				player.image_actuel = player.image_left
				if player.invincible == 0 :
					monstre.mouvement(fenetre, player, list_coordonnee)
				else :
					player.invincible -= 1
				
			if event.key == K_RIGHT :
				pos_x += 25
				player.direction_explo = "RIGHT"
				player.image_actuel = player.image_right
				if player.invincible == 0 :
					monstre.mouvement(fenetre, player, list_coordonnee)
				else :
					player.invincible -= 1

			if event.key == K_SPACE and player.item_equip == "Arc" :
				player.tirer(fenetre, list_coordonnee, monstre)
				#######################################
				#####Double mouvement des monstres#####
				#######################################
				if monstre.nombre > 0 :
					if player.invincible == 0 :
						monstre.mouvement(fenetre, player, list_coordonnee)
					else :
						player.invincible -= 1
					list_coordonnee.chargement(fenetre, player, monstre)
					pygame.time.wait(100)
					if player.invincible == 0 :
						monstre.mouvement(fenetre, player, list_coordonnee)
					else :
						player.invincible -= 1
				
			if event.key == K_ESCAPE :
				back_to_accueil = True

			if event.key == 13 :
				minage(fenetre, player, list_coordonnee)
				if player.invincible == 0 :
					monstre.mouvement(fenetre, player, list_coordonnee)
				else :
					player.invincible -= 1
			if event.unicode == "e" :
				open_inventory(fenetre, player, list_coordonnee, monstre)
			if event.unicode == "t" and player.item_quantite["Torche"] > 0:
				player.item_quantite["Torche"]-=1
				list_coordonnee.explo_lantern.append(player.pos)
				if player.item_quantite["Torche"] <= 0 :
					if player.item_equip == "Torche" :
						player.item_equip = player.item_possess[0]
					compteur = 0
					for item in player.item_possess :
						if item == "Torche" :
							del player.item_possess[compteur]
						compteur+=1

			#######################
			########Débugage#######
			#######################
			if event.unicode == "u" :
				print(monstre.nombre, monstre.vie, list_coordonnee.explo_monstre, player.pos)

			if event.unicode == "p" and "Marqueur" in player.item_spe_possess :
				list_coordonnee.explo_marqueur = {}
				list_coordonnee.explo_marqueur[player.pos_explo] = player.pos
				player.item_quantite["Marqueur"]-=1
				if player.item_quantite["Marqueur"]<=0 :
					compteur=int(0)
					for item in player.item_spe_possess :
						if item == "Marqueur" :
							del player.item_spe_possess[compteur]
						compteur+=1
						del player.item_quantite["Marqueur"]

			if event.unicode == "m" and "Carte" in player.item_spe_possess :
				map_open = True
				time_now = pygame.time.get_ticks()
				time_afficher = pygame.time.get_ticks()+100
				while map_open :
					ligne = int(0)
					colonne = int(0)
					fenetre.fill((0,0,0))
					for zone_deja_explore in player.zone_explo_deja_explore :
						for coordonnee_sol in list_coordonnee.explo_sol_zone_deja_explore[zone_deja_explore] :
							coordonnee_sol_affichage_x = ((coordonnee_sol[0]/25)*2)+(zone_deja_explore[0]*40)+130
							coordonnee_sol_affichage_y = ((coordonnee_sol[1]/25)*2)+(zone_deja_explore[1]*40)+50
							sol_affichage=pygame.draw.rect(fenetre, (74,74,74), (coordonnee_sol_affichage_x, coordonnee_sol_affichage_y, 2, 2))
						for coordonnee_coal in list_coordonnee.explo_coal_zone_deja_explore[zone_deja_explore] :
							coordonnee_coal_affichage_x = ((coordonnee_coal[0]/25)*2)+(zone_deja_explore[0]*40)+130
							coordonnee_coal_affichage_y = ((coordonnee_coal[1]/25)*2)+(zone_deja_explore[1]*40)+50
							coal_affichage=pygame.draw.rect(fenetre, (74,74,74), (coordonnee_coal_affichage_x, coordonnee_coal_affichage_y, 2, 2))

					if time_now > time_afficher :
						coordonnee_perso_x = ((player.pos[0]/25)*2)+(player.pos_explo[0]*40)+130
						coordonnee_perso_y = ((player.pos[1]/25)*2)+(player.pos_explo[1]*40)+50
						perso = pygame.draw.rect(fenetre, (0,255,0), (coordonnee_perso_x, coordonnee_perso_y, 2, 2))
					if time_now > time_afficher+100 :
						time_afficher = pygame.time.get_ticks()+100

					pygame.display.flip()
					for event in pygame.event.get() :
						if event.type == KEYDOWN :
							if event.key == K_ESCAPE :
								map_open = False
						if event.type == QUIT :
							map_open = False
							quitter = True
					time_now = pygame.time.get_ticks()

		if event.type == QUIT :
			quitter = True
	player.pos = (pos_x, pos_y)
	for coordonnee_mur in list_coordonnee.explo_mur :
		if player.pos == coordonnee_mur :
			player.pos = pos_initiale
			player.direction_explo = direction_initial
	pygame.display.flip()
	element_return = [quitter, back_to_accueil]
	return element_return

def verif_change_zone(player, fenetre, list_coordonnee, monstre) :
	pos_zone_x = player.pos_explo[0]
	pos_zone_y = player.pos_explo[1]
	change_zone = False
	if player.pos[0] <= 0 and player.direction_explo == "LEFT" :
		pos_zone_x-=1
		player.pos = (475 ,player.pos[1])
		change_zone = True
	if player.pos[0] >= 475 and player.direction_explo == "RIGHT" :
		pos_zone_x+=1
		player.pos = (0, player.pos[1])
		change_zone = True
	if player.pos[1] <= 0 and player.direction_explo == "UP" :
		pos_zone_y-=1
		player.pos = (player.pos[0], 475)
		change_zone = True
	if player.pos[1] >= 475 and player.direction_explo == "DOWN" :
		pos_zone_y+=1
		player.pos = (player.pos[0], 0)
		change_zone = True

	player.pos_explo = (pos_zone_x, pos_zone_y)

	if change_zone :
		list_coordonnee.explo_mur = []
		list_coordonnee.explo_sol = []
		list_coordonnee.explo_coal = []
		list_coordonnee.explo_general_sol = []
		list_coordonnee.explo_case_eviter_monstre = []
		list_coordonnee.explo_lantern = []
		monstre.vie = []
		chargement_explo (fenetre, player, list_coordonnee, monstre)

def minage (fenetre, player, list_coordonnee) :
	if player.item_equip == "Pioche Pierre" :
		
		compteur = int(0)
		for coordonnee_coal in list_coordonnee.explo_coal :
			if player.pos == coordonnee_coal :
				if player.minerai_quantite["Charbon"] <= 0 :
					player.minerai.append("Charbon")
				player.minerai_quantite["Charbon"]+=1
				del list_coordonnee.explo_coal[compteur]
				list_coordonnee.explo_sol.append(coordonnee_coal)
			compteur += 1