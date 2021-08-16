FROM nginx:alpine
LABEL MAITAINER="Ali Loloee Jahromi"

COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]