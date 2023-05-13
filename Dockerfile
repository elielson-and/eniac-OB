FROM python:3.11-slim-buster

# Defines default work directory inside the container
WORKDIR /app

# Copy the requirements file to container workspace
COPY requirements.txt .

# Update packages inside container (Debian distribuition) and install project dependencies
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get install --no-install-recommends --no-install-suggests -y build-essential \
    && apt-get install --no-install-recommends --no-install-suggests -y libgmp-dev libmpfr-dev libmpc-dev \
    && apt-get install --no-install-recommends --no-install-suggests -y g++ make \
    && apt-get install -y wget \
    && wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xvzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ && ./configure --prefix=/usr \
    && make && make install \
    && pip install ta-lib \
    && cd .. && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Open a door to expose the server outside the machine (if needed)
# EXPOSE 8000

# Init container Shell
CMD ["bash"]
