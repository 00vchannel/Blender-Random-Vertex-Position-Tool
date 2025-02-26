bl_info = {
    "name": "Random Vertex Position",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Sidebar > Random Vertex",
    "description": "Randomize position of selected vertices with sliders",
    "category": "Mesh",
}

import bpy
import random
from bpy.props import FloatProperty

class MESH_OT_random_vertices(bpy.types.Operator):
    """Randomize position of selected vertices"""
    bl_idname = "mesh.random_vertices"
    bl_label = "Randomize Vertices"
    bl_options = {'REGISTER', 'UNDO'}
    
    x_factor: FloatProperty(
        name="X Random Factor",
        description="Random displacement strength on X axis",
        default=0.0,
        min=0.0,
        max=10.0
    )
    
    y_factor: FloatProperty(
        name="Y Random Factor",
        description="Random displacement strength on Y axis",
        default=0.0,
        min=0.0,
        max=10.0
    )
    
    z_factor: FloatProperty(
        name="Z Random Factor",
        description="Random displacement strength on Z axis",
        default=0.0,
        min=0.0,
        max=10.0
    )
    
    def execute(self, context):
        obj = context.active_object
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Must be in Edit Mode!")
            return {'CANCELLED'}
        
        # Get mesh data
        bpy.ops.object.mode_set(mode='OBJECT')
        selected_verts = [v for v in obj.data.vertices if v.select]
        
        # Check if any vertices are selected
        if len(selected_verts) == 0:
            self.report({'ERROR'}, "Please select some vertices first!")
            bpy.ops.object.mode_set(mode='EDIT')
            return {'CANCELLED'}
        
        # Apply random displacement
        for v in selected_verts:
            if self.x_factor > 0:
                v.co.x += random.uniform(-self.x_factor, self.x_factor)
            if self.y_factor > 0:
                v.co.y += random.uniform(-self.y_factor, self.y_factor)
            if self.z_factor > 0:
                v.co.z += random.uniform(-self.z_factor, self.z_factor)
        
        # Return to edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}

class MESH_PT_random_panel(bpy.types.Panel):
    """Random Vertex Position Panel"""
    bl_label = "Random Vertex Position"
    bl_idname = "MESH_PT_random_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Random Vertex"
    
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator("mesh.random_vertices")

classes = (
    MESH_OT_random_vertices,
    MESH_PT_random_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()