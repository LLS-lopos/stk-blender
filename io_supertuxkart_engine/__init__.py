import bpy

bl_info = {
    "name": "SuperTuxKartRender",
    "author": "Ludérïck Le Saouter @LLS",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "category": "Render",
    "description": "SuperTuxKartRender integration for Blender",
    "warning": "alpha",
    "wiki_url": "",
    "tracker_url": "",
}

from . import moteur, nodes, panel
from .moteur.base import STKrendu #STKrenduGPU
from .panel.STKrenduSortie import (STKsortiePanel, STKfomatPanel, STKframePanel)
from .panel.STKrenduPanel import (
    STKechantillonPanel,
    STKocclussionAmbiantPanel,
    STKbloomPanel,
    STKombrePanel,
    STKprofondeurDeChampPanel
)

classe = (
    STKrendu,
    STKsortiePanel,
    STKfomatPanel,
    STKframePanel,
    STKechantillonPanel,
    STKocclussionAmbiantPanel,
    STKbloomPanel,
    STKombrePanel,
    STKprofondeurDeChampPanel,
)

def register():
    for i in classe:
        bpy.utils.register_class(i)

def unregister():
    for i in reversed(classe):
        bpy.utils.unregister_class(i)
    
if __name__ == "__main__":
    register()
