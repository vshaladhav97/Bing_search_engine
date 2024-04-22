# middlewares.py
class RangeRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method == 'GET' and 'HTTP_RANGE' in request.META:
            range_header = request.META['HTTP_RANGE']
            byte1, byte2 = 0, None
            if range_header.startswith('bytes='):
                byte1, byte2 = range_header[6:].split('-')
                byte1, byte2 = int(byte1), (int(byte2) if byte2 else response['Content-Length'] - 1)
            if byte2:  # Calculate the content length for the range
                response.status_code = 206
                response['Content-Range'] = f'bytes {byte1}-{byte2}/{response["Content-Length"]}'
                response.content = response.content[byte1:byte2+1]
                response['Content-Length'] = str(byte2 - byte1 + 1)
        return response
