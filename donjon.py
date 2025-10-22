#! python3.2
import pygame
from pygame.locals import *
import classes
from math import *

def donjon_prog(fenetre, player, list_coordonnee, boss1, liste_fleche) :
	jouer, accueil, dungeon = True, False, True
	chargement_donjon(fenetre, player, list_coordonnee, boss1, liste_fleche)
	jouer, acceuil, dungeon, liste_fleche = mouvement(fenetre, player, list_coordonnee, liste_fleche, boss1)
	if not player.invincible_dungeon[0] or pygame.time.get_ticks() > player.invincible_dungeon[1]+player.invincible_dungeon[2] :
		boss1.attaque_corps_a_corps(player, fenetre, list_coordonnee)
	time_now = pygame.time.get_ticks()
	if time_now >= boss1.last_time_movement+boss1.vitesse[1] : #Le boss bouge toutes les x millisecondes, x étant le deuxième élément du tuple self.vitesse
		boss1.mouvement(fenetre, player, list_coordonnee)
	pygame.display.flip()
	return jouer, accueil, dungeon


def donjon_arrivee_chargement(list_coordonnee, player) :
	colonne = int(0)
	numero_ligne = int(0)
	with open ("donjon/map_1.txt", "r") as fichier :
		for ligne in fichier :
			for lettre in ligne :
				if lettre == "0" :
					list_coordonnee.donjon_sol.append((colonne*25, numero_ligne*25))
				colonne+=1
			numero_ligne+=1
			colonne = 0
	player.pos = (250, 250)

def chargement_donjon(fenetre, player, list_coordonnee, boss1, liste_fleche) :
	fenetre.fill((0,0,0))
	sol_image = pygame.image.load("Image/sol_explo.jpg")
	for coordonnee_sol in list_coordonnee.donjon_sol :
		fenetre.blit(sol_image, coordonnee_sol)
	boss1.affichage(fenetre)
	fenetre.blit(player.image_actuel, player.pos)

def mouvement(fenetre, player, list_coordonnee, liste_fleche, boss) :
	jouer, acceuil, dungeon = True, False, True
	bouger = False
	pos_initial = player.pos
	for event in pygame.event.get() :
		if event.type == KEYDOWN :
			keys = pygame.key.get_pressed()
			if keys[pygame.K_w] :
				player.image_actuel = player.image_up
				player.pos = (player.pos[0], player.pos[1]-player.vitesse)
				player_direction = "UP"
				bouger = True
			if keys[pygame.K_s] :
				player.image_actuel = player.image_down
				player.pos = (player.pos[0], player.pos[1]+player.vitesse)
				player_direction = "DOWN"
				bouger = True
			if keys[pygame.K_d] :
				player.image_actuel = player.image_right
				player.pos = (player.pos[0]+player.vitesse, player.pos[1])
				player_direction = "RIGHT"
				bouger = True
			if keys[pygame.K_a] :
				player.image_actuel = player.image_left
				player.pos = (player.pos[0]-player.vitesse, player.pos[1])
				player_direction = "LEFT"
				bouger = True
			if keys[pygame.K_SPACE] :
				player_attaque(player, fenetre, boss, liste_fleche, list_coordonnee)
			if event.key == K_ESCAPE :
				jouer, acceuil, dungeon = True, True, False
		if event.type == QUIT :
			jouer, acceuil, dungeon = False, False, False

	if bouger :
		player_sur_sol = False
		pos_player_test_collision_x = player.pos[0]+6
		pos_player_test_collision_y = player.pos[1]+6
		if player.pos[0] > int(pygame.display.get_surface().get_size()[0]/2) :
			pos_player_test_collision_x += 13
		if player.pos[1] > int(pygame.display.get_surface().get_size()[1]/2) :
			pos_player_test_collision_y += 13
		if not (int((pos_player_test_collision_x)/25)*25, int((pos_player_test_collision_y)/25)*25) in list_coordonnee.donjon_sol :
			player.pos = pos_initial
		else :
			player.direction_explo = player_direction

	if pygame.mouse.get_pressed()[2] :
		tir_a_larc(player, fenetre, liste_fleche)
	if pygame.mouse.get_pressed()[0] :
		liste_fleche.append(classes.Fleche((player.pos[0]+player.largeur/2, player.pos[1]+player.longueur/2), pygame.mouse.get_pos()))

	return jouer, acceuil, dungeon, liste_fleche

def tir_a_larc (player, fenetre, liste_fleche) :
	mouse_pos = pygame.mouse.get_pos()
	player_pos = (player.pos[0]+player.largeur/2, player.pos[1]+player.longueur/2)
	hypothenuse = sqrt(((mouse_pos[0]-player_pos[0])**2) + ((mouse_pos[1]-player_pos[1])**2))
	dist_fleche_player_x = 20*abs(mouse_pos[0]-player_pos[0])/hypothenuse
	dist_fleche_player_y = 20*abs(mouse_pos[1]-player_pos[1])/hypothenuse
	if mouse_pos[1]<player_pos[1] :
		ordonee_bout_fleche = player_pos[1]-dist_fleche_player_y
	else :
		ordonee_bout_fleche = dist_fleche_player_y+player_pos[1]
	if mouse_pos[0]<player_pos[0] :
		abscisse_bout_fleche = player_pos[0]-dist_fleche_player_x
	else :
		abscisse_bout_fleche = dist_fleche_player_x+player_pos[0]
	pygame.draw.line(fenetre, (255,255,255), player_pos, (abscisse_bout_fleche, ordonee_bout_fleche))
	pygame.display.flip()

def player_attaque (player, fenetre, boss, liste_fleche, list_coordonnee) :
	player_pos = (player.pos[0]+player.largeur/2, player.pos[1]+player.longueur/2)
	boss_pos = (boss.pos[0]+boss.longeur_largeur[(boss.direction, boss.last_numero_image)][0]/2, boss.pos[1]+boss.longeur_largeur[(boss.direction, boss.last_numero_image)][1]/2)
	if (boss_pos[0] < player_pos[0]+player.portee and boss_pos[0] > player_pos[0]-player.portee) and (boss_pos[1]<player_pos[1]+player.portee and boss_pos[1]>player_pos[1]-player.portee) :
		boss.vie-=player.degat
		fin_animation = pygame.time.get_ticks()+1000
		player_image_initiale = player.image_actuel
		direction_player = player.direction_explo.lower()
		numero_animation = 0
		while 1 :
			try :
				numero_animation+=1
				image = pygame.image.load("Image/hero_attack_{}_{}.png".format(direction_player, str(numero_animation)))
			except :
				break
		time_entre_animation = (1000/(numero_animation-1))#Le -10 représente le temps mis par pygame pour charger les images, ... Permet de s'assurer que toutes les images seront chargés
		#Quitte à ce que la dernière image reste affichée plus longtemps et le -1 à cause de la première image qui est affichée immédiatement
		time_entre_recul = (1000/(player.recul-1))#Ici seulement -3 car le recul tourne aux alentours de 10-20 pixels, soit 3-4 fois plus que numero_animation environ
		numero_animation = 1
		time_next_animation = pygame.time.get_ticks()
		time_next_recul = pygame.time.get_ticks()
		while pygame.time.get_ticks() < fin_animation :
			chargement_donjon(fenetre, player, list_coordonnee, boss, liste_fleche)
			if pygame.time.get_ticks() >= time_next_animation :
				player.image_actuel = pygame.image.load("Image/hero_attack_{}_{}.png".format(direction_player, str(numero_animation))).convert()
				player.image_actuel.set_colorkey((0,255,0))
				numero_animation+=1
				time_next_animation = pygame.time.get_ticks()+time_entre_animation
			if pygame.time.get_ticks() >= time_next_recul :
				if player.direction_explo == "RIGHT" :
					boss.pos = (boss.pos[0]+1, boss.pos[1])
				if player.direction_explo == "LEFT" :
					boss.pos = (boss.pos[0]-1, boss.pos[1])
				if player.direction_explo == "UP" :
					boss.pos = (boss.pos[0], boss.pos[1]-1)
				if player.direction_explo == "DOWN" :
					boss.pos = (boss.pos[0], boss.pos[1]+1)
				time_next_recul = pygame.time.get_ticks()+time_next_recul
			pygame.display.flip()
		player.image_actuel = player_image_initiale