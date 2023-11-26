FROM python:3.10

WORKDIR /code

RUN apt-get update && python3.10 -m pip install --upgrade pip 
COPY ./requirements.txt /code/requirements.txt
RUN python3.10 -m pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# PORT
# EXPOSE 80/tcp

COPY ./src /code

# RUN
CMD ["python3.10", "main.py"]

