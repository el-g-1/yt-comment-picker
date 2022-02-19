import http.server
import socketserver
from urllib.parse import urlparse, unquote
from randomizer import Randomizer
from comment_fetcher import Fetcher
from LRU import LRUCache
import json


class Server(socketserver.TCPServer):
    def __init__(self, port, handler):
        self.allow_reuse_address = True
        super(Server, self).__init__(("", port), handler)
        self.allow_reuse_address = True
        self.cache = LRUCache(10000)
        with open(
            "/Users/kisa/PycharmProjects/CommentPicker/data/yt_api_key.txt"
        ) as myfile:
            self.api_key = myfile.read()


def main():
    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        def load_comments(self, params):
            cache_key = params["session"]
            all_comments = self.server.cache.get(cache_key)
            if not all_comments:
                all_comments = Fetcher(
                    self.server.api_key, params["video_id"], "snippet"
                ).fetch()
                self.server.cache.put(cache_key, all_comments)
            response = {"num_comments": len(all_comments)}
            return response

        def handle_load_comments(self, params):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {}
            try:
                response = self.load_comments(params)
            except Exception:
                response["error"] = "Failed to load comments"
            self.wfile.write(json.dumps(response).encode())

        def pick_comment(self, params):
            all_comments = self.server.cache.get(params["session"])
            response = {}
            if not all_comments:
                response["error"] = "No comments were loaded"
                return response
            filter_text = params.get("filter_text", None)
            if filter_text is not None:
                filter_text = unquote(filter_text)
            randomizer = Randomizer(
                all_comments, params["remove_duplicates"], filter_text
            )
            random_comment = randomizer.randomize()
            if not random_comment:
                response["error"] = "No comments were filtered"
                return response
            response = random_comment.as_dict()
            response["author"] = random_comment.author.as_dict()
            return response

        def handle_pick_comment(self, params):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = self.pick_comment(params)
            self.wfile.write(json.dumps(response).encode())
            return

        def handle_404(self):
            self.send_error(404, "Page not found")
            return

        def get_params(self):
            parsed_path = urlparse(self.path)
            params_list = [t.split("=") for t in parsed_path.query.split("&")]
            params = {p[0]: p[1] for p in params_list}
            return params

        def do_GET(self):
            if self.path == "/":
                self.path = "src/index.html"
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            if self.path.startswith("/load_comments"):
                self.handle_load_comments(self.get_params())
                return
            if self.path.startswith("/comment"):
                self.handle_pick_comment(self.get_params())
                return
            self.handle_404()
            return

    # Create an object of the above class
    handler_object = MyHttpRequestHandler

    PORT = 8000
    my_server = Server(PORT, handler_object)

    # Start the server
    my_server.serve_forever()


if __name__ == "__main__":
    main()
