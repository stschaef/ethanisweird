"""REST API for comments."""
import flask
import ethanisweird
from ethanisweird.api.util import get_logged_in, out_of_range


@ethanisweird.app.route('/api/v1/p/<int:postid_url_slug>/comments/',
                    methods=["GET", "POST"])
def get_comments(postid_url_slug):
    """Return comments on postid.

    Example
    {
        "comments": [
        {
            "commentid": 1,
            "owner": "awdeorio",
            "owner_show_url": "/u/awdeorio/",
            "postid": 3,
            "text": "#chickensofinstagram"
        },
        {
            "commentid": 2,
            "owner": "jflinn",
            "owner_show_url": "/u/jflinn/",
            "postid": 3,
            "text": "I <3 chickens"
        },
        {
            "commentid": 3,
            "owner": "michjc",
            "owner_show_url": "/u/michjc/",
            "postid": 3,
            "text": "Cute overload!"
        }
        ],
        "url": "/api/v1/p/3/comments/"
    }
    {
        "message": "Bad Request",
        "status_code": 400
    }
    """
    if not get_logged_in():
        return flask.make_response(flask.jsonify({'message': 'Forbidden', 'status_code': 403}), 403)

    postid = postid_url_slug

    if out_of_range(postid):
        return flask.make_response(flask.jsonify({'message': 'Not Found', 'status_code': 404}), 404)

    # User
    logname = flask.session["username"]
    
    context = {}

    if flask.request.method == "POST":
        text_in = flask.request.get_json()
        text_ = str(text_in)
        connection = ethanisweird.model.get_db()
        connection.cursor().execute(
            'INSERT INTO comments(owner, postid, text) VALUES (?, ?, ?)',
            (logname, postid, text_,))
        comment_added = connection.cursor().execute(
            'SELECT * FROM comments ORDER BY commentid DESC').fetchone()
        context["commentid"] = comment_added['commentid']
        context["commentid"] = comment_added['commentid']
        context["owner"] = comment_added['owner']
        context["owner_show_url"] = "/u/" + comment_added['owner'] + "/"
        context["postid"] = postid
        context["text"] = comment_added['text']

        return flask.make_response(flask.jsonify(**context), 201)

    # url
    context["url"] = flask.request.path

    connection = ethanisweird.model.get_db()
    cur = connection.execute(
        "SELECT commentid, owner, text FROM comments WHERE postid = ? ",
        (postid,)
    )

    comments_info = cur.fetchall()

    context["comments"] = []
    for comment in comments_info:
        comment_ = {}
        comment_["commentid"] = comment['commentid']
        comment_["owner"] = comment['owner']
        comment_["owner_show_url"] = "/u/" + comment['owner'] + "/"
        comment_["postid"] = postid
        comment_["text"] = comment['text']
        context["comments"].append(comment_)

    return flask.make_response(flask.jsonify(**context), 200)
