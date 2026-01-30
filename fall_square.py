import pygame # type: ignore
import os


pygame.init()

pygame.font.init()

# Position the window at (x, y) - e.g., 2000, 0 to open on a second monitor
x = 2560
y = 20
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
pygame.init()

pygame.font.init()

WIDTH, HEIGHT = 1080.0 , 1850.0
screen_resolution_width, screen_resolution_height =  1080.0, 1920.0
real_screen_width, real_screen_height = 0.295, 0.525

px_per_meter = screen_resolution_height/ real_screen_height
pixel_length = (real_screen_width / screen_resolution_width) 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



class rect:
    
    def __init__(self, color, heightinM, widthinM, GRAVITY):
        self.height = heightinM * (px_per_meter)
        self.width = widthinM * (px_per_meter)
        self.x, self.y = WIDTH/2, self.height
        self.color = color
        self.Vy = 0
        self.Ay = GRAVITY
        self.bottomTime = 0
        self.COR = 0.8 #Coefficient of Restitution (COR) (e) Bounce coefficient

    def draw(self, dt):
        self.Vy += self.Ay * dt
        self.y += (self.Vy  * dt) * (px_per_meter)

        if self.bottomTime != None:
            self.bottomTime +=dt

        if self.y >= (HEIGHT-self.height):
            self.y = HEIGHT - self.height
            self.Vy = -self.Vy * self.COR  #concrete
            if self.bottomTime != None:
             print("For gravity: ", self.Ay, "m/s², time to bottom was: ", self.bottomTime, "s")
            self.bottomTime = None

        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))  





earthSquare= rect((0,0,255), 0.002, 0.010, 9.817)


running = True
while running:
    dt = clock.tick(120) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
              earthSquare.Vy = 0
              earthSquare.y = 0
              

    earthSquare.draw(dt)

    font = pygame.font.SysFont("arial", 24)
    text = f"FPS: {int(clock.get_fps())}  sHeight = {real_screen_height} m, sWidth = {real_screen_width}"
    text_surf = font.render(text, True, (220, 220, 255))
    screen.blit(text_surf, (10, 10))
 
    pygame.display.flip()
    screen.fill((0, 0, 0))
     
