import random

from components.models import BackendDSConfig

def fetch(config: BackendDSConfig):
    return random.randint(1, 100)