from flask import Flask, request, make_response, render_template
from randomizer import Randomizer
from comment_fetcher import Fetcher
from LRU import LRUCache
import json
import argparse
import threading


class Server:
    def __init__(self, yt_key_filename):
        self.cache = LRUCache(10000)
        self.cache_lock = threading.Lock()
        with open(yt_key_filename) as f:
            self.api_key = f.read()

    def load_comments(self, params):
        cache_key = params["session"]
        with self.cache_lock:
            all_comments = self.cache.get(cache_key)
        if not all_comments:
            all_comments = Fetcher(
                self.api_key, params["video_id"], "snippet"
            ).fetch()
            with self.cache_lock:
                self.cache.put(cache_key, all_comments)
        response = {"num_comments": len(all_comments)}
        return response

    def handle_load_comments(self, params):
        try:
            return self.load_comments(params)
        except Exception as ex:
            return make_response(json.dumps({"error": str(ex)}), 500)

    def pick_comment(self, params):
        all_comments = self.cache.get(params["session"])
        response = {}
        if not all_comments:
            response["error"] = "No comments were loaded"
            return response
        filter_text = params.get("filter_text", None)
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
        try:
            return self.pick_comment(params)
        except Exception as ex:
            return make_response(json.dumps({"error": str(ex)}), 500)


def main():

    parser = argparse.ArgumentParser(description="YouTube comment picker")
    parser.add_argument("--dev_key", "-d", required=True, help="YouTube API key")

    args = parser.parse_args()

    app = Flask("yt_comment_picker", template_folder="yt_comment_picker/templates")
    server = Server(yt_key_filename=args.dev_key)

    @app.route("/")
    def root_handler():
        return render_template("index.html")

    @app.route("/load_comments")
    def load_comments_handler():
        return server.handle_load_comments(request.args)

    @app.route("/comment")
    def pick_comment_handler():
        return server.handle_pick_comment(request.args)

    app.run()


if __name__ == "__main__":
    main()
