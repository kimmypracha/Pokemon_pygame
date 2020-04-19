import random
from characters import CHARACTERS
from moves_dictionary import MOVES_DICTIONARY
from powers import POWERS
from stats import STATS
import pygame
class Pokemon:


    def __init__(self,name):
        tmp_char = CHARACTERS[name]
        self.name = name
        self.type_ = tmp_char['Type']
        self.HP = tmp_char['HP']
        self.Attack = tmp_char['Attack']
        self.Defense = tmp_char['Defense']
        self.Speed = tmp_char['Speed']
        self.Moves = tmp_char['Moves']
        self.Experience = 0
        self.Level = 1


    def __str__(self):
        
        tmp_str = f"{self.name} has is type {self.type_}\n" + f"{self.name} has moves {self.Moves}.\n"
        genre = ['super effective against','not very effective against']
        for move in self.Moves:
            move_info = MOVES_DICTIONARY[move]
            tmp_str += f"{move} with {move_info['power']} power is {genre[0]} the type: {move_info[genre[0]]}.\n" # super effective against
            tmp_str += f"{move} is {genre[1]} the type: {move_info[genre[1]]}.\n" # not very effective against
        return tmp_str


    def who_attack_first(self,enemy): 
        ''' This method get the enemy instance of Pokemon and return True if the Pokemon represent by this instance get to attack first otherwise return False'''
        if self.Speed == enemy.Speed:
            toss = random.choice([-1,1])
            self.Speed += toss
        else:
            toss = 0
        if self.Speed > enemy.Speed:
            self.Speed -= toss
            print(f"{self.name} attack first.")
            return True
        elif self.Speed < enemy.Speed:
            self.Speed -= toss
            print(f"{enemy.name} attack first.")
            return False

    def critical_coeficient(self,screen=None):
        '''This method return 2 if the attack landed critical hit, otherwise return 1'''
        #num = random.randint(0,511)
        num = self.Speed
        if num <= self.Speed:
            print("Critical hit!")
            if screen:
                basicFont = pygame.font.SysFont('Monospace',24)
                critical_text = basicFont.render('Critical Hit!!',True,(255,255,255))
                critical_rect = critical_text.get_rect()
                critical_rect.center = (400,550)
                screen.blit(critical_text,critical_rect)
                pygame.display.flip()
            return 2
        else:
            return 1


    def Type_coeficient(self,move,enemy):
        '''This method get the move name and enemy instance and return the Type coeficient'''
        Type = 1
        move_dict = MOVES_DICTIONARY[move]
        for enemy_type in enemy.type_:
            if enemy_type in move_dict['super effective against']:
                Type = Type*2
            elif enemy_type in move_dict['not very effective against']:
                Type = Type*0.5
        return Type


    def calculate_damage(self,defender,move,screen=None):
        ''' This method get enemy instance and the move that self instance is going to use , and return the overall damage self instance gonna take to the enemy'''
        modifier = self.critical_coeficient(screen)*(random.randint(85,100)/100)*self.Type_coeficient(move,defender)
        damage = ((2*self.Level)/5+2)*POWERS[move]*(STATS[self.name]['Attack']/STATS[defender.name]['Defense'])*modifier
        damage = damage/50
        return damage


    def update_level(self,enemy_name):
        ''' This method get the enemy name who was defeated and update inplace to the Experience and Level Attribute in the Pokemon class'''
        self.Experience = self.Experience + CHARACTERS[enemy_name]['Experience']
        self.Level = (self.Experience)**(1/3)

    def choose_move(self,screen=None):
        ''' This method will let user choose a move and return the information of that move if it is valid'''
        if screen == None:
            print("-----------------------------------------Please choose a move-------------------------------------")
            for move in self.Moves:
                print(move)
            print("--------------------------------------------------------------------------------------------------")
            move = input("Enter the move")
            if move in self.Moves:
                return MOVES_DICTIONARY[move]
            else:
                print("Invalid move, please try again.")
                return self.choose_move()
        else:
            pygame.draw.rect(screen,(255,165,0),(50,425,700,150))
            basicFont = pygame.font.SysFont('Monospace',24)
            option_text = basicFont.render("Choose a move",True,(255,255,255))
            option_rect = option_text.get_rect()
            option_rect.center = (400,450)
            screen.blit(option_text,option_rect)
            move_button = []
            current_pos = 150
            for move in self.Moves:
                tmp_text = basicFont.render(move,True,(255,255,255))
                tmp_rect = tmp_text.get_rect()
                tmp_rect.center = (current_pos,475)
                tmp_button = screen.blit(tmp_text,tmp_rect)
                move_button.append((tmp_button,move))
                current_pos += 150
            pygame.display.flip()
            clicked = False
            while not clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        clicked = False
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        for button,name in move_button:
                            if button.collidepoint(pos):
                                clicked = True
                                return MOVES_DICTIONARY[name]


    def choose_optimal_move(self,defender):
        ''' This method will return the optimal move that will deal the most damage amongst of all the move that we can choose. We will return the information of that move from the MOVES_DICTIONARY'''
        moves_tuple = []
        for move in self.Moves:
            moves_tuple.append(((POWERS[move]*self.Type_coeficient(move,defender)),move))
        moves_tuple.sort(reverse=True)
        optimal_move = moves_tuple[0][1]
        return MOVES_DICTIONARY[optimal_move]


    def battle(self,enemy,screen=None):
        ''' Battle until one Pokemon dies'''
        first = self.who_attack_first(enemy)
        sentences = "" 
        self_full_HP = self.HP
        enemy_full_HP = enemy.HP
        while self.HP > 0 and enemy.HP > 0:
            if first == True:
                user_move = self.choose_move(screen)
            else:
                enemy_move = enemy.choose_optimal_move(self)
            if screen:
                pygame.draw.rect(screen,(255,165,0),(50,425,700,150))
            if first == True:
                damage = self.calculate_damage(enemy,user_move['name'],screen)
                enemy.HP = enemy.HP - damage
                sentences = []
                sentences += [f"After your {self.name}'s {user_move['name']} attack worth {damage :.2f} points:"]
                sentences += [f"Your HP: {self.HP :.2f} Enemy HP: {enemy.HP:.2f}"]
                print("\n".join(sentences))
                first = not first
            else:
                damage = enemy.calculate_damage(self,enemy_move['name'],screen)
                self.HP = self.HP - damage
                sentences = []
                sentences += [f"After enemy's {enemy.name}'s {enemy_move['name']} attack worth {damage:.2f} points:"]
                sentences += [f"Your HP: {self.HP:.2f} Enemy HP: {enemy.HP:.2f}"]
                print("\n".join(sentences))
                first = not first
            if screen:
                    self_HP_ratio = max(0,self.HP/self_full_HP)
                    enemy_HP_ratio = max(0,enemy.HP/enemy_full_HP)
                    pygame.draw.rect(screen,(255,0,0),(50,50,300,25))
                    pygame.draw.rect(screen,(255,0,0),(450,50,300,25))
                    pygame.draw.rect(screen,(0,255,0),(50,50,self_HP_ratio*300,25))
                    pygame.draw.rect(screen,(0,255,0),(450,50,enemy_HP_ratio*300,25))
                    basicFont = pygame.font.SysFont('Monospace',24)
                    current_pos = 450
                    for sentence in sentences:
                        battle_text = basicFont.render(sentence,True,(255,255,255))
                        battle_rect = battle_text.get_rect()
                        battle_rect.center = (400,current_pos)
                        screen.blit(battle_text,battle_rect)
                        current_pos += 40
                    pygame.display.flip()
                    clicked = False
                    while not clicked:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                clicked = False
                            if event.type == pygame.KEYDOWN or pygame.mouse.get_pressed()[0]:
                                clicked = True
        if self.HP <= 0:
            sentences = "Game Over!!!"
            print(sentences)
        elif enemy.HP <= 0:
            sentences = f"You beat {enemy.name}!"
            print()
            self.update_level(enemy.name)
        if screen:
                pygame.draw.rect(screen,(255,165,0),(50,425,700,150))
                basicFont = pygame.font.SysFont('Monospace',24)
                battle_text = basicFont.render(sentences,True,(255,255,255))
                battle_rect = battle_text.get_rect()
                battle_rect.center = (400,450)
                screen.blit(battle_text,battle_rect)
                pygame.display.flip()
                clicked = False
                while not clicked:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            clicked = False
                        if event.type == pygame.KEYDOWN or pygame.mouse.get_pressed()[0]:
                            clicked = True 
        

string_to_pokemon_class = {'Pikachu' : Pokemon('Pikachu'),
                          'Charizard' : Pokemon('Charizard'),
                           'Squirtle' : Pokemon('Squirtle'),
                          'Jigglypuff' : Pokemon('Jigglypuff'),
                          'Gengar': Pokemon('Gengar'),
                          'Magnemite': Pokemon('Magnemite'),
                          'Bulbasaur': Pokemon('Bulbasaur'),
                          'Charmander': Pokemon('Charmander'),
                          'Beedrill': Pokemon('Beedrill'),
                          'Golem': Pokemon('Golem'),
                          'Dewgong': Pokemon('Dewgong'),
                          'Hypno': Pokemon('Hypno'),
                          'Cleffa': Pokemon('Cleffa'),
                          'Cutiefly': Pokemon('Cutiefly')}