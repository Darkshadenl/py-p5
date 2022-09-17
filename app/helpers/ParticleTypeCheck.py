from app.components.Particle import Particle

def ParticleTypeCheck(item: any) -> Particle:
    if not isinstance(item, Particle):
        raise TypeError("Argument should be of type Particle")
    else:
        return item