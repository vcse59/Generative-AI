# Use Node.js with Debian-based dependencies
FROM node:18-bullseye AS builder

# Set working directory
WORKDIR /app

# Copy package.json
COPY package.json ./ 

# Install project dependencies
RUN npm install

# Copy the rest of the project files
COPY . .

# Expose port 8080 for serving the app
EXPOSE 8080

# Serve the app using the `serve` package
CMD ["npm", "start"]
