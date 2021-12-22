#!/usr/bin/env python

# Author: Kwasi Mensah (kmensah@andrew.cmu.edu)
# Date: 8/02/2005
#
# This is meant to be a simple example of how to draw a cube
# using Panda's new Geom Interface. Quads arent directly supported
# since they get broken down to trianlges anyway.
#

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import lookAt
from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import PerspectiveLens, OrthographicLens
from panda3d.core import CardMaker
from panda3d.core import Light, Spotlight
from panda3d.core import TextNode
from panda3d.core import LVector3
import sys
import os
import time


base = ShowBase()
base.disableMouse()
base.camera.setPos(0, -100, 0)

title = OnscreenText(text="Panda3D: Tutorial - Making a Cube Procedurally",
                     style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07,
                     parent=base.a2dBottomRight, align=TextNode.ARight)
escapeEvent = OnscreenText(text="1: Set a Texture onto the Cube",
                           style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.08),
                           align=TextNode.ALeft, scale=.05,
                           parent=base.a2dTopLeft)
spaceEvent = OnscreenText(text="2: Toggle Light from the front On/Off",
                          style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.14),
                          align=TextNode.ALeft, scale=.05,
                          parent=base.a2dTopLeft)
upDownEvent = OnscreenText(text="3: Toggle Light from on top On/Off",
                           style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.20),
                           align=TextNode.ALeft, scale=.05,
                           parent=base.a2dTopLeft)


# You can't normalize inline so this is a helper function
def normalized(*args):
    myVec = LVector3(*args)
    myVec.normalize()
    return myVec

# helper function to make a square given the Lower-Left-Hand and
# Upper-Right-Hand corners

def makeSquare(x1, y1, z1, x2, y2, z2):
    format = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('square', format, Geom.UHDynamic)

    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    texcoord = GeomVertexWriter(vdata, 'texcoord')

    # make sure we draw the sqaure in the right plane
    if x1 != x2:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y1, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y2, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y2 - 1, 2 * z2 - 1))

    else:
        vertex.addData3(x1, y1, z1)
        vertex.addData3(x2, y2, z1)
        vertex.addData3(x2, y2, z2)
        vertex.addData3(x1, y1, z2)

        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z1 - 1))
        normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
        normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z2 - 1))

    # adding different colors to the vertex for visibility
    color.addData4f(1.0, 0.0, 0.0, 1.0)
    color.addData4f(0.0, 1.0, 0.0, 1.0)
    color.addData4f(0.0, 0.0, 1.0, 1.0)
    color.addData4f(1.0, 0.0, 1.0, 1.0)

    texcoord.addData2f(0.0, 1.0)
    texcoord.addData2f(0.0, 0.0)
    texcoord.addData2f(1.0, 0.0)
    texcoord.addData2f(1.0, 1.0)

    # Quads aren't directly supported by the Geom interface
    # you might be interested in the CardMaker class if you are
    # interested in rectangle though
    tris = GeomTriangles(Geom.UHDynamic)
    tris.addVertices(0, 1, 3)
    tris.addVertices(1, 2, 3)

    square = Geom(vdata)
    square.addPrimitive(tris)
    return square

def makeTriangle(x1, y1, z1, x2, y2, z2, x3, y3, z3,s):
    x1, y1, z1, x2, y2, z2, x3, y3, z3 = [s*k for k in [x1, y1, z1, x2, y2, z2, x3, y3, z3]]
    format = GeomVertexFormat.getV3n3cpt2()
    vdata = GeomVertexData('square', format, Geom.UHDynamic)

    vertex = GeomVertexWriter(vdata, 'vertex')
    normal = GeomVertexWriter(vdata, 'normal')
    color = GeomVertexWriter(vdata, 'color')
    texcoord = GeomVertexWriter(vdata, 'texcoord')


    vertex.addData3(x1, y1, z1)
    vertex.addData3(x2, y2, z2)
    vertex.addData3(x3, y3, z3)

    normal.addData3(normalized(2 * x1 - 1, 2 * y1 - 1, 2 * z1 - 1))
    normal.addData3(normalized(2 * x2 - 1, 2 * y2 - 1, 2 * z2 - 1))
    normal.addData3(normalized(2 * x3 - 1, 2 * y3 - 1, 2 * z3 - 1))


    # adding different colors to the vertex for visibility
    color.addData4f(0.9, 0.9, 1.0, 0.0)
    color.addData4f(0.7, 0.7, 1.0, 0.0)
    color.addData4f(0.7, 0.7, 1.0, 0.0)

    texcoord.addData2f(0.0, 1.0)
    texcoord.addData2f(0.0, 0.0)
    texcoord.addData2f(1.0, 0.0)

    # Quads aren't directly supported by the Geom interface
    # you might be interested in the CardMaker class if you are
    # interested in rectangle though
    tris = GeomTriangles(Geom.UHDynamic)
    tris.addVertices(0, 1, 2)

    tri = Geom(vdata)
    tri.addPrimitive(tris)
    return tri

# Note: it isn't particularly efficient to make every face as a separate Geom.
# instead, it would be better to create one Geom holding all of the faces.
ss = 4
tri0 = makeTriangle(-1,0,0,1,0.1,0,1,0,-0.5,ss)
tri1 = makeTriangle(-1,0,0,1,0.1,0,1,0.5,0,ss)
tri2 = makeTriangle(-1,0,0,1,-0.1,0,1,0,-0.5,ss)
tri3 = makeTriangle(-1,0,0,1,-0.1,0,1,-0.5,0,ss)

snode = GeomNode('square')
snode.addGeom(tri0)
snode.addGeom(tri1)
snode.addGeom(tri2)
snode.addGeom(tri3)

avi = render.attachNewNode(snode)
#cube.hprInterval(1.5, (360, 360, 360)).loop()

# OpenGl by default only draws "front faces" (polygons whose vertices are
# specified CCW).
avi.setTwoSided(True)


class MyTapper(DirectObject):

    def __init__(self):
        self.testTexture = loader.loadTexture("maps/envir-reeds.png")
        self.accept("1", self.toggleTex)
        self.accept("2", self.toggleLightsSide)
        self.accept("3", self.toggleLightsUp)

        self.LightsOn = False
        self.LightsOn1 = False
        slight = Spotlight('slight')
        slight.setColor((1, 1, 1, 1))
        lens = OrthographicLens()
        slight.setLens(lens)
        self.slnp = render.attachNewNode(slight)
        self.slnp1 = render.attachNewNode(slight)

    def toggleTex(self):
        global avi
        if avi.hasTexture():
            avi.setTextureOff(1)
        else:
            avi.setTexture(self.testTexture)

    def toggleLightsSide(self):
        global avi
        self.LightsOn = not self.LightsOn

        if self.LightsOn:
            render.setLight(self.slnp)
            self.slnp.setPos(avi, 100, 400, 0)
            self.slnp.lookAt(100, 0, 0)
        else:
            render.setLightOff(self.slnp)

    def toggleLightsUp(self):
        global avi
        self.LightsOn1 = not self.LightsOn1

        if self.LightsOn1:
            render.setLight(self.slnp1)
            self.slnp1.setPos(avi, 10, 0, 400)
            self.slnp1.lookAt(10, 0, 0)
        else:
            render.setLightOff(self.slnp1)

t = MyTapper()
start = time.perf_counter()
fps = 15
p = 1
while True:
    tm = time.perf_counter() - start
    if tm >= 1/fps: 
        p +=10
        avi.setHpr(p,p,0)
        taskMgr.step()
        start = time.perf_counter()
