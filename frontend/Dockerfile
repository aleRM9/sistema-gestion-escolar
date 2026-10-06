# Usar node.js 20
FROM node:20-alpine as builder

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .
RUN npm run build

# Fase de producción
FROM node:20-alpine

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY package*.json .
RUN npm install --production

CMD ["npm", "run", "preview"]

