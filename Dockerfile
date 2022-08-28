FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8080
ARG PIP_NO_CACHE_DIR=1

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Copy files
WORKDIR /usr/src/app
COPY . .

# Upgrade pip, install pipenv
RUN pip install --upgrade pip

# Generate requirements.txt and install dependencies from there
RUN pip install -r requirements.txt

RUN python chrome_driver_install.py

CMD gunicorn -b 0.0.0.0:$PORT --workers 1 --threads 1 --timeout 0 main:app
