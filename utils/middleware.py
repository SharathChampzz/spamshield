import time
import logging
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("api_logger")


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, "start_time"):
            total_time = time.time() - request.start_time

            # Prepare log data
            log_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "time_taken": f"{total_time:.2f}s",
                "user": (
                    str(request.user) if request.user.is_authenticated else "anonymous"
                ),
            }

            # Add request parameters if any
            if request.GET:
                log_data["query_params"] = dict(request.GET)

            # Try to parse response content
            if hasattr(response, "content"):
                try:
                    log_data["response"] = json.loads(response.content)
                except json.JSONDecodeError:
                    log_data["response"] = "Non-JSON response"

            # Log the data
            logger.info(json.dumps(log_data))

        return response
