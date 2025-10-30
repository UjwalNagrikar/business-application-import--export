FROM nginx:alpine

# Remove default NGINX static files
RUN rm -rf /usr/share/nginx/html/*

# Copy everything from current directory into NGINX
COPY . /usr/share/nginx/html/

EXPOSE 80
