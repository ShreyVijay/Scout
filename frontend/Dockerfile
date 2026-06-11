# frontend/Dockerfile
FROM node:20-slim AS builder

WORKDIR /app

ARG VITE_API_BASE_URL=https://skaut-backend-436757595175.us-central1.run.app
ARG VITE_GOOGLE_MAPS_API_KEY=
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_GOOGLE_MAPS_API_KEY=$VITE_GOOGLE_MAPS_API_KEY

COPY package*.json ./
RUN npm ci

COPY . .

# Debug: verify .env.production was copied
RUN cat .env.production || echo "NO .env.production FOUND"

RUN npm run build

# Verify the build output contains the backend URL
RUN grep -r "skaut-backend" dist/assets/*.js && echo "BACKEND URL FOUND IN BUNDLE" || echo "WARNING: BACKEND URL NOT IN BUNDLE"

FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
