FROM python:3.7-alpine


ENV PYTHONDONTWRITEBYTECODE=1

ADD requirements.txt ./

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-u", "/batch_queue_manager.py"]