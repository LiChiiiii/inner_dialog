FROM node:18-alpine as frontend_build
# Set the public IP and port for backend.
# because we are accessing from the user's browser.
ARG VITE_API_URL
ENV VITE_API_URL $VITE_API_URL
WORKDIR /app
COPY . /app
RUN npm install
RUN npm run build

FROM nginx
COPY --from=frontend_build /app/dist/ /usr/share/nginx/html
COPY /nginx.conf /etc/nginx/conf.d/default.conf