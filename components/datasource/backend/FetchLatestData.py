import requests

from components.configs import BackendDSConfig

def fetch(ctx, config: BackendDSConfig):
    ctx.info(f"Polling BE@{config.polling_endpoint}")
    return requests.get(config.polling_endpoint).json()