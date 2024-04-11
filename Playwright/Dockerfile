FROM mcr.microsoft.com/playwright:v1.43.0-jammy as build-image

# Install aws-lambda-ric build dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev \
    autoconf \
    libtool

# Define custom function directory
ARG FUNCTION_DIR="/function"

# Create function dir and install node packages
RUN mkdir -p ${FUNCTION_DIR}
COPY function/ ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}

RUN npm install -g npm
RUN npm install
RUN npm install aws-lambda-ric

# Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/local/bin/aws-lambda-rie
RUN chmod 755 /usr/local/bin/aws-lambda-rie
COPY entrypoint.sh /
RUN chmod 755 /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]

# Set function handler
CMD ["index.handler"]