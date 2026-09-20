#!BPY

# Copyright (c) 2020 SuperTuxKart author(s)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import bpy
from bpy.types import Menu, GeometryNodeCustomGroup


class STKNodeMenu(Menu):
    bl_idname = "STK_MT_NodeMenu"
    bl_label = "SuperTuxKart"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("node.add_node", text="STK Particles").type = STKparticles.bl_idname


class Point(object):
    __slots__ = ('position', 'rotation', 'scale')

    def __init__(self, position, rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0)):
        self.position = tuple(position)[:3]
        if hasattr(rotation, 'to_euler'):
            rotation = rotation.to_euler()
        if hasattr(scale, 'to_vector'):
            scale = scale.to_vector()
        self.rotation = tuple(
            (rotation[0], rotation[1], rotation[2])
            if hasattr(rotation, '__len__') and len(rotation) >= 3
            else (0.0, 0.0, 0.0))
        self.scale = tuple(
            (scale[0], scale[1], scale[2])
            if hasattr(scale, '__len__') and len(scale) >= 3
            else (float(scale), float(scale), float(scale))
            if isinstance(scale, (int, float))
            else (1.0, 1.0, 1.0))

    def __len__(self):
        return 9

    def __getitem__(self, index):
        if index < 3:
            return self.position[index]
        if index < 6:
            return self.rotation[index - 3]
        return self.scale[index - 6]

    def __iter__(self):
        for v in self.position[:3] + self.rotation[:3] + self.scale[:3]:
            yield v

    def __repr__(self):
        return "Point(pos=%r, rot=%r, scale=%r)" % (
            self.position, self.rotation, self.scale)


def _make_duplicate(src_obj, name, point):
    obj = src_obj.copy()
    try:
        obj.data = src_obj.data.copy()
    except Exception:
        pass
    obj.name = name
    obj.matrix_basis = src_obj.matrix_basis
    obj.location = point.position
    obj.rotation_euler = point.rotation
    obj.scale = point.scale
    return obj

def _read_attr(mesh, name):
    """Lit un attribut nommé du mesh (ex: rotation/scale), None si absent."""
    if mesh.attributes is None:
        return None
    attr = mesh.attributes.get(name)
    if attr is None:
        return None
    values = []
    for item in attr.data:
        try:
            values.append(tuple(item.vector))
        except Exception:
            try:
                v = item.value
                if hasattr(v, '__len__'):
                    values.append(tuple(v))
                else:
                    values.append((v, v, v))
            except Exception:
                values.append((0.0, 0.0, 0.0))
    return values

def dump_mesh(obj, evaluate=True, limit=10):
    """Affiche dans la console mesh, sommets et attributs d'un objet."""
    try:
        if evaluate:
            dg = bpy.context.evaluated_depsgraph_get()
            ev = dg.objects.get(obj.name, obj)
        else:
            ev = obj
        mesh = ev.to_mesh()
        if mesh is None:
            print("dump_mesh: pas de mesh évalué")
            return None
        try:
            print(f"obj={ev.name} type={getattr(mesh, 'type', '?')} "
                  f"verts={len(mesh.vertices)} edges={len(mesh.edges)} polys={len(mesh.polygons)}")
            for a in mesh.attributes:
                vals = [d for d in list(a.data)[:limit]]
                print(f"  attr '{a.name}' type={a.data_type} domain={a.domain} values={vals}")
            for i, v in enumerate(mesh.vertices[:limit]):
                print(f"  vert {i} pos={tuple(v.co)}")
            return mesh
        finally:
            try:
                ev.to_mesh_clear()
            except Exception:
                pass
    except Exception as exc:
        print(f"dump_mesh: erreur : {exc}")
        return None


class STKparticles(GeometryNodeCustomGroup):
    bl_idname = 'STKNodeParticles'
    bl_label = 'STK Particles'
    bl_icon = 'NONE'

    def init(self, context):
        self.node_tree = bpy.data.node_groups.new('STKParticles', 'GeometryNodeTree')

        # Définir les inputs/outputs du groupe
        self.node_tree.inputs.new('NodeSocketGeometry', 'Points')
        self.node_tree.inputs.new('NodeSocketObject', 'Object')
        self.node_tree.inputs.new('NodeSocketVector', 'Rotation')
        self.node_tree.inputs.new('NodeSocketFloat', 'Scale Min')
        self.node_tree.inputs.new('NodeSocketFloat', 'Scale Max')
        self.node_tree.inputs.new('NodeSocketInt', 'Random Scale')

        self.node_tree.outputs.new('NodeSocketGeometry', "Geometry")

        # define init value
        self.inputs["Scale Max"].default_value = 1

        # Node Internes
        nodes = self.node_tree.nodes

        ## groupe inputs
        group_input = nodes.new('NodeGroupInput')
        group_input.location = (-600, 0)

        ## stocker attribut rotation
        st_rot = nodes.new('GeometryNodeStoreNamedAttribute')
        st_rot.location = (-400, 150)
        st_rot.data_type = 'FLOAT_VECTOR'
        st_rot.domain = 'POINT'
        st_rot.inputs[2].default_value = 'rotation'

        ## stocker attribut scale
        st_scale = nodes.new('GeometryNodeStoreNamedAttribute')
        st_scale.location = (-200, 150)
        st_scale.data_type = 'FLOAT'
        st_scale.domain = 'POINT'
        st_scale.inputs[2].default_value = 'scale'

        ## random value scale
        random_scale = nodes.new('FunctionNodeRandomValue')
        random_scale.label = 'STK random scale'
        random_scale.location = (-400, -100)
        random_scale.data_type = 'FLOAT'

        ## mesh ligne
        mesh_line = nodes.new('GeometryNodeMeshLine')
        mesh_line.mode = 'OFFSET'
        mesh_line.location = (-200, -100)
        mesh_line.inputs[0].default_value = 2
        mesh_line.inputs[2].default_value = (0.0, 0.0, 0.0)
        mesh_line.inputs[3].default_value = (0.0, 0.0, 0.0)

        ## instance on point
        inst_on_pts = nodes.new('GeometryNodeInstanceOnPoints')
        inst_on_pts.location = (0, 150)

        ## realize instance
        realize = nodes.new('GeometryNodeRealizeInstances')
        realize.location = (200, 150)

        ## indice
        index_node = nodes.new('GeometryNodeInputIndex')
        index_node.location = (0, -200)

        ## math modulo
        math_mod = nodes.new('ShaderNodeMath')
        math_mod.operation = 'MODULO'
        math_mod.location = (200, -100)
        math_mod.inputs[1].default_value = 2

        ## delete geometry
        delete_geo = nodes.new('GeometryNodeDeleteGeometry')
        delete_geo.domain = 'POINT'
        delete_geo.mode = 'ALL'
        delete_geo.location = (400, 150)

        ## groupe outputs
        group_output = nodes.new('NodeGroupOutput')
        group_output.location = (600, 0)

        # Relier les node
        self.links = self.node_tree.links

        self.links.new(st_rot.inputs['Geometry'], group_input.outputs['Points'])
        self.links.new(st_scale.inputs['Geometry'], st_rot.outputs[0])
        self.links.new(inst_on_pts.inputs['Points'], st_scale.outputs[0])
        self.links.new(st_rot.inputs[3], group_input.outputs['Rotation'])
        self.links.new(random_scale.inputs[2], group_input.outputs['Scale Min'])
        self.links.new(random_scale.inputs[3], group_input.outputs['Scale Max'])
        self.links.new(random_scale.inputs[8], group_input.outputs['Random Scale'])
        self.links.new(st_scale.inputs[4], random_scale.outputs[1])
        self.links.new(inst_on_pts.inputs['Instance'], mesh_line.outputs['Mesh'])
        self.links.new(inst_on_pts.inputs['Rotation'], group_input.outputs['Rotation'])
        self.links.new(realize.inputs['Geometry'], inst_on_pts.outputs['Instances'])
        self.links.new(delete_geo.inputs['Geometry'], realize.outputs['Geometry'])
        self.links.new(math_mod.inputs[0], index_node.outputs[0])
        self.links.new(delete_geo.inputs['Selection'], math_mod.outputs[0])
        self.links.new(group_output.inputs['Geometry'], delete_geo.outputs[0])

    def draw_buttons(self, context, layout):
        op = layout.operator("stk.geo_node", text="teste modal", icon='NONE')
        op.node_name = self.name
        
        obj = self.resolve_object()
        op.obj_lib = obj.name if obj is not None else ""

    def fetch_points(self, context):
        if context is None:
            return []
        try:
            dg = context.evaluated_depsgraph_get()
        except Exception:
            return []
        tree_name = self.id_data.name
        matched = None
        candidates = []
        for ev_obj in dg.objects:
            for mod in ev_obj.modifiers:
                if mod.type != 'NODES':
                    continue
                ng = getattr(mod, 'node_group', None)
                if ng is None:
                    continue
                is_match = ng == self.id_data or (
                    ng.name == tree_name and
                    any(n.bl_idname == STKparticles.bl_idname for n in ng.nodes))
                candidates.append((ev_obj.name, ng.name, bool(is_match)))
                if is_match:
                    matched = ev_obj
        if matched is None:
            return []
        return self._points_from_object(matched, dg)

    def _points_from_object(self, ev_obj, dg):
        mesh = None
        try:
            mesh = ev_obj.to_mesh()
        except Exception:
            mesh = None
        if mesh is None:
            try:
                mesh = ev_obj.to_mesh(depsgraph=dg)
            except Exception:
                mesh = None
        if mesh is not None:
            try:
                verts = list(mesh.vertices)
                rotation = _read_attr(mesh, 'rotation')
                scale = _read_attr(mesh, 'scale')
                if verts:
                    out = []
                    for i, v in enumerate(verts):
                        rot = rotation[i] if rotation is not None else (0.0, 0.0, 0.0)
                        scl = scale[i] if scale is not None else (1.0, 1.0, 1.0)
                        out.append(Point(ev_obj.matrix_world @ v.co, rot, scl))
                    return out
            finally:
                try:
                    ev_obj.to_mesh_clear()
                except Exception:
                    pass
        try:
            data = ev_obj.data
            if data and getattr(data, 'type', '') == 'POINTCLOUD':
                pts = list(data.points)
                if pts:
                    return [
                        Point(p.position, p.rotation, p.scale)
                        for p in pts
                    ]
        except Exception:
            pass
        return []

    def _owner_modifier(self):
        """Retourne le modifier Geometry Nodes dont le groupe = self.id_data."""
        tree = self.id_data
        if tree is None:
            return None
        for obj in bpy.data.objects:
            for mod in obj.modifiers:
                if mod.type != 'NODES':
                    continue
                if getattr(mod, 'node_group', None) == tree:
                    return mod
        return None

    def _read_input(self, mod, name, default=None):
        """Lit la valeur d'un input du modifier, mémorisée par identifier."""
        ng = getattr(mod, 'node_group', None)
        if ng is None:
            return default
        try:
            items = ng.inputs
        except Exception:
            items = getattr(ng, 'interface', None)
            if items is not None:
                items = [
                    it for it in items.items_tree
                    if getattr(it, 'item_type', None) == 'SOCKET'
                    and getattr(it, 'in_out', None) == 'INPUT']
            else:
                items = []
        for item in items:
            if getattr(item, 'name', None) != name:
                continue
            ident = getattr(item, 'identifier', None)
            if ident is not None:
                try:
                    return mod[ident]
                except (KeyError, TypeError):
                    pass
            return getattr(item, 'default_value', default)
        return default

    def resolve_object(self):
        mod = self._owner_modifier()
        if mod is not None:
            obj = self._read_input(mod, 'Object')
            if obj is not None:
                return obj
        if self.inputs[1].is_linked and hasattr(self.inputs[1].links[0].from_socket, 'default_value'):
            return self.inputs[1].links[0].from_socket.default_value
        try:
            return self.inputs[1].default_value
        except Exception:
            return None

    def process(self, context, id, path):
        obj = self.resolve_object()
        if obj is not None:
            print(f"STK [{self.name}] Object UI: {obj.name}")
        else:
            print(f"STK [{self.name}] Object UI: aucun objet défini")

        if context is None:
            return []
        
        points = self.fetch_points(context)
        count = len(points)
        
        if count == 0 and getattr(self, '_warned_zero', False) is False:
            self._warned_zero = True
            print(f"STK Particles [{self.name}]: 0 points")

        if count != getattr(self, '_last_count', -1):
            self._last_count = count
            self._cached_points = list(points)
            for i, pt in enumerate(points):
                print(f"STK [{self.name}] pt{i}: pos={pt.position} rot={pt.rotation} scale={pt.scale}")

        return points

    def update(self):
        self.process(bpy.context, None, None)

class ListePoint(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Point", default="IDK")

    loc: bpy.props.FloatVectorProperty(name="location", default=(0.0, 0.0, 0.0))
    rot: bpy.props.FloatVectorProperty(name="rotation", default=(0.0, 0.0, 0.0))
    scale: bpy.props.FloatVectorProperty(name="scale", default=(0.0, 0.0, 0.0))

class CheckActif(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "stk.geo_node"
    bl_label = "CHECK Actif"

    node_name: bpy.props.StringProperty(default="")
    point: bpy.props.CollectionProperty(type=ListePoint)
    obj_lib: bpy.props.StringProperty(default="")

    def _resolve_node(self, context):
        node = None
        if self.node_name:
            space = getattr(context, 'space_data', None)
            tree = getattr(space, 'node_tree', None) if space else None
            if tree is not None and self.node_name in tree.nodes:
                node = tree.nodes[self.node_name]
        if node is None or node.bl_idname != STKparticles.bl_idname:
            return None
        return node

    def modal(self, context, event):
        return {'FINISHED'}

    def invoke(self, context, event):
        if context.object:
            node = self._resolve_node(context)
            if node is None:
                self.report({'WARNING'}, "Aucun node STK Particles trouvé")
                return {'CANCELLED'}
            points = node.fetch_points(context)
            count = len(points)
            if count != getattr(node, '_last_count', -1):
                node._last_count = count
                node._cached_points = list(points)
                self.point.clear()
                for p in points:
                    item = self.point.add()
                    item.name = f"LIBSTK_P_{self.obj_lib}_{len(self.point) - 1}"
                    item.loc = p.position
                    item.rot = p.rotation
                    item.scale = p.scale
                self.report({'INFO'}, f"{count} points récupérés de {node.name}")
            for i in self.point:
                self.report({'INFO'}, 
                            f"nom: {i.name}, loc: {i.loc[0], i.loc[1], i.loc[2]},"
                            f"rot: {i.rot[0], i.rot[1], i.rot[2]},"
                            f"scale: {i.scale[0], i.scale[1], i.scale[2]}")
                pt = Point((i.loc[0], i.loc[1], i.loc[2]),
                            (i.rot[0], i.rot[1], i.rot[2]),
                            (i.scale[0], i.scale[1], i.scale[2]))
                dup = _make_duplicate(bpy.data.objects[self.obj_lib], i.name, pt)
                try:
                    bpy.context.scene.collection.objects.link(dup)
                except Exception:
                    pass

            else:
                self.report({'INFO'}, "compte inchangé, rien à récupérer")

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}