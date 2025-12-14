import bpy

from ...base.node_base import node


class STK_test_race(node):
    bl_idname = 'STK_Test_Race'
    bl_label = 'Racing'
    bl_icon = 'NONE'

    entrer: bpy.props.StringProperty(name="input", default="")
    sortie: bpy.props.StringProperty(name="output", default="")

    num_kart: bpy.props.IntProperty(name="N_karts", default=5,
                                    min=0, max=20, description="define number of kart for racing",
                                    update=lambda self, context: self.update())

    laps: bpy.props.IntProperty( name="N_laps", description="define number of lap for the race",
                                 default=1, min=0, max=20,
                                 update=lambda self, context: self.update())

    choix_track: bpy.props.StringProperty(name="choise track", default="", update=lambda self, context: self.update())
    choix_kart: bpy.props.StringProperty(name="choise kart", default="", update=lambda self, context: self.update())
    reverse: bpy.props.BoolProperty(name="Reverse Track", default=False, update=lambda self, context: self.update())

    def init(self, context):
        self.node_entrer("NodeSocketString", "input_0", "", "")
        self.node_sortie('NodeSocketString', 'Race', 'race', "")

    def draw_buttons(self, context, layout):
        ligne = layout.row()
        ligne.prop(self, "reverse")
        ligne.prop(self, "num_kart")
        ligne.prop(self, "laps")

        layout.prop(self, "choix_track")
        layout.prop(self, "choix_kart")

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
                            self.entrer = str(value)
                        except:
                            pass

                    # If that fails, try to get the default_value
                    if hasattr(from_socket, "default_value"):
                        self.entrer = str(from_socket.default_value)
            else:
                self.entrer = ""

        # Build the complete instruction with the input and properties
        if len(self.outputs) > 0 and hasattr(self.outputs[0], "default_value"):
            self.sortie = ""
            if self.entrer != "":
                self.sortie += self.entrer + " "
            self.sortie += f"--numkarts={self.num_kart} --laps={self.laps}"
            if self.choix_track != "":
                self.sortie += f" --track={self.choix_track}"
            if self.choix_kart != "":
                self.sortie += f" --kart={self.choix_kart}"
            if self.reverse != False:
                self.sortie += f" --reverse"
            self.sortie += f" --mode=0"
            self.outputs[0].default_value = str(self.sortie)
        return self.sortie

    def update(self):
        self.process(bpy.context, None, None)
