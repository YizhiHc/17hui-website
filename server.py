import socketserver
import sys
from util.request import Request


class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        received_data = self.request.recv(2048)
        print(self.client_address)
        print("--- received data ---")
        print(received_data)
        print("--- end of data ---\n\n")
        request = Request(received_data)

        # TODO: Parse the HTTP request and use self.request.sendall(response) to send your response
        # response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 5\r\n\r\nHello\r\n\r\n"
        # self.request.sendall(response.encode("utf-8"))

        visit_count = 1

        if request.method == 'GET':
            if request.path == '/visit-counter':
                # look for Cookie in header that was stored
                cookie = request.headers.get('Cookie')

                if cookie:  # if cookie exist
                    # print(cookie)
                    cookie_values = cookie.split('; ')
                    # print(cookie_values)
                    for cookie in cookie_values:
                        name, value = cookie.split('=')
                        # print(name + ',,,' + value)
                        if name == 'vist_time':
                            visit_count = int(value) + 1

                response = "HTTP/1.1 200 OK\r\n"
                response += "Content-Type: text/plain\r\n"
                response += "Content-Length: ".format(len(str(visit_count)))
                response += "X-Content-Type-Options: nosniff\r\n"
                response += "Set-Cookie: vist_time={}; Max-Age=3600; Path=/visit-counter\r\n".format(visit_count)
                response += "\r\n"
                response += str(visit_count)

                self.request.sendall(response.encode("utf-8"))

            else:
                if request.path == '/':  # default file
                    file_path = "public/index.html"
                else:   # skip the first
                    file_path = request.path[1:]

                # mime file type that use
                mime_types = {
                    '.html': 'text/html',
                    '.css': 'text/css',
                    '.js': 'application/javascript',
                    '.jpg': 'image/jpeg',
                }

                try:
                    with open(file_path, 'rb') as file:  # open the file and read it as binary
                        file_content = file.read()

                    content_length = len(file_content)  # store the length
                    print("File length = " + str(content_length))

                    # split the file name and the extension
                    file_extension = file_path.split('.')[-1]

                    check_file = '.' + file_extension

                    # check if the mine type
                    if check_file in mime_types:
                        # print(file_extension)
                        mime_type = mime_types[check_file]
                        print("MIME type = " + mime_type)
                    else:
                        # set to empty
                        mime_type = ""

                    response = "HTTP/1.1 200 OK\r\n"
                    response += "Content-Type: {}; charset=utf-8\r\n".format(mime_type)
                    response += "Content-Length: {}\r\n".format(content_length)
                    response += "X-Content-Type-Options: nosniff\r\n"
                    response += "\r\n"
                    response = response.encode("utf-8") + file_content

                    self.request.sendall(response)

                except FileNotFoundError:
                    response = "HTTP/1.1 404 Not Found\r\n"
                    response += "Content-Type: text/plain\r\n"
                    response += "Content-Length: 39\r\n"
                    response += "X-Content-Type-Options: nosniff\r\n"
                    response += "\r\n"
                    response += "404 the requested content was not found"
                    self.request.sendall(response.encode("utf-8"))


def main():
    host = "0.0.0.0"
    port = 8080

    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))
    sys.stdout.flush()
    sys.stderr.flush()

    server.serve_forever()


if __name__ == "__main__":
    main()
