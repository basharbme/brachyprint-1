
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
A 3D vector class for the ``mesh'' package.
'''

from __future__ import division
from math import sqrt
from numbers import Number
from random import random

from vector2d import Vector2d

from mesh_settings import epsilon

class Vector(object):
    '''
    Class representing a vector.
    '''

    def __init__(self, x, y=None, z=None):
        if isinstance(x, tuple) or isinstance(x, list) or isinstance(x, Vector):
            y = x[1]
            z = x[2]
            x = x[0]
    
        self.x, self.y, self.z = float(x), float(y), float(z)
        self.epsilon = epsilon

    def __hash__(self):
        return hash((Vector,self.x,self.y,self.z))

    def __eq__(self, v):
        return abs(self.x - v[0]) <= self.epsilon and abs(self.y - v[1]) <= self.epsilon and abs(self.z - v[2]) <= self.epsilon

    def __ne__(self, v):
        return not self.__eq__(v)

    def __gt__(self, v):
        raise TypeError("Ambiguous meaning for a Vector")

    def __lt__(self, v):
        raise TypeError("Ambiguous meaning for a Vector")

    def __lshift__(self, other):
        raise TypeError("Vector is not a binary type")

    def __rshift__(self, other):
        raise TypeError("Vector is not a binary type")

    def __and__(self, other):
        raise TypeError("Vector is not a binary type")

    def __xor__(self, other):
        raise TypeError("Vector is not a binary type")

    def __or__(self, other):
        raise TypeError("Vector is not a binary type")

    def __add__(self, v):
        try:
            return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
        except AttributeError:
            raise TypeError

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __sub__(self, v):
        try:
            return Vector(self.x - v.x, self.y - v.y, self.z - v.z)
        except AttributeError:
            raise TypeError
        
    def __mul__(self, val):
        if isinstance(val,Number):
            return Vector(self.x*val, self.y*val, self.z*val)
        else:
            raise TypeError

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, val):
        if isinstance(val,Number):
            return Vector(self.x/val, self.y/val, self.z/val)
        else:
            raise TypeError

    def __truediv__(self, val):
        if isinstance(val,Number):
            return Vector(self.x/val, self.y/val, self.z/val)
        else:
            raise TypeError

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __iadd__(self, v):
        try:
            self.x += v.x
            self.y += v.y
            self.z += v.z
            return self
        except AttributeError:
            raise TypeError
        
    def __isub__(self, v):
        try:
            self.x -= v.x
            self.y -= v.y
            self.z -= v.z
            return self
        except AttributeError:
            raise TypeError

    def __imul__(self, val):
        if isinstance(val,Number):
            self.x *= val
            self.y *= val
            self.z *= val
            return self
        else:
            raise TypeError

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        else:
            raise IndexError

    def __len__(self):
        return 3

    def __repr__(self):
        return "Vector(%f, %f, %f)"%(self.x, self.y, self.z)

    def __str__(self):
        return "Vector(%f, %f, %f)"%(self.x, self.y, self.z)

    def parallel(self, other, tolerance=0.000001):
        return self.cross(other).magnitude() < tolerance

    def cross(self, v):
        try:
            return Vector(self.y * v.z - self.z * v.y,
                          self.z * v.x - self.x * v.z,
                          self.x * v.y - self.y * v.x)
        except AttributeError:
            raise TypeError

    def dot(self, v):
        try:
            return float(self.x * v.x + self.y * v.y + self.z * v.z)
        except AttributeError:
            raise TypeError

    def magnitude(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def distance(self,other):
	return (self-other).magnitude()

    def normalise(self):
        m = self.magnitude()
        if m == 0.0:
            return Vector(self.x, self.y, self.z)
        else:
            return Vector(self.x/m, self.y/m, self.z/m)

    def project2d(self, u, v):
        '''
        Project the vector into 2d using the basis vectors 'u' and 'v'.
        '''
        return [self.dot(u), self.dot(v)]

    def get_orthogonal_vectors(self):
        '''
        Returns two orthogonal vectors
        '''
        a = self.normalise()
        for bv in basisVectors:
            p = a.cross(bv)
            if p.magnitude() > 0.1:
                p = p.normalise()
                return p, a.cross(p)

    def project2dvector(self, u, v):
        '''
        Project the vector into 2d using the basis vectors 'u' and 'v'.
        '''
        return Vector2d(self.dot(u), self.dot(v))


basisVectors = [Vector(0,0,1), Vector(0,1,0), Vector(1,0,0)]
nullVector = Vector(0, 0, 0)


def random_unit_vector():
    """A random vector of unit length, uniformly distributed around the
    sphere.
    """
    while True:
        x = random() - 0.5
        y = random() - 0.5
        z = random() - 0.5
        v = Vector(x, y, z)
        if v.magnitude() > 0.01:
            return v.normalise()
