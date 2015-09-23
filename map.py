import heapq
from math import hypot


class Map(object):

    dr = [-1, -1, -1, 0, 0, 1, 1, 1]
    dc = [-1, 0, 1, -1, 1, -1, 0, 1]

    def __init__(self, width, height, start=None, end=None):
        self.width = width
        self.height = height
        self.data = [[True] * width for _ in xrange(height)]
        self.start = start
        self.end = end

    def __call__(self, row, col):
        return self.data[row][col]

    def set(self, row, col):
        self.data[row][col] = False

    def valid(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width and \
            self.data[row][col]

    def iter_adj(self, row, col):
        for ar, ac in zip(self.dr, self.dc):
            r = row + ar
            c = col + ac
            if self.valid(r, c):
                yield r, c, hypot(ar, ac)

    def heuristic(self, row, col):
        return hypot(row - self.end[0], col - self.end[1])

    def go(self):
        if not self.start or not self.end:
            return [], []
        edges = []
        parent = {}
        visited = set()
        heap = [(0, self.start)]
        dist = {self.start: 0}
        pos = None
        while heap:
            _, pos = heapq.heappop(heap)
            if pos in visited:
                continue
            visited.add(pos)
            if pos in parent:
                edges.append((parent[pos], pos))
            if pos == self.end:
                break
            for r, c, d in self.iter_adj(*pos):
                if (r, c) not in dist or dist[pos] + d < dist[(r, c)]:
                    dist[(r, c)] = dist[pos] + d
                    parent[(r, c)] = pos
                    heapq.heappush(heap,
                                   (dist[(r, c)] + self.heuristic(r, c),
                                    (r, c)))
        path = []
        if pos == self.end:
            while pos != self.start:
                path.append((parent[pos], pos))
                pos = parent[pos]
        path.reverse()
        return edges, path
