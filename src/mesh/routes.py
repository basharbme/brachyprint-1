class point_to_point:
    def __init__(self, s, e, endPoint = None, endFace = None):
        self.s, self.e = s,e 
    def points(self):
        return [((self.s[0], self.s[1], self.s[2]), (self.e[0], self.e[1], self.e[2]))]
    def get_edges(self):
        return []

class point_to_vertex:
    def __init__(self, sx, sy, sz, e, endPoint = None, endFace = None):
        self.sx, self.sy, self.sz, self.e = sx, sy, sz, e
        self.endPoint, self.endFace = endPoint, endFace
    def dist(self):
        return ((self.sx - self.e.x) ** 2 + (self.sy - self.e.y) ** 2 + (self.sz - self.e.z) ** 2) ** 0.5
    def crowdist(self):
        return ((self.e.x - self.endPoint[0]) ** 2 + (self.e.y - self.endPoint[1]) ** 2 + (self.e.z - self.endPoint[2]) ** 2) ** 0.5
    def end(self):
        return self.e
    def points(self):
        return [((self.sx, self.sy, self.sz), (self.e.x, self.e.y, self.e.z))]
    def new_Paths(self):
        results = [follow_edge(self.e, v, self.endPoint, self.endFace, edge) for v, edge in self.e.adjacent_vertices()] 
        if self.endPoint is not None and self.endFace in self.e.faces:
            results += [vertex_to_point(self.e, self.endPoint)]
        return results
    def finished(self):
        return False
    def get_edges(self):
        return []
    #def __str__(self):
     

class follow_edge:
    def __init__(self, s, e, endPoint = None, endFace = None, edge = None):
        self.s, self.e = s, e
        self.endPoint, self.endFace = endPoint, endFace
        self.edge = edge
    def dist(self):
        return ((self.s.x - self.e.x) ** 2 + (self.s.y - self.e.y) ** 2 + (self.s.z - self.e.z) ** 2) ** 0.5
    def end(self):
        return self.e
    def points(self):
        return [((self.s.x, self.s.y, self.s.z), (self.e.x, self.e.y, self.e.z))]
    def new_Paths(self):
        results =  [follow_edge(self.e, v, self.endPoint, self.endFace, edge) for v, edge in self.e.adjacent_vertices()] 
        if self.endPoint is not None and self.endFace in self.e.faces:
            results += [vertex_to_point(self.e, self.endPoint)]
        return results
    def finished(self):
        return False
    def crowdist(self):
        return ((self.e.x - self.endPoint[0]) ** 2 + (self.e.y - self.endPoint[1]) ** 2 + (self.e.z - self.endPoint[2]) ** 2) ** 0.5
    def get_edges(self):
        return [self.edge]

class vertex_to_point:
    def __init__(self, s, (ex, ey, ez)):
        self.s, self.ex, self.ey, self.ez = s, ex, ey, ez
    def dist(self):
        return ((self.s.x - self.ex) ** 2 + (self.s.y - self.ey) ** 2 + (self.s.z - self.ez) ** 2) ** 0.5
    def finished(self):
        return True
    def points(self):
        return [((self.s.x, self.s.y, self.s.z), (self.ex, self.ey, self.ez))]
    def end(self):
        return "Finished!!!"
    def get_edges(self):
        return []