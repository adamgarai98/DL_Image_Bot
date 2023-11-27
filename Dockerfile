FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /code

COPY requirements.txt /code/

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

RUN echo \
    && apt-get --yes install build-essential

RUN apt-get install -y \
    git \
    python3.10 \
    python3-pip \
    python3-dev \
    libglib2.0-0


RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src /code/src
COPY .env /code/

RUN pip install python-dotenv

CMD ["python3", "/code/src/dlim/__main__.py"]