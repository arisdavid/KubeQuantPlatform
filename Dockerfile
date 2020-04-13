FROM python:3.6


ENV PYTHONDONTWRITEBYTECODE=1

ADD requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "-u", "/task_queue_manager.py"]