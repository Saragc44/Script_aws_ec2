FROM python:3.8


WORKDIR /code

COPY listar-buckets.py .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "./listar-buckets.py"]
