FROM python:3.8.6-slim-buster
WORKDIR /usr/src

RUN apt-get update && \
    apt-get install -y --no-install-recommends fonts-ipaexfont-gothic=00401-1 &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /usr/src/requirements.txt

RUN pip install pip==20.2.3 && \
    pip install -r /usr/src/requirements.txt

RUN useradd app
RUN mkdir -p /home/app && chown -R app:app /home/app
USER app
COPY config/matplotlibrc /usr/local/lib/python3.8/site-packages/matplotlib/mpl-data/matplotlibrc
COPY config/jupyter_notebook_config.py /home/app/.jupyter/jupyter_notebook_config.py
