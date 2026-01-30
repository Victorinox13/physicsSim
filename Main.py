import pygame # type: ignore
import os
import random

# Position the window at (x, y) - e.g., 2000, 0 to open on a second monitor
x = 2560
y = 20
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
pygame.init()

pygame.font.init()

WIDTH, HEIGHT = 1080.0 , 1850.0
screen_resolution_width, screen_resolution_height =  1080.0, 1920.0
real_screen_width, real_screen_height = 0.295, 1
scale = 1

px_per_meter = screen_resolution_height/ real_screen_height
pixel_length = (real_screen_width / screen_resolution_width) 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



class Ball:
    
    def __init__(self, color,pos, sizeinM, GRAVITY):
        self.sizeinPx = sizeinM * (px_per_meter*scale)
        self.x, self.y = pos, self.sizeinPx
        self.color = color
        self.sizeinPx = sizeinM * (px_per_meter*scale)
        
        self.Vy = 0
        self.Vx = 0
        self.Ay = GRAVITY or 0
        self.bottomTime = 0
        self.COR = 0.8

    def draw(self, dt):
        self.Vy += self.Ay * dt
        self.y += (self.Vy  * dt) * (px_per_meter*scale)

        self.x += self.Vx*dt * px_per_meter*scale

        if self.bottomTime != None:
            self.bottomTime+=dt

        if self.y >= (HEIGHT-self.sizeinPx):
            self.y = HEIGHT - self.sizeinPx
            self.Vy = -self.Vy * self.COR  #concrete
            if self.bottomTime != None:
             print("For gravity: ", self.Ay, "m/s², time to bottom was: ", self.bottomTime, "s")
            self.bottomTime = None
        if self.y - self.sizeinPx < 0:
            self.y = self.sizeinPx
            self.Vy = -self.Vy * self.COR 

         # Left wall
        if self.x - self.sizeinPx < 0:
            self.x = self.sizeinPx
            self.Vx = -self.Vx * self.COR 

        # Right wall
        if self.x + self.sizeinPx > WIDTH:
            self.x = WIDTH - self.sizeinPx
            self.Vx = -self.Vx * self.COR 

        pygame.draw.circle(screen, self.color, (self.x, self.y), self.sizeinPx)




balls = []
earthBall = Ball((0,0,255),(WIDTH/6) , 0.010, 9.817)
balls.append(earthBall)
moonBall = Ball((255,255,255),(WIDTH/6) *2, 0.010, 1.62)
balls.append(moonBall)
marsBall = Ball((255,0,0),(WIDTH/6) *3, 0.010, 3.73)
balls.append(marsBall)


running = True
while running:
    dt = clock.tick(120) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
         # Optional: continuous small thrust while holding space
    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
           for ball in balls:
            ball.y -= 50
    if keys[pygame.K_SPACE] or keys[pygame.K_DOWN]:
           for ball in balls:
            ball.y += 50
    if keys[pygame.K_RIGHT]:
        for ball in balls:
            ball.Vx += 0.1
    if keys[pygame.K_LEFT]:
        for ball in balls:
            ball.Vx -= 0.1



    elif keys[pygame.K_r]:
          for ball in balls :
              ball.Vy = 0
              ball.y = 0
              ball.Vx = 0
              ball.x = random.randint(50, int(WIDTH)-50)


    font = pygame.font.SysFont("arial", 24)
    text = f"FPS: {int(clock.get_fps())}  sHeight = {real_screen_height*(1.0/scale)} m, sWidth = {real_screen_width*(1.0/scale)}"
    text_surf = font.render(text, True, (220, 220, 255))
    screen.blit(text_surf, (10, 10))

    for ball in balls :
              ball.draw(dt)
    pygame.display.flip()
    screen.fill((0, 0, 0))
     
