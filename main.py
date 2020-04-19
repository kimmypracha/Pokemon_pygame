import pygame
from pokemon import string_to_pokemon_class, Pokemon
from pokemoncli import choose_character,generate_enemy,reset_game
import os
pygame.init()
screen = pygame.display.set_mode((800,600),pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Pokemon Game!")
run = True
w,h = pygame.display.get_surface().get_size()
white = (255,255,255)
orange = (255,165,0)
yellow = (255,229,124)
black = (0,0,0)
bg = pygame.image.load(os.path.join('images','pokemon.jpg'))
screen.blit(pygame.transform.scale(bg,(800,600)), (0,0))

basicFont = pygame.font.SysFont('Monospace',36)
newgame_text = basicFont.render('New Game',True,white,orange)
exit_text = basicFont.render('Exit',True, white,orange)

newgame_rect = newgame_text.get_rect()
newgame_rect.center = (100,400)
exit_rect = exit_text.get_rect()
exit_rect.center = (100,450)

newgame_button = screen.blit(newgame_text,newgame_rect)
exit_button = screen.blit(exit_text,exit_rect)

pygame.display.flip()
def battle_mode(user,enemy):
    newgame_bg = pygame.image.load(os.path.join('images','pokemon_background_2.png'))
    screen.blit(pygame.transform.scale(newgame_bg,(800,600)),(0,0))
    pygame.display.flip()
    user_img = pygame.image.load(os.path.join('images',user.name.lower()+'.jpg'))
    enemy_img = pygame.image.load(os.path.join('images',enemy.name.lower()+'.jpg'))
    screen.blit(pygame.transform.scale(user_img,(300,300)),(50,100))
    screen.blit(pygame.transform.scale(enemy_img,(300,300)),(450,100))
    user_displayname = user.name + " (Level " + str(int(user.Level)) +")"
    enemy_displayname = enemy.name + " (Level " + str(int(enemy.Level)) +")"
    user_text = basicFont.render(user_displayname,True,white,black)
    enemy_text = basicFont.render(enemy_displayname,True,white,black)
    user_rect = user_text.get_rect()
    enemy_rect = enemy_text.get_rect()
    user_rect.center = (150,30)
    enemy_rect.center= (550,30)
    screen.blit(user_text,user_rect)
    screen.blit(enemy_text,enemy_rect)
    pygame.draw.rect(screen,(0,255,0),(50,50,300,25))
    pygame.draw.rect(screen,(0,255,0),(450,50,300,25))
    pygame.display.flip()
    user.battle(enemy,screen)

def start_game():
    choices = ['Squirtle','Bulbasaur','Charmander','Jigglypuff','Pikachu','Golem']
    game_over = False
    while not game_over:
        newgame_bg = pygame.image.load(os.path.join('images','pokemon_background_1.jpg'))
        screen.blit(pygame.transform.scale(newgame_bg,(800,600)),(0,0))
        pygame.display.flip()
        pokemon = choose_character(choices,screen)
        enemy = generate_enemy()
        battle_mode(pokemon,enemy)
        game_over, choices = reset_game(pokemon,enemy,choices)



while run:
    w,h = pygame.display.get_surface().get_size()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # if event.type == pygame.VIDEORESIZE:
        #     real_screen = pygame.display.set_mode(event.dict['size'],pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF)
        #     real_screen.blit(pygame.transform.scale(screen,event.dict['size']),(0,0))
        #     pygame.display.flip()
        #    w,h = pygame.display.get_surface().get_size()

        #    screen.blit(newgame_button.image,(w//10,(h*5)//10))
        #    newgame_button.corner = (w//10, (h*5)//10)

        #    screen.blit(exit_button.image,(w//10,(h*9)//10))
        #    exit_button.corner = (w//10, (h*9)//10)
        #    pygame.display.flip()

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if exit_button.collidepoint(pos):
                run = False
            if newgame_button.collidepoint(pos):
                start_game()
                run = False
pygame.quit()