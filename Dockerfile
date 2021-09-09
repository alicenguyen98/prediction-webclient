# Import base image
FROM python:3.9-slim

# Create directories
RUN mkdir /app

# copy all the stuff to directory
ADD ./prediction_webclient /app
ADD ./requirements.txt /app

# run pip to install dependencies
RUN pip install -r /app/requirements.txt

# Run server
CMD ["python", "-m", "app"]