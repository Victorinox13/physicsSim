import pygame # type: ignore
import os

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
pixel_length = (real_screen_height / screen_resolution_height) 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



class Ball:
    
    def __init__(self, color,  pos, mass, diameterInM, GRAVITY):
        self.sizeinPx = diameterInM * (px_per_meter)
        self.x, self.y = pos, self.sizeinPx

        self.color = color
        #---------------------DRAG CALCULATION
        self.area = (diameterInM*diameterInM * 3.142) / 4
        self.mass = mass
        self.dragForce = 0
        #-------------------------------------------------
        self.Vy = 0
        self.GRAVITY = GRAVITY
        self.Ay = GRAVITY
        self.bottomTime = 0
        self.COR = 0.8 #Coefficient of Restitution (COR) (e) Bounce coefficient

    def draw(self, dt):

        Vair = 0 #m/s
        rel_velocity = self.Vy
        DRAGCOEFFICIENT = 0.47
        AIRDENC = 1.255 #kg*m³

        drag_direction =  1 if self.Vy > 0 else -1    # vallen = +, verhogen = -

        self.dragForce = 0.5*AIRDENC*(rel_velocity*rel_velocity)*DRAGCOEFFICIENT*self.area
        dragAcceleration = (self.dragForce/self.mass) *drag_direction
        self.Ay = self.GRAVITY - dragAcceleration
        #_-----------------------
        self.Vy += self.Ay * dt
        self.y += (self.Vy  * dt) * (px_per_meter)
        #_-----------------------
        
        

        if self.bottomTime != None:
            self.bottomTime +=dt
        if self.y >= (HEIGHT-self.sizeinPx):
            self.y = HEIGHT - self.sizeinPx
            self.Vy = -self.Vy * self.COR  #concrete
            if self.bottomTime != None:
             print("For gravity: ", self.Ay, "m/s², time to bottom was: ", self.bottomTime, "s")
            self.bottomTime = None

        pygame.draw.circle(screen, self.color, (self.x, self.y), self.sizeinPx)



earthBall = Ball((0,0,255), (WIDTH/2), 0.1, 0.008, 9.817)


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

    earthBall.draw(dt)

    font = pygame.font.SysFont("arial", 24)
    text = f"FPS: {int(clock.get_fps())}  sHeight = {real_screen_height} m, sWidth = {real_screen_width} Velocity: {earthBall.Vy:.2f}, objectHeight: {(earthBall.y)*pixel_length:.2f}"
    text2 = f"Mass: {earthBall.mass} kg, diameter:{earthBall.sizeinPx*pixel_length}"
    text_surf = font.render(text, True, (220, 220, 255))
    text_surf2 = font.render(text2, True, (220, 220, 255))
    screen.blit(text_surf, (10, 10))
    screen.blit(text_surf2, (10, 30))
 
    pygame.display.flip()
    screen.fill((0, 0, 0))
     
