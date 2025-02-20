class Request:

    def __init__(self, request: bytes):
        # TODO: parse the bytes of the request and populate the following instance variables

        self.body = b""
        self.method = ""
        self.path = ""
        self.http_version = ""
        self.headers = {}

        # decode it and split it by
        request_data = request.decode("utf-8")
        request_lines = request_data.split("\r\n")

        # split the first part to 3 piece
        first_line_parts = request_lines[0].split()

        self.method = first_line_parts[0]
        self.path = first_line_parts[1]
        self.http_version = first_line_parts[2]

        self.headers = {}
        for line in request_lines[1:]:
            if line:  # two parts name and value
                header_parts = line.split(': ')
                header_name = header_parts[0]
                header_value = header_parts[1]
                self.headers[header_name] = header_value
