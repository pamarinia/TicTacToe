# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 15:26:20 2024

@author: polux

Jeu 2048
"""
import pygame

class Bloc:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sign = 0
    
    def draw(self, window, color):
        pygame.draw.rect(window, color, (self.x, self.y, self.width, self.height))
        if self.sign == 1: #croix
            pygame.draw.line(window, (0,0,0), (self.x + 20, self.y + 20), (self.x + self.width - 20, self.y + self.height - 20), 5)
            pygame.draw.line(window, (0,0,0), (self.x + 20, self.y + self.height - 20), (self.x + self.width - 20, self.y + 20), 5)
        elif self.sign == 2: #rond
            pygame.draw.circle(window, (0,0,0), (self.x + self.width/2, self.y + self.height/2), self.width/3, 5)

    def click(self, x_mouse, y_mouse, player_turn):
        is_click = False
        if self.x <= x_mouse <= self.x + self.width:
            if self.y <= y_mouse <= self.y + self.height:
                if self.sign == 0:
                    self.sign = player_turn
                    is_click = True
        return is_click
    
def test_win(playground):
    win = False
    for i in range(3):
        if playground[i][0].sign == playground[i][1].sign == playground[i][2].sign and playground[i][0].sign != 0 :
            win = True
        elif playground[0][i].sign == playground[1][i].sign == playground[2][i].sign and playground[0][i].sign != 0 :
            win = True
        elif playground[0][0].sign == playground[1][1].sign == playground[2][2].sign and playground[0][0].sign != 0 :
            win = True 
        elif playground[0][2].sign == playground[1][1].sign == playground[2][0].sign and playground[0][2].sign != 0 :
            win = True
    if win:
        print('You Win !')
    return win

def new_game():
    playground = [[[],[],[]],
                  [[],[],[]],
                  [[],[],[]]]
    # Set up each Square
    square_width = 200
    square_height = 200
    for i in range(3):
        for j in range(3):
            playground[i][j] = Bloc(10 + (square_width+10)*i, 10+(square_height+10)*j, square_width, square_height)
    return playground


  




if __name__=='__main__':
    pygame.init()

    # Set up the screen
    screen_width = 640
    screen_height = 800
    window = pygame.display.set_mode((screen_width, screen_height))
    window.fill((130, 110, 90))

    # Définition de la police de caractères
    police = pygame.font.Font(None, 36)

    player_1_score = 0
    player_2_score = 0
    player_turn = 1  
    
    playground = new_game()
    
    # Bouton nouvelle partie
    position_bouton = pygame.Rect(400, 650, 200, 50)
    couleur_bouton = (200, 180, 100)
    couleur_texte = (255, 255, 255)
    texte_bouton = "Nouvelle Partie"
    
    run = True
    is_win = False
    while run:
        window.fill((130, 110, 90))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Obtention des coordonnées de la souris
                x_mouse, y_mouse = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(3):
                        if playground[i][j].click(x_mouse, y_mouse, player_turn):
                            player_turn = (player_turn % 2) + 1
                if is_win:
                    if position_bouton.collidepoint(x_mouse, y_mouse):
                        print("Nouvelle partie démarrée!")
                        playground = new_game()
                        is_win = False
                        
        if not is_win:
            if test_win(playground):
                is_win = True
                if player_turn == 1:
                    player_2_score += 1
                    print(player_2_score)
                elif player_turn == 2:
                    player_1_score += 1
                    print(player_1_score)
        
        
        
        for i in range(3):
            for j in range(3):
                playground[i][j].draw(window, (150,140,120))
        
        # Affichage score
        surface_texte = police.render(f"Player 1 : {player_1_score} - {player_2_score} : Player 2", True, (255, 255, 255))
        window.blit(surface_texte, (100, 660))
   
    
        # Affichage du bouton
        pygame.draw.rect(window, couleur_bouton, position_bouton)
        # Affichage du texte sur le bouton
        texte_surface = police.render(texte_bouton, True, couleur_texte)
        texte_rect = texte_surface.get_rect(center=position_bouton.center)
        window.blit(texte_surface, texte_rect)
        
        pygame.display.flip() 
        
        