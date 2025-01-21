FROM nvidia/cuda:11.8.0-base-ubuntu22.04

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt