import bpy

from ...base.node_base import node


class STK_graphic(node):
    bl_idname = 'STK_Graphic'
    bl_label = 'Graphic'
    bl_icon = 'NONE'

    s_input: bpy.props.StringProperty(name="input", default="")
    s_output: bpy.props.StringProperty(name="output", default="")

    custom_graphic: bpy.props.BoolProperty(
        name="Custom", default=False,
        description="Use Custom Graphic",
        update=lambda self, context: self.update())

    # if custom graphic is FALSE
    gfx_preset: bpy.props.IntProperty(
        name="Graphical Level", default=1,
        min=1, max=7, description="Set the graphics settings to the selected preset",
        update=lambda self, context: self.update())

    blur_level: bpy.props.IntProperty(
        name="Blur Level", default=0,
        min=0, max=2, description="active Blur and DoF",
        update=lambda self, context: self.update())
    
    render_resolution: bpy.props.EnumProperty(
        name="Render Resolution", 
        description="Render resolution (30-200).",
        items=[
            ('30', '30', '', '', 0), ('35', '35', '', '', 1),
            ('40', '40', '', '', 2), ('45', '45', '', '', 3),
            ('50', '50', '', '', 4), ('55', '55', '', '', 5),
            ('60', '60', '', '', 6), ('65', '65', '', '', 7),
            ('70', '70', '', '', 8), ('75', '75', '', '', 9),
            ('80', '80', '', '', 10), ('85', '85', '', '', 11),
            ('90', '90', '', '', 12), ('95', '95', '', '', 13),
            ('100', '100', '', '', 14), ('125', '125', '', '', 15),
            ('150', '150', '', '', 16), ('200', '200', '', '', 17),
            ],
            default='100', update=lambda self, context: self.update())

    # if custom graphic is TRUE

    animation_kart: bpy.props.BoolProperty(
        name="Anim Characters",  description="Enable/Disable animated characters.",
        default=False, update=lambda self, context: self.update())
    
    tex_compression: bpy.props.BoolProperty(
        name="Compression Texture", description="Enable/Disable texture compression.",
        default=False, update=lambda self, context: self.update())

    particle: bpy.props.BoolProperty(
        name="Particle", description="Enable/Disable particles effects.",
        default=False, update=lambda self, context: self.update())
    
    tex_quality: bpy.props.EnumProperty(
        name="Quality Texture",  description="Texture resolution (0 to disable).",
        items=[
            ('0', 'Disabled', 'Disabled', '', 0), ('256', 'Low', 'Low', '', 1),
            ('512', 'Medium', 'Medium', '', 2), ('1024', 'High', 'High', '', 3),
            ], default='0', update=lambda self, context: self.update())
    
    lod: bpy.props.IntProperty(
        name="Level of Detail", description="Difine the Level Of Detail object",
        default=0, min=0, max=5, update=lambda self, context: self.update())
    
    render_driver: bpy.props.EnumProperty(
        name="Render Driver", description="Render driver to use (gl or directx9).",
        items=[
            ('gl', 'OpenGL', 'OpenGL', '', 0),
            ('directx9', 'DirectX9', 'DirectX9', '', 1),
            ('vulkan', 'Vulkan', 'Vulkan', '', 2),
            ], default='gl', update=lambda self, context: self.update())
    
    anisotropic: bpy.props.EnumProperty(
        name="Anisotropic", description="Anisotropic filtering quality (0 to disable) 2-4-8-16.",
        items=[
            ("0", "0", "0", "", 0),
            ("2", "2", "2", "", 1),
            ("4", "4", "4", "", 2),
            ("8", "8", "8", "", 3),
            ("16", "16", "16", "", 4),
        ], default="4", update=lambda self, context: self.update())
    
    render_superior: bpy.props.BoolProperty(
        name="Advenced", description="Enable/Disable advanced pipeline",
        default=False, update=lambda self, context: self.update())

    shadows: bpy.props.EnumProperty(
        name="Shadows",  description="Shadow resolution (0 to disable).",
        items=[
            ('0', 'Disabled', 'Disabled', '', 0),
            ('512', 'Low', 'Low', '', 1),
            ('1024', 'Medium', 'Medium', '', 2),
            ('2048', 'High', 'High', '', 3),
            #('4096', 'Very high', 'Very high', '', 4),
            ], default='0', update=lambda self, context: self.update())
    
    mlaa: bpy.props.BoolProperty(
        name="mlaa", description="Enable/Disable anti-aliasing.", 
        default=False, update=lambda self, context: self.update())
    
    light_scattering: bpy.props.BoolProperty(
        name="Light Scattering", description="Enable/Disable light scaterring.",
        default=False, update=lambda self, context: self.update())
    
    glow: bpy.props.BoolProperty(
        name="glow", description="Enable/Disable glow effect.",
        default=False, update=lambda self, context: self.update())
    
    ibl: bpy.props.BoolProperty(
        name="ibl", description="Enable/Disable image based lighting.",
        default=False, update=lambda self, context: self.update())
    
    light_shaft: bpy.props.BoolProperty(
        name="Light Shaft", description="Enable/Disable light shafts (God rays).",
        default=False, update=lambda self, context: self.update())
    
    bloom: bpy.props.BoolProperty(
        name="bloom", description="Enable/Disable bloom effect.",
        default=False, update=lambda self, context: self.update())
    
    ssao: bpy.props.BoolProperty(
        name="ssao", description="Enable/Disable screen space ambiant occlusion.",
        default=False, update=lambda self, context: self.update())

    ssr: bpy.props.BoolProperty(
        name="ssr", description="Enable/Disable screen space reflexion.",
        default=False, update=lambda self, context: self.update())


    motion_blur: bpy.props.BoolProperty(
        name="blur", description="Enable/Disable motion blur.",
        default=False, update=lambda self, context: self.update())

    dof: bpy.props.BoolProperty(
        name="dof", description="Enable/Disable depth of field.",
        default=False, update=lambda self, context: self.update())
    
    def init(self, context):
        self.node_input("NodeSocketString", "input_0", "", "")
        self.node_output('NodeSocketString', 'output_0', '', "")

    def draw_buttons(self, context, layout):
        box = layout.box()
        line = box.row()
        line.prop(self, "custom_graphic")
        if self.custom_graphic:
            line = layout.row()
            line.prop(self, "animation_kart")
            line.prop(self, "tex_compression")
            line = layout.row()
            line.prop(self, "particle")
            #layout.prop(self, "tex_quality")
            line.prop(self, "lod")
            line = box.row()
            line.prop(self, "render_superior")
            if self.render_superior:
                box = box.box()
                box.prop(self, "render_resolution")
                box.prop(self, "shadows")
                line = box.row()
                line.prop(self, "mlaa")
                line.prop(self, "light_scattering")
                line = box.row()
                line.prop(self, "glow")
                line.prop(self, "ibl")
                line = box.row()
                line.prop(self, "light_shaft")
                line.prop(self, "bloom")
                line = box.row()
                line.prop(self, "ssao")
                line.prop(self, "ssr")
                line = box.row()
                line.prop(self, "motion_blur")
                line.prop(self, "dof")
        else:
            line = box.row()
            line.prop(self, "gfx_preset")
            if self.gfx_preset >= 3:
                line = box.row()
                line.prop(self, "blur_level")
                line = box.row()
                line.prop(self, "render_resolution")
        layout.prop(self, "render_driver")
        layout.prop(self, "anisotropic")

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
            
            self.s_output += f" --render-driver={self.render_driver}"
            self.s_output += f" --anisotropic={self.anisotropic}"

            if self.custom_graphic:
                if self.render_superior:
                    self.s_output += f" --enable-dynamic-lights"
                    self.s_output += f" --shadows={self.shadows}"
                    if self.mlaa: self.s_output += f" --enable-mlaa"
                    else: self.s_output += f" --disable-mlaa"
                    if self.light_scattering: self.s_output += f" --enable-light-scatter"
                    else: self.s_output += f" --disable-light-scatter"
                    if self.glow: self.s_output += f" --enable-glow"
                    else: self.s_output += f" --disable-glow"
                    if self.ibl: self.s_output += f" --enable-ibl"
                    else: self.s_output += f" --disable-ibl"
                    if self.light_shaft: self.s_output += f" --enable-light-shaft"
                    else: self.s_output += f" --disable-light-shaft"
                    if self.bloom: self.s_output += f" --enable-bloom"
                    else: self.s_output += f" --disable-bloom"
                    if self.ssao: self.s_output += f" --enable-ssao"
                    else: self.s_output += f" --disable-ssao"
                    if self.ssr: self.s_output += f" --enable-ssr"
                    else: self.s_output += f" --disable-ssr"
                    if self.motion_blur: self.s_output += f" --enable-motion-blur"
                    else: self.s_output += f" --disable-motion-blur"
                    if self.dof: self.s_output += f" --enable-dof"
                    else: self.s_output += f" --disable-dof"
                    self.s_output += f" --rtt-scale={self.render_resolution}"
                else:
                    self.s_output += f" --disable-dynamic-lights"
                    self.s_output += f" --shadows=0"
                    self.s_output += f" --disable-mlaa"
                    self.s_output += f" --disable-light-scatter"
                    self.s_output += f" --disable-glow"
                    self.s_output += f" --disable-ibl"
                    self.s_output += f" --disable-light-shaft"
                    self.s_output += f" --disable-bloom"
                    self.s_output += f" --disable-ssao"
                    self.s_output += f" --disable-ssr"
                    self.s_output += f" --disable-motion-blur"
                    self.s_output += f" --disable-dof"
                    self.s_output += f" --rtt-scale=100"

                if self.animation_kart: self.s_output += f" --enable-animated-characters"
                else: self.s_output += f" --disable-animated-characters"
                if self.tex_compression: self.s_output += f" --enable-texture-compression"
                else: self.s_output += f" --disable-texture-compression"
                if self.particle: self.s_output += f" --enable-particles"
                else: self.s_output += f" --disable-particles"
                self.s_output += f" --geometry-level={self.lod}"
                
            else:
                self.s_output += f" --gfx-preset={self.gfx_preset}"
                if self.gfx_preset >= 3:
                    if self.blur_level == 2:
                        self.s_output += f" --enable-motion-blur"
                        self.s_output += f" --enable-dof"
                    elif self.blur_level == 1:
                        self.s_output += f" --enable-motion-blur"
                        self.s_output += f" --disable-dof"
                    else:
                        self.s_output += f" --disable-motion-blur"
                        self.s_output += f" --disable-dof"
                    self.s_output += f" --rtt-scale={self.render_resolution}"
                else:
                    self.s_output += f" --disable-motion-blur --disable-dof --rtt-scale=100"

            self.outputs[0].default_value = str(self.s_output)
        return self.s_output

    def update(self):
        self.process(bpy.context, None, None)
