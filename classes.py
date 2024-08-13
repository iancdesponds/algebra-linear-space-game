import pygame
import numpy as np
import sys
import time


class Projectile:
    def __init__(self, start_pos, velocity_x, velocity_y, gravity_constant, screen, color=(255, 255, 255)):
        self.position = list(start_pos)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity_constant = gravity_constant
        self.screen = screen
        self.color = color
        self.image = pygame.image.load('sprites/laser.png')
        self.rect = self.image.get_rect(center=start_pos)
        self.radius = 10

    def update(self):
        self.position[0] += self.velocity_x
        self.position[1] += self.velocity_y

    def draw(self):
        self.rect.center = self.position
        self.screen.blit(self.image, self.rect)



class Cannon:
    def __init__(self, position, gravity_constant, screen):
        self.position = position
        self.gravity_constant = gravity_constant
        self.screen = screen
        self.original_image = pygame.image.load('sprites/ship.png')
        self.original_image = pygame.transform.scale(self.original_image, (69, 69))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=position)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=self.rect.center) 

    def shoot(self, target_pos):
        velocity_scale = 0.01
        angle, magnitude = self.get_angle_and_magnitude(self.position, target_pos)
        speed = magnitude * velocity_scale

        velocity_x = np.cos(angle) * speed
        velocity_y = np.sin(angle) * speed

        return Projectile(self.position, velocity_x, velocity_y, self.gravity_constant, self.screen)

    def get_angle_and_magnitude(self, start_pos, end_pos):
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        angle = np.arctan2(dy, dx)
        magnitude = np.sqrt(dx**2 + dy**2)
        return angle, magnitude
    
    def get_angle_to_mouse(self, cannon_pos, mouse_pos):
        dx = mouse_pos[0] - cannon_pos[0]
        dy = mouse_pos[1] - cannon_pos[1]
        angle = np.arctan2(dy, dx)
        angle_degrees = np.degrees(angle) + 90
        return angle_degrees
        
    def draw(self):
        # resized_image = pygame.transform.scale(self.image, (50, 50))
        self.screen.blit(self.image, self.rect)



class Planet:
    def __init__(self, position, G, screen):
        self.position = position
        self.G = G
        self.screen = screen
        self.image = pygame.image.load('sprites/planets/Lava.png')
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=position)
        self.radius = 50

    def get_force(self, projectile):
        dx = self.position[0] - projectile.position[0]
        dy = self.position[1] - projectile.position[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance != 0:
            direction_x = dx / distance
            direction_y = dy / distance
        else:
            direction_x, direction_y = 0, 0
        
        acceleration_magnitude = self.G / distance**2
        
        acceleration_x = direction_x * acceleration_magnitude
        acceleration_y = direction_y * acceleration_magnitude
        
        return acceleration_x, acceleration_y
    
    def draw(self):
        self.screen.blit(self.image, self.rect)



class Death_star:
    def __init__(self, position, screen):
        self.position = position
        self.screen = screen
        self.image = pygame.image.load('sprites/death_star.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=position)
        self.radius = 75
    
    def draw(self):
        self.screen.blit(self.image, self.rect)

class Mainscreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))

        self.mainscreen = pygame.image.load('./src/img/mainscreen.jpeg')
        self.mainscreen = pygame.transform.scale(self.mainscreen, (1280, 720))
        self.play_button = pygame.image.load('./src/img/play_button.jpeg')
        self.play_button = pygame.transform.scale(self.play_button, (250, 80))
        self.lvl_1 = False

    def loop(self):
        clock = pygame.time.Clock()
        
        pygame.mixer.init()
        pygame.mixer.music.load('src/audio/Star_Wars_Main_Theme_Song.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        pygame.display.set_caption("Death Star Attack")


        while True:
            for event in pygame.event.get():
                # esc sai do jogo
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # pausa a música quando aperta s
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    pygame.mixer.music.pause()
                # despausa a música quando aperta p
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pygame.mixer.music.unpause()
                # clicar no botão play
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 515 <= mouse_pos[0] <= 765 and 500 <= mouse_pos[1] <= 580:
                        self.lvl_1 = True

            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.mainscreen, (0, 0))
            self.screen.blit(self.play_button, (515, 500))

            pygame.display.flip()
            clock.tick(60)

            if self.lvl_1:
                break

class Level_1:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.gravity_constant = 0.05
        self.G = 6900
        self.cannon = Cannon((100, 500), self.gravity_constant, self.screen)
        self.planets = [
            Planet((720, 240), self.G, self.screen),
            Planet((800, 560), self.G, self.screen),
        ]
        self.death_star = Death_star((1000, 200), self.screen)
        self.background = pygame.image.load('./sprites/backgrounds/Space_Stars6.png')
        self.background = pygame.transform.scale(self.background, (1280, 720))
        self.level_text = pygame.image.load('./src/img/level1.png')
        self.lives = 3
        self.font = pygame.font.SysFont('Arial', 36)

    def check_collision_circle(self, projectile, planet):
        center_distance = np.sqrt((projectile.position[0] - planet.position[0])**2 + (projectile.position[1] - planet.position[1])**2)
        sum_radii = projectile.radius + planet.radius
        if center_distance < sum_radii:
            return True
        else:
            return False
        
    def check_collision_star(self, projectile, death_star):
        center_distance = np.sqrt((projectile.position[0] - death_star.position[0])**2 + (projectile.position[1] - death_star.position[1])**2)
        sum_radii = projectile.radius + death_star.radius
        if center_distance < sum_radii:
            return True
        else:
            return False

    def game_loop(self):
        clock = pygame.time.Clock()
        projectiles = []
        
        pygame.mixer.init()
        pygame.mixer.music.load('src/audio/Star_Wars_Main_Theme_Song.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        blaster = pygame.mixer.Sound('src/audio/blaster.mp3')
        pygame.mixer.Sound.set_volume(blaster, 0.4)
        pygame.display.set_caption("Death Star Attack - Level 1")

        self.lvl2 = False


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    projectiles.append(self.cannon.shoot(mouse_pos))
                    blaster.play()

            mouse_pos = pygame.mouse.get_pos()
            angle_to_mouse = self.cannon.get_angle_to_mouse(self.cannon.position, mouse_pos)
            self.cannon.rotate(angle_to_mouse)
            self.screen.blit(self.background, (0, 0))

            lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.screen.blit(lives_text, (10, 10))

            self.screen.blit(self.level_text, (540, 30))

            self.cannon.draw()
            self.death_star.draw()
            for planet in self.planets:
                planet.draw()

            for projectile in projectiles:
                for planet in self.planets:
                    if self.check_collision_circle(projectile, planet):
                        projectiles.remove(projectile)
                        self.lives -= 1

                    elif self.check_collision_star(projectile, self.death_star):
                        self.lvl2 = True

                    else:
                        acceleration_x, acceleration_y = planet.get_force(projectile)
                        projectile.velocity_x += acceleration_x
                        projectile.velocity_y += acceleration_y
                
                        projectile.update()
                        projectile.draw()

            if self.lives == 0:
                game_over = GameOver()
                game_over.loop()

            if self.lvl2:
                break

            pygame.display.flip()
            clock.tick(60)

class Level_2:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.gravity_constant = 0.05
        self.G = 6900
        self.cannon = Cannon((100, 500), self.gravity_constant, self.screen)
        self.planets = [
            Planet((900, 300), self.G, self.screen),
            Planet((500, 500), self.G, self.screen),
            Planet((900, 700), self.G, self.screen),
            
        ]
        self.death_star = Death_star((1100, 600), self.screen)
        self.background = pygame.image.load('./sprites/backgrounds/Space_Stars6.png')
        self.background = pygame.transform.scale(self.background, (1280, 720))
        self.level_text = pygame.image.load('./src/img/level2.png')
        self.lives = 3
        self.font = pygame.font.SysFont('Arial', 36)

    def check_collision_circle(self, projectile, planet):
        center_distance = np.sqrt((projectile.position[0] - planet.position[0])**2 + (projectile.position[1] - planet.position[1])**2)
        sum_radii = projectile.radius + planet.radius
        if center_distance < sum_radii:
            return True
        else:
            return False
        
    def check_collision_star(self, projectile, death_star):
        center_distance = np.sqrt((projectile.position[0] - death_star.position[0])**2 + (projectile.position[1] - death_star.position[1])**2)
        sum_radii = projectile.radius + death_star.radius
        if center_distance < sum_radii:
            return True
        else:
            return False

    def game_loop(self):
        clock = pygame.time.Clock()
        projectiles = []
        
        pygame.mixer.init()
        pygame.mixer.music.load('src/audio/Star_Wars_Main_Theme_Song.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        blaster = pygame.mixer.Sound('src/audio/blaster.mp3')
        pygame.mixer.Sound.set_volume(blaster, 0.4)
        pygame.display.set_caption("Death Star Attack - Level 2")

        self.lvl3 = False


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    projectiles.append(self.cannon.shoot(mouse_pos))
                    blaster.play()

            mouse_pos = pygame.mouse.get_pos()
            angle_to_mouse = self.cannon.get_angle_to_mouse(self.cannon.position, mouse_pos)
            self.cannon.rotate(angle_to_mouse)
            self.screen.blit(self.background, (0, 0))

            lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.screen.blit(lives_text, (10, 10))

            self.screen.blit(self.level_text, (540, 30))

            self.cannon.draw()
            self.death_star.draw()
            for planet in self.planets:
                planet.draw()

            for projectile in projectiles:
                for planet in self.planets:
                    if self.check_collision_circle(projectile, planet):
                        projectiles.remove(projectile)
                        self.lives -= 1
                    
                    elif self.check_collision_star(projectile, self.death_star):
                        self.lvl3 = True

                    else:
                        acceleration_x, acceleration_y = planet.get_force(projectile)
                        projectile.velocity_x += acceleration_x
                        projectile.velocity_y += acceleration_y
                
                        projectile.update()
                        projectile.draw()

            if self.lives == 0:
                game_over = GameOver()
                game_over.loop()

            if self.lvl3:
                break

            pygame.display.flip()
            clock.tick(60)

class Level_3:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.gravity_constant = 0.05
        self.G = 6900
        self.cannon = Cannon((100, 500), self.gravity_constant, self.screen)
        self.planets = [
            Planet((900, 300), self.G, self.screen),
            Planet((1000, 700), self.G, self.screen),
            Planet((800, 500), self.G, self.screen),
            Planet((451, 141), self.G, self.screen),
            Planet((817, 813), self.G, self.screen),
            Planet((400, 500), self.G, self.screen),
        ]
        self.death_star = Death_star((1000, 130), self.screen)
        self.background = pygame.image.load('./sprites/backgrounds/Space_Stars6.png')
        self.background = pygame.transform.scale(self.background, (1280, 720))
        self.level_text = pygame.image.load('./src/img/level3.png')
        self.lives = 3
        self.font = pygame.font.SysFont('Arial', 36)

    def check_collision_circle(self, projectile, planet):
        center_distance = np.sqrt((projectile.position[0] - planet.position[0])**2 + (projectile.position[1] - planet.position[1])**2)
        sum_radii = projectile.radius + planet.radius
        if center_distance < sum_radii:
            return True
        else:
            return False
    
    def check_collision_star(self, projectile, death_star):
        center_distance = np.sqrt((projectile.position[0] - death_star.position[0])**2 + (projectile.position[1] - death_star.position[1])**2)
        sum_radii = projectile.radius + death_star.radius
        if center_distance < sum_radii:
            return True
        else:
            return False

    def game_loop(self):
        clock = pygame.time.Clock()
        projectiles = []
        
        pygame.mixer.init()
        pygame.mixer.music.load('src/audio/Star_Wars_Main_Theme_Song.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
        blaster = pygame.mixer.Sound('src/audio/blaster.mp3')
        pygame.mixer.Sound.set_volume(blaster, 0.4)
        pygame.display.set_caption("Death Star Attack - Level 3")

        self.win = False


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    projectiles.append(self.cannon.shoot(mouse_pos))
                    blaster.play()

            mouse_pos = pygame.mouse.get_pos()
            angle_to_mouse = self.cannon.get_angle_to_mouse(self.cannon.position, mouse_pos)
            self.cannon.rotate(angle_to_mouse)
            self.screen.blit(self.background, (0, 0))

            lives_text = self.font.render(f'Lives: {self.lives}', True, (255, 255, 255))
            self.screen.blit(lives_text, (10, 10))

            self.screen.blit(self.level_text, (540, 30))

            self.cannon.draw()
            self.death_star.draw()
            for planet in self.planets:
                planet.draw()

            for projectile in projectiles:
                for planet in self.planets:
                    if self.check_collision_circle(projectile, planet):
                        projectiles.remove(projectile)
                        self.lives -= 1

                    elif self.check_collision_star(projectile, self.death_star):
                        self.win = True

                    else:
                        acceleration_x, acceleration_y = planet.get_force(projectile)
                        projectile.velocity_x += acceleration_x
                        projectile.velocity_y += acceleration_y
                
                        projectile.update()
                        projectile.draw()

            if self.lives == 0:
                game_over = GameOver()
                game_over.loop()

            if self.win:
                break

            pygame.display.flip()
            clock.tick(60)

class GameOver:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))

        self.mainscreen = pygame.image.load('./src/img/gameover.png')
        self.mainscreen = pygame.transform.scale(self.mainscreen, (1024, 576))

    def loop(self):
        clock = pygame.time.Clock()
        
        pygame.mixer.init()
        pygame.mixer.music.load('src/audio/Star_Wars_Main_Theme_Song.mp3')
        pygame.mixer.music.set_volume(0.4)

        pygame.display.set_caption("Death Star Attack - Game Over")


        while True:
            for event in pygame.event.get():
                # esc sai do jogo
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # pausa a música quando aperta s 
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    pygame.mixer.music.pause()
                # despausa a música quando aperta p
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pygame.mixer.music.unpause()

            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.mainscreen, (128, 72))

            pygame.display.flip()
            clock.tick(60)

            time.sleep(5)
            pygame.quit()
            sys.exit()

class Victory:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))

        self.mainscreen = pygame.image.load('./src/img/victory.png')
        self.mainscreen = pygame.transform.scale(self.mainscreen, (1024, 576))

    def loop(self):
        clock = pygame.time.Clock()
        
        pygame.mixer.init()
        pygame.mixer.music.load('src/audio/Star_Wars_Main_Theme_Song.mp3')
        pygame.mixer.music.set_volume(0.4)

        pygame.display.set_caption("Death Star Attack - You Win!")


        while True:
            for event in pygame.event.get():
                # esc sai do jogo
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # pausa a música quando aperta s 
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    pygame.mixer.music.pause()
                # despausa a música quando aperta p
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pygame.mixer.music.unpause()

            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.mainscreen, (128, 72))

            pygame.display.flip()
            clock.tick(60)

            time.sleep(5)
            pygame.quit()
            sys.exit()
