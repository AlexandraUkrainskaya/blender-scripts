import bpy
import math
import mathutils

def get_location_origin(obj):
    return obj.matrix_world.to_translation()


def get_face_location(face, obj):
    centroid = sum((obj.data.vertices[v].co for v in face.vertices), mathutils.Vector((0, 0, 0))) / len(face.vertices)
    return centroid


def update_selection(obj):
    # Switch to Object Mode to refresh the context
    bpy.ops.object.mode_set(mode='OBJECT')

    # Now switch back to Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')


def calculate_edit(obj):
    update_selection(obj)
    selected_faces = [face for face in obj.data.polygons if face.select]
    selected_faces_count = len(selected_faces)
    selected_edges = [edge for edge in obj.data.edges if edge.select]
    selected_edge_count = len(selected_edges)
    selected_vertices = [v for v in obj.data.vertices if v.select]
    selected_vertex_count = len(selected_vertices)
    location_one, location_two = None, None
    if selected_faces_count == 2:
        location_one = get_face_location(selected_faces[0], obj)
        location_two = get_face_location(selected_faces[1], obj)
    elif selected_edge_count == 2:
        location_one = get_face_location(selected_edges[0], obj)
        location_two = get_face_location(selected_edges[1], obj)
    elif selected_vertex_count == 2:
        location_one = selected_vertices[0].co
        location_two = selected_vertices[1].co
    return location_one, location_two


def make_text(y_len, x_len, z_len, x_y_len, x_z_len, y_z_len, total_len):
    return f"y: {y_len}\nx: {x_len}\nz:{z_len}\nxy len: {x_y_len}\nxz len: {x_z_len}\nyz len: {y_z_len}\ntotal len: {total_len}"

box_message = ""
# test call to the

active_object = bpy.context.active_object
if active_object:
    mode = active_object.mode
    location_one, location_two = None, None
    y_len, x_len, z_len, x_y_len, x_z_len, y_z_len, total_len = -1, -1, -1, -1, -1, -1, -1
    if mode == 'EDIT':
        returns = calculate_edit(active_object)
        location_one = returns[0]
        location_two = returns[1]

    elif mode == 'OBJECT':
        selected_objects_count = len([obj for obj in bpy.context.selected_objects])
        if selected_objects_count == 2:
            object_one = bpy.context.selected_objects[0]
            object_two = bpy.context.selected_objects[1]
            location_one = get_location_origin(object_one)
            location_two = get_location_origin(object_two)
        else:
            location_one = None
            location_two = None
    if location_one is not None and location_two is not None:
        y_len = abs(location_one.y - location_two.y)
        x_len = abs(location_one.x - location_two.x)
        z_len = abs(location_one.z - location_two.z)
        x_y_len = math.sqrt((location_one.x - location_two.x) ** 2
                   + (location_one.y - location_two.y) ** 2)
        x_z_len = math.sqrt((location_one.x - location_two.x) ** 2
                   + (location_one.z - location_two.z) ** 2)
        y_z_len = math.sqrt((location_one.z - location_two.z) ** 2
                   + (location_one.y - location_two.y) ** 2)
        total_len = math.sqrt((location_one.x - location_two.x) ** 2
                     + (location_one.y - location_two.y) ** 2
                     + (location_one.z - location_two.z) ** 2)
    print("location:", location_one, location_two)
    box_message = make_text(y_len, x_len, z_len, x_y_len, x_z_len, y_z_len, total_len)
    print(box_message)
