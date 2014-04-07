"""Unit testing for the Vector class
"""

from __future__ import division

from unittest import TestCase, main

from math import pi, sin, sqrt

import mesh


class SizeTests(TestCase):

    def test_cube_closed(self):
        m = mesh.Mesh()
        mesh.primitives.add_cube(m, 100)
        self.assertTrue(m.closed())

    def test_cylinder_closed(self):
        m = mesh.Mesh()
        mesh.primitives.add_cylinder(m, 10, 100, 100)
        self.assertTrue(m.closed())

    def test_sphere_closed(self):
        m = mesh.Mesh()
        mesh.primitives.add_sphere(m, 1.0)
        self.assertTrue(m.closed())

    def test_something_not_closed(self):
        m = mesh.Mesh()
        v1 = m.add_vertex(0, 0, 0)
        v2 = m.add_vertex(10, 0, 0)
        v3 = m.add_vertex(0, 10, 0)
        m.add_face(v1, v2, v3)
        self.assertFalse(m.closed())

    def expected_cube_volume(self,l):
        return l**3

    def test_cube1_volume(self):
        m = mesh.Mesh()
        l = 100
        mesh.primitives.add_cube(m, l)
        self.assertAlmostEqual(m.volume(), self.expected_cube_volume(l))

    def test_cube1_volume(self):
        m = mesh.Mesh()
        l = 100
        o = [10, 20, 99]
        mesh.primitives.add_cube(m, l, o)
        self.assertAlmostEqual(m.volume(), self.expected_cube_volume(l))

    def expected_cylinder_volume(self,r,h,n):
        return 0.5*r*r*sin(2*pi/n)*n*h

    def test_cylinder_volume(self):
        m = mesh.Mesh()
        r,h,n = 10,100,100
        mesh.primitives.add_cylinder(m,r,h,n)
        self.assertAlmostEqual(m.volume(), self.expected_cylinder_volume(r,h,n))

    def test_cylinder2_volume(self):
        m = mesh.Mesh()
        r,h,n = 10,100,10000
        mesh.primitives.add_cylinder(m,r,h,n)
        self.assertAlmostEqual(m.volume(), self.expected_cylinder_volume(r,h,n))

    def expected_octahedron_volume(self,r):
        return 4/3 * r**3

    def test_octahedron_volume(self):
        m = mesh.Mesh()
        r = 1
        mesh.primitives.add_sphere(m, r, detail_level=1)
        self.assertAlmostEqual(m.volume(), self.expected_octahedron_volume(r))

    def test_sphere_volume(self):
        m = mesh.Mesh()
        mesh.primitives.add_sphere(m, 1.0, detail_level=2)
        # XXX: this should really be calculated
        volume = 2.942809041582063
        self.assertAlmostEqual(m.volume(), volume)

    def test_cube_centroids(self):
        m = mesh.Mesh()
        mesh.primitives.add_cube(m, 100)
        centroid0 = mesh.core.Vector(50.0,50.0,50.0)
        centroid1 = m.solid_centroid()
        centroid2 = m.surface_centroid()
        self.assertAlmostEqual(centroid1.x, centroid0.x)
        self.assertAlmostEqual(centroid1.y, centroid0.y)
        self.assertAlmostEqual(centroid1.z, centroid0.z)
        self.assertAlmostEqual(centroid2.x, centroid0.x)
        self.assertAlmostEqual(centroid2.y, centroid0.y)
        self.assertAlmostEqual(centroid2.z, centroid0.z)
  
    def test_cube_area(self):
        m = mesh.Mesh()
        mesh.primitives.add_cube(m, 100)
        area = 100.0*100.0*6
        self.assertAlmostEqual(m.surface_area(), area)

    def expected_cylinder_area(self,r,h,n):
        return r*r*sin(2*pi/n)*n + 2*r*sin(pi/n)*n*h

    def test_cylinder1_area(self):
        m = mesh.Mesh()
        r,h,n = 10,100,4
        mesh.primitives.add_cylinder(m, r, h, n)
        self.assertAlmostEqual(m.surface_area(), self.expected_cylinder_area(r,h,n))

    def test_cylinder2_area(self):
        m = mesh.Mesh()
        r,h,n = 10,100,100
        mesh.primitives.add_cylinder(m, r, h, n)
        self.assertAlmostEqual(m.surface_area(), self.expected_cylinder_area(r,h,n))

    def expected_octahedron_area(self,r):
        return 4*sqrt(3)*r**2

    def test_octahedron_area(self):
        m = mesh.Mesh()
        r = 1
        mesh.primitives.add_sphere(m, r, detail_level=1)
        self.assertAlmostEqual(m.surface_area(), self.expected_octahedron_area(r))


if __name__ == '__main__':
    main()

