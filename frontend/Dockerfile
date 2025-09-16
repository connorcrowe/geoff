# Build
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Serve with nginx
FROM nginx:alpine

## Remove default nginx 
RUN rm -rf /usr/share/nginx/html/*

## Copy build output to nginx html folder
COPY --from=builder /app/dist usr/share/nginx/html

## Expose port
EXPOSE 80

## Run nginx
CMD ["nginx", "-g", "daemon off;"]