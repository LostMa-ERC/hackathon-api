FROM node:20.9.0-alpine3.18
WORKDIR /hackathon-api/frontend
COPY package.json .
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]
