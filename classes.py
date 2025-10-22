#! python3.2
import pygame
from pygame.locals import *
from random import randrange
from fonction import *
from donjon import *
import socket
from random import randrange
from math import *

class Player :
	def __init__(self) :
		self.name = "Flowey"
		self.money = int(1000)
		self.vie = int(9)
		self.exp = int(0)
		self.exp_require_lvl_up = int(100)
		self.lvl = int(0)
		self.fleche_tirer = int(0)
		self.first_time_ville = True

		################
		#####Images#####
		################
		self.image_actuel = pygame.image.load("Image/hero_down.png").convert()
		self.image_actuel.set_colorkey((0,0,0))
		self.image_down = pygame.image.load("Image/hero_down.png").convert()
		self.image_down.set_colorkey((0,0,0))
		self.image_up = pygame.image.load("Image/hero_up.png").convert()
		self.image_up.set_colorkey((0,0,0))
		self.image_left = pygame.image.load("Image/hero_left.png").convert()
		self.image_left.set_colorkey((0,0,0))
		self.image_right = pygame.image.load("Image/hero_right.png").convert()
		self.image_right.set_colorkey((0,0,0))
		self.image_punch_epee = pygame.image.load("Image/hero_attack_down_1.png").convert()
		self.image_punch_epee.set_colorkey((0,0,0))

		##################
		####Coordonnee####
		##################
		self.pos_explo = (0,0)
		self.pos = (225, 75)
		self.go_explo = False
		self.direction_explo = "DOWN"
		self.zone_explo_deja_explore = []
		self.zone_explo_carte = []
		self.largeur = self.image_actuel.get_rect()[2]
		self.longueur = self.image_actuel.get_rect()[2]

		############
		####Item####
		############
		self.item_equip = "Pioche Pierre"
		self.item_possess = ["Torche", "Pioche Pierre"]
		self.item_spe_possess = []
		self.item_quantite={}
		self.item_quantite["Torche"] = 10
		self.item_quantite["Pioche Pierre"] = 1
		self.minerai = []
		self.minerai_quantite = {}
		self.minerai_quantite["Charbon"] = 0
		self.item_durabilite = {}

		#############
		####Stats####
		#############
		self.degat = int(1)
		self.defense = int(10)
		self.portee = int(20)
		self.invincible = int(0)

		####################
		####Info Dongeon####
		####################
		self.vitesse = int(6)
		self.recul = 20
		self.invincible_dungeon = (False, 0, 0) #True ou False puis nombre de milliseconde que dure l'invincibilité et enfin le moment où elle a commencé

		self.in_boucle = False #Pas lié au personnage juste plus pratique à manipuler entre les fichiers / Role : éviter que pdt une boucle
#les évenements ne continuent à être détécté par pygame. Ex : éviter que lorsque le perso se fasse touche, pdt que l'image du perso clignote et recule,
#le joueur puisse marteler la touche bas et que suite à l'animation le perso se téléporte comme s'il avait été déplacé du nombre de fois que la touche a été tapé
	
	def lvl_up(self, fenetre, list_coordonnee, monstre) :
		self.lvl+=1
		time_now = pygame.time.get_ticks()
		time_afficher = pygame.time.get_ticks()+200
		time_end = pygame.time.get_ticks()+1000
		police =  pygame.font.Font("Police/pixel.ttf", 24)
		txt_lvl_up = police.render("LEVEL UP !!", True, (255,255,255))
		while time_now<time_end :
			list_coordonnee.chargement(fenetre, self, monstre)
			if time_now > time_afficher :
				fenetre.blit(txt_lvl_up, (100, 230))
			if time_now > time_afficher+200 :
				time_afficher = pygame.time.get_ticks()+200
			time_now = pygame.time.get_ticks()
			pygame.display.flip()
		pygame.display.flip()

	def change_stat(self) :
		if self.item_equip == "Pioche Pierre" :
			self.degat = int(1)
			self.defense = int(10)
			self.portee = int(1)
		if self.item_equip == "Epée" :
			self.degat = int(2)
			self.defense = int(10)
			self.portee = int(1)
		if self.item_equip == "Arc" :
			self.degat = int(1)
			self.defense = int(10)
			self.portee = int(20)
	def tirer (self, fenetre, list_coordonnee, monstre) :
		try :
			munition = self.item_quantite["Fleches"]
			if self.item_equip == "Arc" and munition > 0 :
				if self.direction_explo == "RIGHT" or self.direction_explo == "LEFT" :
					list_coordonnee.explo_fleche.append((self.pos[0], self.pos[1]+12))
				if self.direction_explo == "UP" or self.direction_explo == "DOWN" :
					list_coordonnee.explo_fleche.append((self.pos[0]+12, self.pos[1]))
				list_coordonnee.explo_time_fleche_tirer.append(pygame.time.get_ticks())
				list_coordonnee.explo_direction_fleche_tirer.append(self.direction_explo)
				self.item_quantite["Fleches"]-=1
				self.fleche_tirer+=1
		except :
			pass

	def toucher (self, fenetre, list_coordonnee, monstre) :
		toucher = False
		haut = False
		bas = False
		gauche = False
		droite = False
		direction = int(4)
		numero_monstre = int(0)
		for coordonnee_monstre in list_coordonnee.explo_monstre :
			if toucher == False :
				if coordonnee_monstre[0]-25 == self.pos[0] and coordonnee_monstre[1] == self.pos[1] :
					toucher = True
					gauche = True
					numero_monstre_toucher = numero_monstre
				if coordonnee_monstre[0]+25 == self.pos[0] and coordonnee_monstre[1] == self.pos[1] :
					toucher = True
					droite = True
					numero_monstre_toucher = numero_monstre
				if coordonnee_monstre[1]-25 == self.pos[1] and coordonnee_monstre[0] == self.pos[0] :
					toucher = True
					haut = True
					numero_monstre_toucher = numero_monstre
				if coordonnee_monstre[1]+25 == self.pos[1] and coordonnee_monstre[0] == self.pos[0] :
					toucher = True
					bas = True
					numero_monstre_toucher = numero_monstre
				if coordonnee_monstre == self.pos :
					toucher = True
					direction = randrange(4) #0, 1, 2 ou 3
					numero_monstre_toucher = numero_monstre
			numero_monstre+=1
		player_frappe = False
		if toucher :
			player_frappe = self.time_to_punch(fenetre, list_coordonnee, numero_monstre_toucher, monstre)
		if player_frappe :
			self.invincible +=1
			if direction != 4 :
				self.invincible+=1
			self.vie-=1
			time_end = pygame.time.get_ticks()
			time_end+=1000
			time = pygame.time.get_ticks()
			recul = True

			for coordonnee_mur in list_coordonnee.explo_mur :
				if droite or direction == 0 :
					if coordonnee_mur == (self.pos[0]+25, self.pos[1]) :
						recul = False
				if gauche or direction == 1 :
					if coordonnee_mur == (self.pos[0]-25, self.pos[1]) :
						recul = False
				if haut or direction == 2 :
					if coordonnee_mur == (self.pos[0], self.pos[1]-25) :
						recul = False
				if bas or direction == 3 :
					if coordonnee_mur == (self.pos[0], self.pos[1]+25) :
						recul = False
			if recul == True :
				while time < time_end :
					self.in_boucle = True
					if droite or direction == 0 :
						self.pos = (self.pos[0]+5, self.pos[1])
					if gauche or direction == 1 :
						self.pos = (self.pos[0]-5, self.pos[1])
					if haut or direction == 2 :
						self.pos = (self.pos[0], self.pos[1]-5)
					if bas or direction == 3 :
						self.pos = (self.pos[0], self.pos[1]+5)

					list_coordonnee.chargement(fenetre, self, monstre)

					pygame.display.flip()

					pygame.time.wait(200)
					time = pygame.time.get_ticks()
				self.in_boucle = False

	def time_to_punch (self, fenetre, list_coordonnee, numero_monstre, monstre) :
		time_end = pygame.time.get_ticks()+500
		time_print_punch = pygame.time.get_ticks()
		time_close_punch = pygame.time.get_ticks()+100
		time = pygame.time.get_ticks()
		frapper = False
		toucher = True
		tentative_frappe = False
		coordonnee_monstre = list_coordonnee.explo_monstre[numero_monstre]
		police_time_to_punch = pygame.font.Font("Police/pixel.ttf", 24)
		Time_to_punch = police_time_to_punch.render("TIME TO PUNCH !!!", True, (255,255,255))
		while time < time_end :
			self.in_boucle = True

			list_coordonnee.chargement(fenetre, self, monstre)

			if time > time_print_punch and time < time_close_punch :
				fenetre.blit(Time_to_punch, (100, 230))

			if time >= time_close_punch :
				time_close_punch+=200
				time_print_punch+=200

			for event in pygame.event.get() :
				if event.type == KEYDOWN :
					if event.key == K_RIGHT :
						self.direction_explo = "RIGHT"
						self.image_actuel = self.image_right
						time_end+=100
					if event.key == K_LEFT :
						self.direction_explo = "LEFT"
						self.image_actuel = self.image_left
						time_end+=100
					if event.key == K_DOWN :
						self.direction_explo = "DOWN"
						self.image_actuel = self.image_down
						time_end+=100
					if event.key == K_UP :
						self.direction_explo == "UP"
						self.image_actuel = self.image_up
						time_end+=100
					if event.key == K_SPACE and frapper == False :
						tentative_frappe = True
			if tentative_frappe :
				if coordonnee_monstre[0] == self.pos[0]-25 and coordonnee_monstre[1] == self.pos[1] and self.direction_explo == "LEFT" :
					frapper = True
				if coordonnee_monstre[0] == self.pos[0]+25 and coordonnee_monstre[1] == self.pos[1] and self.direction_explo == "RIGHT" :
					frapper = True
				if coordonnee_monstre[0] == self.pos[0] and coordonnee_monstre[1] == self.pos[1]-25 and self.direction_explo == "UP" :
					frapper = True
				if coordonnee_monstre[0] == self.pos[0] and coordonnee_monstre[1] == self.pos[1]+25 and self.direction_explo == "DOWN" :
					frapper = True
					self.image_punch_epee.set_colorkey((0,0,0))					
				if coordonnee_monstre == self.pos :
					frapper = True
			fenetre.blit(self.image_actuel, self.pos)
			pygame.display.flip()
			time = pygame.time.get_ticks()
			if frapper :
				time = time_end+10 #Le 10 est normalement inutile mais permet d'être sûr que time >= time_end et ne change rien pour la suite
		self.in_boucle = False
		if frapper == True :
			toucher = False
			monstre.toucher(self.degat, fenetre, list_coordonnee, numero_monstre, self.direction_explo, self)
		return toucher

class Coordonnee :
	def __init__(self) :
		self.explo_mur = []
		self.explo_sol = []
		self.explo_coal = []
		self.explo_general_sol = []
		self.explo_monstre = []
		self.explo_case_eviter_monstre = []
		self.explo_fleche = []
		self.explo_time_fleche_tirer = [] #Pas en lien avec coordonnée mais plus pratique pour y accéder depuis différent fichier
		self.explo_direction_fleche_tirer = [] #Idem que précédent
		self.explo_lantern = []
		self.explo_mur_zone_deja_explore = {}
		self.explo_sol_zone_deja_explore = {}
		self.explo_coal_zone_deja_explore = {}
		self.explo_lantern_zone_deja_explore = {}
		self.ville_mur = []
		self.ville_sol = []
		self.explo_marqueur = {}
		self.donjon_mur = []
		self.donjon_sol = []

	def chargement(self, fenetre, player, monstre, num_monstre_non_print="") :
		fenetre.fill((0,0,0))
		sol = pygame.image.load("Image/sol_explo.jpg").convert()
		coal = pygame.image.load("Image/coal.png").convert_alpha()
		for coordonnee_sol in self.explo_sol :
			fenetre.blit(sol, coordonnee_sol)
		for coordonnee_coal in self.explo_coal :
			fenetre.blit(coal, coordonnee_coal)
		monstre.chargement(fenetre, self, num_monstre_non_print)

		##########################################################
		####Chargement des lumières et de l'obscurité ambiante####
		##########################################################
		lantern = pygame.image.load("Image/torch.png").convert()
		lantern.set_colorkey((0,255,0))

		obscurite = pygame.surface.Surface((500,500))
		obscurite.fill(pygame.color.Color(150, 150, 150))

		light = pygame.image.load("Image/cercle.png").convert()
		light.set_colorkey((255,255,255))

		for coordonnee_lantern in self.explo_lantern :
			fenetre.blit(lantern, coordonnee_lantern)
			obscurite.blit(light, (coordonnee_lantern[0]-150, coordonnee_lantern[1]-150), special_flags=pygame.BLEND_RGBA_MIN)
		if player.item_equip == "Torche" :
			obscurite.blit(light, (player.pos[0]-150, player.pos[1]-150), special_flags=pygame.BLEND_RGBA_MIN)
		fenetre.blit(obscurite, (0,0), special_flags=pygame.BLEND_RGBA_SUB)
		fenetre.blit(player.image_actuel, player.pos)

		self.chargement_info_perso(fenetre, player)

	def chargement_info_perso(self, fenetre, player) :

		background_1 = pygame.draw.rect(fenetre, (0,0,0), (2, 2, 95, 90))
		contour_background_1 = pygame.draw.rect(fenetre, (255,255,255), (0, 0, 99, 94), 2)
		police = pygame.font.Font(None, 20)

		name_player = police.render(player.name, True, (255, 255, 255))
		fenetre.blit(name_player, (5,5))

		txt_level = police.render("Lvl : " + str(player.lvl), True, (255,255,255))
		fenetre.blit(txt_level, (5, 20))
		txt_exp = police.render("Exp : "+str(player.exp)+"/"+str(player.exp_require_lvl_up), True, (255,255,255))
		fenetre.blit(txt_exp, (5, 35))
		txt_money = police.render("Money : " + str(player.money) + "$", True, (255,255,255))
		fenetre.blit(txt_money, (5, 50))

		txt_item_equip = police.render(str(player.item_equip), True, (255,255,255))
		fenetre.blit(txt_item_equip, (5, 65))
		
		background_vie = pygame.draw.rect(fenetre, (255,255,255), (5, 80, 74, 10), 1)
		for vie in range(player.vie) :
			affichage_vie = pygame.draw.rect(fenetre, (0,255,0), (6+(8*vie), 79, 8, 8))

	def chargement_fleche(self, fenetre, player, monstre) :
		numero_fleche = int(0)
		for coordonnee_fleche in self.explo_fleche :
			fleche = pygame.image.load("Image/arrow.png").convert()
			fleche.set_colorkey((0,0,0))
			fleche_detruite = False
			time_tirer_fleche = self.explo_time_fleche_tirer[numero_fleche]
			time = pygame.time.get_ticks()

			if time >= time_tirer_fleche+20 :
				abscisse_fleche = coordonnee_fleche[0]
				ordonnee_fleche = coordonnee_fleche[1]
				abscisse_fleche_test_mur = coordonnee_fleche[0]
				ordonnee_fleche_test_mur = coordonnee_fleche[1]
				direction = self.explo_direction_fleche_tirer[numero_fleche]
				if direction == "RIGHT" :
					abscisse_fleche+=5
					abscisse_fleche_test_mur+=25
					ordonnee_fleche_test_mur-=12 #Lié au -12 de l'ordonnée effectué afin de centrer la flèche
				if direction == "LEFT" :
					abscisse_fleche-=5
					abscisse_fleche_test_mur-=25
					ordonnee_fleche_test_mur-=12
				if direction == "UP" :
					ordonnee_fleche-=5
					ordonnee_fleche_test_mur-=25
					abscisse_fleche_test_mur-=12
				if direction == "DOWN" :
					ordonnee_fleche+=5
					ordonnee_fleche_test_mur+=25
					abscisse_fleche_test_mur-=12
				for coordonnee_mur in self.explo_mur :
					numero_monstre = int(0)
					for coordonnee_monstre in self.explo_monstre :
						if coordonnee_monstre == (abscisse_fleche_test_mur, ordonnee_fleche_test_mur) and fleche_detruite == False :
							monstre.toucher(int(1), fenetre, self, numero_monstre, direction, player)
							del self.explo_fleche[numero_fleche]
							del self.explo_time_fleche_tirer[numero_fleche]
							del self.explo_direction_fleche_tirer[numero_fleche]
							fleche_detruite = True
						numero_monstre+=1
					if coordonnee_mur == (abscisse_fleche_test_mur, ordonnee_fleche_test_mur) and fleche_detruite==False :
						del self.explo_fleche[numero_fleche]
						del self.explo_time_fleche_tirer[numero_fleche]
						del self.explo_direction_fleche_tirer[numero_fleche]
						fleche_detruite = True
					elif fleche_detruite == False :
						self.explo_fleche[numero_fleche] = (abscisse_fleche, ordonnee_fleche)
				if fleche_detruite == False :
					self.explo_time_fleche_tirer[numero_fleche] = time
					numero_fleche+=1

		numero_fleche = int(0)
		for coordonnee_fleche in self.explo_fleche :
			fleche = pygame.image.load("Image/arrow.png").convert()
			fleche.set_colorkey((0,0,0))
			if self.explo_direction_fleche_tirer[numero_fleche] == "RIGHT" :
				fleche = pygame.transform.rotate(fleche, 180)
			if self.explo_direction_fleche_tirer[numero_fleche] == "UP" :
				fleche = pygame.transform.rotate(fleche, -90)
			if self.explo_direction_fleche_tirer[numero_fleche] == "DOWN" :
				fleche = pygame.transform.rotate(fleche, 90)
			fenetre.blit(fleche, coordonnee_fleche)
			numero_fleche+=1

class Monstre :
	def __init__(self) :
		self.vie = []
		self.nombre = int(0)
		self.image = pygame.image.load("Image/monstre.png").convert_alpha()
		self.image.set_colorkey((255,255,255))
		self.value_exp = int(10)
	def chargement(self, fenetre, list_coordonnee, num_monstre_non_print) :
		numero_monstre = int(0)
		for coordonnee_monstre in list_coordonnee.explo_monstre :
			if type(num_monstre_non_print)==int :
				if num_monstre_non_print == numero_monstre :
					continue
			fenetre.blit(self.image, coordonnee_monstre)
			rectangle_vie_plein = pygame.draw.rect(fenetre, (0,0,0), (coordonnee_monstre[0], (coordonnee_monstre[1]-4), 25, 4))
			rectangle_vie_contour = pygame.draw.rect(fenetre, (255,255,255), (coordonnee_monstre[0], coordonnee_monstre[1]-4, 25, 4), 1)
			for quantite_vie in range(self.vie[numero_monstre]) :
				carre_vie = pygame.draw.rect(fenetre, (0,255,0), (coordonnee_monstre[0]+(quantite_vie*5), coordonnee_monstre[1]-3, 5, 2))
			numero_monstre+=1

	def toucher (self, degat, fenetre, list_coordonnee, numero_monstre, direction, player) :
		self.vie[numero_monstre]-=degat
		presence_mur = False
		coordonnee_monstre = list_coordonnee.explo_monstre[numero_monstre]
		for coordonnee_mur in list_coordonnee.explo_mur :
			if direction == "RIGHT" and coordonnee_monstre[0]+25 == coordonnee_mur[0] and coordonnee_monstre[1] == coordonnee_mur[1] :
				presence_mur = True
			if direction == "LEFT" and coordonnee_monstre[0]-25 == coordonnee_mur[0] and coordonnee_monstre[1] == coordonnee_mur[1] :
				presence_mur = True
			if direction == "UP" and coordonnee_monstre[0] == coordonnee_mur[0] and coordonnee_monstre[1]-25 == coordonnee_mur[1] :
				presence_mur = True
			if direction == "DOWN" and coordonnee_monstre[0] == coordonnee_mur[0] and coordonnee_monstre[1]+25 == coordonnee_mur[1] :
				presence_mur = True

		time_end = pygame.time.get_ticks()+1000
		time_animation_punch = pygame.time.get_ticks()
		time = pygame.time.get_ticks()
		direction_perso = player.direction_explo.lower()
		numero_image_animation = int(1)
		compteur = int(1)
		image_initial_player = player.image_actuel
		while time < time_end or compteur<=5 :
			player.in_boucle = True
			if presence_mur == False :
				if direction == "RIGHT" and compteur<=5 :
					coordonnee_monstre = (coordonnee_monstre[0]+5, coordonnee_monstre[1])
				if direction == "LEFT" and compteur<=5 :
					coordonnee_monstre = (coordonnee_monstre[0]-5, coordonnee_monstre[1])
				if direction == "DOWN" and compteur<=5 :
					coordonnee_monstre = (coordonnee_monstre[0], coordonnee_monstre[1]+5)
				if direction == "UP" and compteur<=5 :
					coordonnee_monstre = (coordonnee_monstre[0], coordonnee_monstre[1]-5)

				list_coordonnee.explo_monstre[numero_monstre] = coordonnee_monstre
				
			list_coordonnee.chargement(fenetre, player, self, numero_monstre)
			if direction_perso == "right" or direction_perso =="up" :
				image_animation = pygame.image.load("Image/hero_attack_"+direction_perso+"_"+str(numero_image_animation)+".png").convert()
				image_animation.set_colorkey((0,255,0))
				fenetre.blit(image_animation, player.pos)
				player.image_actuel = image_animation
				numero_image_animation+=1

			if direction_perso == "left" or direction_perso == "down" and numero_image_animation<6 :
				image_animation = pygame.image.load("Image/hero_attack_"+direction_perso+"_"+str(numero_image_animation)+".png").convert()
				image_animation.set_colorkey((0,255,0))
				fenetre.blit(image_animation, player.pos)
				player.image_actuel = image_animation
				numero_image_animation+=1

			list_coordonnee.chargement_info_perso(fenetre, player)
			pygame.display.flip()
			pygame.time.wait(100)
			list_coordonnee.chargement(fenetre, player, self)
			pygame.display.flip()
			pygame.time.wait(100)
			time = pygame.time.get_ticks()
			compteur+=1
		player.image_actuel = image_initial_player

		player.in_boucle = False
		if self.vie[numero_monstre] <= 0 :

			coordonnee_monstre_mort = list_coordonnee.explo_monstre[numero_monstre]
			time_end = pygame.time.get_ticks()+500
			time = pygame.time.get_ticks()
			while time < time_end :
				player.in_boucle = True
				list_coordonnee.chargement(fenetre, player, self, numero_monstre)
				pygame.display.flip()
				pygame.time.wait(100)
				list_coordonnee.chargement(fenetre, player, self)
				pygame.display.flip()
				pygame.time.wait(100)
				time = pygame.time.get_ticks()

			################################
			#########Animation loot#########
			################################
			time_end = pygame.time.get_ticks()+200
			time_affichage = pygame.time.get_ticks()+20
			loot = randrange(4)
			if loot == 0 :
				value_loot = randrange(10, 30)
				player.money+=value_loot
				police = pygame.font.Font(None, 20)
				text_loot = police.render(str(value_loot)+"$", True, (255,255,255))
				coordonnee_text_loot = player.pos

				while time < time_end :
					list_coordonnee.chargement(fenetre, player, self)
					coordonnee_text_loot = (coordonnee_text_loot[0], coordonnee_text_loot[1]-2)
					fenetre.blit(text_loot, coordonnee_text_loot)
					pygame.display.flip()
					pygame.time.wait(10)
					time = pygame.time.get_ticks()
				list_coordonnee.chargement(fenetre, player, self)
				pygame.display.flip()

			player.in_boucle = False
			del self.vie[numero_monstre]
			del list_coordonnee.explo_monstre[numero_monstre]
			self.nombre-=1
			player.exp+=self.value_exp

	def mouvement(self, fenetre, player, list_coordonnee) :
		for numero_monstre in range(self.nombre) :

			coordonnee_monstre = list_coordonnee.explo_monstre[numero_monstre]
			da_MP = coordonnee_monstre[0] - player.pos[0] #Distance entre le monstre et le player sur l'axe des abscisses
			do_MP = coordonnee_monstre[1] - player.pos[1] #MM chose sur l'axe des ordonnées
			nouvel_abscisse = coordonnee_monstre[0]
			nouvel_ordonnee = coordonnee_monstre[1]
			abscisse_change = False
			ordonee_change = False
			mur_droite = False
			mur_gauche = False
			mur_bas = False
			mur_haut = False
			forcer_gauche_droite = False

			for coordonnee_mur in list_coordonnee.explo_case_eviter_monstre :
				if coordonnee_mur == (nouvel_abscisse+25, nouvel_ordonnee) :
					mur_droite = True
				if coordonnee_mur == (nouvel_abscisse-25, nouvel_ordonnee) :
					mur_gauche = True
				if coordonnee_mur == (nouvel_abscisse, nouvel_ordonnee+25) :
					mur_bas = True
				if coordonnee_mur == (nouvel_abscisse, nouvel_ordonnee-25) :
					mur_haut = True
			mouvement = False
			while mouvement == False :
				if abs(da_MP) < abs(do_MP) and (mur_bas == False or mur_haut == False) and forcer_gauche_droite == False : #abs() = valeur absolue
					if do_MP < 0 and mur_bas == False :
						nouvel_ordonnee+=25
						mouvement = True
					elif do_MP >= 0 and mur_haut == False:
						nouvel_ordonnee-=25
						mouvement = True
					else :
						forcer_gauche_droite = True

				elif (abs(da_MP) >= abs(do_MP) and (mur_gauche == False or mur_droite == False)) or (forcer_gauche_droite == True) or (mur_bas == True and mur_haut == True) :

					if da_MP<0 and mur_droite == False :
						nouvel_abscisse+=25
						mouvement = True
					elif da_MP >= 0 and mur_gauche == False :
						nouvel_abscisse-=25
						mouvement = True
					elif forcer_gauche_droite == False and (mur_bas == False or mur_haut == False) :
						if mur_bas == False :
							nouvel_ordonnee+=25
							mouvement = True
						elif mur_haut == False:
							nouvel_ordonnee-=25
							mouvement = True
					else :
						list_coordonnee.explo_case_eviter_monstre.append(coordonnee_monstre)
						if mur_haut == False :
							nouvel_ordonnee-=25
							mouvement = True
						if mur_bas == False :
							nouvel_ordonnee+=25
							mouvement = True
						if mur_gauche == False :
							nouvel_abscisse-=25
							mouvement = True
						if mur_droite == False :
							nouvel_abscisse+=25
							mouvement = True

			list_coordonnee.explo_monstre[numero_monstre] = (nouvel_abscisse, nouvel_ordonnee)
			pygame.display.flip()

class Item :
	def __init__(self) :
		self.item_to_buy = ["Bandage", "Epée", "Torche", "Arc", "Fleches", "Pioche Pierre", "Carte", "Marqueur"]
		self.item_spe = ["Carte", "Marqueur"]
		self.item_price = {}
		self.item_price["Epée"] = 20
		self.item_price["Arc"] = 30
		self.item_price["Torche"] = 1
		self.item_price["Bandage"] = 10
		self.item_price["Pioche Pierre"] = 10
		self.item_price["Fleches"] = 3
		self.item_price["Carte"] = 50
		self.item_price["Marqueur"] = 10

		self.minerai_price = {}
		self.minerai_price["Charbon"] = 1

		self.item_durabilite = {}
		self.item_durabilite["Epée"] = 10
		self.item_durabilite["Pioche"] = 30
		self.item_durabilite["Arc"] = 50

class Boss :
	def __init__(self) :
		self.vie = 50
		self.pos = (210, 230)
		self.vitesse = (3, 40) #nbre pixel bouge et nbre milliseconde entre chaque mouvement
		self.image = pygame.image.load("Image/boss1.png").convert()
		self.image.set_colorkey((0,255,0))
		self.longeur_largeur = {}

		#######Info mouvement#######
		self.last_time_movement = 0
		self.last_changement_image = 0
		self.last_numero_image = 1
		self.direction = "RIGHT"
		self.nombre_image = {}
		image_exist = True
		direction = ["RIGHT", "LEFT", "UP", "DOWN"]
		changement_direction = 0
		nombre_image = 0
		while image_exist :
			try :
				image = pygame.image.load("Image/boss1_{}_{}.png".format(self.direction, self.last_numero_image))
				self.longeur_largeur[(self.direction, self.last_numero_image)] = (image.get_rect()[2], image.get_rect()[3])
				print("Image : Image/boss1_{}_{}.png load".format(self.direction, str(self.last_numero_image)))
				nombre_image+=1
				self.last_numero_image+=1
			except :
				print("Pour la direction {}, il y a {} images.".format(str(self.direction), str(nombre_image)))
				self.nombre_image[self.direction] = nombre_image
				nombre_image = 0
				self.last_numero_image = 1
				changement_direction+=1
				print('Changement direction numéro : ', str(changement_direction))
				if changement_direction >= 4 :
					image_exist = False
				else :
					self.direction = direction[changement_direction]

		########Info attaque######
		self.portee = 30
		self.chargement_attaque = 0
		self.debut_attaque = 0
		self.degat = 50
		self.force = 20 #nombre de pixel que le joueur est projeté en arrière


	def mouvement (self, fenetre, player, list_coordonnee) :
		abscisse_boss, ordonnee_boss = self.pos
		direcion = ""
		distance_x = self.pos[0]-player.pos[0]
		distance_y = self.pos[1]-player.pos[1]
		if abs(distance_x) > abs(distance_y) : #abs() = valeur absolue
			if distance_x > 0 :
				abscisse_boss -= self.vitesse[0]
				direction = "LEFT"
			else :
				abscisse_boss += self.vitesse[0]
				direction = "RIGHT"
		else : #Si distance_x = distance_y -> monstre bouge sur axe ordonnee
			if distance_y > 0 :
				ordonnee_boss -= self.vitesse[0]
				direction = "UP"
			else :
				ordonnee_boss += self.vitesse[0]
				direction = "DOWN"

		############################
		#####Test collision mur#####
		############################

		abscisse_test_collision, ordonnee_test_collision = abscisse_boss, ordonnee_boss
		if self.pos[0] > int(pygame.display.get_surface().get_size()[0]/2) :
			abscisse_test_collision+=self.longeur_largeur[(self.direction, self.last_numero_image)][0]
		if self.pos[1] > int(pygame.display.get_surface().get_size()[1]/2) :
			ordonnee_test_collision+=self.longeur_largeur[(self.direction, self.last_numero_image)][1]

		if (int(abscisse_test_collision/25)*25, int(ordonnee_test_collision/25)*25) in list_coordonnee.donjon_sol :
			self.pos = (abscisse_boss, ordonnee_boss)
			if self.direction == direction :
				if int(pygame.time.get_ticks()) > self.last_changement_image+200 :
					self.last_numero_image+=1
					self.last_changement_image = pygame.time.get_ticks()
					if self.last_numero_image > self.nombre_image[self.direction] :
						self.last_numero_image=1
			else :
				self.direction = direction

		self.last_time_movement = pygame.time.get_ticks()

	def affichage(self, fenetre) :
		self.image = pygame.image.load("Image/boss1_{}_{}.png".format(self.direction, str(self.last_numero_image))).convert()
		self.image.set_colorkey((0,255,0))
		fenetre.blit(self.image, self.pos)
		pygame.draw.circle(fenetre, (255,255,255), (self.pos[0]+int(self.longeur_largeur[(self.direction, self.last_numero_image)][0]/2), 
			self.pos[1]+int(self.longeur_largeur[(self.direction, self.last_numero_image)][1]/2)), self.portee, 1)

	def attaque_corps_a_corps(self, player, fenetre, list_coordonnee) :
		center_monster_pos = (self.pos[0]+int(self.longeur_largeur[(self.direction, self.last_numero_image)][0]/2), self.pos[1]+int(self.longeur_largeur[(self.direction, self.last_numero_image)][1]/2))
		dist_monster_player_x = min([center_monster_pos[0]-player.pos[0], center_monster_pos[0]-player.pos[0]-player.largeur])
		dist_monster_player_y = min([center_monster_pos[1]-player.pos[1], center_monster_pos[1]-player.pos[1]-player.longueur])

		if abs(dist_monster_player_x) <= self.portee and abs(dist_monster_player_y) <= self.portee :

			if self.debut_attaque == 0 : #si c'est la première fois que le joueur entre dans la portee du monstre
				self.chargement_attaque = randrange(100, 300)
				self.debut_attaque = pygame.time.get_ticks()
			elif pygame.time.get_ticks() > self.chargement_attaque + self.debut_attaque :
				player.vie -= self.degat
				time_end_recul = pygame.time.get_ticks()+500
				time_next_apparition_image_player = pygame.time.get_ticks()+100
				time_last_recul = pygame.time.get_ticks()
				while pygame.time.get_ticks() < time_end_recul :
					fenetre.fill((0,0,0))
					sol_image = pygame.image.load("Image/sol_explo.jpg")
					for coordonnee_sol in list_coordonnee.donjon_sol :
						fenetre.blit(sol_image, coordonnee_sol)
					self.affichage(fenetre)
					if pygame.time.get_ticks() > time_next_apparition_image_player :
						fenetre.blit(player.image_actuel, player.pos)
					if pygame.time.get_ticks() > time_next_apparition_image_player+100 :
						time_next_apparition_image_player = pygame.time.get_ticks()+100
					if pygame.time.get_ticks() > time_last_recul :
						recul = self.force/20
						if self.direction == "RIGHT" :
							player.pos = (player.pos[0]-recul, player.pos[1])
						if self.direction == "LEFT" :
							player.pos = (player.pos[0]+recul, player.pos[1])
						if self.direction == "UP" :
							player.pos = (player.pos[0], player.pos[1]-recul)
						if self.direction == "DOWN" :
							player.pos = (player.pos[0], player.pos[1]+recul)
						time_last_recul+=(500/20)
					pygame.display.flip()
				player.invincible_dungeon = (True, 1000, pygame.time.get_ticks())
		else :
			self.debut_attaque = 0

class Fleche :
	def __init__ (self, mouse_pos, player_pos) :
		self.pos = player_pos
		if mouse_pos[0] == player_pos[0] :
			if mouse_pos[1] < player_pos[1] :
				self.direction == "UP"
			else :
				self.direction == "DOWN"
			self.angle = 90
		else :
			self.coef_directeur = (mouse_pos[1]-player_pos[1])/(mouse_pos[0]-player_pos[0])
			self.ordonee_origine = mouse_pos[1]-(self.coef_directeur*mouse_pos[0])
			if self.coef_directeur <= 1 and self.coef_directeur >= -1 :
				try :
					self.angle = degrees(atanh(self.coef_directeur))
				except :
					print(self.coef_directeur)
				if mouse_pos[0] < player_pos[0] :
					self.direction = "RIGHT"
					self.angle = -self.angle
				else :
					self.direction = "LEFT"
					self.angle=180-self.angle
			else :
				self.angle = degrees(atanh(1/self.coef_directeur))
				if mouse_pos[1] < player_pos[1] :
					self.angle-=90
				else :
					self.angle+=90
		print(self.angle)
		self.vitesse = 4

	def mouvement (self) :
		if self.direction == "LEFT" :
			self.pos = (self.pos[0]+self.vitesse, (self.coef_directeur*(self.pos[0]+self.vitesse))+self.ordonee_origine)
		elif self.direction == "RIGHT" :
			self.pos = (self.pos[0]-self.vitesse, (self.coef_directeur*(self.pos[0]-self.vitesse))+self.ordonee_origine)
		elif self.direction == "DOWN" :
			self.pos = (self.pos[0], self.pos[1]+self.vitesse)
		elif self.direction == "UP" :
			self.pos = (self.pos[0], self.pos[1]-self.vitesse)

class Serveur :
	def __init__(self) :
		self.connecte = False
		self.hote = False
		self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = int(666)
		self.adresse = ''