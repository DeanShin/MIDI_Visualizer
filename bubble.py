class Bubble():
    def __init__(self, pygame, window, color, gro_spd, x, y, radius):
        self.color = color
        self.alpha = 255
        self.gro_spd = gro_spd
        self.x = x
        self.y = y
        self.radius = radius
        self.surface = pygame.Surface(window.get_size())
        self.surface.set_colorkey((0,0,0))

    def update(self):
        self.radius += int(self.gro_spd / 8)
        self.alpha -= int(self.gro_spd / 8)
        if self.alpha <= 0:
            return True

    def draw(self, pygame, window):
        pygame.draw.circle(self.surface, self.color, \
            (self.x,self.y), self.radius, 0)
        self.surface.set_alpha(self.alpha)
        window.blit(self.surface, (0,0))