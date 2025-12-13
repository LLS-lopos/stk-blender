from .moteur.AntarcticaRenderEngine import AntarcticaRenderEngine
from .nodes.interface import editor_are
from .panel.STKrenduPanel import STKechantillonPanel, STKocclussionAmbiantPanel, STKbloomPanel, STKombrePanel, \
    STKprofondeurDeChampPanel
from .panel.STKrenduSortie import STKsortiePanel, STKfomatPanel, STKframePanel

bl_info = {
    "name": "Antarctica Render Engine",
    "author": "LLS",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "category": "Render",
    "description": "SuperTuxKart renderer integration",
    "warning": "alpha",
    "wiki_url": "",
    "tracker_url": "",
}

import bpy

classe = (
    AntarcticaRenderEngine,
    STKechantillonPanel,
    STKocclussionAmbiantPanel,
    STKbloomPanel,
    STKombrePanel,
    STKprofondeurDeChampPanel,
    STKsortiePanel,
    STKfomatPanel,
    STKframePanel,
    editor_are,
)


def get_panels():
    exclude_panels = {
        'VIEWLAYER_PT_filter',
        'VIEWLAYER_PT_layer_passes',
    }

    panels = []
    for panel in bpy.types.Panel.__subclasses__():
        if hasattr(panel, 'COMPAT_ENGINES') and 'BLENDER_RENDER' in panel.COMPAT_ENGINES:
            if panel.__name__ not in exclude_panels:
                panels.append(panel)

    return panels


def add_stk_node_shader_menu(self, context):
    if context.space_data.tree_type != editor_are.bl_idname:
        return


def register():
    for i in classe:
        bpy.utils.register_class(i)
    for panel in get_panels():
        panel.COMPAT_ENGINES.add(AntarcticaRenderEngine.bl_idname)
    bpy.types.NODE_MT_add.append(add_stk_node_shader_menu)


def unregister():
    for i in reversed(classe):
        bpy.utils.unregister_class(i)
    for panel in get_panels():
        if AntarcticaRenderEngine.bl_idname in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove(AntarcticaRenderEngine.bl_idname)


if __name__ == "__main__":
    register()
