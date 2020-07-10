FROM python:3.8.3-slim-buster

# The below is convention
WORKDIR /usr/src/API

# The file with python packages should be installed.
COPY requirements-d.txt .
# nstall packages
RUN pip install --no-cache-dir -r requirements-d.txt

# Copy all project to working directory.
COPY . .

EXPOSE 5000

CMD [ "python", "app.py" ]
