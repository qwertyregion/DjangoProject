FROM python:3.7-slim
WORKDIR /app

# Настройка зеркала APT
# RUN sed -i 's|http://deb.debian.org/debian|http://deb.debian.org/debian|' /etc/apt/sources.list && \
#     sed -i 's|http://deb.debian.org/debian-security|http://deb.debian.org/debian-security|' /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y supervisor gcc libpq-dev
RUN rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY ./djangomain /app
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN mkdir -p /app/staticfiles
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=main_app.settings
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main_app.wsgi:application"]