
# Frontend Dockerfile for FitintyTrade
FROM node:18-alpine

WORKDIR /app

COPY frontend_ui /app

RUN npm install
EXPOSE 5173

CMD ["npm", "run", "dev"]
