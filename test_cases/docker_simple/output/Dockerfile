FROM nginx:latest

WORKDIR /usr/share/nginx/html

COPY ./readme.txt .

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
SAVE IMAGE --push my-image-name:$(date +%s)