FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

RUN echo \
    && apt-get --yes install build-essential

RUN pip install -r requirements.txt

COPY src /code/src
COPY .env /code/

RUN pip install python-dotenv

CMD ["python", "/code/src/dlim/__main__.py"]