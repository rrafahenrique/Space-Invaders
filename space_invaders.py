import pygame
import os
import random

pygame.init()

#Dimensões da Janela
LARGURA = 1200 
ALTURA = 800

#Cores
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
BRANCO = (255,255,255)

#Linhas e Colunas dos Aliens
LINHAS = 5
COLUNAS = 12

#Título do jogo e criação da janela
pygame.display.set_caption("Space Invaders")
JANELA = pygame.display.set_mode((LARGURA, ALTURA))

#====================SPRITES==========================
FUNDO = pygame.image.load(os.path.join("Sprites", "fundo.png"))

NAVE = pygame.transform.scale(pygame.image.load(os.path.join("Sprites", "nave_prata.png")), (60, 60)) 
LASER = pygame.image.load(os.path.join("Sprites", "laser.png"))
LASER_ALIEN = pygame.image.load(os.path.join("Sprites", "laser-alien.png"))

#==========================Efeitos Sonoros==============================
EXPLOSAO_ALIEN = pygame.mixer.Sound("Sons/exp.wav")
EXPLOSAO_ALIEN.set_volume(0.20)
EXPLOSAO_NAVE = pygame.mixer.Sound("Sons/explosion2.wav")
LASER_NAVE = pygame.mixer.Sound("Sons/laser.wav")
LASER_NAVE.set_volume(0.30)
LASER_ALIEN_SOM = pygame.mixer.Sound("Sons/laser.wav")
LASER_ALIEN_SOM.set_volume(0.25)

#=====================Cria a Classe Nave==========================
class Nave(pygame.sprite.Sprite):
	def __init__(self, x, y, vida):
		pygame.sprite.Sprite.__init__(self)

		self.image = NAVE
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.ultimo_disparo = pygame.time.get_ticks()       #pega o tempo do último disparo dado
		self.vida_total = vida
		self.vida_restante = vida

	def update(self):
		vel_nave = 8                 #Velocidade da nave
		recarregar = 500             #Tempo entre um disparo e outro (tempo em milisegundos)
		game_over = 0 

		#==============Controle da Nave (Esquerda e Direira)======================
		setas = pygame.key.get_pressed()
		if setas[pygame.K_LEFT] and self.rect.left > 10:
			self.rect.x -= vel_nave
		if setas[pygame.K_RIGHT] and self.rect.right < LARGURA - 10:
			self.rect.x += vel_nave
		#=========================================================================

		self.mask = pygame.mask.from_surface(self.image)

		#==============================================================================
		#Faz com que seja disparado apenas um laser por vez
		tempo_atual = pygame.time.get_ticks() #pega o tempo atual
		#Disparo do Laser
		if setas[pygame.K_SPACE] and tempo_atual - self.ultimo_disparo > recarregar:
			laser = Laser(self.rect.centerx, self.rect.top)
			laser_grupo.add(laser)
			LASER_NAVE.play()
			self.ultimo_disparo = tempo_atual
		#==============================================================================

		#Desenha a barra de vida da nave (Um renângulo vermelho por baixo e outro verde por cima)
		pygame.draw.rect(JANELA, VERMELHO, (self.rect.x, self.rect.bottom, self.rect.width, 10))
		if self.vida_restante > 0:
			#Retângulo verde, faz o calculo para diminuir a barra de acordo com o hit (são 3, definidos no Grupo Nave)
			pygame.draw.rect(JANELA, VERDE, (self.rect.x, self.rect.bottom, int(self.rect.width * (self.vida_restante/self.vida_total)) , 10))
		elif self.vida_restante <= 0:
			#Grupo das Explosões
			explosao = Explosao(self.rect.centerx, self.rect.centery)
			explosao_grupo.add(explosao)
			self.kill()
			game_over = -1

		return game_over

#======================Cria a Classe Laser - Nave===================
class Laser(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = LASER
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.y -= 5
		#Elimina os disparos depois que sairam da tela
		if self.rect.bottom < 0:
			self.kill()

		#Verifica Colisão do Laser da Nave com os Aliens
		if pygame.sprite.spritecollide(self, alien_grupo, True, pygame.sprite.collide_mask):
			self.kill()
			EXPLOSAO_ALIEN.play()
			explosao = Explosao(self.rect.centerx, self.rect.centery)
			explosao_grupo.add(explosao)

#==================Cria a Classe dos Alien==========================
class Alien(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.transform.scale(pygame.image.load("Aliens/alien" + str(random.randint(1, 7)) + ".png"), (60,60))
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.contador = 0
		self.muda_direcao = 1   #será 1 ou -1 para mudar a direção

	def update(self):
		#Faz os aliens irem de um lado para outro
		self.rect.x += self.muda_direcao
		self.contador += 1
		if abs(self.contador) > 55:
			self.muda_direcao *= -1
			self.contador *= self.muda_direcao

		self.mask = pygame.mask.from_surface(self.image)
	
#===============Cria a Classe Laser - Aliens==================
class Laser_Alien(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image = LASER_ALIEN
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def update(self):
		self.rect.y += 2
		
		#Elimina os disparos depois que sairam da tela
		if self.rect.top > ALTURA:
			self.kill()

		#Verifica Colisão do Laser dos Aliens com a Nave
		if pygame.sprite.spritecollide(self, nave_grupo, False, pygame.sprite.collide_mask):
			self.kill()
			EXPLOSAO_NAVE.play()
			#Dimunui a barra de vida da nave
			nave.vida_restante -= 1
			explosao = Explosao(self.rect.centerx, self.rect.centery)
			explosao_grupo.add(explosao)

#==================Cria a Classe Explosão===================
class Explosao(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.image_explosao = []

		for num in range(1, 6):
			img = pygame.transform.scale(pygame.image.load(f"Explosão/exp{num}.png"), (60,60))
			self.image_explosao.append(img)

		self.img_atual = 0
		self.image = self.image_explosao[self.img_atual]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.contador = 0           #controle a velocidade da animanção da explosão

	def update(self):
		vel_explosao = 3
		self.contador += 1

		if self.contador >= vel_explosao and self.img_atual < len(self.image_explosao) - 1:
			self.contador = 0
			self.img_atual += 1
			self.image = self.image_explosao[self.img_atual]

		#se a animação da explosão terminar, deletar a explosão
		if self.img_atual >= len(self.image_explosao) - 1 and self.contador >= vel_explosao:
			self.kill()

#Função para escrever na tela
def texto_jogo(msg, cor, tam, x, y):
	FONTE = pygame.font.Font("Fontes/Retro Gaming/Retro-Gaming.ttf", tam)
	texto = FONTE.render(msg, True, cor)
	JANELA.blit(texto, texto.get_rect(center = [x, y]))

#==================Grupo da Nave======================
nave_grupo = pygame.sprite.Group()
nave = Nave(LARGURA//2, ALTURA - 50, 3)  #O três representa o número de vezes que a nave pode ser atingida
nave_grupo.add(nave)

#==============Grupo dos Lasers da Nave==========================
laser_grupo = pygame.sprite.Group()

#==============Grupo dos Aliens=======================
alien_grupo = pygame.sprite.Group()

#=============Grupo dos Laser dos Aliens=======================
laser_alien_grupo = pygame.sprite.Group()

#================Grupo das Explosões==============================
explosao_grupo = pygame.sprite.Group()

#=========Função para gerar os aliens(forma uma matriz de alien)====================
def criar_aliens():
	#Gera os alien
	for i in range(LINHAS):
		for j in range(COLUNAS):
			alien = Alien(100 + j * 90, 90 + i * 70)   #Posição dos aliens na tela
			alien_grupo.add(alien)

criar_aliens()

#====================Código Principal======================

run = True
game_over = 0        #0 é não gameover, 1 jogador ganhou, -1 jogador perdeu

contagem_regressiva = 3
ult_contagem = pygame.time.get_ticks()

alien_recarregar = 700        #milisegundos
alien_ult_disparo = pygame.time.get_ticks()

relogio = pygame.time.Clock()
FPS = 60

while run:
	
	relogio.tick(FPS)

	#Desenha o background
	JANELA.blit(FUNDO, (0,0))

	if contagem_regressiva == 0:
		#=============Cria de forma aleatória os lasers dos Aliens==========
		tempo_atual = pygame.time.get_ticks()
		#limita o número de disparos do alien em 15
		if tempo_atual - alien_ult_disparo > alien_recarregar and len(laser_alien_grupo) < 15 and len(alien_grupo) > 0:
			alien_ataque = random.choice(alien_grupo.sprites())
			laser_alien = Laser_Alien(alien_ataque.rect.centerx, alien_ataque.rect.bottom)
			laser_alien_grupo.add(laser_alien)
			LASER_ALIEN_SOM.play()
			alien_ult_disparo = tempo_atual

		if len(alien_grupo) == 0:
			game_over = 1

		if game_over == 0:
			#Atualiza o desenho da Nave
			game_over = nave.update()
			#Atualiza o Laser da Nave
			laser_grupo.update()
		else:
			if game_over == -1:
				texto_jogo("GAME OVER", BRANCO, 50, LARGURA//2, ALTURA//2 + 50)
			if game_over == 1:
				texto_jogo("YOU WIN!", BRANCO, 50, LARGURA//2, ALTURA//2)
	
	#Atualiza o desenho dos Aliens
	alien_grupo.update()
	#Atualiza os Lasers dos Aliens
	laser_alien_grupo.update()

	#Contagem regressiva para início do jogo
	if contagem_regressiva > 0:
		texto_jogo("GET READY!", BRANCO, 40, LARGURA//2, ALTURA//2 + 50)
		texto_jogo(str(contagem_regressiva), BRANCO, 40, LARGURA//2, ALTURA//2 + 100)
		cronometro = pygame.time.get_ticks()
		if cronometro - ult_contagem > 1000:
			contagem_regressiva -= 1
			ult_contagem = cronometro

	#Atualiza a Explosão
	explosao_grupo.update()

	#Desenha a Nave
	nave_grupo.draw(JANELA)
	#Desenha os Lasers da Nave
	laser_grupo.draw(JANELA)
	
	#Desenha os Aliens
	alien_grupo.draw(JANELA)
	#Desenha os Lasers dos Aliens
	laser_alien_grupo.draw(JANELA)

	#Desenha a Explosão
	explosao_grupo.draw(JANELA)

	#=============Loop Principal====================
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	#===============================================

	pygame.display.update()