######## DOCKERFILE FOR API ############

# Pull Python image
FROM python:3.8

# Update pip
RUN python -m pip install --upgrade pip

# Install pipenv
RUN pip install pipenv

# Switch into working directory
WORKDIR /app

# Copy Pipfiles and API content from local file to image
COPY Pipfile . /app
COPY Pipfile.lock . /app
COPY api/ /app
COPY . /app

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Expose 8080 port
EXPOSE 8080

# Append parameters to perform command to run application
CMD [ "pipenv", "run", "python", "main.py", "--host=0.0.0.0" ]