FROM python:3.8-slim-buster

# Defines default work directory inside the container
WORKDIR /app

# Copy the requirements file to container workspace
COPY requirements.txt .

# Update packages inside container (Debian distribuition) and install project dependencies
RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Open a door to expose the server outside the machine (if needed)
# EXPOSE 8000

# Init container Shell
CMD ["bash"]