import bpy

from ...base.node_base import node


class STK_graphic(node):
    bl_idname = 'STK_Graphic'
    bl_label = 'Graphic'
    bl_icon = 'NONE'

    s_input: bpy.props.StringProperty(name="input", default="")
    s_output: bpy.props.StringProperty(name="output", default="")

    glow: bpy.props.BoolProperty(name="GLOW", description="Enable/Disable glow effect.", default=False,
                                 update=lambda self, context: self.update())
    bloom: bpy.props.BoolProperty(name="BLOOM", description="Enable/Disable bloom effect.", default=False,
                                  update=lambda self, context: self.update())
    light_shaft: bpy.props.BoolProperty(name="LIGHT SHAFT", description="Enable/Disable light shafts (God rays).",
                                        default=False, update=lambda self, context: self.update())
    dof: bpy.props.BoolProperty(name="DOF", description="Enable/Disable depth of field.", default=False,
                                update=lambda self, context: self.update())
    particule: bpy.props.BoolProperty(name="PARTICULE", description="Enable/Disable particles.", default=False,
                                      update=lambda self, context: self.update())
    animation_kart: bpy.props.BoolProperty(name="ANIM KART", description="Enable/Disable animated characters.",
                                           default=False, update=lambda self, context: self.update())
    motion_blur: bpy.props.BoolProperty(name="BLUR", description="Enable/Disable motion blur.", default=False,
                                        update=lambda self, context: self.update())
    mlaa: bpy.props.BoolProperty(name="MLAA", description="Enable/Disable MLAA.", default=False,
                                 update=lambda self, context: self.update())
    tex_compression: bpy.props.BoolProperty(name="COMPRESSION TEXTURE",
                                            description="Enable/Disable texture compression.", default=False,
                                            update=lambda self, context: self.update())
    ssao: bpy.props.BoolProperty(name="SSAO", description="Enable/Disable SSAO.", default=False,
                                 update=lambda self, context: self.update())
    ibl: bpy.props.BoolProperty(name="IBL", description="Enable/Disable IBL.", default=False,
                                update=lambda self, context: self.update())
    tex_hd: bpy.props.BoolProperty(name="HD TEXTURE", description="Enable/Disable HD textures.", default=False,
                                   update=lambda self, context: self.update())
    light_dynamic: bpy.props.BoolProperty(name="DYNAMIC LIGHT", description="Enable/Disable dynamic lights.",
                                          default=False, update=lambda self, context: self.update())

    anisotropic: bpy.props.IntProperty(name="ANISOTROPIC", description="Anisotropic filtering quality (0 to disable).",
                                       default=0, update=lambda self, context: self.update())
    shadows: bpy.props.EnumProperty(name="SHADOWS", 
                                   description="Shadow resolution (0 to disable).",
                                   items=[
                                       ('0', 'Disabled', 'Disabled', '', 0),
                                       ('256', 'Low', 'Low', '', 1),
                                       ('512', 'Medium', 'Medium', '', 2),
                                       ('1024', 'High', 'High', '', 3),
                                       ('2048', 'Very high', 'Very high', 4),
                                       ],
                                       default='0', update=lambda self, context: self.update())
    render_driver: bpy.props.EnumProperty(name="RENDER DRIVER",
                                          description="Render driver to use (gl or directx9).",
                                          items=[
                                              ('gl', 'OpenGL', 'OpenGL', '', 0),
                                              ('directx9', 'DirectX9', 'DirectX9', '', 1),
                                              ('vulkan', 'Vulkan', 'Vulkan', '', 2),
                                          ],
                                          default='gl', update=lambda self, context: self.update())
    render_superior: bpy.props.BoolProperty(name="Render +", default=False, update=lambda self, context: self.update())

    def init(self, context):
        self.node_input("NodeSocketString", "input_0", "", "")
        self.node_output('NodeSocketString', 'output_0', '', "")

    def draw_buttons(self, context, layout):
        box = layout.box()
        ligne = box.row()
        ligne.prop(self, "particule")
        ligne.prop(self, "animation_kart")
        ligne.prop(self, "tex_compression")

        ligne = box.row()
        ligne.prop(self, "render_superior")
        if self.render_superior:
            ligne = box.row()
            box.prop(self, "shadows")
            box.prop(self, "anisotropic")

            ligne = box.row()
            ligne.prop(self, "mlaa")
            ligne.prop(self, "light_dynamic")

            ligne = box.row()
            ligne.prop(self, "glow")
            ligne.prop(self, "tex_hd")

            ligne = box.row()
            ligne.prop(self, "light_shaft")
            ligne.prop(self, "bloom")
            
            ligne = box.row()
            ligne.prop(self, "ibl")
            ligne.prop(self, "ssao")

            ligne = box.row()
            ligne.prop(self, "blur")
            ligne.prop(self, "dof")

        ligne = box.row()
        box.prop(self, "render_driver")

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

            if self.animation_kart == True:
                self.s_output += f" --enable-animated-characters"
            else:
                self.s_output += f" --disable-animated-characters"
            
            if self.tex_compression == True:
                self.s_output += f" --enable-texture-compression"
            else:
                self.s_output += f" --disable-texture-compression"
            
            if self.particule == True:
                self.s_output += f" --enable-particles"
            else:
                self.s_output += f" --disable-particles"

            if self.render_superior:
                if self.glow == True: self.s_output += f"--enable-glow"
                else: self.s_output += f"--disable-glow"
                if self.bloom == True: self.s_output += f" --enable-bloom"
                else: self.s_output += f" --disable-bloom"
                if self.light_shaft == True: self.s_output += f" --enable-light-shaft"
                else: self.s_output += f" --disable-light-shaft"
                if self.dof == True: self.s_output += f" --enable-dof"
                else: self.s_output += f" --disable-dof"
                if self.motion_blur == True: self.s_output += f" --enable-motion-blur"
                else: self.s_output += f" --disable-motion-blur"
                if self.mlaa == True: self.s_output += f" --enable-mlaa"
                else: self.s_output += f" --disable-mlaa"
                if self.ssao == True: self.s_output += f" --enable-ssao"
                else: self.s_output += f" --disable-ssao"
                if self.ibl == True: self.s_output += f" --enable-ibl"
                else: self.s_output += f" --disable-ibl"
                if self.tex_hd == True: self.s_output += f" --enable-hd-textures"
                else: self.s_output += f" --disable-hd-textures"
                if self.light_dynamic == True: self.s_output += f" --enable-dynamic-lights"
                else: self.s_output += f" --disable-dynamic-lights"
                self.s_output += f" --anisotropic={self.anisotropic}"
                self.s_output += f" --shadows={self.shadows}"
            else:
                self.s_output += f"--disable-glow"
                self.s_output += f" --disable-bloom"
                self.s_output += f" --disable-light-shaft"
                self.s_output += f" --disable-dof"
                self.s_output += f" --disable-motion-blur"
                self.s_output += f" --disable-mlaa"
                self.s_output += f" --disable-ssao"
                self.s_output += f" --disable-ibl"
                self.s_output += f" --disable-hd-textures"
                self.s_output += f" --disable-dynamic-lights"
                self.s_output += f" --anisotropic=0"
                self.s_output += f" --shadows=0"

            
            self.s_output += f" --render-driver={self.render_driver}"

            self.outputs[0].default_value = str(self.s_output)
        return self.s_output

    def update(self):
        self.process(bpy.context, None, None)
