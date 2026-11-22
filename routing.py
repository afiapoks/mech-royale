"""Small walking grid: A* searches around solid map footprints."""
import heapq
import json
import math
from pathlib import Path
from time import perf_counter


def inside(x, y, ring):
    hit = False
    points = list(zip(ring[::2], ring[1::2]))
    for (ax, ay), (bx, by) in zip(points, points[1:] + points[:1]):
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax:
            hit = not hit
    return hit


def near_edge(x, y, ring, margin):
    points = list(zip(ring[::2], ring[1::2]))
    for (ax, ay), (bx, by) in zip(points, points[1:] + points[:1]):
        dx, dy = bx - ax, by - ay
        t = max(0, min(1, ((x-ax)*dx + (y-ay)*dy) / max(dx*dx+dy*dy, 1e-9)))
        if math.hypot(x-ax-t*dx, y-ay-t*dy) < margin:
            return True
    return False


class Router:
    step = 8.0

    def __init__(self, world):
        self.bounds = world['bounds']
        b = self.bounds
        self.nx = int((b['maxX']-b['minX'])/self.step)+1
        self.ny = int((b['maxY']-b['minY'])/self.step)+1
        self.blocked = set()
        # Bridges can be walked under; ignore them here. Low bridges remain a limitation.
        for p in world['prisms']:
            if p['kind'] == 'bridge':
                continue
            r = p['ring']
            lo = self.cell((min(r[::2])-5, min(r[1::2])-5))
            hi = self.cell((max(r[::2])+5, max(r[1::2])+5))
            for i in range(lo[0], hi[0]+1):
                for j in range(lo[1], hi[1]+1):
                    x, y = self.point((i,j))
                    solid = inside(x,y,r) and not any(inside(x,y,h) for h in p.get('holes',[]))
                    if solid or near_edge(x,y,r,5):
                        self.blocked.add((i,j))
        self.path = []
        self.last_tick = -1000
        self.last_goal = None

    @classmethod
    def load(cls, directory):
        try:
            return cls(json.loads((Path(directory)/'v2/world.json').read_text()))
        except (OSError, ValueError, KeyError):
            return None

    def cell(self, pos):
        return (max(0,min(self.nx-1,round((pos[0]-self.bounds['minX'])/self.step))),
                max(0,min(self.ny-1,round((pos[1]-self.bounds['minY'])/self.step))))

    def point(self, cell):
        return (self.bounds['minX']+cell[0]*self.step,self.bounds['minY']+cell[1]*self.step)

    def free(self, cell):
        return 0 <= cell[0] < self.nx and 0 <= cell[1] < self.ny and cell not in self.blocked

    def nearest(self, cell):
        if self.free(cell):
            return cell
        for radius in range(1,16):
            choices = [(cell[0]+dx,cell[1]+dy) for dx in range(-radius,radius+1)
                       for dy in range(-radius,radius+1) if max(abs(dx),abs(dy))==radius]
            choices = [c for c in choices if self.free(c)]
            if choices:
                return min(choices,key=lambda c:math.dist(c,cell))
        return None

    def search(self, start, goal, zone):
        start, goal = self.nearest(self.cell(start)), self.nearest(self.cell(goal))
        if start is None or goal is None:
            return []
        queue = [(math.dist(start,goal),0,start)]
        costs = {start:0}
        parents = {}
        visited = 0
        deadline = perf_counter() + 0.008
        best = start
        while queue and visited < 2000:
            _, cost, cell = heapq.heappop(queue)
            if cost != costs[cell]:
                continue
            visited += 1
            if math.dist(cell,goal) < math.dist(best,goal):
                best = cell
            if cell == goal or (visited % 32 == 0 and perf_counter() >= deadline):
                if cell != goal:
                    cell = best
                path = [cell]
                while cell in parents:
                    cell = parents[cell]
                    path.append(cell)
                return [self.point(c) for c in reversed(path)]
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                nxt = (cell[0]+dx,cell[1]+dy)
                if not self.free(nxt):
                    continue
                # A diagonal must not squeeze between two blocked corners.
                if dx and dy and (not self.free((cell[0]+dx,cell[1])) or not self.free((cell[0],cell[1]+dy))):
                    continue
                penalty = 5 if math.dist(self.point(nxt),zone['center']) > zone['radius']-8 else 0
                new = cost+math.hypot(dx,dy)+penalty
                if new < costs.get(nxt,float('inf')):
                    costs[nxt], parents[nxt] = new, cell
                    heapq.heappush(queue,(new+math.dist(nxt,goal),new,nxt))
        if best != start:
            path = [best]
            while best in parents:
                best = parents[best]
                path.append(best)
            return [self.point(c) for c in reversed(path)]
        return []

    def waypoint(self, pos, goal, zone, tick):
        if not self.path or tick-self.last_tick >= 30 or (self.last_goal is None or math.dist(self.last_goal,goal)>8):
            self.path = self.search(pos,goal,zone)
            self.last_tick, self.last_goal = tick, tuple(goal)
        while len(self.path)>1 and math.dist(pos[:2],self.path[0]) < 7:
            self.path.pop(0)
        return self.path[0] if self.path else goal
