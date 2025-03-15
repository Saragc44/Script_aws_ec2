FROM python:3.8


WORKDIR /code

COPY listar-buckets.py .

RUN pip install boto3

ENTRYPOINT  ["python", "./listar-buckets.py"]

CMD[]
