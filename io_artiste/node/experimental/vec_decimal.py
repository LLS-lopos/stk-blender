import bpy
from ...base.node import node
from mathutils import Vector


class VecDecimal(node):
    bl_idname = 'STK_exp_vec_decimal'
    bl_label = 'Vec Float Input'
    bl_icon = 'NONE'

    simple_3: bpy.props.FloatVectorProperty(name="", step=3, default=Vector((0.0, 0.0, 0.0)), precision=2, update=lambda self, context: self.update())

    def init(self, context):
        self.node_sortie('NodeSocketVectorXYZ', 'output_2', "Output_2")

    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.prop(self, 'simple_3', index=0, text='x')
        col.prop(self, 'simple_3', index=1, text='y')
        col.prop(self, 'simple_3', index=2, text='z')

    def process(self, context, id, path):
        vec_3 = Vector((
            self.simple_3[0],
            self.simple_3[1],
            self.simple_3[2],
            ))
        self.outputs[0].default_value = vec_3
        return self.outputs[0].default_value

    def update(self):
        self.process(bpy.context, None, None)

