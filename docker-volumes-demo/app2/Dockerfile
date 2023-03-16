FROM python:3.10-alpine

WORKDIR /app

ADD * .

RUN pip install -r requirements.txt

EXPOSE 5002

ENTRYPOINT ["python"]
CMD ["app.py"]
