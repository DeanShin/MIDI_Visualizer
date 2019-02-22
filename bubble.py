class Bubble():
    def __init__(self, pygame, window, color, spd, x, y, radius):
        self.color = color
        self.alpha = 255
        self.spd = max(spd, 1)
        if spd <= 40:
            self.spd += int(40 - spd / 2)
        self.x = int(x)
        self.y = int(y)
        self.radius = int(radius)
        self.surface = pygame.Surface(window.get_size())
        self.surface.set_colorkey((0,0,0))

    def update(self):
        self.radius += int(self.spd / 8) + 4
        self.alpha -= int(self.spd / 8) + 4
        if self.alpha <= 0:
            return True

    def draw(self, pygame, window):
        pygame.draw.circle(self.surface, self.color, \
            (self.x, self.y), self.radius, 1)
        self.surface.set_alpha(self.alpha)
        window.blit(self.surface, (0,0))
