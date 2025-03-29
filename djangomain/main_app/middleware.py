import logging

logger = logging.getLogger('django.request')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug(f"Request: {request.method} {request.path}")  # Логируем запрос
        response = self.get_response(request)  # Получаем ответ
        logger.debug(f"Response: {response.status_code}")  # Логируем ответ
        return response
    