FROM python:3.10-slim-buster AS builder

# set variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /app
# copy project
COPY . /app

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends\
    ffmpeg \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \ 
    && wget -P /root/.cache/whisper https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt
    
# run app
CMD ["python", "main.py"]