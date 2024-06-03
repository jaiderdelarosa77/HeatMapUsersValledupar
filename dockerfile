# Use an official Python runtime as a parent image
FROM python:3.11-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app

RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"
RUN pip install pandas folium fastapi uvicorn openpyxl

COPY . .
# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--reload", "--host","0.0.0.0", "--port", "80"]
