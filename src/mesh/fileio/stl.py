
'''
Functions to read and write STL files.

See https://en.wikipedia.org/wiki/STL_%28file_format%29

read_stl(filename)
write_stl(mesh, filename)
'''

from mesh import *

STL_FORMAT_ASCII = 1
STL_FORMAT_BINARY = 2

class StlWriter(object):
    '''
    StlWriter

    Class to write STL files.
    '''

    def __init__(self, outputformat=STL_FORMAT_ASCII):
        self.outputformat = outputformat
    
    def write(self, m, name, filename):
        if self.outputformat == STL_FORMAT_ASCII:
            self.write_ascii(m, name, filename)
        elif self.outputformat == STL_FORMAT_BINARY:
            self.write_binary(m, name, filename)
        else:
            raise TypeError()

    def write_ascii(self, m, name, filename):
        with open(filename, 'wb') as fp:
            # write the header
            fp.write("solid %s\n" % (name))

            for f in m.faces:
                n = f.normal.normalise()
                v = f.vertices

                fp.write("facet normal %f %f %f\n" % (n[0], n[1], n[2]))
                fp.write("    outer loop\n")
                for i in range(3):
                    fp.write("        vertex %f %f %f\n" % (v[i][0], v[i][1], v[i][2]))
                fp.write("    endloop\n")
                fp.write("endfacet\n")

            # write the footer
            fp.write("endsolid %s\n" % (name))
    
    def write_binary(self, m, name, filename):
        raise NotImplementedError()


class StlReader(object):
    '''
    StlReader

    Class to read STL files.
    '''

    def __init__(self):
        pass

    def read(self, filename):
        with open(filename, 'rb') as fp:

            fileContent = fp.read()

            if len(fileContent) < 5:
                raise IOError("Not enough data")

            # read the header
            if fileContent[0:4] == "80sI":
                self.decode_binary(fileContent)
            elif fileContent[0:5] == "solid":
                self.decode_ascii(fileContent)
            else:
                raise IOError("Invalid STL file")

    def decode_ascii(self, data):
        #while i < len(data)
            # read a line
            
        raise NotImplementedError()

    def decode_binary(self, data):
        raise NotImplementedError()


def write_stl(m, filename, name="mesh"):
    '''
    Write a mesh to an STL file.
    '''
    StlWriter().write(m, name, filename)


def read_stl(filename):
    '''
    Read an STL file and create a mesh from it.
    '''
    return StlReader().read(filename)
