FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

ENV PYTHONUNBUFFERED=1


EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "jelly_backend.wsgi:application", "--log-level", "debug"]
