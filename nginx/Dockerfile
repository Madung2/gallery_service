
FROM nginx:1.22.0
COPY conf/default.conf etc/nginx/conf.d

RUN apt update
# RUN apt-get install -y gnupg2 software-properties-common
RUN apt-get install -y software-properties-common
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C2518248EEA14886
RUN apt-get install python3-certbot-nginx -y

