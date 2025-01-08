import pygame, random
from PIL import Image

# radius balls can bounce around
FRAME_RADIUS = 200
# minimum size the brush gets
MIN_PIXEL_SIZE = 5

# class for anything displayed
class Entity:
    def __init__(self, x=None, y=None, color=None, radius=None):
        self.x = x or 50
        self.y = y or 50
        self.color = color or (0, 0, 0)
        self.radius = radius or 50
    
    def update(self):
        pass
    
    def display(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2))
        
# ball is the painter and bounces aroudn the frame
class Ball(Entity):
    def __init__(self, x=None, y=None, color=None, radius=None):
        super().__init__(x, y, color, radius)
        self.x = x or 50
        self.y = y or 50
        self.color = color or (0, 0, 0)
        self.radius = 50
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.speed = 5
    
    # check boundary collisions, shrinks ball, updates color and moves
    def update(self, color, bounds):
        self.color = color
        self.radius = max(MIN_PIXEL_SIZE, self.radius - 0.05)
        if self.x < bounds[0][0] or self.x > bounds[0][1]:
            self.direction[0] = -self.direction[0] + random.uniform(-0.1, 0.1)
        if self.y < bounds[1][0] or self.y > bounds[1][1]:
            self.direction[1] = -self.direction[1] + random.uniform(-0.1, 0.1)
        
        self.x = self.x + (self.direction[0] * 2)
        self.y = self.y + (self.direction[1] * 2)

# handles all the rendering
# uses modified code from a prior project
class Simulation:
    def __init__(self, image_path, screen_width=None, screen_height=None, title=None):
        self.screen_width = screen_width or 1200
        self.screen_height = screen_height or 800
        self.title = title or "Picasso"
        
        self.image = Image.open(image_path)
    
        # from image find the smallest side length
        self.image_radius = min(self.image.size[0], self.image.size[1])
        
        # find scale from image to frame (lets us map a position in the frame to a pixel on the picture to sample a color)
        self.relative_scale = self.image_radius / (FRAME_RADIUS * 2)

        
        self.bounds = ((self.screen_width / 2 - FRAME_RADIUS, 
                        self.screen_width / 2 + FRAME_RADIUS), 
                       (self.screen_height / 2 - FRAME_RADIUS, 
                        self.screen_height / 2 + FRAME_RADIUS))
        
        # SIMULATION OBJECTS
        self.balls =[]
        self.entities = []
        self.entity_count = 0
        
        # INIT PYGAME
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(self.title)
        self.running = True
        
    # adds an entity
    def add_entity(self, entity):
        self.entities.append(entity)
        self.entity_count += 1
    
    # adds a ball
    def add_ball(self, ball):
        self.balls.append(ball)
    
    # event handling
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            print(f"QUIT!")
        
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
    
    def handle_keydown(self, event):
        if event.key == pygame.K_x:
            self.running = False
            print(f"QUIT!")
        if event.key == pygame.K_SPACE:
            self.add_ball(Ball(x=600, y=400, color=(255,0,0)))
            

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            # kill if too many entitys
            if len(self.entities) > 50000:
                self.running = False
                print("Exiting due to excess entities")
            
            for event in pygame.event.get():
                self.handle_event(event)
                
            self.screen.fill((0, 0, 0))    
            
            for entity in self.entities:
                entity.display(self.screen)
            
            for ball in self.balls:
                # find relative position from balls current position in the uploaded picture
                pix_pos = (
                    max(0, min(self.relative_scale * (ball.x - self.bounds[0][0]), self.image_radius - 1)), 
                    max(0, min(self.relative_scale * (ball.y - self.bounds[1][0]), self.image_radius - 1))
                )
                ball.update(self.image.getpixel(pix_pos), self.bounds)
                ball.display(self.screen)
                self.add_entity(Entity(ball.x, ball.y, ball.color, ball.radius))
            
            
            # draw bounding boxes            
            pygame.draw.rect(self.screen, (0, 0, 124), (0, 0, self.bounds[0][0], self.screen_height))
            pygame.draw.rect(self.screen, (0, 0, 124), (self.bounds[0][1], 0, self.bounds[0][0], self.screen_height))
            pygame.draw.rect(self.screen, (0, 0, 124), (0, 0, self.screen_width, self.bounds[1][0]))
            pygame.draw.rect(self.screen, (0, 0, 124), (0, self.bounds[1][1], self.screen_width, self.bounds[1][0]))
            
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.bounds[0][0] - 10, self.screen_height))
            pygame.draw.rect(self.screen, (0, 0, 0), (self.bounds[0][1] + 10, 0, self.bounds[0][0], self.screen_height))
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.screen_width, self.bounds[1][0] - 10))
            pygame.draw.rect(self.screen, (0, 0, 0), (0, self.bounds[1][1] + 10, self.screen_width, self.bounds[1][0]))
            
            pygame.display.flip()
            clock.tick(120)

        pygame.quit()


if __name__ == "__main__":
    # CHANGE TO YOUR IMAGE.
    # # only tested on JPGs, but others might work
    s = Simulation("osaka.jpg")
    
    
    s.run()
    