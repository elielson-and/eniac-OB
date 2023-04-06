
FROM python:3.7.2

# Defines default work directory inside the container
WORKDIR /app

# Copy the requirements file to container workspace
COPY requirements.txt .

# Update packages inside container (Debian distribuition)
RUN apt-get update && apt-get install -y nano curl

# install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Open a door to expose the server outside the machine
#EXPOSE 8000

# Init container Shell
CMD ["bash"]