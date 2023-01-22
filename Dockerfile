FROM ubuntu:20.04
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y wget unzip
RUN apt-get install -y gnupg
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome*.deb; apt-get -fy install
RUN rm -rf google-chrome*.deb


RUN wget https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_linux64.zip
RUN unzip -o ./chromedriver_linux64.zip
RUN rm -rf chromedriver_linux64.zip

RUN apt-get install -y xvfb

RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip --no-cache-dir
RUN pip3 install -r /app/requirements.txt --no-cache-dir

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

# FROM python:3.9-slim
# RUN apt-get -y update
# RUN apt-get -y install wget
# RUN apt-get -y install unzip

# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt-get install ./google-chrome-stable_current_amd64.deb

# RUN wget https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_mac64.zip
# RUN unzip -o ./chromedriver_mac64.zip
# RUN rm -rf chromedriver_mac64.zip