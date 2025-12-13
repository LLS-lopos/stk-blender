# Antarctica Render Engine
import array

import bpy
import gpu
from gpu_extras.presets import draw_texture_2d


class AntarcticaRenderEngine(bpy.types.RenderEngine):
    # These three members are used by blender to set up the
    # RenderEngine; define its internal name, visible name and capabilities.
    bl_idname = "STKRENDER"
    bl_label = "Antarctica"
    bl_use_preview = True
    bl_use_gpu_context = True
    bl_use_shading_nodes_custom = False

    # Init is called whenever a new render engine instance is created. Multiple
    # instances may exist at the same time, for example for a viewport and final
    # render.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = None
        self.scene_data = None
        self.draw_data = None

    # When the render engine instance is destroy, this is called. Clean up any
    # render engine data here, for example stopping running render threads.
    def __del__(self):
        """Nettoyage des ressources"""
        try:
            self.free()
        except Exception as e:
            print(f"Erreur lors du nettoyage des ressources: {e}")

    def free(self):
        """Libère les ressources GPU"""
        print("Libération des ressources GPU...")

        # Nettoyage du gestionnaire de dessin
        if hasattr(self, 'draw_handle') and self.draw_handle:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle, 'WINDOW')
                self.draw_handle = None
                print("Gestionnaire de dessin supprimé")
            except Exception as e:
                print(f"Erreur lors de la suppression du gestionnaire de dessin: {e}")

        # Nettoyage de l'événement
        if hasattr(self, 'draw_event') and self.draw_event:
            try:
                bpy.msgbus.clear_by_owner(self.draw_event)
                self.draw_event = None
                print("Événement de dessin nettoyé")
            except Exception as e:
                print(f"Erreur lors du nettoyage de l'événement de dessin: {e}")

        # Libération de la texture
        if hasattr(self, 'texture') and self.texture:
            try:
                self.texture.free()
                self.texture = None
                print("Texture libérée")
            except Exception as e:
                print(f"Erreur lors de la libération de la texture: {e}")

        # Nettoyage des batches
        if hasattr(self, 'batches'):
            self.batches.clear()
            print("Cache des batches vidé")

    # This is the method called by Blender for both final renders (F12) and
    # small preview for materials, world and lights.
    def render(self, depsgraph):
        scene = depsgraph.scene
        scale = scene.render.resolution_percentage / 100.0
        self.size_x = int(scene.render.resolution_x * scale)
        self.size_y = int(scene.render.resolution_y * scale)

        # Fill the render result with a flat color. The framebuffer is
        # defined as a list of pixels, each pixel itself being a list of
        # R,G,B,A values.
        if self.is_preview:
            color = [0.1, 0.2, 0.1, 1.0]
        else:
            color = [0.2, 0.1, 0.1, 1.0]

        pixel_count = self.size_x * self.size_y
        rect = [color] * pixel_count

        # Here we write the pixel values to the RenderResult
        result = self.begin_result(0, 0, self.size_x, self.size_y)
        layer = result.layers[0].passes["Combined"]
        layer.rect = rect
        self.end_result(result)

    # For viewport renders, this method gets called once at the start and
    # whenever the scene or 3D viewport changes. This method is where data
    # should be read from Blender in the same thread. Typically a render
    # thread will be started to do the work while keeping Blender responsive.
    def view_update(self, context, depsgraph):
        region = context.region
        view3d = context.space_data
        scene = depsgraph.scene

        # Get viewport dimensions
        dimensions = region.width, region.height

        if not self.scene_data:
            # First time initialization
            self.scene_data = []
            first_time = True

            # Loop over all datablocks used in the scene.
            for datablock in depsgraph.ids:
                pass
        else:
            first_time = False

            # Test which datablocks changed
            for update in depsgraph.updates:
                print("Datablock updated: ", update.id.name)

            # Test if any material was added, removed or changed.
            if depsgraph.id_type_updated('MATERIAL'):
                print("Materials updated")

        # Loop over all object instances in the scene.
        if first_time or depsgraph.id_type_updated('OBJECT'):
            for instance in depsgraph.object_instances:
                pass

    # For viewport renders, this method is called whenever Blender redraws
    # the 3D viewport. The renderer is expected to quickly draw the render
    # with OpenGL, and not perform other expensive work.
    # Blender will draw overlays for selection and editing on top of the
    # rendered image automatically.
    def view_draw(self, context, depsgraph):
        region = context.region
        scene = depsgraph.scene

        # Get viewport dimensions
        dimensions = region.width, region.height

        # Bind shader that converts from scene linear to display space,
        gpu.state.blend_set('ALPHA_PREMULT')
        self.bind_display_space_shader(scene)

        if not self.draw_data or self.draw_data.dimensions != dimensions:
            self.draw_data = CustomDrawData(dimensions)

        self.draw_data.draw()

        self.unbind_display_space_shader()
        gpu.state.blend_set('NONE')

    # final render
    def update(self, data, depsgraph):
        pass


class CustomDrawData:
    def __init__(self, dimensions):
        # Generate dummy float image buffer
        self.dimensions = dimensions
        width, height = dimensions

        pixels = width * height * array.array('f', [0.1, 0.2, 0.1, 1.0])
        pixels = gpu.types.Buffer('FLOAT', width * height * 4, pixels)

        # Generate texture
        self.texture = gpu.types.GPUTexture((width, height), format='RGBA16F', data=pixels)

        # Note: This is just a didactic example.
        # In this case it would be more convenient to fill the texture with:
        # self.texture.clear('FLOAT', value=[0.1, 0.2, 0.1, 1.0])

    def __del__(self):
        del self.texture

    def draw(self):
        draw_texture_2d(self.texture, (0, 0), self.texture.width, self.texture.height)
