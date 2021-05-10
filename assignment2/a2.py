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
import Rhino.Geometry as rg
import ghpythonlib.treehelpers as th
import math
import ghpythonlib.components as ghc

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
print type(d)

#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!

remapped_angles=[]
min_offset = minoff
max_offset = maxoff

for i in c:
    remapped = ( (i-min(c)) / ( max(c) - min(c))  ) * (max_offset - min_offset) + min_offset
    remapped_angles.append(remapped)

#1.move faces in relation to sun vector
moved_faces=[]
for i in range(len(d)):
    face=rg.Mesh.Duplicate(d[i])
    vector = s+rg.Vector3d(a[i])/200
    moved=rg.Mesh.Transform(face,rg.Transform.Translation(-vector/8)) #gives true/false
    moved_faces.append(face)
#2.scale faces in relation to angle value
#2.1 Get faces outlines
moved_outlines=[]
for i in moved_faces:
    FaceOutlines=rg.Mesh.GetNakedEdges(i)
    moved_outlines.append(FaceOutlines)
#2.2 Convert to curves and Join

joined_moved=[]
for i in range(len(moved_outlines)):
    curves=[]
    for j in range(len(moved_outlines[i])):
        #convert to nurbs curve
        curve=rg.Polyline.ToNurbsCurve(moved_outlines[i][j])
        curves.append(curve)
    joined_curves=rg.NurbsCurve.JoinCurves(curves)[0]
    joined_moved.append(joined_curves)
#2.3 Offset joined outlines

offset_outlines=[]
for i in range(len(joined_moved)):
    #convert mesh to surface
    face_points=rg.Mesh.Vertices.GetValue(moved_faces[i])
    surface=rg.NurbsSurface.CreateFromPoints([rg.Point3d(pt) for pt in face_points],2,2,2,2)#list_comprehension 
    offseted = rg.Curve.OffsetOnSurface(joined_moved[i],surface,remapped_angles[i],.001)[0]
    offset_outlines.append(offseted)
#########################
outlines=[]
for i in exploded:
    FaceOutlines=rg.Mesh.GetNakedEdges(i)
    outlines.append(FaceOutlines)
joined=[]
for i in range(len(outlines)):
    curves=[]
    for j in range(len(outlines[i])):
        #convert to nurbs curve
        curve=rg.Polyline.ToNurbsCurve(outlines[i][j])
        curves.append(curve)
    joined_curves=rg.NurbsCurve.JoinCurves(curves)[0]
    joined.append(joined_curves)

h = joined

#2.4 Loft 
panels_with_openings=[]
for i in range(len(offset_outlines)):
    curves_list=[offset_outlines[i],joined[i]]
    lofted=rg.Brep.CreateFromLoft(curves_list,rg.Point3d.Unset,rg.Point3d.Unset,rg.LoftType.Normal,False)[0]
    panels_with_openings.append(lofted)

g = panels_with_openings

move_point=[]
for i in b:
    point_move=[]
    newPt= i - s
    point_move.append(newPt)
    move_point.append(point_move)

e = th.list_to_tree(move_point)


#Move vertices of mesh in relation to the sun vector
V_mesh=m.Vertices


print(V_mesh)
print(type(V_mesh))
print(len(V_mesh))


AllVert=[]
for i in V_mesh:
    vertix=[]
    v= rg.Point3d(i)
    move_pt= v - s
    vertix.append(move_pt)
    AllVert.append(vertix)

f = th.list_to_tree(AllVert)

