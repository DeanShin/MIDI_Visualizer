class Button():

    def __init__(self, pygame, fontsize, x, y, w, h, ic, ac, text=''):
        btn_font = pygame.font.Font("resources/fonts/SoukouMincho.ttf", fontsize)
        self.btn_text = btn_font.render(text, True, (0,0,0))
        self.center = ((x+(w/2)-self.btn_text.get_width()/2), (y+(h/2)-self.btn_text.get_height()/2))
        self.rect = pygame.Rect(x,y,w,h)
        self.ic = ic
        self.ac = ac
        self.col_with_mouse = False
        self.text = text
        self.color = ic

    def handle_event(self, pygame, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.text == 'Exit Program':
                #Exit Program
                    return 1
                elif self.text == 'Start Program':
                #Start Visualization
                    return 2
        return 0

    def update(self, pygame, (x, y)):
        if self.rect.collidepoint(x, y):
        # Toggle the col_with_mouse variable.
            self.col_with_mouse = True
        else:
            self.col_with_mouse = False
        self.color = self.ac if self.col_with_mouse else self.ic

    def draw(self, pygame, window):
        pygame.draw.rect(window, self.color, self.rect, 0)
        window.blit(self.btn_text, self.center)
