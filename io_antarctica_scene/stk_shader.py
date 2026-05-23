#!BPY

# Copyright (c) 2020 SuperTuxKart author(s)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import bpy
from bpy.types import Menu
from .stk_node_shader import (shader_solid)

# sous menu ADD
class STKshaderMenu(Menu):
    bl_idname = 'NODE_MT_STK_Shader'
    bl_label = 'SuperTuxKart'

    @classmethod
    def poll(cls, context):
        return context.area.ui_type == 'ShaderNodeTree'
    
    def draw(self, context):
        layout = self.layout
        layout.operator("node.add_node", text=shader_solid.ShaderStkSolid.bl_label, icon="MATERIAL").type = shader_solid.ShaderStkSolid.bl_idname
        layout.separator()
