FROM python:3.7-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY ./fast_main /app
RUN mkdir -p /app/staticfiles
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=fast_main.settings
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "fast_main.wsgi:application"]