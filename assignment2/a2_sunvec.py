import Rhino.Geometry as rg
import rhinoscriptsyntax as rs
import math

#create a sun vector

#1. create a Sphere at point (0,0,0) with radius 1 and output it to a
#output the sphere to a

#a = sphere

center = rg.Point3d(0, 0, 0)
print center
a = rg.Sphere(center, 1)

# How can I coerce the Sphere to Surface
# a = rg.coerceSurface(a) not working
# a = rg.Surface.SetDomain(a, 0, rg.Interval(0,1))


#2. evaluate a point in the sphere using rg.Sphere.PointAt() at coordintes x and y
#the point should only be on the upper half of the sphere (upper hemisphere)
#the angles are in radians, so you might want to use math.pi for this
#output the point to b

#b = point on the sphere

b = rg.Sphere.PointAt(a, x, y)

print b
print type(b)


#create a vector from the origin  and reverse the vector
#keep in mind that Reverse affects the original vector
#output the vector to c


#c = vector



c = rs.CreateVector(b)
c = rg.Vector3d.Negate(c)
print c
print type(c)
