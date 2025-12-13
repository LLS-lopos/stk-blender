import bpy

from ..moteur.AntarcticaRenderEngine import AntarcticaRenderEngine


class STKechantillonPanel(bpy.types.Panel):
    bl_idname = "STK_PT_echantillon"
    bl_label = "Échantillonnage"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.scene.render.engine == AntarcticaRenderEngine.bl_idname)

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='RENDER_STILL')

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        box.label(text="Qualité de rendu")

        # Échantillonnage
        col = box.column(align=True)
        # col.prop(scene.cycles, "samples", text="Échantillons")
        # col.prop(scene.cycles, "preview_samples", text="Aperçu")

        # Désactivation progressive
        box.prop(scene.cycles, "use_adaptive_sampling", text="Échantillonnage adaptatif")
        if scene.cycles.use_adaptive_sampling:
            col = box.column(align=True)
            # col.prop(scene.cycles, "adaptive_threshold", text="Seuil")
            # col.prop(scene.cycles, "adaptive_min_samples", text="Échantillons min")


class STKocclussionAmbiantPanel(bpy.types.Panel):
    bl_idname = "STK_PT_occlusion_ambiante"
    bl_label = "Occlusion ambiante"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.scene.render.engine == AntarcticaRenderEngine.bl_idname)

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='LIGHT')

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        box.prop(scene.world.light_settings, "use_ambient_occlusion", text="Activer")

        if scene.world.light_settings.use_ambient_occlusion:
            col = box.column()
            col.prop(scene.world.light_settings, "ao_factor", text="Facteur")
            col.prop(scene.world.light_settings, "distance", text="Distance")


class STKbloomPanel(bpy.types.Panel):
    bl_idname = "STK_PT_bloom"
    bl_label = "Effet Bloom"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.scene.render.engine == AntarcticaRenderEngine.bl_idname)

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='LIGHT_SUN')

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        box.prop(scene.eevee, "use_bloom", text="Activer Bloom")

        if scene.eevee.use_bloom:
            col = box.column()
            col.prop(scene.eevee, "bloom_threshold", text="Seuil")
            col.prop(scene.eevee, "bloom_knee", text="Transition")
            col.prop(scene.eevee, "bloom_radius", text="Rayon")
            col.prop(scene.eevee, "bloom_intensity", text="Intensité")
            col.prop(scene.eevee, "bloom_clamp", text="Valeur max")


class STKombrePanel(bpy.types.Panel):
    bl_idname = "STK_PT_ombres"
    bl_label = "Ombres"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.scene.render.engine == AntarcticaRenderEngine.bl_idname)

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='SHADING_RENDERED')

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        box.label(text="Qualité des ombres")

        col = box.column()
        col.prop(scene.eevee, "shadow_cube_size", text="Taille du cube")
        col.prop(scene.eevee, "shadow_cascade_size", text="Taille en cascade")

        # Nouvelle approche pour la gestion des ombres douces
        use_soft_shadows = getattr(scene.eevee, "use_soft_shadows", False)
        col.prop(scene.eevee, "use_soft_shadows", text="Ombres douces")

        if use_soft_shadows:
            # Pour Blender 3.6+ (shadow_softness_factor)
            if hasattr(scene.eevee, 'shadow_softness_factor'):
                col.prop(scene.eevee, "shadow_softness_factor", text="Doux")
            # Pour les versions antérieures (light_soft_size_scale)
            elif hasattr(scene.eevee, 'light_soft_size_scale'):
                col.prop(scene.eevee, "light_soft_size_scale", text="Doux")


class STKprofondeurDeChampPanel(bpy.types.Panel):
    bl_idname = "STK_PT_profondeur_champ"
    bl_label = "Profondeur de champ"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return (context.scene.render.engine == AntarcticaRenderEngine.bl_idname and context.scene.camera)

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon='CAMERA_DATA')

    def draw(self, context):
        layout = self.layout
        camera = context.scene.camera.data
        dof = camera.dof

        box = layout.box()
        box.prop(dof, "use_dof", text="Activer la profondeur de champ")

        if dof.use_dof:
            col = box.column()
            col.prop(dof, "focus_object", text="Cible")

            if dof.focus_object is None:
                col.prop(dof, "focus_distance", text="Distance de mise au point")

            col.prop(dof, "aperture_fstop", text="Ouverture (f/stop)")
            col.prop(dof, "aperture_blades", text="Lames")
            col.prop(dof, "aperture_rotation", text="Rotation")
            col.prop(dof, "aperture_ratio", text="Ratio")


"""
élément à ajouter pour les paramètre de rendu STK

échantillonnage
occlusion ambiante
flou lumineux (bloom)
ombre
profondeur de champ
"""
