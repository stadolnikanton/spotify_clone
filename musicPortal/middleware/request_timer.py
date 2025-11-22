import time


class RequestTimerMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time_start = time.time()
        response = self.get_response(request)
        time_end = time.time()

        print(f"Время на обработку запроса: {(time_end - time_start):.2f} sec")
        return response
