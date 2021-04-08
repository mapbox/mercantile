# To develop in a reproducible dev environment
#
# 1. build the docker image
#
#   docker build -t mapbox/mercantile .
#
# 2. mount the source into the container and run tests
#
#   docker run --rm -v $PWD:/usr/src/app mapbox/mercantile


FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest-cov~=2.8 pytest~=5.3.0

COPY . .

RUN pip install -e .[test]

CMD ["python", "-m", "pytest"]
