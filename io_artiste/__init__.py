bl_info = {
    "name": "STK RUNNER",
    "author": "LLS",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "category": "Node",
    "description": "nodal editor test SuperTuxKart Project",
    "location": "Node Editor > STK Run Test",
}

import bpy
from .base import (node_base, menu, node_editor)
from .geo_node import (stk_geo_node)
from .node.run import (runner, preview_cmd)
from .node.mode import (leader, time_trial, capture_flag, cutscene, egg_party, demo, game_mode)
from .node.debug import (direct_run, controller, graphic_d, kart)
from .node.init import (cli, init_stk, graphic, windows)

classes = (
    node_editor.STKeditor,
    menu.STKmenu,
    menu.STKoperator,
    menu.STKmode, 
    menu.STKdebug,
    node_base.node,
    init_stk.STK_initial,
    init_stk.STK_Pick_Executable_Operator,
    init_stk.STK_Pick_TracksFolder_Operator,
    init_stk.STK_Pick_kartsFolder_Operator,
    cli.STK_cli,
    runner.STK_run,
    runner.STK_OT_RunStk,
    stk_geo_node.STKNodeMenu,
    stk_geo_node.STKparticles,
    stk_geo_node.ListePoint,
    stk_geo_node.CheckActif,
    preview_cmd.STK_preview_cmd,
    demo.STK_demo,
    direct_run.STK_direct_run,
    game_mode.STK_game_mode,
    windows.STK_windows,
    graphic.STK_graphic,
    leader.STK_leader,
    time_trial.STK_time_trial,
    controller.STK_debug_controller,
    graphic_d.STK_debug_graphique,
    kart.STK_debug_kart,
    cutscene.STK_cut_scene,
    capture_flag.STK_capture_flag,
    egg_party.STK_egg_party,
)

def add_stk_node_menu(self, context):
    if context.space_data.tree_type != node_editor.STKeditor.bl_idname: return
    self.layout.menu(menu.STKoperator.bl_idname)
    self.layout.menu(menu.STKmode.bl_idname)
    self.layout.menu(menu.STKdebug.bl_idname)

# Define custom STK geometry node
def menu_stk_geo_node(self, context):
    self.layout.menu(stk_geo_node.STKNodeMenu.bl_idname, text="SuperTuxKart", icon='AUTO')


    self.layout.menu(menu.STKmenu.bl_idname)
        

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.NODE_MT_add.append(add_stk_node_menu)
    bpy.app.handlers.depsgraph_update_post.append(node_editor.STKeditor.update_scene_handler)
    bpy.types.NODE_MT_geometry_node_add_all.append(menu_stk_geo_node)

def unregister():
    bpy.types.NODE_MT_add.remove(add_stk_node_menu)
    bpy.types.NODE_MT_geometry_node_add_all.remove(menu_stk_geo_node)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.app.handlers.depsgraph_update_post.remove(node_editor.STKeditor.update_scene_handler)


if __name__ == "__main__":
    register()
