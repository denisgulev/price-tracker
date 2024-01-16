# Use an official Node.js runtime as a base image
FROM node:16.20.2

# Set the working directory inside the container
WORKDIR /Frontend

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 3000 (the default port used by Create React App)
EXPOSE 3000

# Define the command to run your application
CMD ["npm", "start"]
