
#    Brachyprint -- 3D printing brachytherapy moulds
#    Copyright (C) 2013-14  James Cranch, Martin Green and Oliver Madge
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


'''
A 2D vertex class for the ``mesh'' package.
'''

from __future__ import division

from vector2d import Vector2d, nullVector2d

class Vertex2d(Vector2d):
    '''
    A class representing a polygon vertex.
    '''

    def __init__(self, x, y, name):
        super(Vertex2d, self).__init__(x, y)
        self.name = name
        self.lines = []

    def __repr__(self):
        return "Vertex2d(%f, %f, %d)"%(self.x, self.y, self.name)

    def __str__(self):
        return "<Vertex2d %d (%f,%f)>"%(self.name, self.x, self.y)

    def add_line(self, line):
        '''
        Associate a line with the vertex.
        '''
        self.lines.append(line)

    def remove_line(self, line):
        '''
        Remove a line from a vertex.
        '''
        self.lines.remove(line)

