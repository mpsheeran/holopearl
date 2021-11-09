FROM python:3.8
COPY . /app
RUN pip3 install -r /app/pip-requirements.txt
CMD ["python3", "/app", "prod"]
