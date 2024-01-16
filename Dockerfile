FROM python:3.12.0-slim

# install needed packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libcairo2-dev

# clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /bookapp

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn src.wsgi
