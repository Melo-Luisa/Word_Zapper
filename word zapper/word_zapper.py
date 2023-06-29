import pygame, random, os, easygui
from pathlib import Path

 
pygame.init()
pygame.display.set_caption("Word Zapper")
width = 800
height = 690
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
play = True


font = pygame.font.Font(None, 26)


font_path = ("word zapper/img/font.TTF")  # Substitua pelo caminho correto do arquivo de fonte
font = pygame.font.Font(font_path, 25)


def caminho_arquivo(nome):
    caminho = os.getcwd()
    caminhoAbsoluto = os.path.join(caminho, "word zapper/img", nome)
    caminhoAbsoluto = Path(caminhoAbsoluto)
    return caminhoAbsoluto



def walk(): #player 
    if keys[pygame.K_UP]:
        player_pos.y -= speed
    if keys[pygame.K_DOWN]:
        player_pos.y += speed
    if keys[pygame.K_LEFT]:
        player_pos.x -= speed
    if keys[pygame.K_RIGHT]:
        player_pos.x += speed

def delimit_player(player_pos):
    # Verifica se o jogador está fora dos limites da tela
    if player_pos.y > 510 : #posição y embaixo
        player_pos.y = 510
    elif player_pos.y < 140: #limite y alphabet
        player_pos.y = 140
    elif player_pos.x > 730:
        player_pos.x = 730
    elif player_pos.x < -50:
        player_pos.x = -50  


def shoot():
     #aperte space para shoot
    if keys[pygame.K_SPACE]:
        # Cria um novo tiro na posição atual do player
        tiro_pos = pygame.Vector2(player_pos.x + 15, player_pos.y - 8) #pos.x - posição do tiro na horizontal || pos.y qual a posição que sai o tiro
        shoots.append(tiro_pos)
    
      #movimentos dos shoots
    for tiro in shoots:
        
        tiro.y -= speed  # Movimento do tiro para cima 
        screen.blit(shoot_resized, tiro)
 
def move_alphabet():  
# Movimento do alphabet
    alphabet_pos.x += speed_alphabet

    # Verifica se o alphabet saiu da 
    if alphabet_pos.x > width:
        alphabet_pos.x = -len(alphabet) * square_size
    
def draw_alphabet(): #gira gira jequiti
    global texto_surface
    for i, letra in enumerate(alphabet):
        posicao_letra = pygame.Vector2(alphabet_pos.x + i * square_size, alphabet_pos.y)
        texto_surface = font.render(letra, True, (255, 255, 255))
        screen.blit(texto_surface, posicao_letra)
 
with open(caminho_arquivo('palavras.txt')) as arquivo:
    #comando que tira o  \n do arquivo externo
    palavras = [linha.strip() for linha in arquivo.readlines()]
drawn = random.choice(palavras)

traits_position = []

def traits(): #draw on screen traits on length of sort word
    global drawn, pos
    for i in range(len(drawn)):
        pos = pygame.Vector2(100 + i * 75, 620)
        traits_position.append(pos) 
        traits_surface = font.render("_", True, (255, 255, 255)) #imprimi os risco
        screen.blit(traits_surface, pos)
   
letras_selecionadas = []

def reached_alphabet():
    # Verifica cada tiro em relação à posição do alphabet
    for tiro in shoots:
        tiro_rect = pygame.Rect(tiro.x, tiro.y, shoot_resized.get_width(), shoot_resized.get_height()) #transforma em rect
        # Verifica cada letra do alphabet em relação à posição do tiro
        for i, letra in enumerate(alphabet):
            letra_rect = pygame.Rect(alphabet_pos.x + i * square_size, alphabet_pos.y, square_size, square_size) #tbm
                # Verifica a colisão entre o tiro e a letra do alphabet
            if tiro_rect.colliderect(letra_rect):  
                
                # print(letras_selecionadas)
                #verifica se a letra está denrto da palavra e adiciona a letra na tela
                for i in range(len(drawn)):
                    if drawn[i] == letra:
                        letras_selecionadas.append(letra)
                        letra_surface = font.render(letra, True, (153, 51, 153))
                        screen.blit(letra_surface, traits_position[i])
                
def winner():
    if len(set(letras_selecionadas)) == len(set(drawn)): #se preencheu tudo, ent venceu
       # print('venceu')
        winnig = pygame.image.load(caminho_arquivo('winner.png'))
        winnig = pygame.transform.scale(winnig, (width,height))
        screen.blit(winnig, (0,0))
        if keys[pygame.K_RETURN]: #para sair aperte enter
            exit()


                
def loser(): #pededor
    #print('perdeu')
    loser_player = pygame.image.load(caminho_arquivo('loser.png'))
    loser_player = pygame.transform.scale(loser_player, (width,height))
    screen.blit(loser_player, (0,0))
    if keys[pygame.K_RETURN]: #para sair aperte enter
        exit()
    play = False
    trash.clear()
    alphabet.clear()


nave = pygame.image.load(caminho_arquivo('nave.png')) #player img
nave_resized = pygame.transform.scale(nave, (80, 90))

red_square = pygame.image.load(caminho_arquivo('shoot.png')) #shoots img
shoot_resized = pygame.transform.scale(red_square, (50, 32))

trash_space = pygame.image.load(caminho_arquivo('trash_space.png')) #asteroide img
trash_space_resized = pygame.transform.scale(trash_space, (10, 10))

background = pygame.image.load(caminho_arquivo('space_2.png'))

#posição e speed do jogador
player_pos = pygame.Vector2(350, 500)
player_rect = pygame.Rect(player_pos.x, player_pos.y, nave_resized.get_width(), nave_resized.get_height())
speed = 10

 # segundos total
total_timer = 90
time_inicial = pygame.time.get_ticks()


#alphabet
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z']
alphabet_pos = pygame.Vector2(200, 90)
speed_alphabet = 2.5 #speed do alphabet
square_size = 85 #espaçamento das letras

#armazendo varios trash
trash = [
    {'img': trash_space, 'rect': pygame.Rect(300, 150, 50, 50), 'speed': 6},
    {'img': trash_space, 'rect': pygame.Rect(400, 250, 50, 50), 'speed': 3},
    {'img': trash_space, 'rect': pygame.Rect(500, 350, 50, 50), 'speed': 8},
    {'img': trash_space, 'rect': pygame.Rect(700, 500, 50, 50), 'speed': 4}
]

shoots = []  # Lista para armazenar os shoots
less = 0


begining = easygui.buttonbox(f'Game: Word Zapper \nWord Drawn : {drawn}', 'Welcome', ('instructions', 'Play', 'Exit'))
if begining == 'instructions':
    tutorial = easygui.buttonbox('How to play: Use the arrow keys to walk and the space bar to shoot. Objective: Avoid the asteroids, they take your points, and hit the word. If you lose or win to leave the final image press enter. \n Good Look!', 'instructions', ('Back', 'Play'))
    if tutorial == 'Back':
        begining = easygui.buttonbox(f'Game: Word Zapper \nWord Drawn : {drawn}', 'Welcome', ('instructions', 'play', 'Exit'))
    else: 
        play
elif begining == 'Sair':
    running = False
    exit()
else:
    pass
while play:
    global keys
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
  
    screen.blit(background, (0,0))
    screen.blit(nave_resized, player_pos)        
  
    walk() #player
    # Atualização do tempo decorrido em segundos
    present_timer = (pygame.time.get_ticks() - time_inicial ) // 1000
    # Atualização do tempo restante
    time_left = max(total_timer - present_timer, 0) - less
    player_rect = pygame.Rect(player_pos.x, player_pos.y, nave_resized.get_width(), nave_resized.get_height())
    if time_left < 0:
        time_left = 0
        loser()
    for trash_space in trash:
        trash_space['rect'].x += trash_space['speed'] #anda na linha de acordo com a speed

        if trash_space['rect'].x > width: #caso passe da tela
            trash_space['rect'].x = -50  # Reinicia a posição do carro
        trash_space_resized = pygame.transform.scale(trash_space['img'], (50, 50)) #coloca o carro no tamanho de acordo com a lista
        screen.blit(trash_space_resized, trash_space['rect']) #imprimi imagem

        if player_rect.colliderect(trash_space['rect']): #quando bater desconta meio segundo
            less += 0.5
    
        
          
    timer_screen = font.render(f"Cronômetro: {time_left}", True, (255, 255, 255))
    screen.blit(timer_screen, (10, 10))
       
        
   
    delimit_player(player_pos)

    shoot() #player

    move_alphabet() #alphabet

    draw_alphabet() #alphabet
  
    reached_alphabet()

    traits()  

    winner()
    
    
  
    pygame.display.update()
    pygame.display.flip()  # Atualiza a tela
    clock.tick(120)

pygame.quit()
