FROM node:18

WORKDIR /app

# Supprimer le node_modules existant qui est monté depuis l'hôte
# et réinstaller les dépendances dans l'environnement Docker
CMD [ "sh", "-c", "npm install && npm run dev -- --host 0.0.0.0" ]