# frontend/Dockerfile
FROM node:20-slim AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .

# Debug: verify .env.production was copied
RUN cat .env.production || echo "NO .env.production FOUND"

RUN npm run build

# Verify the build output contains the backend URL
RUN grep -r "scout-backend" dist/assets/*.js && echo "BACKEND URL FOUND IN BUNDLE" || echo "WARNING: BACKEND URL NOT IN BUNDLE"

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
