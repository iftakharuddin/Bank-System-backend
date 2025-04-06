from models.models import db, APIClient
import secrets
from app import app

def register_client(client_name):
    client = APIClient(client_name=client_name)
    client_secret = secrets.token_hex(16)  # Generate a random secret
    client.set_secret(client_secret)

    db.session.add(client)
    db.session.commit()

    return {"client_id": client.client_id, "client_secret": client_secret}


with app.app_context():
    print(register_client("TakaFlow"))