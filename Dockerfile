FROM python:3.8.2

RUN apt-get update && apt-get install -y --no-install-recommends \
		sqlite3 \
    && rm -rf /var/lib/apt/lists/*

ADD . /api
WORKDIR /api
RUN pip install -r requirements.txt

EXPOSE 5000
RUN pytest genre_api/tests/
ENTRYPOINT ["python3", "app.py"]
