FROM python:3.9

# RUN apt-get update
# RUN apt-get install -y vim

WORKDIR /app

RUN pip install --no-cache-dir flask

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 5000

WORKDIR /app/webapp

COPY . .

# Set the entrypoint script as the entry point for the container
ENTRYPOINT ["/app/entrypoint.sh"]