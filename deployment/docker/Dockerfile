# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install MkDocs and the Material theme
RUN pip install mkdocs mkdocs-material

# Build the MkDocs documentation
RUN mkdocs build -f docs/mkdocs.yml

# Make port 8000 available to the world outside this container
EXPOSE 8000
# Make port 8080 available for the documentation
EXPOSE 8080

# Create a script to run both FastAPI and MkDocs
RUN echo '#!/bin/bash\n\
uvicorn api.main:app --host 0.0.0.0 --port 8000 &\n\
python -m http.server 8080 --directory /app/site\n\
wait' > /app/start.sh

RUN chmod +x /app/start.sh

# Run the script when the container launches
CMD ["/app/start.sh"]