import socket
# import time
import json
import logging

request_logger = logging.getLogger('main')


class RequestLogMiddleware:
    """Request Logging Middleware."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # start_time = time.time()
        log_data = {
            'remote_address': request.META['REMOTE_ADDR'],
            'server_hostname': socket.gethostname(),
            'request_method': request.method,
            'request_path': request.get_full_path(),
        }
        if '/api/' in str(request.get_full_path()):
            req_body = (
                json.loads(request.body.decode("utf-8"))
                if request.body else {}
            )
            log_data['request_body'] = req_body
        response = self.get_response(request)
        response_status = getattr(response, 'status_code', None)
        log_data['response_status'] = response_status
        # if response and response['content-type'] == 'application/json':
        #     response_body = json.loads(response.content.decode('utf-8'))
        #     log_data['response_body'] = response_body
        # log_data['run_time'] = time.time() - start_time
        if response_status is not None and response_status >= 400:
            request_logger.error(msg=log_data)
        else:
            request_logger.info(msg=log_data)
        return response

    def process_exception(self, request, exception):
        try:
            raise exception
        except Exception as e:
            request_logger.exception('Необработанное исключение: ' + str(e))
        return exception
