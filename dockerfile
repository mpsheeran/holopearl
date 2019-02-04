FROM python:3.7
COPY . /app
RUN pip3 install -r /app/pip-requirements.txt
CMD python3.7 /app/holopearl/holopearl.py