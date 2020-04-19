import random
import pygame
from characters import CHARACTERS
from pokemon import string_to_pokemon_class,Pokemon
def choose_character(choices,screen = None):
    ''' Asks user to choose from available Pokemons. Return that pokemon's subclass. '''
    if screen == None:
        print("Pokemon List:")
        for pokemon in choices:
            print(pokemon)
        name = input("Choose your pokemon")
        if name in string_to_pokemon_class: #check if the name is valid
            return string_to_pokemon_class[name]
        else:
            print("Invalid Name! Try again!")
            return choose_character(choices)
    else:
        basicFont = pygame.font.SysFont('Monospace',36)
        menu_text = basicFont.render('Choose your Pokemon',True,(255,255,255))
        menu_rect = menu_text.get_rect()
        menu_rect.center = (200,50)
        screen.blit(menu_text,menu_rect)
        pokemon_button = []
        current_pos = 100
        for pokemon in choices:
            tmp_text = basicFont.render(pokemon,True,(255,255,255),(255,165,0))
            tmp_rect = tmp_text.get_rect()
            tmp_rect.center = (200,current_pos)
            tmp_button = screen.blit(tmp_text,tmp_rect)
            current_pos += 50
            pokemon_button.append((tmp_button,pokemon))
        pygame.display.flip()
        chosen = False
        while not chosen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    for button,name in pokemon_button:
                        if button.collidepoint(pos):
                            chosen = True
                            return string_to_pokemon_class[name]
            

def generate_enemy():
    ''' Randomly generates one of 14 Pokemons to fight user. Returns that pokemon's subclass. '''
    name_list = list(string_to_pokemon_class.keys())
    chosen_name = random.choices(name_list)[0]
    return Pokemon(chosen_name)


def reset_game(pokemon, enemy, choices):
    '''If your pokemon loses, the game is over.
    If you won, add the defeated Pokemon
    to your list of possible Pokemon choices for the next round.'''
    if pokemon.HP <= 0:
        choices = ['Squirtle', 'Bulbasaur', 'Charmander']
        print("-----------------------------------------END-------------------------------------------")
        return True, choices
    else:
        if enemy.name not in choices:
            choices.append(enemy.name)
        pokemon.HP = CHARACTERS[pokemon.name]['HP']
        print("---------------------------------------NEXT-LEVEL--------------------------------------")
        return False, choices

def announce(pokemon,enemy):
    ''' This method will get both pokemon instance and display both data to user'''
    print("------------------------------------ THE BATTLE INFORMATION! --------------------------------")
    print("Your pokemon's data:")
    print(pokemon)
    print("Enemy pokemon's data:")
    print(enemy)
    print("---------------------------------------------------------------------------------------")

#if __name__ == "__main__":
choices = ['Squirtle','Bulbasaur','Charmander']
# game_over = False
# while  game_over == False:
#     pokemon = choose_character(choices)
#     enemy = generate_enemy()
#     announce(pokemon,enemy)
#     pokemon.battle(enemy)
#     game_over, choices = reset_game(pokemon,enemy,choices)