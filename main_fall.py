import pygame # type: ignore
import random


pygame.init()

pygame.font.init()

WIDTH, HEIGHT = 1200.0 , 800.0
screen_resolution_width, screen_resolution_height =  2560.0 , 1600.0
real_screen_width, real_screen_height = 0.335, 0.215

px_per_meter = screen_resolution_height/ real_screen_height
pixel_length = (real_screen_width / screen_resolution_width) 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



class Ball:
    
    def __init__(self, color,pos, sizeinM, GRAVITY):
        self.sizeinPx = sizeinM * (px_per_meter)
        self.x, self.y = pos, self.sizeinPx
        self.color = color
        self.sizeinPx = sizeinM * (px_per_meter)
        self.Vy = 0
        self.Ay = GRAVITY
        self.bottomTime = 0
        self.COR = 0.8 #Coefficient of Restitution (COR) (e) Bounce coefficient

    def draw(self, dt):
        self.Vy += self.Ay * dt
        self.y += (self.Vy  * dt) * (px_per_meter)

        if self.bottomTime != None:
            self.bottomTime +=dt

        if self.y >= (HEIGHT-self.sizeinPx):
            self.y = HEIGHT - self.sizeinPx
            self.Vy = -self.Vy * self.COR  #concrete
            if self.bottomTime != None:
             print("For gravity: ", self.Ay, "m/s², time to bottom was: ", self.bottomTime, "s")
            self.bottomTime = None

        pygame.draw.circle(screen, self.color, (self.x, self.y), self.sizeinPx)





earthBall = Ball((0,0,255),(WIDTH/2) , 0.010, 9.817)


running = True
while running:
    dt = clock.tick(120) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
              earthBall.Vy = 0
              earthBall.y = 0
              earthBall.Vx = 0
              earthBall.x = random.randint(50, int(WIDTH)-50)

    earthBall.draw(dt)

    font = pygame.font.SysFont("arial", 24)
    text = f"FPS: {int(clock.get_fps())}  sHeight = {real_screen_height} m, sWidth = {real_screen_width}"
    text_surf = font.render(text, True, (220, 220, 255))
    screen.blit(text_surf, (10, 10))
 
    pygame.display.flip()
    screen.fill((0, 0, 0))
     
