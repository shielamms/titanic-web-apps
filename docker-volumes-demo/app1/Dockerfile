FROM python:3.10-alpine

WORKDIR /app

RUN mkdir templates
ADD templates/* templates/
ADD *.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 5001

ENTRYPOINT ["python"]
CMD ["app.py"]
