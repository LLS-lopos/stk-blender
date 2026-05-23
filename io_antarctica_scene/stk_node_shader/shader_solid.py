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

# =============================================================================
# STK Solid + Full Lighting (combines sun + IBL + fog in gpu_extras)
# =============================================================================

import bpy

from bpy.types import ShaderNodeCustomGroup
from .shader_base import ShaderStkBase

_SOLID_GROUP = ".ShaderStkSolid_Group"

def _get_group():
    group = bpy.data.node_groups.get(_SOLID_GROUP)
    if group is not None:
        return group
    
    # définition du group de propriété personalisé (entré/sortie)
    group = bpy.data.node_groups.new(_SOLID_GROUP, "ShaderNodeTree")

    """# On définit ses entrées (prises d'entrée)
    group.inputs.new("NodeSocketColor", "Color")
    group.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    # R = rugosité | V = metal | B = emission
    group.inputs.new("NodeSocketColor", "Glossy_Map")
    group.inputs["Glossy_Map"].default_value = (1.0, 0.0, 0.0, 1.0)
    group.inputs["Glossy_Map"].description = "R for rougness, G for metal, B for emmision"
    group.inputs.new("NodeSocketVector", "Normal")

    # On définit sa sortie (prise de sortie)
    group.outputs.new("NodeSocketShader", "PBR Solid")

    # On crée les sockets visible
    nodes = group.nodes

    entrer = nodes.new("NodeGroupInput")
    entrer.location = (-800, 0)

    sortie = nodes.new("NodeGroupOutput")
    sortie.location = (600, 0)

    # On crée les nœuds interne
    glossy_separator = nodes.new("ShaderNodeSeparateRGB")
    glossy_separator.location = (-600, 0)

    # On connecte les nœuds entre eux
    links = group.links
    links.new(entrer.outputs["Color"], sortie.inputs["PBR Solid"])
    # On retourne le groupe tout prêt"""
    group.inputs.new("NodeSocketColor", "Diffuse")
    group.inputs.new("NodeSocketColor", "PBR Data")
    group.inputs.new("NodeSocketVector", "Normal")
    group.inputs.new("NodeSocketColor", "Vertex Color")
    group.outputs.new("NodeSocketShader", "BSDF")

    nodes = group.nodes
    group_input = nodes.new("NodeGroupInput")
    group_input.location = (-800, 0)
    
    group_output = nodes.new("NodeGroupOutput")
    group_output.location = (600, 0)

    separate = nodes.new("ShaderNodeSeparateRGB")
    separate.location = (-400, 100)

    multiply = nodes.new("ShaderNodeMixRGB")
    multiply.blend_type = 'MULTIPLY'
    multiply.inputs[0].default_value = 1.0
    multiply.location = (-200, -100)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (200, 0)
    bsdf.inputs["Roughness"].default_value = 0.5

    spec_input = bsdf.inputs.get("Specular IOR Level") or bsdf.inputs.get("Specular")

    links = group.links
    links.new(group_input.outputs["PBR Data"], separate.inputs[0])
    links.new(separate.outputs[0], spec_input)
    links.new(separate.outputs[1], bsdf.inputs["Metallic"])
    links.new(separate.outputs[2], bsdf.inputs["Emission Strength"])
    links.new(group_input.outputs["Diffuse"], multiply.inputs[1])
    links.new(group_input.outputs["Vertex Color"], multiply.inputs[2])
    links.new(multiply.outputs[0], bsdf.inputs["Base Color"])
    links.new(multiply.outputs[0], bsdf.inputs["Emission"])
    links.new(group_input.outputs["Normal"], bsdf.inputs["Normal"])
    links.new(bsdf.outputs[0], group_output.inputs["BSDF"])
    return group


def _free_group():
    group = bpy.data.node_groups.get(_SOLID_GROUP)
    if group is not None:
        bpy.data.node_groups.remove(group)


class ShaderStkSolid(ShaderNodeCustomGroup, ShaderStkBase):
    bl_idname = 'ShaderStkSolid'
    bl_label = 'STK Solid'
    bl_icon = 'MATERIAL'

    def init(self, context):
        self.node_tree = _get_group()

    def draw_buttons(self, context, layout):
        pass
    
    def gpu_extras(self, context):
        return {
            'vertex': '''
                // --- STK sp_pass.vert adapted for Eevee ---
                // Uses Blender built-in uniforms:
                //   ModelViewProjectionMatrix, ModelMatrix, NormalMatrix
                //   viewMatrix (mat4), projMatrix (mat4)

                in vec3 pos;
                in vec3 normal;
                in vec4 vert_color;
                in vec2 uv;

                out vec3 v_normal;
                out vec4 v_color;
                out vec2 v_uv;
                out vec3 v_world_pos;
                out vec3 v_eyedir;

                void main() {
                    vec4 world_pos = ModelMatrix * vec4(pos, 1.0);
                    v_world_pos = world_pos.xyz;
                    v_normal = normalize((ModelMatrix * vec4(normal, 0.0)).xyz);
                    v_color = vert_color;
                    v_uv = uv;

                    vec4 view_pos = viewMatrix * world_pos;
                    v_eyedir = -normalize(view_pos.xyz);

                    gl_Position = ModelViewProjectionMatrix * vec4(pos, 1.0);
                }
            ''',
            'fragment': '''
                // ============================================================
                // STK Full Lighting Pipeline (deferred combined into forward)
                // Sources:
                //   - sp_solid.frag         (G-buffer: diffuse, normal, PBR data)
                //   - sunlight.frag         (sun directional light)
                //   - IBL.frag              (image-based lighting + SSR)
                //   - utils/DiffuseBRDF.frag (Lambert)
                //   - utils/SpecularBRDF.frag (Blinn-Phong + Fresnel Schlick)
                //   - utils/DiffuseIBL.frag (spherical harmonics irradiance)
                //   - utils/SpecularIBL.frag (cube probe + roughness LOD)
                //   - utils/SunMRP.frag     (Most Representative Point for area sun)
                //   - utils/decodeNormal.frag
                //   - utils/rgb_conversion.frag
                //   - utils/sp_texture_sampling.frag
                // ============================================================

                // --- Material textures ---
                uniform sampler2D u_diffuse_tex;
                uniform sampler2D u_pbr_tex;       // Gloss map: R=spec, G=metal, B=emiss

                // --- Sun light (sunlight.frag) ---
                uniform vec3 u_sun_direction;       // Sun direction in world space
                uniform vec3 u_sun_color;           // Sun color (RGB)
                uniform float u_sun_angle;          // Sun angular radius (degrees)

                // --- IBL spherical harmonics (DiffuseIBL.frag) ---
                // Precomputed irradiance SH coefficients (9 per channel)
                uniform float u_sh_red[9];
                uniform float u_sh_green[9];
                uniform float u_sh_blue[9];

                // --- IBL specular (SpecularIBL.frag) ---
                uniform samplerCube u_probe;        // Environment cube map

                // --- Fog (from header.txt) ---
                uniform vec4 u_fog_data;            // x=start, y=end, z=max, w=density
                uniform vec4 u_fog_color;

                // --- Colorization ---
                uniform float u_hue;
                uniform bool u_colorizable;
                uniform bool u_advanced;

                in vec3 v_normal;
                in vec4 v_color;
                in vec2 v_uv;
                in vec3 v_world_pos;
                in vec3 v_eyedir;

                out vec4 frag_color;

                // ---------- Include: utils/rgb_conversion.frag ----------
                vec3 rgbToHsv(vec3 c) {
                    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
                    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
                    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
                    float d = q.x - min(q.w, q.y);
                    float e = 1.0e-10;
                    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
                }
                vec3 hsvToRgb(vec3 c) {
                    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
                    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
                    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
                }
                // ---------------------------------------------------------

                // ---------- Include: utils/decodeNormal.frag ----------
                vec3 DecodeNormal(vec2 n) {
                    n = n * 2.0 - 1.0;
                    vec3 ret = vec3(n.x, n.y, 1.0 - abs(n.x) - abs(n.y));
                    float t = max(-ret.z, 0.0);
                    ret.x += ret.x >= 0.0 ? -t : t;
                    ret.y += ret.y >= 0.0 ? -t : t;
                    return normalize(ret);
                }
                // -------------------------------------------------------

                // ---------- Include: utils/DiffuseBRDF.frag ----------
                vec3 DiffuseBRDF(vec3 normal, vec3 eyedir, vec3 lightdir,
                                 vec3 color, float roughness) {
                    return color;    // Lambert
                }
                // -----------------------------------------------------

                // ---------- Include: utils/SpecularBRDF.frag ----------
                vec3 SpecularBRDF(vec3 normal, vec3 eyedir, vec3 lightdir,
                                  vec3 color, float roughness) {
                    float exponentroughness = exp2(10.0 * roughness + 1.0);
                    vec3 H = normalize(eyedir + lightdir);
                    float NdotH = clamp(dot(normal, H), 0.0, 1.0);
                    float normalisationFactor = (exponentroughness + 2.0) / 8.0;
                    vec3 FresnelSchlick = color + (1.0 - color) *
                        pow(1.0 - clamp(dot(eyedir, H), 0.0, 1.0), 5.0);
                    return max(pow(NdotH, exponentroughness) *
                        FresnelSchlick * normalisationFactor, vec3(0.0));
                }
                // -------------------------------------------------------

                // ---------- Include: utils/SunMRP.frag ----------
                vec3 SunMRP(vec3 normal, vec3 eyedir, vec3 sun_dir,
                            float sun_angle) {
                    vec3 R = reflect(-eyedir, normal);
                    float angularRadius = 3.14159 * sun_angle / 180.0;
                    vec3 D = sun_dir;
                    float d = cos(angularRadius);
                    float r = sin(angularRadius);
                    float DdotR = dot(D, R);
                    vec3 S = R - DdotR * D;
                    return (DdotR < d)
                        ? normalize(d * D + normalize(S) * r)
                        : R;
                }
                // -------------------------------------------------

                // ---------- Include: utils/DiffuseIBL.frag ----------
                mat4 getSHMatrix(float L00, float L1m1, float L10, float L11,
                                 float L2m2, float L2m1, float L20,
                                 float L21, float L22) {
                    float c1 = 0.429043, c2 = 0.511664;
                    float c3 = 0.743125, c4 = 0.886227, c5 = 0.247708;
                    return mat4(
                        c1 * L22, c1 * L2m2, c1 * L21, c2 * L11,
                        c1 * L2m2, -c1 * L22, c1 * L2m1, c2 * L1m1,
                        c1 * L21, c1 * L2m1, c3 * L20, c2 * L10,
                        c2 * L11, c2 * L1m1, c2 * L10, c4 * L00 - c5 * L20
                    );
                }
                vec3 DiffuseIBL(vec3 normal) {
                    vec4 n = vec4(normal, 0.0);
                    n.w = 1.0;
                    mat4 rmat = getSHMatrix(
                        u_sh_red[0], u_sh_red[1], u_sh_red[2], u_sh_red[3],
                        u_sh_red[4], u_sh_red[5], u_sh_red[6], u_sh_red[7],
                        u_sh_red[8]);
                    mat4 gmat = getSHMatrix(
                        u_sh_green[0], u_sh_green[1], u_sh_green[2],
                        u_sh_green[3], u_sh_green[4], u_sh_green[5],
                        u_sh_green[6], u_sh_green[7], u_sh_green[8]);
                    mat4 bmat = getSHMatrix(
                        u_sh_blue[0], u_sh_blue[1], u_sh_blue[2],
                        u_sh_blue[3], u_sh_blue[4], u_sh_blue[5],
                        u_sh_blue[6], u_sh_blue[7], u_sh_blue[8]);
                    float r = dot(n, rmat * n);
                    float g = dot(n, gmat * n);
                    float b = dot(n, bmat * n);
                    return max(vec3(r, g, b), vec3(0.0));
                }
                // -----------------------------------------------------

                // ---------- Include: utils/SpecularIBL.frag ----------
                vec3 SpecularIBL(vec3 normal, vec3 V, float roughness) {
                    vec3 sampleDir = reflect(-V, normal);
                    sampleDir = (inverseViewMatrix * vec4(sampleDir, 0.0)).xyz;
                    float lodval = 7.0 * (1.0 - roughness);
                    return clamp(textureLod(u_probe, sampleDir, lodval).rgb,
                                 0.0, 1.0);
                }
                // -----------------------------------------------------

                // ---------- Fog computation (sp_transparent.frag) ----
                float computeFog(vec3 world_pos) {
                    float dist = length(world_pos);
                    float fog = smoothstep(u_fog_data.x, u_fog_data.y, dist);
                    return min(fog, u_fog_data.z);
                }
                // -----------------------------------------------------

                void main() {
                    // ================================================
                    // Step 1: G-buffer generation (sp_solid.frag)
                    // ================================================
                    vec4 col = texture(u_diffuse_tex, v_uv);

                    // Colorization (hue change for karts/library objects)
                    if (u_colorizable && u_hue > 0.0) {
                        float mask = col.a;
                        vec3 old_hsv = rgbToHsv(col.rgb);
                        float mask_step = step(mask, 0.5);
                        float saturation = u_advanced
                            ? mask * 2.5
                            : mask * 1.825;
                        vec2 new_xy = mix(
                            vec2(old_hsv.x, old_hsv.y),
                            vec2(u_hue, max(old_hsv.y, saturation)),
                            vec2(mask_step, mask_step)
                        );
                        col = vec4(
                            hsvToRgb(vec3(new_xy.x, new_xy.y, old_hsv.z)),
                            1.0);
                    }

                    vec3 albedo = col.xyz * v_color.xyz;
                    vec3 normal = normalize(v_normal);

                    // Gloss map: R=specularity, G=metalness, B=emission
                    vec3 gloss = texture(u_pbr_tex, v_uv).rgb;
                    float specular = gloss.r;
                    float metalness = gloss.g;
                    float emission = gloss.b;
                    float roughness = 0.5;  // default, mapped from specular

                    // ================================================
                    // Step 2: Sun light (sunlight.frag)
                    // ================================================
                    vec3 sun_dir = normalize(u_sun_direction);
                    vec3 light_dir = SunMRP(normal, v_eyedir,
                                            sun_dir, u_sun_angle);

                    float NdotL = clamp(dot(normal, light_dir), 0.0, 1.0);

                    vec3 spec_color = mix(vec3(specular), albedo, metalness);
                    vec3 sun_spec = SpecularBRDF(normal, v_eyedir, light_dir,
                                                 spec_color, roughness);
                    vec3 sun_diff = DiffuseBRDF(normal, v_eyedir, light_dir,
                                                albedo, roughness);

                    vec3 sun_light = NdotL * (sun_diff + sun_spec) * u_sun_color;

                    // ================================================
                    // Step 3: IBL (DiffuseIBL.frag + SpecularIBL.frag)
                    // ================================================
                    vec3 ibl_diff = DiffuseIBL(normal) * albedo;
                    vec3 ibl_spec = SpecularIBL(normal, v_eyedir, roughness)
                                    * spec_color;

                    // ================================================
                    // Step 4: Emission from gloss map blue channel
                    // ================================================
                    vec3 emissive = albedo * emission;

                    // ================================================
                    // Step 5: Combine lighting
                    // ================================================
                    vec3 final = sun_light
                                + 0.25 * ibl_diff
                                + 0.25 * ibl_spec
                                + emissive;

                    // ================================================
                    // Step 6: Fog
                    // ================================================
                    float fog = computeFog(v_world_pos);
                    final = mix(final, u_fog_color.rgb, fog);

                    frag_color = vec4(final, 1.0);
                }
            ''',
        }
