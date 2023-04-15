import pygame, sys, random
pygame.init()

screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=(300,300))
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.centery > 10:
            self.rect.centery -= 3
        if keys[pygame.K_DOWN] and self.rect.centery < 590:
            self.rect.centery += 3
        if keys[pygame.K_LEFT] and self.rect.centerx > 10:
            self.rect.centerx -= 3
        if keys[pygame.K_RIGHT] and self.rect.centerx < 590:
            self.rect.centerx += 3
    def update(self):
        self.movement()
player_group = pygame.sprite.Group()
player = Player()
player_group.add(player)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill("red")
        self.rect = self.image.get_rect()
        self.spawning_location()
    def spawning_location(self):
        self.types = [1,2,3,4]
        self.random_type = random.choice(self.types)
        if self.random_type == 1:
            self.rect.centerx = -10
            self.rect.centery = random.randint(10,590)  
        elif self.random_type == 2:
            self.rect.centerx = random.randint(10,590)
            self.rect.centery = -10
        elif self.random_type == 3:
            self.rect.centerx = 610
            self.rect.centery = random.randint(10,590)
        elif self.random_type == 4:
            self.rect.centerx = random.randint(10,590)
            self.rect.centery = 610
    def movement(self):
        if self.random_type == 1:
            self.rect.centerx += 2
        elif self.random_type == 2:
            self.rect.centery += 2
        elif self.random_type == 3:
            self.rect.centerx -= 2
        elif self.random_type == 4:
            self.rect.centery -= 2
    def update(self):
        self.movement()
enemy_group = pygame.sprite.Group()
timer = 0
def spawn_enemies():
    global timer
    timer += 1
    if timer % 15 == 0:
        enemy = Enemy()
        enemy_group.add(enemy)

def start_menu():
    title_font = pygame.font.Font(None, 80)
    title = title_font.render("DONT GET HIT!", False, "Red")
    title_rect = title.get_rect(center=(300,225))
    start_font = pygame.font.Font(None, 60)
    start = start_font.render("start", False, "White")
    start_rect = start.get_rect(center=(300,300))
    screen.blit(title, title_rect)
    screen.blit(start, start_rect)
    mouse_pos = pygame.mouse.get_pos()
    if start_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() != (False, False, False):
        global start_menu_state, run_game_state
        start_menu_state = False
        run_game_state = True

def game_lost():
    font = pygame.font.Font(None, 50)
    lost = font.render("YOU LOST!", False, "Red")
    lost_rect = lost.get_rect(center=(300,200))
    again = font.render("again", False, "White")
    again_rect = again.get_rect(center=(300,300))
    screen.blit(lost, lost_rect)
    screen.blit(again, again_rect)
    mouse_pos = pygame.mouse.get_pos()
    if again_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() != (False, False, False):
        global game_won_state, run_game_state, game_time, time
        game_won_state = False
        run_game_state = True
        game_time = 30
        time = 0
        enemy_group.empty()
    
def game_won():
    font = pygame.font.Font(None, 50)
    won = font.render("YOU WON!", False, "Red")
    won_rect = won.get_rect(center=(300,200))
    again = font.render("again", False, "White")
    again_rect = again.get_rect(center=(300,300))
    screen.blit(won, won_rect)
    screen.blit(again, again_rect)
    mouse_pos = pygame.mouse.get_pos()
    if again_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed() != (False, False, False):
        global game_won_state, run_game_state, game_time, time
        game_won_state = False
        run_game_state = True
        game_time = 30
        time = 0
        enemy_group.empty()


timer_font = pygame.font.Font(None,30)
game_time = 30
time = 0

start_menu_state = True
run_game_state = False
game_lost_state = False
game_won_state = False
               
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill("black")
    if start_menu_state:
        start_menu()
    elif run_game_state:
        time += 1
        if time % 60 == 0:
            game_time -= 1
        if game_time == 0:
            run_game_state = False
            game_won_state = True
        collided = pygame.sprite.spritecollide(player, enemy_group, False)
        for i in collided:
            if i != None:
                run_game_state = False
                game_lost_state = True
        timer_surf = timer_font.render("Timer: " + str(game_time), False, "grey", "black")
        timer_rect = timer_surf.get_rect(center=(300,50))
        player_group.update()
        player_group.draw(screen)
        spawn_enemies()
        enemy_group.update()
        enemy_group.draw(screen)
        screen.blit(timer_surf, timer_rect)
    elif game_lost_state:
        game_lost()
    elif game_won_state:
        game_won()
        
    pygame.display.update()
    clock.tick(60)
