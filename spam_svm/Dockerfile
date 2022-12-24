# FROM selenium/standalone-chrome:latest
FROM python:3.10-slim
ADD Dashboard.py .
RUN pip install -U --upgrade pip
WORKDIR /opt/app
COPY requirements.txt /opt/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /opt/app
COPY .streamlit/config.toml /root/.streamlit/config.toml
COPY /data.csv /opt/app/data.csv
# COPY packages.txt /opt/app/packages.txt
# RUN xargs -a packages.txt apt-get install --yes
EXPOSE 8080
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/* 

RUN apt-get update && apt-get install -y wget 
RUN apt-get -y update 
RUN apt-get install zip -y 
RUN apt-get install unzip -y

    # apt-get install -y libglib2.0 libnss3 libgconf-2-4 libfontconfig1

# Install chromedriver
RUN wget -N https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver

RUN apt-get update && apt-get install -y curl 
# Install chrome broswer
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

ENTRYPOINT ["streamlit", "run", "Dashboard.py", "--server.port=8080", "--server.address=0.0.0.0"]


