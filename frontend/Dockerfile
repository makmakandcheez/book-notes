# Build stage
FROM node:22-slim AS build

WORKDIR /app

RUN corepack enable

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

# Baked into the JS bundle at build time (Vite only reads import.meta.env.* at
# build time, not at container start). Defaults to the sibling backend
# container's host-mapped port; override with --build-arg VITE_API_URL=...
# (or via docker-compose.yml) to point a locally-built image elsewhere,
# e.g. your own deployed backend.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

RUN pnpm build

# Serve stage
FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
