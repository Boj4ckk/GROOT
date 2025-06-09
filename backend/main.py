from config.azure_config import AzureConfig, SessionLocal
from Service.user_services import UserService

# Crée une session (très important !)
db = SessionLocal()

try:
    service = UserService(db)
    user = service.create_user("test@example.com", "supermotdepasse")
    print("Utilisateur créé :", user)
finally:
    db.close()  # Toujours fermer proprement la session
