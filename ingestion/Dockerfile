FROM python:3.8-slim
WORKDIR /pipeline
COPY requirements.txt /pipeline
RUN pip install -r requirements.txt
COPY telecom_churn.csv /pipeline
COPY ingestion.py /pipeline