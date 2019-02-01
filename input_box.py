class InputBox:

    def __init__(self, pygame, fontsize, x, y, w, h, ic, ac, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.width = w
        self.color = ic
        self.default = text
        self.text = text
        self.font = pygame.font.Font("resources/fonts/SoukouMincho.ttf", fontsize)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.ac = ac
        self.ic = ic

    def handle_event(self, pygame, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.ac if self.active else self.ic
        if event.type == pygame.KEYDOWN:
            if self.active:
                if self.text == self.default:
                    self.text = ''
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(20, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, pygame, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)