FROM continuumio/miniconda3:4.9.2-alpine

# Switch to nobody

WORKDIR /home/nobody
RUN mkdir /home/nobody/.conda
RUN mkdir /home/nobody/app
RUN mkdir /home/nobody/app/cache

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
COPY ./app/requirements.txt /tmp/requirements.txt
# Install the pip packages
RUN pip install -r /tmp/requirements.txt

WORKDIR /home/nobody/app
USER nobody
# Expose 5035 port for API
EXPOSE 5035

# Run fastapi with the app (api.py)
CMD ["/bin/bash", "-c", "uvicorn --proxy-headers api:app --host=0.0.0.0 --port=5035"]
