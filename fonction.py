#! python3.2
import pygame
from pygame.locals import *
from exploration import *
from classes import *
from random import randrange

def open_inventory (fenetre, player, list_coordonnee, monstre) :
	player_item_non_equip = []
	for item in player.item_possess :
		if item!=player.item_equip :
			player_item_non_equip.append(item)
	inventory_open = True
	hauteur = 1
	while inventory_open :
		list_coordonnee.chargement (fenetre, player, monstre)
		police = pygame.font.Font(None, 20)
		enter_press = False
		background_2 = pygame.draw.rect(fenetre, (0,0,0), (0, 120, 130, 100))
		contour_background_2 = pygame.draw.rect(fenetre, (255,255,255), (0, 120, 130, 100), 2)

		for event in pygame.event.get() :
			if (event.type == KEYDOWN and (event.unicode == "e"or event.key == K_ESCAPE)) or event.type == QUIT:
				inventory_open = False
			if event.type == KEYDOWN :
				if event.key == K_DOWN :
					hauteur += 1
				if event.key == K_UP :
					hauteur -= 1
				if event.key == 13 :
					enter_press = True

		police_select = pygame.font.Font("Police/SuperMario.ttf", 20)
		text_item = police_select.render("ITEM", True, (255,255,255))
		text_minerai = police_select.render("MINERAI", True, (255,255,255))
		text_stat = police_select.render("STAT", True, (255,255,255))
		text_item_spe = police_select.render("ITEM SPE", True, (255,255,255))
		item_select = False
		minerai_select = False
		stat_select = False
		item_spe_select = False
		if hauteur % 4 == 1 :
			text_item = police_select.render("ITEM", True, (255,255,0))
			item_select = True
		if hauteur % 4 == 2 :
			text_item_spe = police_select.render("ITEM SPE", True, (255,255,0))
			item_spe_select = True
		if hauteur % 4 == 3 :
			text_minerai = police_select.render("MINERAI", True, (255,255,0))
			minerai_select = True
		if hauteur % 4 == 0 :
			text_stat = police_select.render("STAT", True, (255,255,0))
			stat_select = True
		fenetre.blit(text_item, (5, 125))
		fenetre.blit(text_item_spe, (5, 150))
		fenetre.blit(text_minerai, (5, 175))
		fenetre.blit(text_stat, (5, 200))
		pygame.display.flip()

		if enter_press :
			quit = False
			hauteur = int(0)
			while quit == False :
				list_coordonnee.chargement(fenetre, player, monstre)
				background_3 = pygame.draw.rect(fenetre, (0,0,0), (135, 120, 180, 230))
				contour_background_3 = pygame.draw.rect(fenetre, (255,255,255), (135, 120, 180, 230), 2)
				if minerai_select :
					text_charbon = police.render("CHARBON : " + str(player.minerai_quantite["Charbon"]), True, (255,255,255))
					fenetre.blit(text_charbon, (140, 125))
				if item_select :

					text_item_select = police.render("EQUIP :", True, (255,255,255))
					fenetre.blit(text_item_select, (140, 125))
					
					text_item_select = police.render(str(player.item_equip), True, (255,255,255))
					fenetre.blit(text_item_select, (140, 145))
					
					text_item = police.render("IN POSSESSION :", True, (255,255,255))
					fenetre.blit(text_item, (140, 180))
					
					compteur = 0
					for item in player_item_non_equip :
						text_item = police.render(str(item), True, (255,255,255))
						fenetre.blit(text_item, (140, 200+(compteur*20)))
						try :
							quantite_item = player.item_quantite[str(item)]
							text_quantite_item = police.render(" x " +str(quantite_item), True, (255,255,255))
							fenetre.blit(text_quantite_item, (250, 200+(compteur*20)))
						except :
							pass
						finally :
							compteur+=1
					if len(player_item_non_equip) > 0 :
						select_item = pygame.draw.rect(fenetre, (255, 255, 0), (137, ((hauteur%len(player_item_non_equip))*20) + 199, 150, 20), 2)

					for event in pygame.event.get() :
						if event.type == KEYDOWN :
							if event.key == K_UP :
								hauteur -= 1
							if event.key == K_DOWN :
								hauteur += 1
							if event.key == 13 and item_select:
								item_select = True
								item_equip = player_item_non_equip[hauteur%len(player_item_non_equip)]
								player_item_non_equip.append(player.item_equip)
								player.item_equip = item_equip
								del player_item_non_equip[hauteur%len(player_item_non_equip)]
								player.change_stat()
						if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
							quit = True

				if stat_select :
					text_defense = police.render("DEFENSE :" + str(player.defense), True, (255,255,255))
					text_force = police.render("DEGAT :" + str(player.degat), True, (255,255,255))
					text_portee = police.render("PORTEE : " + str(player.portee), True, (255, 255, 255))
					fenetre.blit(text_defense, (140, 125))
					fenetre.blit(text_force, (140, 145))
					fenetre.blit(text_portee, (140, 165))

				if item_spe_select :
					text_in_possession = police.render("IN POSSESSION :", True, (255,255,255))
					fenetre.blit(text_in_possession, (140, 125))
					compteur = int(0)
					for item in player.item_spe_possess :
						text_item_possess = police.render(str(item), True, (255,255,255))
						fenetre.blit(text_item_possess, (140, 145+compteur*20))
						try :
							quantite_item = player.item_quantite[item]
						except :
							quantite_item = 1
						text_quantite_item = police.render("x"+str(quantite_item), True, (255,255,255))
						fenetre.blit(text_quantite_item, (250, 145+compteur*20))
						compteur+=1
						pygame.display.flip()
				for event in pygame.event.get() :
					if (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT :
						quit = True

				pygame.display.flip()



def chargement_texte(fenetre, texte) :
	background_1 = pygame.draw.rect(fenetre, (0,0,0), (50, 390, 440, 70))
	contour_background_1 = pygame.draw.rect(fenetre, (255,255,255), (45, 385, 450, 80), 5)
	police = pygame.font.Font(None, 20)
	compteur = int(0)
	ligne = int(0)
	ordonnee = 395
	pygame.key.set_repeat(10,10)
	texte_afficher = True
	time = pygame.time.get_ticks()
	time_when_print = pygame.time.get_ticks()
	while texte_afficher :
		attente = 30
		for event in pygame.event.get() :
			if event.type == KEYDOWN :
				if event.key == 13 :
					attente = 10
		if time > time_when_print+attente :
			time_when_print = pygame.time.get_ticks()
			lettre = texte[compteur]
			abscisse = 55+ligne*10
			if abscisse > 485 :
				ligne = 0
				abscisse = 55
				ordonnee += 15
			if ordonnee > 415 and abscisse > 420 :
				ligne = 0
				abscisse = 55
				ordonnee = 395
				waiting_enter_press(fenetre)
				background_1 = pygame.draw.rect(fenetre, (0,0,0), (50, 390, 440, 70))
				contour_background_1 = pygame.draw.rect(fenetre, (255,255,255), (45, 385, 450, 80), 5)
				attente+=20
			compteur+=1
			ligne+=1
			pos = (abscisse, ordonnee)
			afficher = police.render(str(lettre), True, (255,255,255))
			fenetre.blit(afficher, pos)
		pygame.display.flip()
		time = pygame.time.get_ticks()
		if compteur >= len(texte) :
			texte_afficher = False
	waiting_enter_press(fenetre)

def waiting_enter_press(fenetre) :
	police_enter = pygame.font.Font(None, 15)
	time_init = pygame.time.get_ticks()
	time = pygame.time.get_ticks()
	r=255
	b=255
	g=255
	chargement_texte = True
	while chargement_texte :
		background_2 = pygame.draw.rect(fenetre, (0,0,0), (430,435, 60, 25))
		texte_enter = police_enter.render("Press Enter", True, (r,g,b))
		for event in pygame.event.get() :
			if event.type == KEYDOWN :
				if event.key == 13 :
					chargement_texte = False
		if time > time_init :
			fenetre.blit(texte_enter, (430, 435))
		if time > time_init+200 :
			r-=1
			b-=1
			g-=1
			pygame.time.wait(2)
		if r < 125 :
			time_init+=600
			r=255
			b=255
			g=255
		pygame.display.flip()
		time = pygame.time.get_ticks()
	pygame.key.set_repeat(150, 150)