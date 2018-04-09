FROM python:rc-alpine3.7
ADD . /code
WORKDIR /code
EXPOSE 8080
RUN pip install -r requirements.txt
CMD ["python", "app.py"]