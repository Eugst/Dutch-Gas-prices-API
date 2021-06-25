FROM continuumio/miniconda3:latest

RUN  apt-get update \
    && apt-get install -y curl wget \
	tesseract-ocr \
	libtesseract-dev && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Update miniconda
RUN conda update -y conda

# Install the conda packages
RUN conda config --add channels conda-forge
RUN conda install --yes \
    python=3.7 \
    fastapi=0.43.0 \
    uvicorn=0.9.1 \
    pip

# Copy the python files to the image
COPY ./app/api.py /home/nobody/app/api.py
COPY ./app/gas_prices.py /home/nobody/app/gas_prices.py
COPY ./app/gas_map.py /home/nobody/app/gas_map.py
COPY ./app/requirements.txt /tmp/requirements.txt
# Install the pip packages
RUN pip install -r /tmp/requirements.txt && mkdir -p /home/nobody/app/cache/maps && chown -R nobody /home/nobody/app/

WORKDIR /home/nobody/app
USER nobody
# Expose 5035 port for API
EXPOSE 5035

# Run fastapi with the app (api.py)
CMD ["/bin/sh", "-c", "uvicorn --proxy-headers api:app --host=0.0.0.0 --port=5035"]
