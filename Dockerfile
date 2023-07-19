############################################################
# Dockerfile to build Guest Join App
############################################################
#sudo docker build -t guest-join .
#docker run -i -p 10031:10031 -t guest-join
###########################################################################

FROM python:3.8.1

# File Author / Maintainer
MAINTAINER "Taylor Hanson <tahanson@cisco.com>"

# Copy the application folder inside the container
ADD . .

# Set the default directory where CMD will execute
WORKDIR /

# Get pip to download and install requirements:
RUN pip install aiohttp
RUN pip install python-dotenv
RUN pip install pyjwt
RUN pip install redis

#Copy environment variables file. Overwrite it with prod.env if prod.env exists.
COPY .env prod.env* .env


# Set the default command to execute
# when creating a new container
CMD ["python","server.py"]
