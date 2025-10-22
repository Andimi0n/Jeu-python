#! python3.2
import pygame
from pygame.locals import *
import socket
from fonction import *

def multiplayer(fenetre, player, serveur) :
	multi, jouer, acceuil = True, False, False
	hauteur = 1
	while multi :
		fenetre.fill((0,0,0))
		police = pygame.font.Font("Police/SuperMario.ttf", 24)
		police_sword = pygame.font.Font("Police/Fantasy.ttf", 20)
		sword = police_sword.render("H", True, (255,255,255))
		text_creer_partie = police.render("CREER UNE PARTIE", True, (255, 255, 255))
		text_creer_partie_select = police.render("CREER UNE PARTIE", True, (255, 255, 0))
		text_rejoindre_partie = police.render("REJOINDRE UNE PARTIE", True, (255, 255, 255))
		text_rejoindre_partie_select = police.render("REJOINDRE UNE PARTIE", True, (255, 255, 0))
		hote, connexion = False, False

		if hauteur%2 == 1 :
			fenetre.blit(text_creer_partie_select, (100,235))
			fenetre.blit(text_rejoindre_partie, (95, 265))
			fenetre.blit(sword, (10, 235))
			hote = True
		if hauteur%2 == 0 :
			fenetre.blit(text_creer_partie, (100,235))
			fenetre.blit(text_rejoindre_partie_select, (95, 265))
			fenetre.blit(sword, (5, 265))
			connexion = True

		pygame.display.flip()

		for event in pygame.event.get() :
			if event.type == KEYDOWN :
				if event.key == K_UP :
					hauteur += 1
				if event.key == K_DOWN :
					hauteur -= 1
				if event.key == K_ESCAPE :
					multi, jouer, acceuil = False, True, True
				if event.key == 13 :
					if hote :
						cree_partie(player, serveur, fenetre)
						multi, jouer, acceuil = False, True, True
					if connexion :
						connexion_partie(player, serveur, fenetre)
						multi, jouer, acceuil = False, True, True
			if event.type == QUIT :
				multi, jouer, acceuil = False, False, False

	return jouer, acceuil

def cree_partie(player, serveur, fenetre) :
	adresse_select = True
	police=pygame.font.Font(None, 20)
	demande_entree_adresse = police.render("Adresse de votre partie :", True, (255, 255, 255))
	while adresse_select :
		fenetre.fill((0,0,0))
		fenetre.blit(demande_entree_adresse, (60, 240))
		background = pygame.draw.rect(fenetre, (255,255,255), (245, 235, 200, 20))
		for event in pygame.event.get() :
			if event.type == KEYDOWN :
				if event.unicode in "0123456789.azertyuiopqsdfghjklmwxcvbn" :
					adresse+=str(event.unicode)
				if event.key == 8 :
					adresse = adresse[:-1]
				if event.key == K_ESCAPE :
					adresse_select = False
				if event.key == 13 :
					try :
						serveur.connexion.bind(('', serveur.port))
					except :
						chargement_texte(fenetre, "Adresse impossible, veuillez réessayer !")
			if event.type == QUIT :
				adresse_select = False
	chargement_texte(fenetre, "L'adresse de votre partie est : "+ str(serveur.connexion.getsockname())+ 
		". Veuillez attendre que quelqu'un se connecte à votre partie")
	serveur.connexion.listen(5)
	connexion_avec_client, infos_connexion = serveur.connexion.accept()
	fenetre.fill((0,0,0))
	chargement_texte(fenetre, "Connexion réussie !!!")
	connexion_avec_client.close()
	serveur.connecte = True
	serveur.hote = True

def connexion_partie(player, serveur, fenetre) :
	adresse_select = True
	police=pygame.font.Font(None, 20)
	demande_entree_adresse = police.render("Adresse de la partie à rejoindre :", True, (255, 255, 255))
	adresse = ''
	while adresse_select :
		fenetre.fill((0,0,0))
		fenetre.blit(demande_entree_adresse, (20, 240))
		background = pygame.draw.rect(fenetre, (255,255,255), (245, 235, 200, 20))
		for event in pygame.event.get() :
			if event.type == KEYDOWN :
				if event.unicode in "0123456789.azertyuiopqsdfghjklmwxcvbn" :
					adresse+=str(event.unicode)
				if event.key == 8 :
					adresse = adresse[:-1]
				if event.key == K_ESCAPE :
					adresse_select = False
				if event.key == 13 :
					try :
						serveur.connexion.connect((adresse, serveur.port))
						fenetre.fill((0,0,0))
						chargement_texte(fenetre, "Connexion réussie !!!")
						adresse_select = False
					except :
						chargement_texte(fenetre, "Connexion impossible :( Veuillez réessayer")
			if event.type == QUIT :
				adresse_select = False
		text_adresse = police.render(str(adresse), True, (0, 0, 0))
		fenetre.blit(text_adresse, (250, 240))
		pygame.display.flip()