import pygame


class Main(object):

    cell_width = 8
    wall_color = (0, 0, 0)
    start_color = (50, 100, 240)
    end_color = (240, 30, 0)
    edge_color = (100, 120, 255)
    path_color = (30, 240, 60)
    background_color = (255, 255, 255)

    def __init__(self, _map):
        self.map = _map
        pygame.init()
        self.screen = pygame.display.set_mode((
            self.map.width * self.cell_width, self.map.height * self.cell_width))
        pygame.display.set_caption('A*')
        self.update()

    def get_rectangle(self, row, col):
        return (col * self.cell_width,
                row * self.cell_width,
                self.cell_width,
                self.cell_width),

    def get_center(self, row, col):
        return (col * self.cell_width + self.cell_width / 2,
                row * self.cell_width + self.cell_width / 2)

    def get_row_col(self, pos):
        return pos[1] / self.cell_width, pos[0] / self.cell_width

    def update(self):
        self.screen.fill(self.background_color)
        for row in xrange(self.map.height):
            for col in xrange(self.map.width):
                if not self.map(row, col):
                    pygame.draw.rect(self.screen,
                                     self.wall_color,
                                     self.get_rectangle(row, col))
        if self.map.start:
            pygame.draw.rect(self.screen,
                             self.start_color,
                             self.get_rectangle(*self.map.start))
        if self.map.end:
            pygame.draw.rect(self.screen,
                             self.end_color,
                             self.get_rectangle(*self.map.end))

        if self.map.start and self.map.end:
            edges_used, path = self.map.go()
            for edge in edges_used:
                pygame.draw.line(self.screen, self.edge_color,
                                 self.get_center(*edge[0]),
                                 self.get_center(*edge[1]))
            for edge in path:
                pygame.draw.line(self.screen, self.path_color,
                                 self.get_center(*edge[0]),
                                 self.get_center(*edge[1]), 2)

        pygame.display.flip()

    def run(self):
        pressing = False
        prev_pos = None
        start = None
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pressing = True
                pos = self.get_row_col(event.pos)
                self.map.set(*pos)
                self.update()
                prev_pos = pos
            elif pressing and event.type == pygame.MOUSEMOTION:
                pos = self.get_row_col(event.pos)
                if pos != prev_pos:
                    self.map.set(*pos)
                    self.update()
                    prev_pos = pos
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pressing = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if start is None:
                    start = self.get_row_col(event.pos)
                    self.map.start = start
                    self.map.end = None
                else:
                    end = self.get_row_col(event.pos)
                    if end == start:
                        self.map.start = None
                    else:
                        self.map.end = end
                    start = None
                self.update()
