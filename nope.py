import bpy
import bmesh
import mathutils
from math import cos, sin, pi
import numpy as np

# Clear existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

def R_z(alpha):
    """Rotation matrix around Z-axis"""
    return [
        [cos(alpha), -sin(alpha), 0],
        [sin(alpha), cos(alpha), 0],
        [0, 0, 1]
    ]

def matrix_mult(m, v):
    """Matrix-vector multiplication"""
    return [
        m[0][0]*v[0] + m[0][1]*v[1] + m[0][2]*v[2],
        m[1][0]*v[0] + m[1][1]*v[1] + m[1][2]*v[2],
        m[2][0]*v[0] + m[2][1]*v[1] + m[2][2]*v[2]
    ]

# Constants from Maple code
C_1 = [152024884/259375205, 0, 210152163/259375205]
C_2 = [6632738028e-10, 6106948881e-10, 3980949609e-10]
C_3 = [8193990033e-10, 5298215096e-10, 1230614493e-10]

# Generate cyclic transformations
Cyc_30 = []
for k in range(15):
    for l in range(2):
        sign = (-1) ** l
        rotation = R_z(2 * pi * k / 15)
        # Apply sign to rotation matrix
        signed_rotation = [[sign * elem for elem in row] for row in rotation]
        Cyc_30.append(signed_rotation)

# Generate vertices
vertices = []
for M in Cyc_30:
    vertices.append(matrix_mult(M, C_1))
for M in Cyc_30:
    vertices.append(matrix_mult(M, C_2))
for M in Cyc_30:
    vertices.append(matrix_mult(M, C_3))

# Create mesh and object
mesh = bpy.data.meshes.new("Noperthedron")
obj = bpy.data.objects.new("Noperthedron", mesh)

# Link object to scene
bpy.context.collection.objects.link(obj)

# Create bmesh instance
bm = bmesh.new()

# Add vertices to bmesh
for v in vertices:
    bm.verts.new(v)

# Update bmesh geometry
bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()
bm.faces.ensure_lookup_table()

# Convert vertices to numpy for convex hull
verts_array = np.array(vertices)

# Create convex hull
bmesh.ops.convex_hull(bm, input=bm.verts)

# Update mesh
bm.to_mesh(mesh)
bm.free()

# Set object as active
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

print("Noperthedron created with", len(vertices), "vertices")