FROM python:3.11-slim-buster

# set variables
# python variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# whisper variables
ENV WHISPER_MODEL small
ENV WHISPER_DEVICE cpu
ENV WHISPER_COMPUTE_TYPE int8
ENV WHISPER_BEAM_SIZE 5

# set work directory
WORKDIR /opt/speechex

# copy project
COPY . /opt/speechex

# install dependencies
RUN apt-get update
RUN pip install --no-cache-dir -r /opt/speechex/requirements.txt

# run app
CMD ["python", "main.py"]