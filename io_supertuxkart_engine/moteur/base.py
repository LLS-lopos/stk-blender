import bpy
import math
import mathutils
import gpu
from .eclairage.light import PointLight, AreaLight, SpotLight
import array
from gpu_extras.presets import draw_texture_2d
from gpu_extras.batch import batch_for_shader
from mathutils import Vector, Matrix

"""
def refract(incident, normal, n1, n2):
    # Calcule la direction du rayon réfracté
    n = n1 / n2
    cosI = -incident.dot(normal)
    sinT2 = n * n * (1.0 - cosI * cosI)
    
    if sinT2 > 1.0:  # Réflexion totale
        return None
    
    cosT = math.sqrt(1.0 - sinT2)
    return n * incident + (n * cosI - cosT) * normal
"""
class STKrendu(bpy.types.RenderEngine):
    bl_idname = "STKRENDER"
    bl_label = "SuperTuxKart Antarctica"
    bl_use_preview = True
    bl_use_gpu_context = True
    bl_use_shading_nodes = True
    bl_use_eevee_viewport = True

    def __init__(self):
        self.draw_handle = None
        self.draw_event = None
        self.texture = None
        self.scene_data = None
        self.draw_data = None
        self.batches = {}  # Cache pour les batches d'objets
        print("Initialisation du moteur de rendu STK")

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

    # Méthodes de rendu principales
    def render(self, depsgraph):
        """Méthode appelée pour le rendu final (F12)"""
        print("\n" + "="*80)
        print("DÉBUT DU RENDU FINAL (F12)")
        print("="*80)
        try:
            self.internal_render(depsgraph, is_viewport=False)
            print("\nRendu terminé avec succès!")
        except Exception as e:
            import traceback
            print("\nERREUR LORS DU RENDU:")
            print(traceback.format_exc())
            self.report({'ERROR'}, f"Erreur lors du rendu: {str(e)}")
        print("="*80 + "\n")

    def view_draw(self, context, depsgraph):
        """Méthode appelée pour le rendu dans la vue 3D"""
        if not self.draw_handle:
            self.setup_draw_handlers(context)
        try:
            self.internal_render(depsgraph, is_viewport=True)
        except Exception as e:
            import traceback
            print("\nERREUR LORS DU DESSIN DE LA VUE 3D:")
            print(traceback.format_exc())
            self.report({'ERROR'}, f"Erreur lors du dessin de la vue 3D: {str(e)}")

    def setup_draw_handlers(self, context):
        """Configure les gestionnaires de dessin pour la vue 3D"""
        if self.draw_handle:
            return

        # Créer un gestionnaire de dessin pour la vue 3D
        def draw():
            if not hasattr(self, 'texture') or not self.texture:
                return
            region = context.region
            draw_texture_2d(self.texture, (0, 0), region.width, region.height)

        self.draw_handle = bpy.types.SpaceView3D.draw_handler_add(
            draw, (), 'WINDOW', 'POST_PIXEL')

        # Mettre à jour le rendu quand la scène change
        def msgbus_callback(*args):
            if context.space_data == bpy.context.space_data:
                context.area.tag_redraw()

        subscribe_to = (
            bpy.types.LayerObjects,
            "active",
            "Camera",
            "data",
            "lighting",
            "display",
            "display_light",
            "display_options",
            "display_options.render_asset",
        )

        self.draw_event = bpy.msgbus.subscribe_rna(
            key=subscribe_to,
            owner=self,
            args=(),
            notify=msgbus_callback,
            options={"PERSISTENT"},
        )

    # Méthodes de rendu interne
    def internal_render(self, depsgraph, is_viewport=False):
        """Méthode de rendu interne partagée entre la vue et le rendu final"""
        print("Début du rendu...")
        scene = depsgraph.scene
        scale = scene.render.resolution_percentage / 100.0
        print(f"Résolution: {scene.render.resolution_x}x{scene.render.resolution_y} ({scale*100}%)")
        
        # Déterminer la taille du rendu
        if is_viewport:
            region = bpy.context.region
            width, height = region.width, region.height
        else:
            width = int(scene.render.resolution_x * scale)
            height = int(scene.render.resolution_y * scale)

        # Vérifier la caméra
        cam = scene.camera
        if not cam:
            error_msg = "Aucune caméra active trouvée"
            print(f"ERREUR: {error_msg}")
            self.report({'ERROR'}, error_msg)
            return
        print(f"Caméra utilisée: {cam.name}")

        # Créer ou mettre à jour la texture
        self.ensure_texture(width, height)

        # Rendu hors-écran
        with gpu.matrix.push_pop():
            print("Configuration des matrices de vue...")
            # Configurer la vue
            projection_matrix = cam.calc_matrix_camera(
                depsgraph,
                x=width,
                y=height,
                scale_x=1.0,
                scale_y=1.0,
            )
            
            modelview_matrix = cam.matrix_world.inverted()
            
            print("Configuration du contexte OpenGL...")
            # Activer le contexte de rendu
            gpu.state.depth_test_set('LESS_EQUAL')
            gpu.state.depth_mask(True)
            gpu.state.face_culling_set('BACK')
            
            # Vérifier le contexte OpenGL
            import gpu
            print(f"Contexte OpenGL: {gpu.platform.renderer_get()}")
            print(f"Version OpenGL: {gpu.platform.vendor_get()} {gpu.platform.version_get()}")
            
            # Créer un framebuffer hors-écran
            offscreen = gpu.types.GPUOffScreen(width, height)
            with offscreen.bind():
                fb = gpu.state.active_framebuffer_get()
                fb.clear(color=(0.1, 0.1, 0.1, 1.0))
                
                # Définir les matrices
                gpu.matrix.load_projection_matrix(projection_matrix)
                gpu.matrix.load_matrix(modelview_matrix)
                
                # Rendu de la scène
                self.render_scene(depsgraph, projection_matrix, modelview_matrix)
                
                # Lire le résultat dans la texture
                buffer = gpu.types.Buffer('FLOAT', (width * height * 4))
                fb.textures[0].read_into(buffer, format='FLOAT')
                self.texture.write('FLOAT', buffer.ravel())
            
            offscreen.free()

    def ensure_texture(self, width, height):
        """Crée ou met à jour la texture de rendu si nécessaire"""
        if (not hasattr(self, 'texture') or 
            not self.texture or 
            self.texture.width != width or 
            self.texture.height != height):
            
            if hasattr(self, 'texture') and self.texture:
                self.texture.free()
                
            self.texture = gpu.types.GPUTexture(
                (width, height),
                format='RGBA16F',
                data=gpu.types.Buffer('FLOAT', (width * height * 4), 
                                    [0.0] * (width * height * 4))
            )

    def render_scene(self, depsgraph, projection_matrix, modelview_matrix):
        """Rend les objets de la scène"""
        # Activer le shader de base
        shader = gpu.shader.from_builtin('3D_SMOOTH_COLOR')
        shader.bind()
        
        # Collecter toutes les lumières de la scène
        lights = []
        light_count = 0
        for obj_inst in depsgraph.object_instances:
            obj = obj_inst.object
            if obj.type == 'LIGHT':
                light_count += 1
                print(f"Traitement de la lumière: {obj.name} (type: {obj.data.type})")
                try:
                    if obj.data.type == 'POINT':
                        light = PointLight(
                            position=obj.matrix_world.translation,
                            color=obj.data.color,
                            energy=obj.data.energy,
                            radius=getattr(obj.data, 'shadow_soft_size', 0.2)
                        )
                        lights.append(light)
                        print(f"  - Point light ajoutée: pos={light.position}, energy={light.energy}")
                    elif obj.data.type == 'SUN':
                        light = AreaLight(
                            direction=obj.matrix_world.to_3x3() @ mathutils.Vector((0, 0, -1)),
                            color=obj.data.color,
                            energy=obj.data.energy
                        )
                        lights.append(light)
                        print(f"  - Sun light ajoutée: dir={light.direction}, energy={light.energy}")
                    elif obj.data.type == 'SPOT':
                        light = SpotLight(
                            position=obj.matrix_world.translation,
                            direction=obj.matrix_world.to_3x3() @ mathutils.Vector((0, 0, -1)),
                            color=obj.data.color,
                            energy=obj.data.energy,
                            spot_size=getattr(obj.data, 'spot_size', math.pi/4),
                            spot_blend=getattr(obj.data, 'spot_blend', 0.15)
                        )
                        lights.append(light)
                        print(f"  - Spot light ajoutée: pos={light.position}, angle={light.spot_size:.2f} rad")
                except Exception as e:
                    print(f"  ERREUR lors du traitement de la lumière {obj.name}: {str(e)}")
        
        print(f"{len(lights)} lumières trouvées sur {light_count} objets de type LIGHT")
        
        # Parcourir tous les objets visibles pour le rendu
        object_count = 0
        rendered_count = 0
        for obj_inst in depsgraph.object_instances:
            obj = obj_inst.object
            object_count += 1
            
            # Ignorer les types d'objets non supportés
            if obj.type not in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META'}:
                print(f"Objet ignoré (type non supporté): {obj.name} ({obj.type})")
                continue
                
            # Obtenir ou créer le batch pour cet objet
            print(f"Traitement de l'objet: {obj.name} (type: {obj.type})")
            try:
                batch = self.get_batch(obj)
                if not batch:
                    print(f"  - Aucun batch créé pour {obj.name}")
                    continue
                rendered_count += 1
            except Exception as e:
                print(f"  ERREUR lors de la création du batch pour {obj.name}: {str(e)}")
                continue
            
            # Matrice modèle
            model_matrix = obj_inst.matrix_world
            mvp = projection_matrix @ modelview_matrix @ model_matrix
            
            # Définir les uniformes
            shader.uniform_float("modelViewProjectionMatrix", mvp)
            
            # Définir la couleur de base
            if obj.active_material:
                color = obj.active_material.diffuse_color
                shader.uniform_float("color", (*color[:3], 1.0))
            else:
                shader.uniform_float("color", (0.8, 0.8, 0.8, 1.0))
            
            # Pour une implémentation complète, nous devrions calculer l'éclairage
            # pour chaque sommet/fragment en fonction des lumières collectées
            # Ceci est une simplification qui utilise juste la couleur de base
            
            # Dessiner l'objet
            batch.draw(shader)

    def get_batch(self, obj):
        """Crée ou récupère un batch GPU pour l'objet"""
        # Utiliser le cache si disponible
        if obj.name in self.batches:
            print(f"  - Utilisation du batch en cache pour {obj.name}")
            return self.batches[obj.name]
            
        # Créer un nouveau batch
        try:
            print(f"  - Création d'un nouveau batch pour {obj.name}")
            
            # Vérifier si l'objet a des données de maillage
            if not hasattr(obj, 'data') or not hasattr(obj.data, 'vertices'):
                print(f"  - L'objet {obj.name} n'a pas de données de maillage valides")
                return None
                
            # Convertir en mesh si nécessaire
            print(f"  - Conversion de l'objet en mesh...")
            mesh = obj.to_mesh()
            if not mesh:
                print(f"  - Impossible de convertir l'objet {obj.name} en mesh")
                return None
                
            # Vérifier les données du maillage
            print(f"  - Maillage converti: {len(mesh.vertices)} sommets, {len(mesh.polygons)} faces")
            
            # Créer les données de vertex
            vertices = [v.co for v in mesh.vertices]
            indices = []
            
            # Créer les indices pour les faces
            for poly in mesh.polygons:
                indices.extend(poly.vertices)
                
            print(f"  - Données préparées: {len(vertices)} sommets, {len(indices)} indices")
            
            # Créer le batch
            print("  - Création du batch GPU...")
            shader = gpu.shader.from_builtin('3D_SMOOTH_COLOR')
            batch = batch_for_shader(
                shader,
                'TRIS',
                {"pos": vertices},
                indices=indices if indices else None
            )
            
            # Mettre en cache le batch
            self.batches[obj.name] = batch
            print(f"  - Batch créé avec succès pour {obj.name}")
            return batch
            
        except Exception as e:
            import traceback
            print(f"  ERREUR lors de la création du batch pour {obj.name}: {str(e)}")
            print("  Stack trace:")
            print(traceback.format_exc())
            return None
        finally:
            # Nettoyer le mesh temporaire
            if 'mesh' in locals() and mesh is not None:
                print("  - Nettoyage du mesh temporaire")
                obj.to_mesh_clear()
"""
class CustomDessinDonner:
    def __init__(self, dimensions):
        import gpu

        # Génère un tampon d'image flottant factice
        self.dimensions = dimensions
        width, height = dimensions

        pixels = width * height * array.array('f', [0.1, 0.1, 0.1, 1.0])
        pixels = gpu.types.Buffer('FLOAT', width * height * 4, pixels)

        # Génère une texture
        self.texture = gpu.types.GPUTexture((width, height), format='RGBA16F', data=pixels)

        # Note : Ceci est juste un exemple didactique.
        # Dans ce cas, il serait plus pratique de remplir la texture avec :
        # self.texture.clear('FLOAT', value=[0.1, 0.2, 0.1, 1.0])

    def __del__(self):
        del self.texture

    def draw(self):
        draw_texture_2d(self.texture, (0, 0), self.texture.width, self.texture.height)

class STKrenduGPU(bpy.types.RenderEngine):
    bl_idname = "STKRENDERGPU"
    bl_label = "SupertuxkartGPU"

    # Demande la création et l'activation d'un contexte GPU pour la méthode de rendu.
    # Cela peut être utilisé soit pour effectuer le rendu lui-même, soit pour allouer
    # et remplir une texture pour un dessin plus efficace.
    bl_use_gpu_context = True

    def render(self, depsgraph):
        # Importation différée du module GPU, car le contexte GPU n'est créé qu'à la demande
        # pour le rendu et n'existe pas lors de l'enregistrement.
        #import gpu

        # Effectue la tâche de rendu.
        pass
"""
# Les moteurs de rendu doivent également indiquer avec quels panneaux d'interface ils sont compatibles.
# Nous recommandons d'activer tous les panneaux marqués comme BLENDER_RENDER, puis
# d'exclure les panneaux qui sont remplacés par des panneaux personnalisés enregistrés par
# le moteur de rendu, ou qui ne sont pas pris en charge.
def get_panels():
    exclude_panels = {
        'VIEWLAYER_PT_filter',
        'VIEWLAYER_PT_layer_passes',
    }

    panels = []
    for panel in bpy.types.Panel.__subclasses__():
        if hasattr(panel, 'COMPAT_ENGINES') and 'BLENDER_RENDER' in panel.COMPAT_ENGINES:
            if panel.__name__ not in exclude_panels:
                panels.append(panel)

    return panels
