class Button():
    def __init__(self,pygame,text,fontsize,x,y,w,h,ic,ac,action):
        font_btn = pygame.font.Font("resources/fonts/SoukouMincho.ttf", fontsize)
        self.text_btn = font_btn.render(text, True, (0,0,0))
        self.center = ((x+(w/2)-self.text_btn.get_width()/2), (y+(h/2)-self.text_btn.get_height()/2))
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ic = ic
        self.ac = ac
        self.action = action

    def draw_active(self, pygame, window, active):
        if active:
            pygame.draw.rect(window, self.ac, (self.x,self.y,self.w,self.h))
        else:
            pygame.draw.rect(window, self.ic, (self.x,self.y,self.w,self.h))
        window.blit(self.text_btn, self.center)

    def do_something(self):
        if self.action == 'e':
            #Exit Program
            return 0
        elif self.action == 's':
            #Start Visualization
            return 1
        