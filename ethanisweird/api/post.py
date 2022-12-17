"""REST API for posts."""
import flask
import ethanisweird
from ethanisweird.api.util import get_logged_in, out_of_range


@ethanisweird.app.route('/api/v1/p/', methods=["GET"])
def get_posts():
    """Return posts.

    Example
    {
        "next": "",
        "results": [
        {
            "postid": 3,
            "url": "/api/v1/p/3/"
        },
        {
            "postid": 2,
            "url": "/api/v1/p/2/"
        },
        {
            "postid": 1,
            "url": "/api/v1/p/1/"
        }
        ],
        "url": "/api/v1/p/"
    }
    
    Return 10 newest posts by default
    ?size=N -> Return N newest posts
    ?page=N -> Return N'th page of posts
    {
        "message": "Bad Request",
        "status_code": 400
    }
    """
    if not get_logged_in():
        return flask.make_response(flask.jsonify({'message': 'Forbidden', 'status_code': 403}), 403)

    # User
    logname = flask.session["username"]
    context = {}

    size = flask.request.args.get('size', default=10, type=int)
    if size < 0:
        return flask.make_response(flask.jsonify({'message': 'Bad Request', 'status_code': 400}), 400)

    page = flask.request.args.get('page', default=0, type=int)
    if page < 0:
        return flask.make_response(flask.jsonify({'message': 'Bad Request', 'status_code': 400}), 400)

    
    # url
    context["url"] = flask.request.path
    context["next"] = ""

    connection = ethanisweird.model.get_db()
    cur = connection.execute(
        "SELECT postid, owner FROM posts ORDER BY postid DESC",
    )
    posts_ = cur.fetchall()
    select_following = connection.execute(
        'SELECT username2 FROM following WHERE username1 = ?', (logname,)
        ).fetchall()

    following_list = []
    for name in select_following:
        following_list.append(name['username2'])

    context["results"] = []

    start = size * page
    count = 0
    end = start + size

    for post in posts_:
        if start <= count <= end:
            if post['owner'] in following_list or post['owner'] == logname:
                post_ = {}
                post_["url"] = flask.request.path + str(post['postid']) + "/"
                post_["postid"] = post['postid']
                context["results"].append(post_)
        elif count > end:
            context["next"] = flask.request.path + "?size=" + str(size) \
                + "&page=" + str(page + 1)
        count += 1

    return flask.make_response(flask.jsonify(**context), 200)


@ethanisweird.app.route('/api/v1/p/<int:postid_url_slug>/', methods=["GET"])
def get_post_by_id(postid_url_slug):
    """Return post metadata.

    Example:
    {
        "age": "2017-09-28 04:33:28",
        "img_url": "/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg",
        "owner": "awdeorio",
        "owner_img_url": "/uploads/e1a7c5c32973862
                            ee15173b0259e3efdb6a391af.jpg",
        "owner_show_url": "/u/awdeorio/",
        "post_show_url": "/p/3/",
        "url": "/api/v1/p/3/"
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
    # logname = flask.session["username"]
    context = {}

    # url
    context["url"] = flask.request.path
    # age
    connection = ethanisweird.model.get_db()
    cur = connection.execute(
        "SELECT * FROM posts WHERE postid = ? ",
        (postid,)
    )
    post_collected = cur.fetchone()

    # checking that request wasn't out of range
    cur = connection.execute(
        "SELECT COUNT(*) AS post_count FROM posts"
    )

    # age
    context["age"] = post_collected['created']
    # img_url
    context["img_url"] = "/uploads/" + post_collected['filename']
    # owner
    context["owner"] = post_collected['owner']

    cur = connection.execute(
        "SELECT filename FROM users WHERE username = ?",
        (post_collected['owner'],)
    )
    owner_img = cur.fetchone()
    # owner_img_url
    context["owner_img_url"] = "uploads/" + owner_img['filename']
    # post_url
    context["post_show_url"] = "/p/" + str(postid) + "/"
    # owner_url
    context["owner_show_url"] = "/u/" + post_collected['owner'] + "/"

    return flask.make_response(flask.jsonify(**context), 200)
