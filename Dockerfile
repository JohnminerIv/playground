# Most of the time, Alpine is a great base image to start with.
# If we're building a container for Python, we use something different.
# Learn why here: https://pythonspeed.com/articles/base-image-python-docker-images/
# TLDR: Alpine is very slow when it comes to running Python!

# STEP 1: Install base image. Optimized for Python.
FROM python:3.7-slim-buster

# STEP 2: Copy the source code in the current directory to the container.
# Store it in a folder named /app.
ADD . /app
RUN python3 -m pip install -r /app/requirements.txt

# STEP 3: Set working directory to /app so we can execute commands in it
WORKDIR /app

# STEP 4: Declare environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# STEP 5: Expose the port that Flask is running on
EXPOSE 5000

# STEP 6: Run Flask!
CMD ["python3", "app.py"]