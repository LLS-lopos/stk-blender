import math
import mathutils

class Light:
    def __init__(self, color, energy, name="Light"):
        self.color = mathutils.Color(color)
        self.energy = energy
        self.name = name
        self.shadow = True
    
    def get_illumination(self, point, normal):
        """Retourne l'intensité de la lumière sur un point donné"""
        raise NotImplementedError("Cette méthode doit être implémentée par les sous-classes")

class PointLight(Light):
    def __init__(self, position, color=(1, 1, 1), energy=100.0, radius=0.1, name="Point"):
        super().__init__(color, energy, name)
        self.position = mathutils.Vector(position)
        self.radius = radius
    
    def get_illumination(self, point, normal):
        """Calcule l'illumination d'un point par cette lumière
        
        Args:
            point (mathutils.Vector): Position du point à éclairer
            normal (mathutils.Vector): Vecteur normal au point
            
        Returns:
            mathutils.Color: Couleur résultante de l'illumination
        """
        direction = self.position - point
        distance = direction.length
        
        # Éviter la division par zéro
        if distance < 0.0001:
            return mathutils.Color((1, 1, 1)) * self.energy
            
        direction.normalize()
        
        # Calcul de l'atténuation (modèle physique réaliste)
        # Utilisation du carré inverse de la distance pour les lumières ponctuelles
        attenuation = 1.0 / (1.0 + 0.1 * distance + 0.01 * (distance ** 2))
        
        # Calcul de l'angle d'incidence (lois de Lambert)
        intensity = max(0.0, normal.dot(direction))
        
        # Appliquer l'énergie et la couleur
        result = mathutils.Color()
        for i in range(3):
            result[i] = min(1.0, self.color[i] * self.energy * intensity * attenuation)
            
        return result

class AreaLight(Light):
    def __init__(self, direction, color=(1, 1, 1), energy=1.0, name="Sun"):
        super().__init__(color, energy, name)
        self.direction = mathutils.Vector(direction).normalized()
    
    def get_illumination(self, point, normal):
        """Calcule l'illumination d'un point par cette lumière directionnelle
        
        Args:
            point (mathutils.Vector): Position du point à éclairer (non utilisé pour les lumières directionnelles)
            normal (mathutils.Vector): Vecteur normal au point
            
        Returns:
            mathutils.Color: Couleur résultante de l'illumination
        """
        # Pour une lumière directionnelle, la position n'a pas d'importance
        # Seule la direction compte
        intensity = max(0.0, normal.dot(-self.direction))
        
        # Appliquer l'énergie et la couleur
        result = mathutils.Color()
        for i in range(3):
            result[i] = min(1.0, self.color[i] * self.energy * intensity)
            
        return result

class SpotLight(PointLight):
    def __init__(self, position, direction, color=(1, 1, 1), energy=100.0, 
                 spot_size=math.pi/4, spot_blend=0.15, name="Spot"):
        super().__init__(position, color, energy, name)
        self.direction = mathutils.Vector(direction).normalized()
        self.spot_size = spot_size  # Angle d'ouverture
        self.spot_blend = spot_blend  # Douceur des bords
    
    def get_illumination(self, point, normal):
        """Calcule l'illumination d'un point par cette lumière spot
        
        Args:
            point (mathutils.Vector): Position du point à éclairer
            normal (mathutils.Vector): Vecteur normal au point
            
        Returns:
            mathutils.Color: Couleur résultante de l'éclairage spot
        """
        # Vecteur de la lumière au point
        light_to_point = (point - self.position)
        distance = light_to_point.length
        
        # Normaliser en évitant la division par zéro
        if distance > 0.0001:
            light_to_point.normalize()
        else:
            light_to_point = mathutils.Vector((0, 0, 1))
        
        # Angle entre la direction du spot et le vecteur vers le point
        angle = math.acos(max(-1, min(1, self.direction.dot(light_to_point))))
        
        # Vérifier si le point est en dehors du cône du spot
        if angle > self.spot_size / 2.0:  # spot_size est l'angle total, pas la moitié
            return mathutils.Color((0, 0, 0))
        
        # Calcul de base comme une lumière ponctuelle
        base_illumination = super().get_illumination(point, normal)
        
        # Lissage des bords du spot
        if self.spot_blend > 0.0001 and angle > self.spot_size * 0.5 * (1 - self.spot_blend):
            # Transition douce sur les bords
            falloff = (self.spot_size * 0.5 - angle) / (self.spot_size * 0.5 * self.spot_blend)
            falloff = max(0.0, min(1.0, falloff))  # Clamper entre 0 et 1
            
            result = mathutils.Color()
            for i in range(3):
                result[i] = base_illumination[i] * falloff
            return result
            
        return base_illumination