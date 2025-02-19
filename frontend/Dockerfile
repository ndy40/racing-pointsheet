# Stage 1: Build stage
FROM node:22-alpine AS builder
LABEL authors="ndy40"

# Install dependencies
RUN apk update && apk add --no-cache git
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --include=dev # Use `ci` for cleaner, consistent dependency installation

# Copy app and perform build if required
COPY . .
RUN npm run build # Run the build step (specific to many JavaScript projects)

# Stage 2: Production stage
FROM node:22-alpine
LABEL authors="ndy40"

# Install only production dependencies
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev # Install only production dependencies

# Copy built application files from the builder stage
COPY --from=builder /app ./
RUN npm ci

# Expose necessary ports (e.g., 3000)
EXPOSE 5173

# Default command
CMD ["npm", "run", "dev"]