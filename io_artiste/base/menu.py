import bpy
from ..node.init import (cli, init_stk, demo_info, graphic, windows)
from ..node.run import (runner, preview_cmd)
from ..node.mode import (racing, leader, time_trial, battle, capture_flag, cutscene, egg_party, soccer)
from ..node.debug import (direct_run, controller, graphic_d, kart, track)

class STKoperator(bpy.types.Menu):
    bl_idname = 'NODE_MT_STK_Operator'
    bl_label = 'STK OPERATOR'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("node.add_node", text=init_stk.STK_initial.bl_label).type = init_stk.STK_initial.bl_idname
        layout.separator()
        layout.operator("node.add_node", text=cli.STK_cli.bl_label).type = cli.STK_cli.bl_idname
        layout.operator("node.add_node", text=preview_cmd.STK_info.bl_label).type = preview_cmd.STK_info.bl_idname
        layout.operator("node.add_node", text=windows.STK_windows.bl_label).type = windows.STK_windows.bl_idname
        layout.operator("node.add_node", text=graphic.STK_graphic.bl_label).type = graphic.STK_graphic.bl_idname
        layout.operator("node.add_node", text=demo_info.STK_demo_mode.bl_label).type = demo_info.STK_demo_mode.bl_idname
        layout.separator()
        layout.operator("node.add_node", text=runner.STK_run.bl_label).type = runner.STK_run.bl_idname

class STKmode(bpy.types.Menu):
    bl_idname = 'NODE_MT_STK_mode'
    bl_label = 'STK MODE'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("node.add_node", text=racing.STK_race.bl_label).type = racing.STK_race.bl_idname
        layout.operator("node.add_node", text=leader.STK_leader.bl_label).type = leader.STK_leader.bl_idname
        layout.operator("node.add_node", text=time_trial.STK_time_trial.bl_label).type = time_trial.STK_time_trial.bl_idname
        layout.operator("node.add_node", text=battle.STK_battle.bl_label).type = battle.STK_battle.bl_idname
        layout.operator("node.add_node", text=capture_flag.STK_capture_flag.bl_label).type = capture_flag.STK_capture_flag.bl_idname
        layout.operator("node.add_node", text=cutscene.STK_cut_scene.bl_label).type = cutscene.STK_cut_scene.bl_idname
        layout.operator("node.add_node", text=egg_party.STK_egg_party.bl_label).type = egg_party.STK_egg_party.bl_idname
        layout.operator("node.add_node", text=soccer.STK_soccer.bl_label).type = soccer.STK_soccer.bl_idname
            

class STKdebug(bpy.types.Menu):
    bl_idname = 'NODE_MT_STK_debug'
    bl_label = 'STK DEBUG'
    
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("node.add_node", text=direct_run.STK_direct_run.bl_label).type = direct_run.STK_direct_run.bl_idname
        layout.operator("node.add_node", text=controller.STK_debug_controller.bl_label).type = controller.STK_debug_controller.bl_idname
        layout.operator("node.add_node", text=graphic_d.STK_debug_graphique.bl_label).type = graphic_d.STK_debug_graphique.bl_idname
        layout.operator("node.add_node", text=kart.STK_debug_kart.bl_label).type = kart.STK_debug_kart.bl_idname
        layout.operator("node.add_node", text=track.STK_debug_track.bl_label).type = track.STK_debug_track.bl_idname
