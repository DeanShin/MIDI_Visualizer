class Button():
    def __init__(self,pygame,text,fontsize,x,y,w,h,ic,ac,action):
        font_btn = pygame.font.Font("resources/fonts/SoukouMincho.ttf", fontsize)
        self.text_btn = font_btn.render(text, True, (0,0,0))
        self.center = ((x+(w/2)-self.text_btn.get_width()/2), (y+(h/2)-self.text_btn.get_height()/2))
        self.rect = pygame.Rect(x,y,w,h)
        self.ic = ic
        self.ac = ac
        self.active = False
        self.action = action

    def handle_event(self, pygame, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the button rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the button.
            self.color = self.ac if self.active else self.ic
        if event.type == pygame.MOUSEBUTTONUP:
            if self.action == 'e':
                #Exit Program
                return 1
            elif self.action == 's':
                #Start Visualization
                return 2
        else: 
            return 0

    def update(self):
        pass
        
    def draw(self, pygame, window):
        if self.active:
            pygame.draw.rect(window, self.ac, self.rect)
        else:
            pygame.draw.rect(window, self.ic, self.rect)
        window.blit(self.text_btn, self.center)
