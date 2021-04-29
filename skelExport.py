# Copyright (C) 2021 Talya_taya
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

bl_info = {
    "name": "skelExport: Armature Export for Arma 3",
    "author": "Talya_taya",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "File -> Export",
    "description": "Extracts bones from Blender in cfgSkeleton format for use in Arma 3.",
    "warning": "",
    "wiki_url": "https://github.com/Talyataya/skelExport",
    "tracker_url": "https://github.com/Talyataya/skelExport/issues",
    "category": "Import-Export",
    }
    
import bpy
import bpy_extras
from bpy.utils import register_class, unregister_class
    
def export_skeleton(filepath, object_name, fill_parents=True, wrapped=True):
    try:
        object = bpy.data.objects[object_name]
    except KeyError:
        return 1, []
    armature = object.data
    if type(armature) != bpy.types.Armature:
        return 2, []
    items = object.data.bones.items()
    with open(filepath, 'w') as file:
        if wrapped:
            file.write("skeletonBones[] = {\n")
        for i, [bone_name, bone] in enumerate(items):
            if (not fill_parents) or (bone.parent is None):
                parent_name = ""
            else:
                parent_name = str(bone.parent.name)
            file.write("{tab}\"{bone_name}\",\"{parent_name}\"".format(bone_name=bone_name, parent_name=parent_name, tab="\t" if wrapped else ""))
            if (i != len(items)-1):
                file.write(f",\n")
        if wrapped:
            file.write("\n};")
    return 0, len(items)
    
class SKELEXPORT_OT_ArmatureExport(bpy.types.Operator,
                                 bpy_extras.io_utils.ExportHelper):
    bl_idname = "skelexport.armatureexport"
    bl_label = "Export cfgSkeleton"
    bl_description = "Export cfgSkeleton"
    filename_ext = ".hpp"
    object_name: bpy.props.StringProperty(
        name="Object",
        description="The object with armature to be exported",
        default='')
    fill_parents: bpy.props.BoolProperty(
        name="Retrieve parents",
        description="Fill in the parents using armature hierarchy",
        default=True)
    wrapped: bpy.props.BoolProperty(
        name="Config Entry Mode",
        description="Converts output to skeletonBones[] = {output};",
        default=True)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        column = layout.column()
        column.prop_search(self, "object_name", scene, "objects")
        column.prop(self, "fill_parents")
        column.prop(self, "wrapped")
        
    def execute(self, context):
        result, nBones = export_skeleton(self.filepath,
                         self.object_name,
                         fill_parents=self.fill_parents,
                         wrapped=self.wrapped
                         )
        if result == 0:
            if self.fill_parents:
                self.report({'INFO'}, f"{nBones} bones exported with their parents.")
            else:
                self.report({'INFO'}, f"{nBones} bones exported without their parents.")
        elif result == 1:
            self.report({'ERROR'}, f"Failed to export bones, '{self.object_name}' does not exist.")
        elif result == 2:
            self.report({'ERROR'}, f"Failed to export bones, '{self.object_name}' does not contain a valid armature.")
        else:
            self.report({'ERROR'}, "Unknown Error")
        return {'FINISHED'}

def ArmatureExportMenuFunc(self, context):
    self.layout.operator(SKELEXPORT_OT_ArmatureExport.bl_idname,
                         text="Arma 3 Skeleton (.hpp)")

classes = (
    SKELEXPORT_OT_ArmatureExport,
    )

def register():
    for cls in classes:
        register_class(cls)
    bpy.types.TOPBAR_MT_file_export.append(ArmatureExportMenuFunc)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(ArmatureExportMenuFunc)
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == '__main__':
    register() 