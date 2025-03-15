FROM python:3.8


WORKDIR /code

COPY listar-buckets.py .

RUN pip install boto3

CMD ["python", "./listar-buckets.py"]
