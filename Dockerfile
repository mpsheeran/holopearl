FROM python:3.7.2-stretch
COPY . /app
RUN pip3 install -r /app/pip-requirements.txt
RUN ["/app/setup_prod.sh", ""]
CMD ["python3.7", "/app", "prod"]
