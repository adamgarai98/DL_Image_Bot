FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /code

COPY requirements.txt /code/

RUN apt-get update

RUN apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    build-essential \
    git \
    python3.10 \
    python3-pip


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src /code/src
COPY .env /code/



ENTRYPOINT ["python3", "/code/src/dlim/__main__.py"]