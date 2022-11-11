# Pull official python base image
FROM python:3.11-alpine3.16

# Set work directory
WORKDIR /usr/src/webapp

# prevent pip from 
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# prevent python from making pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# prevent python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Copy requirements.text (for pip install) to the work directory
COPY ./requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy django project into container
COPY . .