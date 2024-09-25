bl_info = {
    "name": "Texture Selector",
    "description": "A tool to select objects with specific textures",
    "author": "Baptiste Mollicone",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "3D View > N-Panel",
    "category": "Tool"
}

import bpy

class TextureSelectorPanel(bpy.types.Panel):
    bl_label = "Texture Selector"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        texture_names = [tex.name for tex in bpy.data.images]
        layout.prop_search(context.scene, "texture_name", bpy.data, "images", icon='IMAGE_DATA')
        layout.operator("texture_selector.select")

class TextureSelectorSelectOperator(bpy.types.Operator):
    bl_idname = "texture_selector.select"
    bl_label = "Select Objects"

    def execute(self, context):
        texture_name = context.scene.texture_name
        texture = bpy.data.images.get(texture_name)
        objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
        selected_objects = []
        for obj in objects:
            for mat in obj.data.materials:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image == texture:
                        selected_objects.append(obj)
                        break
                if obj in selected_objects:
                    break
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selected_objects:
            obj.select_set(True)
        return {'FINISHED'}

class TextureSelectorProps(bpy.types.PropertyGroup):
    texture_name: bpy.props.StringProperty(name="Texture Name", default="")

def register():
    bpy.utils.register_class(TextureSelectorPanel)
    bpy.utils.register_class(TextureSelectorSelectOperator)
    bpy.types.Scene.texture_name = bpy.props.StringProperty(name="Texture Name", default="")
    bpy.utils.register_class(TextureSelectorProps)

def unregister():
    bpy.utils.unregister_class(TextureSelectorPanel)
    bpy.utils.unregister_class(TextureSelectorSelectOperator)
    del bpy.types.Scene.texture_name
    bpy.utils.unregister_class(TextureSelectorProps)

if __name__ == "__main__":
    register()