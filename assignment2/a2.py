#Assignment 2
#Nawapan Suntorachai
#MaCAD AIA_Geometry_Optimization // Synchronous

"""Provides a scripting component.
    Inputs:
        m: a mesh
        s: sun vector
    Output:
        a: List of Vectors
        b: List of Points
        c: list of angles
        d: exploded mesh
        """
        
import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th

#1.
#compute face normals using rg.Mesh.FaceNormals.ComputeFaceNormals()
#output the vectors to a

#a = faceNormals
a = []
num_face =  len(m.Faces)
for i in range(num_face):
    norm = m.FaceNormals[i]
    renorm = rg.Vector3d.Negate(norm)
    a.append(renorm)

print type(a)

#2.
#get the centers of each faces using rg.Mesh.Faces.GetFaceCenter()
#store the centers into a list called centers 
#output that list to b

#b = centers
b = []
for i in range(num_face):
    fc = m.Faces.GetFaceCenter(i)
    b.append(fc)

#3.
#calculate the angle between the sun and each FaceNormal using rg.Vector3d.VectorAngle()
#store the angles in a list called angleList and output it to c

#c = angleList
c = []
for i in range(num_face):
    ang = rg.Vector3d.VectorAngle(a[i],s)
    c.append(ang)


#4. explode the mesh - convert each face of the mesh into a mesh
#for this, you have to first copy the mesh using rg.Mesh.Duplicate()
#then iterate through each face of the copy, extract it using rg.Mesh.ExtractFaces
#and store the result into a list called exploded in output d

#d = exploded
exploded = []
num_new = len(rg.Mesh.Duplicate(m).Faces)
m_new = m.Duplicate()
for i in range(num_new):
    face_mesh = m_new.Faces.ExtractFaces([0])
    exploded.append(face_mesh)

d = exploded
#e = m_new
f = num_new

#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!

"""
Bonus tasks include:
- Propose a different mesh to analyse
- Provide a frame for the resulting mesh by moving edges according to the rg.Mesh.VertexNormals
"""
"""
e = []
for i in range(num_new):
    list_edge = []
    for l in d:
        edge = l.GetNakedEdges()
        list_edge.append(edge)
    e.append(list_edge[i])

g = th.list_to_tree(e)

"""