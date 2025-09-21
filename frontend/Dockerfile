# Utiliser Node 18
FROM node:18

WORKDIR /app

# Copier uniquement package.json pour installer les deps
COPY package*.json ./

# Installer toutes les dépendances (y compris autoprefixer/postcss/tailwind)
RUN npm install

# Copier le reste du projet
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
