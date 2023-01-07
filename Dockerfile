FROM python:3.9
VOLUME /holodata
COPY . /app
RUN pip3 install --no-cache-dir -r /app/pip-requirements.txt
CMD ["python3.9", "/app", "prod"]
