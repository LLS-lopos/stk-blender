import bpy

from ..moteur.AntarcticaRenderEngine import AntarcticaRenderEngine


class STKsortiePanel(bpy.types.Panel):
    bl_idname = "STK_PT_sortie"
    bl_label = "sortie"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.scene.render.engine == AntarcticaRenderEngine.bl_idname)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="sortie")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rd = scene.render

        box = layout.box()

        # Options de sortie
        box.prop(rd.image_settings, "file_format", text="Format")

        # Format de sortie
        box.prop(rd, "use_file_extension", text="Utiliser l'extension de fichier")
        box.prop(rd, "filepath", text="")

        # Afficher les options spécifiques au format sélectionné
        if rd.image_settings.file_format in {'PNG', 'BMP', 'TARGA'}:
            box.prop(rd.image_settings, "color_mode", text="Couleur")
            if rd.image_settings.file_format == 'PNG':
                box.prop(rd.image_settings, "compression")
        elif rd.image_settings.file_format in {'JPEG', 'JPEG2000'}:
            box.prop(rd.image_settings, "quality")
            if rd.image_settings.file_format == 'JPEG2000':
                box.prop(rd.image_settings, "jpeg2k_codec")


class STKfomatPanel(bpy.types.Panel):
    bl_idname = "STK_PT_format_panel"
    bl_label = "Format STK"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.scene.render.engine == AntarcticaRenderEngine.bl_idname)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="Format")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rd = scene.render

        box = layout.box()
        box.label(text="Format de sortie")

        # Résolution
        col = box.column(align=True)
        col.prop(rd, "resolution_x", text="RésolutionX largeur")
        col.prop(rd, "resolution_y", text="RésolutionY hauteur")
        col.prop(rd, "resolution_percentage", text="%")

        # Format de l'image
        box.prop(rd, "pixel_aspect_x", text="Ratio X")
        box.prop(rd, "pixel_aspect_y", text="Ratio Y")


class STKframePanel(bpy.types.Panel):
    bl_idname = "STK_PT_frame_panel"
    bl_label = "Animation STK"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.scene.render.engine == AntarcticaRenderEngine.bl_idname)

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="Frame")

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Section Animation
        box = layout.box()
        box.label(text="Animation")
        box.prop(scene, "frame_start", text="Début")
        box.prop(scene, "frame_end", text="Fin")
        box.prop(scene, "frame_step", text="Saut")


"""
élément à ajouter pour les paramètre de rendu STK

format
intervalle de frames
sortie
métadonnées
"""
