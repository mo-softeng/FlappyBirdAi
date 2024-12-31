import random, pygame, config, brain

class Player: 
    def __init__(self):
        #Bird
        self.flap_duration = 0
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20) # square
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False # when jumps
        self.alive = True 
        self.lifespan = 0

        #AI
        self.decision = None
        self.fitness = 0
        self.vision = [0.5, 1, 0.5] # describes position of bird relative to pipes
        self.input = 3
        self.brain = brain.Brain(self.input)
        self.brain.generate_net()
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)
    
    def sky_collision(self):
        return bool(self.rect.y < 30)
    
    def pipe_collision(self):
        for p in config.pipes: 
            return pygame.Rect.colliderect(self.rect, p.top_rect) or pygame.Rect.colliderect(self.rect, p.bottom_rect)

    def update(self, ground): 
        if not (self.ground_collision(ground) or self.pipe_collision()):
            # gravity
            self.vel += 0.20
            self.rect.y += self.vel 
            if self.vel > 5: 
                self.vel = 5
            self.lifespan += 1
        else: 
            self.alive = False
            self.flap = False
            self.vel = 0

    def bird_flap(self):
        if not self.flap and not self.sky_collision():
            self.flap = True
            self.vel = -5
        if self.vel >= 3:
            self.flap = False

    @staticmethod     
    def closest_pipe():
        for pipe in config.pipes:
            if not pipe.passed:
                return pipe

    # AI related functions
    def look(self):
        if config.pipes:

            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - self.closest_pipe().top_rect.bottom) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].top_rect.bottom))

            # Line to mid pipe
            self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (config.pipes[0].x, self.rect.center[1]))

            # Line to bottom pipe
            self.vision[2] = max(0, self.closest_pipe().bottom_rect.top - self.rect.center[1]) / 500
            pygame.draw.line(config.window, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].bottom_rect.top))
        
    def calculate_fitness(self):
        self.fitness = self.lifespan

    def think(self):
        self.decision = self.brain.feed_forward(vision=self.vision)
        if self.decision > 0.73:
            self.bird_flap()  # Start flapping


    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone