#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

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

import wx
from meshGUI import MainWindow
from settings import *
import mesh

if __name__ == '__main__':
    app = wx.App(False)

    m1 = mesh.Mesh()
    mesh.primitives.add_cuboid(m1, lx=60, ly=60, lz=10,
               nx=12, ny=6, nz=2,)
 
    m2 = mesh.Mesh()
    mesh.primitives.add_cylinder(m2, 2.6, 80, 10, v_axis=[0,1,0], basepoint=[5, -10, 0], n_height = 10)
    mesh.primitives.add_cylinder(m2, 2.8, 80, 10, v_axis=[0,1,0], basepoint=[15, -10, 0], n_height = 10)
    mesh.primitives.add_cylinder(m2, 3, 80, 10, v_axis=[0,1,0], basepoint=[30, -10, 0], n_height = 10)
    mesh.primitives.add_cylinder(m2, 3.2, 80, 10, v_axis=[0,1,0], basepoint=[45, -10, 0], n_height = 10)
    mesh.primitives.add_cylinder(m2, 3.4, 80, 10, v_axis=[0,1,0], basepoint=[55, -10, 0], n_height = 10)

    m3, m4 = mesh.manipulate.split(m1, m2)

    meshes = {"base": m1, "catheter": m2, "sample": m3, "opp": m4}

    frame = MainWindow(meshes = meshes,
                       rois = {},
                       title = "Sample")
    app.MainLoop()
    del frame
    del app

