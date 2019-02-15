from interactable import Interactable

class Button(Interactable):

    def __init__(self, pygame, fontsize, x, y, w, h, ic, hc, ac, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.Font("./resources/fonts/SoukouMincho.ttf", fontsize)
        self.text_surface = self.font.render(text, True, ic, (63,63,63))
        self.ac = ac
        self.hc = hc
        self.ic = ic
        self.color = ic

        self.thickness = 2
        self.text_pos = ((x+(w/2)-self.text_surface.get_width()/2), (y+(h/2)-self.text_surface.get_height()/2))
        self.active = False

    def handle_event(self, pygame, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.color = self.ac
                #Exit Program
                if self.text == 'Exit Program':
                    return 1
                #Start Program
                elif self.text == 'Start Program':
                    return 2
        return 0

    def update(self, mouse_pos):
        Interactable.update(self, mouse_pos)
