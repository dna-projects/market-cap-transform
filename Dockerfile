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
ENV PORT 8000

# Copy requirements.text (for pip install) to the work directory
COPY ./requirements.txt .

RUN apk add nginx

# Install python-based dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add static directory
RUN mkdir -p /user/src/webapp/staticfiles

# Copy django project into container
COPY . .

CMD python manage.py collectstatic --no-input; gunicorn --workers=2 -b 0.0.0.0:$PORT django_core.wsgi