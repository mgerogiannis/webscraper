FROM python:3

WORKDIR /task

COPY requirements.txt .

ADD argyle.py .

RUN pip install -r requirements.txt

CMD ["python", "argyle.py"]
