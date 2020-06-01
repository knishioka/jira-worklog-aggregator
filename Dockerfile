FROM python:3.8.2
WORKDIR /usr/src

RUN apt-get update && \
    apt-get install -y --no-install-recommends fonts-ipaexfont-gothic=00401-1 &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /usr/src/requirements.txt

RUN pip install pip==20.1.1 && \
    pip install -r /usr/src/requirements.txt

RUN useradd app
RUN mkdir -p /home/app && chown -R app:app /home/app
USER app
COPY matplotlibrc /home/app/.config/matplotlib/matplotlibrc
