FROM python:3.10-slim
WORKDIR /app

COPY . /app

#RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --default-timeout=200 --no-cache-dir -r requirements.txt


EXPOSE 5000

ENV FLASK_APP=app.py

ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]
