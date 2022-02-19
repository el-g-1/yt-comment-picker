# yt-comment-picker

This is an application that loads comments from a given YouTube video 
and picks a random comment based on criteria. 
The criteria may include: 
* filtering out duplicate comments (from the same user),
* filtering comments based on specific text.

The project is a Python HTTP server with a simple web UI. 

## Dependencies

To install dependencies:

* `cd` into the project's root directory (where setup.py is located)
* run: `pip install -e .` or `python setup.py install`

## Usage

The server requires YouTube Data API key 
that can be obtained 
via [Obtaining authorization credentials](https://developers.google.com/youtube/registering_an_application).

To run the server:
```
python yt_comment_picker/server.py --dev_key=<path to file containing YouTube API key>
```

