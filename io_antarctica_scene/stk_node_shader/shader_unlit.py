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

# =============================================================================
# Unlit Solid (ignores lighting, always full brightness)
# =============================================================================

import bpy

from bpy.types import ShaderNodeCustomGroup
from .shader_base import ShaderStkBase

_UNLIT_GROUP = ".ShaderStkUnlit_Group"

def _get_splatting_group():
    group = bpy.data.node_groups.get(_UNLIT_GROUP)
    if group is not None:
        return group
    
    # définition du group de propriété personalisé (entré/sortie)
    group = bpy.data.node_groups.new(_UNLIT_GROUP, "ShaderNodeTree")

    return group

def _free_splatting_group():
    group = bpy.data.node_groups.get(_UNLIT_GROUP)
    if group is not None:
        bpy.data.node_groups.remove(group)