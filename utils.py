from functools import wraps
from flask import Flask,jsonify

app = Flask(__name__)

# Custom decorator to log exceptions
def log_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Exception occurred: {e}")
            return jsonify({"error": "An error occurred"}, 500)
    return wrapper


DEFAULT_BG_IMAGE = "https://pirho-web-static.s3.amazonaws.com/dashb/images/background_image.jpg"
S3_BASE = "https://pirho-web-static.s3.amazonaws.com/dashb/images/"
DEFAULT_CLIENT = "https://pirho-web-static.s3.amazonaws.com/dashb/images/activebuildings.png"
CLIENT_BASE = "https://pirho-web-static.s3.amazonaws.com/dashb/images/"