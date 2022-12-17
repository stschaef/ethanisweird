"""
Insta485 post views.

URLs include:
/p/<postid_slug>/
"""
import flask
import ethanisweird
from ethanisweird.model import get_db
from ethanisweird.views.post_helper import get_post_info
# from insta485.views.accounts import show_login


@ethanisweird.app.route('/p/<postid_slug>/', methods=['GET', 'POST'])
def show_post(postid_slug):
    """Display /u/<postid_slug>/ route."""
    check_post = "SELECT COUNT(*) FROM posts where postid = ?"
    post_count = get_db().cursor().execute(
        check_post, (postid_slug,)).fetchone()
    if post_count['COUNT(*)'] == 0:
        return flask.redirect(flask.url_for('show_index'))

    #  Handles POST requests
    if flask.request.method == 'POST':
        if not flask.session['username']:
            flask.abort(403)
        # TO DO: This logical structure may be wrong
        req = flask.request.form.to_dict()
        if 'uncomment' in req:
            delete_comment = 'DELETE FROM comments WHERE commentid = ?'
            get_db().cursor().execute(delete_comment, (req['commentid'],))
        elif 'unlike' in req:
            delete_like = 'DELETE FROM likes WHERE owner = ? AND postid= ?'
            get_db().cursor().execute(
                delete_like, (flask.session['username'], req['postid'],))
        elif 'comment' in req:
            insert_comment = 'INSERT INTO \
            comments(postid, owner, text) VALUES (?, ?, ?)'
            get_db().cursor().execute(
                insert_comment,
                (req['postid'], flask.session['username'], req['text'],))
        elif 'like' in req:
            # TO DO: Line needs to be shorter
            insert_like = 'INSERT INTO likes(owner, postid) VALUES (?, ?)'
            get_db().cursor().execute(
                insert_like, (flask.session['username'], req['postid'],))
        elif 'delete' in req:
            delete_post = 'DELETE FROM posts WHERE owner = ? AND postid = ?'
            get_db().cursor().execute(
                delete_post, (flask.session['username'], req['postid'],))
            delete_comments = 'DELETE FROM comments WHERE postid = ?'
            get_db().cursor().execute(
                delete_comments, (req['postid'],))
            delete_likes = 'DELETE FROM likes WHERE postid = ?'
            get_db().cursor().execute(
                delete_likes, (req['postid'],))
            # Keep running into FOREIGN KEY constraint violated with the above
            # lines

            # TO DO: Delete everything else related to this file and post from
            # the database

            return flask.redirect(flask.url_for('show_index'))

    # Falls through to here in the case of a GET request

    # return flask.render_template("post.html", posts=posts_, user=user_info,
    # likes=likes_dic, comments=comments_info, postid=postid_slug)
    # return flask.render_template("post.html", posts=posts_, user=user_info,
    # likes=likes_dic, comments=comments_info)
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for("show_login"))

    return flask.render_template("post.html", post=get_post_info(postid_slug))
