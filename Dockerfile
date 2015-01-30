FROM ubuntu:14.04
MAINTAINER "Aleksa Sarai <cyphar@cyphar.com>"

# Install basic dependencies.
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python python-pip python-dev

# Set up non-root runtime user.
RUN useradd -M -s/bin/nologin -- drone
RUN passwd -d -- drone

# Set up web source directory.
RUN mkdir -p -- /srv/src
WORKDIR /srv/src

# Install dependencies.
COPY requirements.txt /srv/src/requirements.txt
RUN pip2 install -r requirements.txt

# Install source.
COPY . /srv/src
RUN python2 setup.py install

# Switch to non-root user.
RUN chown -R drone:drone /srv/src
USER drone

# Set up metadata and entrypoints.
EXPOSE 5000
ENTRYPOINT ["python2", "-mfah"]
CMD []
