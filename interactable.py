class Interactable:

    def update(self, (x, y)):
        if self.rect.collidepoint(x, y):
            mouse_hovering = True
        else:
            mouse_hovering = False
        self.color = self.hc if mouse_hovering else self.ic

    def draw(self, pygame, window):
        # Blit the rect.
        pygame.draw.rect(window, self.color, self.rect, self.thickness)
        # Blit the text.
        window.blit(self.text_surface, self.text_pos)

    def on_click():
        pass

    def on_entry():
        pass

    def on_exit():
        pass
