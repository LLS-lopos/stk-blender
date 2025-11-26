import bpy
from ...base.node import node

class STK_debug_graphique(node):
    bl_idname = "STK_Debug_Graphique"
    bl_label = 'Debug Graphique'
    bl_icon = 'NONE'

    def init(self, context):
        return super().init(context)
    
    def draw_buttons(self, context, layout):
        return super().draw_buttons(context, layout)
    
    def process(self, context, id, path):
        return super().process(context, id, path)
    
    def update(self):
        return super().update()