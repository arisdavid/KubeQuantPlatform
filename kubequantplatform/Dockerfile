FROM python:3.7-alpine


ENV PYTHONDONTWRITEBYTECODE=1

ADD ./requirements.txt ./

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/kubequantplatform"

RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "./kubequantplatform/kubequantqm.py"]
