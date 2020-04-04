FROM node:12.14.0
ARG tag
ARG githubToken
ARG PW=docker
# Install VS Code's deps. These are the only two it seems we need.
RUN apt-get update && apt-get install -y \
	libxkbfile-dev \
	libsecret-1-dev

WORKDIR /src
COPY . .

RUN yarn \
	&& DRONE_TAG="$tag" MINIFY=true BINARY=true GITHUB_TOKEN="$githubToken" ./scripts/ci.bash \
	&& rm -r /src/build \
	&& rm -r /src/source

# We deploy with Ubuntu so that devs have a familiar environment.
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
	openssl \
	net-tools \
	git \
	locales \
	sudo \
	dumb-init \
	vim \
	curl \
	wget \
	python3-dev \
	python3-pip \
	&& rm -rf /var/lib/apt/lists/*


RUN pip3 install pandas \
    seaborn \
	matplotlib \
	findspark \
	pyspark \
	scikit-learn  


RUN locale-gen en_US.UTF-8
# We cannot use update-locale because docker will not use the env variables
# configured in /etc/default/locale so we need to set it manually.
ENV LC_ALL=en_US.UTF-8 \
	SHELL=/bin/bash

RUN adduser --gecos '' --disabled-password coder && \
	echo "coder ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd


# install java
# Install OpenJDK-8
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Fix certificate issues
# Setup JAVA_HOME -- useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME



ENV hadoop_ver 3.2.1
ENV spark_ver 2.4.5


# Get Hadoop from US Apache mirror and extract just the native
# libs. (Until we care about running HDFS with these containers, this
# is all we need.)
RUN mkdir -p /opt && \
    cd /opt && \
    wget http://www.us.apache.org/dist/hadoop/common/hadoop-${hadoop_ver}/hadoop-${hadoop_ver}.tar.gz && \
    tar -xvf hadoop-${hadoop_ver}.tar.gz && \
    ln -s hadoop-${hadoop_ver} hadoop && \
    echo Hadoop ${hadoop_ver} native libraries installed in /opt/hadoop/lib/native

# Get Spark from US Apache mirror.
RUN mkdir -p /opt && \
    cd /opt && \
    wget http://www.us.apache.org/dist/spark/spark-${spark_ver}/spark-${spark_ver}-bin-hadoop2.7.tgz && \
        tar -xvf spark-${spark_ver}-bin-hadoop2.7.tgz && \
    ln -s spark-${spark_ver}-bin-hadoop2.7 spark && \
    echo Spark ${spark_ver} installed in /opt



USER coder
# Create first so these directories will be owned by coder instead of root
# (workdir and mounting appear to both default to root).
RUN mkdir -p /home/coder/project \
  && mkdir -p /home/coder/.local/share/code-server

WORKDIR /home/coder/project

# install python  and Pyspark


COPY elasticsearch-spark-hadoop-master  ./
# This ensures we have a volume mounted even if the user forgot to do bind
# mount. So that they do not lose their data if they delete the container.
VOLUME [ "/home/coder/project" ]

COPY --from=0 /src/binaries/code-server /usr/local/bin/code-server

ENTRYPOINT ["dumb-init", "code-server", "--host", "0.0.0.0 ", "--auth", "none" , "password","ubuntu"]

