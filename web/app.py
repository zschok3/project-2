"""
John Doe's Flask API.
"""

from flask import Flask, render_template, abort, request
import os
import configparser


#CONFIG 
def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])
PORT = config["SERVER"]["PORT"]
DEBUG = config["SERVER"]["DEBUG"]
docroot = config["SERVER"]["DOCROOT"]

#FLASK
app = Flask(__name__)

@app.route("/<path:file_path>")
def index(file_path):
    file_path = docroot + "/" + file_path
    app.logger.info(file_path)
    if os.path.exists(file_path):
        return open(file_path, 'rb').read()
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return open(docroot + "/404.html"), 404

@app.errorhandler(403)
def forbidden(e):
    return open(docroot+ "/403.html"), 403

@app.before_request
def prevent_access_hidden_files():
    if ".." in request.path or "~" in request.path:
        abort(403)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
