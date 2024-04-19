FROM python:3.11-slim

ENV DASH_DEBUG_MODE True

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

CMD ["python", "app.py"]