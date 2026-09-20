import bpy
from ..node.debug import (direct_run)
from ..node.init import (cli, init_stk)
from ..node.run import (runner, preview_cmd)
from ..node.mode import (demo, game_mode)


class STKmenu(bpy.types.Menu):
    bl_idname = 'NODE_MT_STK_Menu'
    bl_label = 'STK Node'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.label(text="Operator")
        layout.operator("node.add_node", text=init_stk.STK_initial.bl_label).type = init_stk.STK_initial.bl_idname
        layout.separator()
        layout.operator("node.add_node", text=cli.STK_cli.bl_label).type = cli.STK_cli.bl_idname
        layout.operator("node.add_node", text=preview_cmd.STK_info.bl_label).type = preview_cmd.STK_info.bl_idname
        layout.operator("node.add_node", text=windows.STK_windows.bl_label).type = windows.STK_windows.bl_idname
        layout.operator("node.add_node", text=graphic.STK_graphic.bl_label).type = graphic.STK_graphic.bl_idname
        layout.operator("node.add_node", text=demo_info.STK_demo_mode.bl_label).type = demo_info.STK_demo_mode.bl_idname
        layout.separator()
        layout.operator("node.add_node", text=runner.STK_run.bl_label).type = runner.STK_run.bl_idname
        layout.operator("node.add_node", text=cli.STK_cli.bl_label).type = cli.STK_cli.bl_idname
        layout.operator("node.add_node", text=direct_run.STK_direct_run.bl_label).type = direct_run.STK_direct_run.bl_idname
        layout.separator()
        layout.label(text="Mode")
        layout.operator("node.add_node", text=demo.STK_demo.bl_label).type = demo.STK_demo.bl_idname
        layout.operator("node.add_node", text=game_mode.STK_game_mode.bl_label).type = game_mode.STK_game_mode.bl_idname
        layout.separator()
        layout.operator("node.add_node", text=battle.STK_battle.bl_label).type = battle.STK_battle.bl_idname
        layout.operator("node.add_node", text=racing.STK_racing.bl_label).type = racing.STK_racing.bl_idname
        layout.operator("node.add_node", text=soccer.STK_soccer.bl_label).type = soccer.STK_soccer.bl_idname
            

class STKdebug(bpy.types.Menu):
    bl_idname = 'NODE_MT_STK_debug'
    bl_label = 'STK DEBUG'
    
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("node.add_node", text=preview_cmd.STK_preview_cmd.bl_label).type = preview_cmd.STK_preview_cmd.bl_idname
        layout.operator("node.add_node", text=direct_run.STK_direct_run.bl_label).type = direct_run.STK_direct_run.bl_idname
        layout.operator("node.add_node", text=controller.STK_debug_controller.bl_label).type = controller.STK_debug_controller.bl_idname
        layout.operator("node.add_node", text=graphic_d.STK_debug_graphique.bl_label).type = graphic_d.STK_debug_graphique.bl_idname
        layout.operator("node.add_node", text=kart.STK_debug_kart.bl_label).type = kart.STK_debug_kart.bl_idname
        layout.operator("node.add_node", text=track.STK_debug_track.bl_label).type = track.STK_debug_track.bl_idname
