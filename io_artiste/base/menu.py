import bpy
from ..node.init import (cli, init_stk)
from ..node.run import (runner)
from ..node.mode import (run_race)
from ..node.option import (option_running)

class STKinit(bpy.types.Menu):
    bl_idname = 'NODE_MT_STK_Init'
    bl_label = 'STK INIT'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("node.add_node", text=cli.STK_cli.bl_label).type = cli.STK_cli.bl_idname
        layout.operator("node.add_node", text=init_stk.STK_initial.bl_label).type = init_stk.STK_initial.bl_idname

class STKmode(bpy.types.Menu):
    bl_idname = 'NODE_MT_STK_mode'
    bl_label = 'STK MODE'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("node.add_node", text=run_race.STK_test_race.bl_label).type = run_race.STK_test_race.bl_idname
            
class STKrun(bpy.types.Menu):
    bl_idname = 'NODE_MT_STK_run'
    bl_label = 'STK RUN'

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("node.add_node", text=runner.STK_run.bl_label).type = runner.STK_run.bl_idname
        
class STKdebug(bpy.types.Menu):
    bl_idname = 'NODE_MT_STK_debug'
    bl_label = 'STK DEBUG'
    
    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("node.add_node", text=option_running.STK_op_running.bl_label).type = option_running.STK_op_running.bl_idname
        
# TODO
# add nodes 
# menu: Mode, Init, Run, Debug

## INIT
# Demo Mode
# Graphic
# Windows

## MODE
# Battle
# Capture Flag
# Cutscene
# Leader
# Soccer
# Time Trial
# Egg Party

## RUN
# Preview Info

## DEBUG
# Controller
# Graphique
# Kart
# Track

### Replace Init and Run by Operator