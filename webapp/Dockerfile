# Use Node.js as the base image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy only the package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

COPY . .

# Build the SvelteKit application
RUN npm run build

# Expose the default HTTP port
EXPOSE 3000

# Start the server using @sveltejs/adapter-node
CMD ["node", "build"]
