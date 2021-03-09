import http.server
import socketserver
from urllib.parse import urlparse
from src.randomizer import Randomizer
from src.comment_fetcher import Fetcher

response_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Randomizer</title>
</head>
<body>
<div id='div_output'>Got your request for video: {video_id}</div>
<div id='div_output'>Random comment is: {comment}</div>
</body>
</html>
'''


class Server(socketserver.TCPServer):
    def __init__(self, port, handler):
        self.allow_reuse_address = True
        super(Server, self).__init__(("", port), handler)
        self.allow_reuse_address = True


def main():
    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = 'src/index.html'
            elif self.path.startswith('/action_page.php'):
                parsed_path = urlparse(self.path)
                params_list = [t.split('=') for t in parsed_path.query.split('&')]
                params = {p[0]: p[1] for p in params_list}
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('/Users/kisa/PycharmProjects/CommentPicker/data/yt_api_key.txt') as myfile:
                    api_key = myfile.read()
                fetcher = Fetcher(api_key, params['video_id'], 'snippet')
                all_comments = fetcher.fetch()
                # print(len(all_comments), 'comments were fetched.')
                randomizer = Randomizer(all_comments)
                random_comment = randomizer.randomize()
                page = response_page.format(video_id=params['video_id'], comment=str(random_comment))
                self.wfile.write(page.encode())
                return
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

    # Create an object of the above class
    handler_object = MyHttpRequestHandler

    PORT = 8000
    my_server = Server(PORT, handler_object)

    # Star the server
    my_server.serve_forever()


if __name__ == "__main__":
    main()
