import bpy
import mathutils
import bmesh
import math

def get_loop_distance(obj):
    selected_vertices = [v.co for v in obj.data.vertices if v.select]
    center = mathutils.Vector((0, 0, 0))
    for vertex in selected_vertices:
        center += vertex
    center /= len(selected_vertices)
    return center

def vertex_distance(co_v1, co_v2):
    return math.sqrt((co_v1[0] - co_v2.x) ** 2 + (co_v1[1] - co_v2.y) ** 2
                     + (co_v1[2] - co_v2.z) ** 2)

def inset_by_distance(obj, distance):
    loop = [v.co for v in obj.data.vertices if v.select]
    middle_of_loop = get_loop_distance(obj)
    vertex = loop[0]
    radius = vertex_distance(middle_of_loop, vertex)
    new_radius = radius - distance
    loop_ratio = new_radius/radius
    # Extrude the selected geometry
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, 0)})  # Extrude in Z-axis by 1 unit
    # Now, scale the extruded geometry
    bpy.ops.transform.resize(value=(loop_ratio, loop_ratio, loop_ratio))  # Scale by a factor of 2 in X and Y axes, no scale in Z

    # Update the mesh with the changes
    obj.data.update()


#START
DISTANCE = 0.1
obj = bpy.context.view_layer.objects.active
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.mode_set(mode='EDIT')
inset_by_distance(obj, DISTANCE)
