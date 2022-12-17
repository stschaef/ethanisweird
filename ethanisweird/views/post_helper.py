"""Insta485 posts helper."""
import flask
import arrow
import ethanisweird
from ethanisweird.model import get_db


def get_post_info(postid_slug):
    """Display helper to create postid page."""
    # Get post info
    database = ethanisweird.model.get_db()
    cur = database.cursor()
    posts_ = cur.execute("SELECT * from posts "
                         "WHERE postid = ?",
                         (postid_slug,)).fetchone()

    # Humanizes post for timestamp
    posts_['created'] = arrow.get(posts_['created']).humanize()

    # Get user info from 'users' table
    data = (posts_['owner'],)
    select_owner = 'SELECT * FROM users WHERE username = ?'
    user_info = get_db().cursor().execute(select_owner, data).fetchone()

    # Get like count from 'likes' table
    select_likes = 'SELECT COUNT(*) FROM likes WHERE postid = ?'
    likes_count = get_db().cursor().execute(
        select_likes, (postid_slug,)).fetchone()

    # Check if logged in user liked post
    select_ownerlike = 'SELECT COUNT(*) FROM \
    likes WHERE postid = ? AND owner = ?'
    owner_like = get_db().cursor().execute(
        select_ownerlike, (postid_slug, flask.session['username'],)).fetchone()

    likes_dic = {}
    likes_dic['num_likes'] = likes_count['COUNT(*)']
    likes_dic['owner_like'] = owner_like['COUNT(*)']

    # Get comments
    select_comments = 'SELECT * FROM comments WHERE \
    postid = ? ORDER BY datetime(created) ASC'
    comments_info = get_db().cursor().execute(
        select_comments, (postid_slug,)).fetchall()

    # print('posts_: ', posts_)
    # print('user_info: ', user_info)
    # print('likes_count', likes_count)
    # print('owner_like', owner_like)
    # print('likes_dic (num_likes & likes_count); ', likes_dic)

    out_dic = {}
    out_dic['posts_'] = posts_
    out_dic['user_info'] = user_info
    out_dic['likes_dic'] = likes_dic
    out_dic['comments_info'] = comments_info

    # print('out_dic: ', out_dic)

    return out_dic
