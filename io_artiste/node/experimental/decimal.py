import bpy

from ...base.node import node


class Decimal(node):
    bl_idname = 'STK_exp_decimal'
    bl_label = 'Float Input'
    bl_icon = 'NONE'

    simple: bpy.props.FloatProperty(name="float", default=0.0, precision=2, update=lambda self, context: self.update())

    def init(self, context):
        self.node_sortie('NodeSocketFloat', 'output_1', "Output_1")

    def draw_buttons(self, context, layout):
        layout.prop(self, 'simple')

    def process(self, context, id, path):
        self.outputs[0].default_value = self.simple
        return self.outputs[0].default_value

    def update(self):
        self.process(bpy.context, None, None)
