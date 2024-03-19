# FROM provides the base image from which the assembly begins (1st layer)
FROM python:3.7.9

# RUN executes a provided command (creates a directory) (2d layer)
RUN mkdir -p /usr/src/app
# WORKDIR sets the created directory as current in a container later (3d layer)
WORKDIR /usr/src/app/app

# COPY <source> <target> (copies everything from the app into a container) (4th layer)
# <source> is where Dockerfile (Dockerfile location defines <source>)
COPY . /usr/src/app/app
# Install all necessary libraries from the file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define a port from which the container can be accessed (best practice)
EXPOSE 5000

# When the container is built, the following command will be executed (runs the app)
CMD ["python", "articles.py"]

# Difference between CMD and ENTRYPOINT:
# CMD executes commands using the shell when a container is running 
# ENTRYPOINT executes commands without the shell

# Image Building:
# 1. Create a dockerfile
# 2. Execute the following command where a dockerfile is located: docker build -t <image_name> . (dot means from the current directory)

# Explanation of what will be happening after running the command:
# 1. Assembly mus start with Python 3.6 which we don't have locally
# 2. Docker checks the Image for Python 3.6 on Docker Hub. There is such image (it downloads it)
# 3. Docker adds defined layers on top of downloaded ones 

# Container Running 
# docker run -d -p <local_port>:<container_port> --name container_name --rm img_name: Runs a container in a detached mode and deletes it after stopping
