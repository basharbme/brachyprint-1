#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import wx
from meshGUI import MainWindow
from settings import *
import mesh
from octrees import Octree
from points import expand, make_ply

class OnSelect:
  def __init__(self, mesh, base_file):
    self.mesh = mesh
    self.base_file = base_file
  def __call__(self, roiGUI, triangle):
    avoid_edges = []
    for roi in roiGUI.rois:
        paths = sum(roi.paths, [])
        edges = sum([path.get_edges() for path in paths], [])
        #Make list of edges to avoid.  Where there is a point in the middle of a triangle, an extra edge needs to be found.
        #such that a full ring of avoidance edges is created.
        #Find intial vertex
        if edges[-1].v1 in [edges[0].v1, edges[0].v2]:
            vertex = edges[-1].v1
        elif edges[-1].v2 in [edges[0].v1, edges[0].v2]:
            vertex = edges[-1].v2
        else:
            for extra_edge in edges[-1].v1.edges:
                if extra_edge.v1 == edges[-1].v1 and extra_edge.v2 in [edges[0].v1, edges[0].v2]:
                    avoid_edges.append(extra_edge)
                    vertex = extra_edge.v2
                    break
                if extra_edge.v2 == edges[-1].v1 and extra_edge.v1 in [edges[0].v1, edges[0].v2]:
                    avoid_edges.append(extra_edge)
                    vertex = extra_edge.v1
                    break
            for extra_edge in edges[-1].v2.edges:
                if extra_edge.v1 == edges[-1].v2 and extra_edge.v2 in [edges[0].v1, edges[0].v2]:
                    avoid_edges.append(extra_edge)
                    vertex = extra_edge.v2
                    break
                if extra_edge.v2 == edges[-1].v2 and extra_edge.v1 in [edges[0].v1, edges[0].v2]:
                    avoid_edges.append(extra_edge)
                    vertex = extra_edge.v1
                    break
        #Go around the loop of edges, adding them to the avoidance list, and adding extra edges where necessary.
        for i, edge in enumerate(edges):
            print i
            if edge.v1 == vertex:
                vertex = edge.v2
                avoid_edges.append(edge)
            elif edge.v2 == vertex:
                vertex = edge.v1
                avoid_edges.append(edge)
            else:
                for extra_edge in vertex.edges:
                    if extra_edge.v1 == vertex and extra_edge.v2 == edge.v1:
                        avoid_edges.append(extra_edge)
                        avoid_edges.append(edge)
                        vertex = edge.v2
                        break
                    elif extra_edge.v1 == vertex and extra_edge.v2 == edge.v2:
                        avoid_edges.append(extra_edge)
                        avoid_edges.append(edge)
                        vertex = edge.v1
                        break
                    elif extra_edge.v2 == vertex and extra_edge.v1 == edge.v1:
                        avoid_edges.append(extra_edge)
                        avoid_edges.append(edge)
                        vertex = edge.v2
                        break
                    elif extra_edge.v2 == vertex and extra_edge.v1 == edge.v2:
                        avoid_edges.append(extra_edge)
                        avoid_edges.append(edge)
                        vertex = edge.v1
                        break
                else:
                    assert False
                    avoid_edges.append(edge)
    for e in avoid_edges:
        print repr(e.v1), repr(e.v2)
    #Save the cut out mesh to a file
    roughcut = self.mesh.cloneSubVol(triangle, avoid_edges)
    print "Saving"
    mesh.fileio.write_ply(roughcut, self.base_file + "rough.ply")

    #Expand cut out mesh and save that to a file called external
    minx = min([v.x for v in roughcut.vertices]) - 0.01
    maxx = max([v.x for v in roughcut.vertices]) + 0.01
    miny = min([v.y for v in roughcut.vertices]) - 0.01
    maxy = max([v.y for v in roughcut.vertices]) + 0.01
    minz = min([v.z for v in roughcut.vertices]) - 0.01
    maxz = max([v.z for v in roughcut.vertices]) + 0.01
    points = Octree(((minx, maxx), (miny, maxy), (minz, maxz)))
    for v in roughcut.vertices:
        n = v.normal()
        points.insert((v.x, v.y, v.z), (n.x, n.y, n.z))
    external = expand(points, MOULD_THICKNESS)
    make_ply(external, self.base_file + "external", poisson_depth = POISSON_DEPTH)

if __name__ == '__main__':
    app = wx.App(False)
    #app = wx.PySimpleApp()        
    openFileDialog = wx.FileDialog(None, "Load", DEFAULT_OUTPUT_DIR, DEFAULT_OUTPUT_FILE, wildcard="*.skin.ply")
    openFileDialog.ShowModal()
    skin_file = openFileDialog.GetPath()
    openFileDialog.Destroy()
    base_filename = skin_file[:-8]

    ply_files = {"Skin": skin_file, "Bone": base_filename + "bone.ply"}

    meshes = {}
    for name, filename in ply_files.items():
        meshes[name] = mesh.fileio.read_ply(filename)

    frame = MainWindow(meshes=meshes, 
                       rois = {"Rough Cut": {"meshname": "Skin", "closed": True, "onSelect": OnSelect(meshes["Skin"], base_filename)}}, 
                       title = "Rough Cut")
    app.MainLoop()
    del frame
    del app

