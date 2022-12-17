"""REST API for likes."""
import flask
import ethanisweird
from ethanisweird.api.util import get_logged_in, out_of_range


@ethanisweird.app.route('/api/v1/p/<int:postid_url_slug>/likes/',
                    methods=["GET", "POST", "DELETE"])
def get_likes(postid_url_slug):
    """Return likes on postid.

    Example:
    {
      "logname_likes_this": 1,
      "likes_count": 3,
      "postid": 1,
      "url": "/api/v1/p/1/likes/"
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
        connection = ethanisweird.model.get_db()
        cur = connection.execute(
            "SELECT EXISTS( "
            "  SELECT 1 FROM likes "
            "    WHERE postid = ? "
            "    AND owner = ? "
            "    LIMIT 1"
            ") AS logname_likes_this ",
            (postid, logname)
        )
        # print(cur.fetchone())
        if cur.fetchone()['logname_likes_this'] == 1:
            return flask.make_response(flask.jsonify({'logname' : logname, 'message': 'Conflict', 'postid' : postid, 'status_code': 409}), 409)


        connection = ethanisweird.model.get_db()
        connection.cursor().execute(
            'INSERT INTO likes(owner, postid) VALUES (?, ?)',
            (logname, postid,))
        context["logname"] = logname
        context["postid"] = postid
        return flask.make_response(flask.jsonify(**context), 201)

    if flask.request.method == "DELETE":
        connection = ethanisweird.model.get_db()
        connection.cursor().execute(
            'DELETE FROM likes WHERE owner = ? AND postid = ?',
            (logname, postid,))
        return flask.make_response(('', 204))

    # url
    context["url"] = flask.request.path

    # Post
    context["postid"] = postid

    # Did this user like this post?
    connection = ethanisweird.model.get_db()
    cur = connection.execute(
        "SELECT EXISTS( "
        "  SELECT 1 FROM likes "
        "    WHERE postid = ? "
        "    AND owner = ? "
        "    LIMIT 1"
        ") AS logname_likes_this ",
        (postid, logname)
    )
    logname_likes_this = cur.fetchone()
    context.update(logname_likes_this)

    # Likes
    cur = connection.execute(
        "SELECT COUNT(*) AS likes_count FROM likes WHERE postid = ? ",
        (postid,)
    )
    posts_count = cur.fetchone()
    # if postid > posts_count["likes_count"]:
    #     context = {}
    #     context["message"] = "Not Found"
    #     context["status_code"] = 403
    #     return flask.jsonify(**context)

    # likes_count = cur.fetchone()
    # if likes_count is not None:
    #     context.update(likes_count)

    context['likes_count'] = posts_count['likes_count']

    return flask.make_response(flask.jsonify(**context), 200)
