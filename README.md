# yt-comment-picker

This is an application that loads comments from a given YouTube video 
and picks a random comment based on criteria. 
The criteria may include: 
* filtering out duplicate comments (from the same user),
* filtering comments based on specific text.

The project is a Python HTTP server with a simple web UI. 

## Usage

The server requires YouTube Data API key 
that can be obtained via [Obtaining authorization credentials](https://developers.google.com/youtube/registering_an_application). \
The API key must be stored in `data/yt_api_key.txt`.

To run the server:
```
python src/server.py
```

## Dependencies

* Python 3.6
* google-api-python-client: `pip install google-api-python-client`
