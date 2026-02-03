import bpy

from ...base.node_base import node


class STK_debug_controller(node):
    bl_idname = 'STK_Debug_Control'
    bl_label = 'Debug Controller'
    bl_icon = 'NONE'

    s_input: bpy.props.StringProperty(name="input", default="")
    s_output: bpy.props.StringProperty(name="output", default="")

    visual_gamepad: bpy.props.BoolProperty(name="visual", default=False, update=lambda self, context: self.update())
    bool_keyboard: bpy.props.BoolProperty(name="Keyboard", default=False, update=lambda self, context: self.update())
    bool_wii: bpy.props.BoolProperty(name="WiiMote", default=False, update=lambda self, context: self.update())
    bool_gamepad: bpy.props.BoolProperty(name="Gamepad", default=False, update=lambda self, context: self.update())
    debug_keyboard: bpy.props.BoolProperty(name="debug", default=False, update=lambda self, context: self.update())
    debug_gamepad: bpy.props.BoolProperty(name="debug", default=False, update=lambda self, context: self.update())
    debug_wiimote: bpy.props.BoolProperty(name="debug", default=False, update=lambda self, context: self.update())
    keyboard: bpy.props.IntProperty(name="ID", default=0, min=0, update=lambda self, context: self.update())
    gamepad: bpy.props.IntProperty(name="ID", default=0, min=0, update=lambda self, context: self.update())

    def init(self, context):
        self.node_input("NodeSocketString", "input_0", "", "")
        self.node_output('NodeSocketString', 'output_0', '', "")

    def draw_buttons(self, context, layout):
        layout.prop(self, "bool_keyboard")
        if self.bool_keyboard != False:
            box = layout.box()
            box.prop(self, "keyboard")
            box.prop(self, "debug_keyboard")

        layout.prop(self, "bool_gamepad")
        if self.bool_gamepad != False:
            box = layout.box()
            box.prop(self, "gamepad")
            box.prop(self, "debug_gamepad")
            box.prop(self, "visual_gamepad")
            box = layout.box()
            box.prop(self, "bool_wii")
            if self.bool_wii != False:
                box.prop(self, "debug_wiimote")

    def process(self, context, id, path):
        # Check for input socket existence
        if len(self.inputs) > 0:
            input_socket = self.inputs[0]

            if input_socket.is_linked:
                links = input_socket.links
                if links:
                    from_socket = links[0].from_socket
                    from_node = links[0].from_node

                    # Try to get the value via the source node's process method first
                    if hasattr(from_node, "process"):
                        try:
                            value = from_node.process(context, id, path)
                            self.s_input = str(value)
                        except:
                            pass

                    # If that fails, try to get the default_value
                    if hasattr(from_socket, "default_value"):
                        self.s_input = str(from_socket.default_value)
            else:
                self.s_input = ""

        # Build the complete instruction with the input and properties
        if len(self.outputs) > 0 and hasattr(self.outputs[0], "default_value"):
            self.s_output = ""
            if self.s_input != "":
                self.s_output += self.s_input + " "

            if self.bool_keyboard != False:
                self.s_output += f" --use-keyboard={self.keyboard}"
                if self.debug_keyboard != False:
                    self.s_output += f" --keyboard-debug"
            if self.bool_gamepad != False:
                self.s_output += f" --use-gamepad={self.gamepad}"
                if self.debug_gamepad != False:
                    self.s_output += f" --gamepad-debug"
                if self.visual_gamepad != False:
                    self.s_output += f" --gamepad-visuals"
                if self.bool_wii != False:
                    self.s_output += f" --wii"
                    if self.debug_wiimote != False:
                        self.s_output += f" --wiimote-debug"
            self.outputs[0].default_value = str(self.s_output)
        return self.s_output

    def update(self):
        self.process(bpy.context, None, None)
