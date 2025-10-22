#! python3.2
import pygame
from pygame.locals import *
from fonction import *

def ville_prog(fenetre, player, list_coordonnee, info_item, ville_arrivee) :
	pygame.key.set_repeat(150, 150)
	fenetre = pygame.display.set_mode((500,500))
	ville, jouer, accueil = True, True, False
	chargement_sol(fenetre, player, list_coordonnee)
	if ville_arrivee and player.first_time_ville==True :
		texte = "Bienvenue à la ville, ici tu peux acheter   de l'équipement et des objets à la boutique, ou bien partir à l'exploration ou   visiter les  dongeons !"
		chargement_texte(fenetre, texte)
		ville_arrivee = False
	player.first_time_ville = False
	element_return = mouvement(fenetre, player, list_coordonnee, info_item)
	quitter = element_return[0]
	go_accueil_jeu = element_return[1]
	dungeon = element_return[2]
	explo = element_return[3]
	if dungeon or explo :
		ville = False
		acuueil = False
	if go_accueil_jeu :
		ville = False
		accueil = True
	if quitter :
		ville = False
		jouer = False
		accueil = False
	element_return = [ville, jouer, accueil, dungeon, explo, ville_arrivee]
	return element_return

def sell(fenetre, player, info_item, list_coordonnee) :
	sell_select = True
	hauteur = int(0)
	background = pygame.image.load("Image/background_shop.png").convert()
	while sell_select :
		chargement_interior(fenetre, player, list_coordonnee)
		quitter = False
		police_titre = pygame.font.Font(None, 20)
		police = pygame.font.Font(None, 15)
		txt_sell = police_titre.render("ITEM TO SELL :", True, (255,255,255))
		fenetre.blit(txt_sell, (265, 115))

		item_select=""
		nombre_element_sell = len(player.item_possess) + len(player.minerai)
		if hauteur >= nombre_element_sell :
			hauteur = int(0)
		elif hauteur < 0 :
			hauteur = nombre_element_sell-1
		item, minerai = False, False
		if hauteur < len(player.item_possess) :
			item_select=player.item_possess[hauteur-1]
			price_item_select = info_item.item_price[str(item_select)]-2
			if price_item_select <= 0:
				price_item_select=1
			item = True
		elif hauteur < nombre_element_sell :
			item_select = player.minerai[hauteur-len(player.item_possess)]
			price_item_select = info_item.minerai_price[str(item_select)]
			minerai = True
		compteur = int(0)
		possibilite_quantite = False
		for item_to_sell in player.item_possess :
			try :
				quantite_item = player.item_quantite[str(item_to_sell)]
				possibilite_quantite = True
			except :
				quantite_item = 1
			if quantite_item>0 :
				if item_to_sell == item_select :
					couleur = (255,255,0)
				else :
					couleur = (255,255,255)
				text_item = police.render(str(item_to_sell)+" x "+str(quantite_item), True, couleur)
				price_item_sell = int(info_item.item_price[str(item_to_sell)]) - 2
				if price_item_sell <= 0 :
					price_item_sell = 1
				text_price_item = police.render(str(price_item_sell)+" $", True, couleur)
				fenetre.blit(text_item, (265, 140+(compteur*15)))
				fenetre.blit(text_price_item, (360, 140+(compteur*15)))
				compteur+=1
		for item_to_sell in player.minerai :
			try :
				quantite_item = player.minerai_quantite[str(item_to_sell)]
				possibilite_quantite = True
			except :
				quantite_item = 1
			if quantite_item>0 :
				if item_to_sell == item_select :
					couleur = (255,255,0)
				else :
					couleur = (255,255,255)
				price_item_sell = info_item.minerai_price[str(item_to_sell)]
				text_item = police.render(str(item_to_sell)+" x "+str(quantite_item), True, couleur)
				text_price_item = police.render(str(price_item_sell)+" $", True, couleur)
				fenetre.blit(text_item, (265, 140+(compteur*15)))
				fenetre.blit(text_price_item, (360, 140+(compteur*15)))
				compteur+=1
		for event in pygame.event.get() :
			if event.type == QUIT :
				sell_select = False
				quitter = True
			if event.type == KEYDOWN :
				if event.key == K_ESCAPE :
					sell_select = False
				if event.key == K_DOWN :
					hauteur+=1
				if event.key == K_UP :
					hauteur-=1
				if event.key == 13 :
					player.money+=price_item_select
					if possibilite_quantite :
						if minerai :
							player.minerai_quantite[str(item_to_sell)]-=1
							if player.minerai_quantite[str(item_to_sell)] <= 0 :
								del player.minerai[hauteur-len(player.item_possess)]
						if item :
							player.item_quantite[str(item_to_sell)]-=1
							if player.item_quantite[str(item_to_sell)] <= 0 :
								del player.item_possess[hauteur-1]
					else :
						if item :
							del player.item_possess[hauteur-1]
						elif minerai :
							del player.minerai[hauteur-len(player.item_possess)]
					
		pygame.display.flip()
	return quitter

def buy(fenetre, player, info_item, list_coordonnee) :
	buy_select = True
	hauteur = int(0)
	quitter = False
	while buy_select :
		chargement_interior(fenetre, player, list_coordonnee)
		police_titre = pygame.font.Font(None, 20)
		police = pygame.font.Font(None, 15)
		txt_buy = police_titre.render("ITEM TO BUY :", True, (255,255,255))
		fenetre.blit(txt_buy, (265, 115))
		compteur = int(0)
		achat = False
		for event in pygame.event.get() :
			if event.type == KEYDOWN :
				if event.key == K_UP :
					hauteur-=1
				if event.key == K_DOWN :
					hauteur+=1
				if event.key == 13 :
					achat = True
				if event.key == K_ESCAPE :
					buy_select = False
			if event.type == QUIT :
				buy_select = False
				quitter = True

		if hauteur < 0 :
			hauteur = len(info_item.item_to_buy)-1
		if hauteur >= len(info_item.item_to_buy) :
			hauteur = int(0)

		compteur = int(0)
		for item_to_buy in info_item.item_to_buy :
			price_item = info_item.item_price[str(item_to_buy)]
			if item_to_buy == info_item.item_to_buy[hauteur] :
				text_item_to_buy = police.render(str(item_to_buy), True, (255,255,0))
				text_price_item = police.render(str(price_item)+" $", True, (255,255,0))
			else :
				text_item_to_buy = police.render(str(item_to_buy), True, (255,255,255))
				text_price_item = police.render(str(price_item)+" $", True, (255,255,255))
			fenetre.blit(text_item_to_buy, (265, 140+(compteur*15)))
			fenetre.blit(text_price_item, (350, 140+(compteur*15)))
			compteur+=1

		item_select = str(info_item.item_to_buy[hauteur])
		price_item_select = info_item.item_price[item_select]
		if achat and player.money >= price_item_select :
			player.money-= price_item_select
			try :
				if player.item_quantite[item_select] <= 0 :
					player.item_possess.append(item_select)
				player.item_quantite[item_select]+=1
			except :
				if item_select in info_item.item_spe :
					player.item_spe_possess.apend(item_select)
				else :
					player.item_quantite[item_select] = 1
					player.item_possess.append(item_select)

		pygame.display.flip()
	return quitter

def chargement_interior(fenetre, player, list_coordonnee) :
	police = pygame.font.Font(None, 20)
	background = pygame.image.load("Image/background_shop.png").convert()
	fenetre.blit(background, (0,0))
	list_coordonnee.chargement_info_perso(fenetre, player)
	background_1 = pygame.draw.rect(fenetre, (0,0,0), (0, 120, 180, 230))
	contour_background_1 = pygame.draw.rect(fenetre, (255,255,255), (0, 120, 180, 230), 2)
	background_2 = pygame.draw.rect(fenetre, (0,0,0), (264, 114, 112, 192))
	background_2_contour = pygame.draw.rect(fenetre, (255,255,255), (260, 110, 120, 200), 5)

	text_item_select = police.render("EQUIP :", True, (255,255,255))
	fenetre.blit(text_item_select, (5, 125))				
	text_item_select = police.render(str(player.item_equip), True, (255,255,255))
	fenetre.blit(text_item_select, (5, 145))
	
	text_item = police.render("IN POSSESSION :", True, (255,255,255))
	fenetre.blit(text_item, (5, 180))
	
	compteur = 0
	for item in player.item_possess :
		if item == player.item_equip :
			continue
		text_item = police.render(str(item), True, (255,255,255))
		fenetre.blit(text_item, (5, 200+(compteur*20)))
		try :
			quantite_item = player.item_quantite[str(item)]
			text_quantite_item = police.render(" x " +str(quantite_item), True, (255,255,255))
			fenetre.blit(text_quantite_item, (115, 200+(compteur*20)))
		except :
			pass
		finally :
			compteur+=1

def chargement_sol(fenetre, player, list_coordonnee) :
	wall = pygame.image.load("Image/wall_ville.jpg").convert()
	sol = pygame.image.load("Image/sol_ville.jpg").convert()
	numero_ligne, numero_colonne = int(0), int(0)
	with open('ville/ville.txt', 'r') as fichier :
		for ligne in fichier :
			for lettre in ligne :
				coordonnee = (numero_colonne*25, numero_ligne*25)
				if lettre == "0" :
					fenetre.blit(sol, coordonnee)
					list_coordonnee.ville_sol.append(coordonnee)
				if lettre == "m" :
					fenetre.blit(wall, coordonnee)
					list_coordonnee.ville_mur.append(coordonnee)
				numero_colonne+=1
			numero_ligne+=1
			numero_colonne=0
	fenetre.blit(player.image_actuel, player.pos)
	shop_exterior = pygame.image.load("Image/shop_exterior.png").convert()
	shop_exterior.set_colorkey((0,255,0))
	fenetre.blit(shop_exterior, (225,50))
	pygame.display.flip()

def mouvement(fenetre, player, list_coordonnee, info_item) :
	quitter = False
	dungeon = False
	explo = False
	go_accueil_jeu = False
	new_abs = player.pos[0]
	new_ord = player.pos[1]
	for event in pygame.event.get() :
		if event.type == KEYDOWN :
			if event.key == K_UP :
				new_ord-=25
				player.image_actuel = player.image_up
			if event.key == K_DOWN :
				new_ord+=25
				player.image_actuel = player.image_down
			if event.key == K_RIGHT :
				new_abs+=25
				player.image_actuel = player.image_right
			if event.key == K_LEFT :
				new_abs-=25
				player.image_actuel = player.image_left
			if event.key == K_ESCAPE :
				go_accueil_jeu = True
		if event.type == QUIT :
			quitter = True
	new_pos = (new_abs, new_ord)
	for coo_mur in list_coordonnee.ville_mur :
		if coo_mur == new_pos :
			new_pos = player.pos
	if player.pos[0] < 0 :
		dungeon = True
	if player.pos[0] > 475 :
		explo = True
	player.pos = new_pos
	if player.pos in ((225,50), (225,75), (250,50), (250,75)) :
		quitter = in_shop(fenetre, player, list_coordonnee, info_item)

	element_return = [quitter, go_accueil_jeu, dungeon, explo]
	return element_return

def in_shop(fenetre, player, list_coordonnee, info_item) :
	in_shop = True
	hauteur = int(1)
	while in_shop :	
		quitter = False
		fenetre = pygame.display.set_mode((700,400))
		background = pygame.image.load("Image/background_shop.png").convert()
		dollar = pygame.image.load("Image/dollar.png").convert()
		dollar.set_colorkey((255,255,255))
		fenetre.blit(background, (0,0))
		quitter = False
		for event in pygame.event.get() :
			if event.type == QUIT :
				quitter, in_shop = True, False
			if event.type == KEYDOWN :
				if event.key == K_UP :
					hauteur += 1
				if event.key == K_DOWN :
					hauteur -= 1
				if event.key == 13 :
					if hauteur%2 == 1:
						quitter = sell(fenetre, player, info_item, list_coordonnee)
					if hauteur%2 == 0:
						quitter = buy(fenetre, player, info_item, list_coordonnee)
				if event.key == K_ESCAPE :
					in_shop = False
					player.pos = (225,100)
		fenetre.blit(background, (0,0))
		list_coordonnee.chargement_info_perso(fenetre, player)
		background_1 = pygame.draw.rect(fenetre, (0,0,0), (264, 114, 112, 192))
		background_1_contour = pygame.draw.rect(fenetre, (255,255,255), (260, 110, 120, 200), 5)
		police = pygame.font.Font("Police/SuperMario.ttf", 20)
		text_sell = police.render("$ SELL $", True, (255,255,255))
		text_buy = police.render("$ BUY $", True, (255,255,255))
		if hauteur%2 == 1 :
			text_sell = police.render("$ SELL $", True, (0,255,0))
		if hauteur%2 == 0 :
			text_buy = police.render("$ BUY $", True, (0,255,0))
		fenetre.blit(text_sell, (270, 180))
		fenetre.blit(text_buy, (275, 240))
		pygame.display.flip()
		if quitter :
			quitter = True
			in_shop = False
	return quitter
