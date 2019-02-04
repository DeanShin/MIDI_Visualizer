class Button():
    def __init__(self,pygame,fontsize,x,y,w,h,ic,ac,text):
        font_btn = pygame.font.Font("resources/fonts/SoukouMincho.ttf", fontsize)
        self.text_btn = font_btn.render(text, True, (0,0,0))
        self.center = ((x+(w/2)-self.text_btn.get_width()/2), (y+(h/2)-self.text_btn.get_height()/2))
        self.rect = pygame.Rect(x,y,w,h)
        self.ic = ic
        self.ac = ac
        self.active = False
        self.text = text

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
        # Toggle the active variable.
            self.active = True
        else:
            self.active = False
        self.color = self.ac if self.active else self.ic

    def draw(self, pygame, window):
        if self.active:
            pygame.draw.rect(window, self.ac, self.rect)
        else:
            pygame.draw.rect(window, self.ic, self.rect)
        window.blit(self.text_btn, self.center)
