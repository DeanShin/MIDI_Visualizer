from interactable import Interactable

class InputBox(Interactable):

    def __init__(self, pygame, fontsize, x, y, w, h, ic, hc, ac, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.Font("resources/fonts/SoukouMincho.ttf", fontsize)
        self.text_surface = self.font.render(text, True, ic)
        self.ac = ac
        self.hc = hc
        self.ic = ic
        self.color = ic

        self.default_text = text
        self.thickness = 2
        self.text_pos = (self.rect.x+5, self.rect.y+5)
        self.active = False


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
                if self.text == self.default_text:
                    self.text = ''
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.text_surface = self.font.render(self.text, True, self.color)


    def update(self, mouse_pos):
        # Resize the box if the text is too long.
        width = max(20, self.text_surface.get_width()+10)
        self.rect.w = width
        if not self.active:
            Interactable.update(self, mouse_pos)
