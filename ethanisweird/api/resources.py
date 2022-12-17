"""REST API for resource URLs."""
import flask
import ethanisweird
from ethanisweird.api.util import get_logged_in


@ethanisweird.app.route('/api/v1/', methods=["GET"])
def get_resource_urls():
    """Return resource urls.

    Example:
    {
        "posts": "/api/v1/p/",
        "url": "/api/v1/"
    }
    {
        "message": "Bad Request",
        "status_code": 400
    }
    """
    if not get_logged_in():
        return flask.make_response(flask.jsonify({'message': 'Forbidden', 'status_code': 403}), 403)

    # User
    # logname = flask.session["username"]
    context = {}

    # url
    context["url"] = flask.request.path
    context["posts"] = "/api/v1/p/"

    return flask.make_response(flask.jsonify(**context), 200)
