"""
Insta485 user views.

URLs include:
/u/<user_url_slug>/
/u/<user_url_slug>/followers/
/u/<user_url_slug>/following/
"""
import flask
import ethanisweird
from ethanisweird.model import get_db
from ethanisweird.views.view_helper import hash_file_and_save


@ethanisweird.app.route('/u/<user_url_slug>/', methods=['GET', 'POST'])
def show_user(user_url_slug):
    """Display /u/<user_url_slug>/ route."""
    user_count = get_db().cursor().execute(
        "SELECT COUNT(*) FROM users where username = ?",
        (user_url_slug,)).fetchone()
    if user_count['COUNT(*)'] == 0:
        return flask.redirect(flask.url_for('show_index'))

    # Handles POST requests
    if flask.request.method == 'POST':
        if 'username' not in flask.session:
            flask.abort(403)
        req = flask.request.form.to_dict()

        # Attempt to upload a new post
        if 'create_post' in req:
            if user_url_slug != flask.session['username']:
                flask.abort(403)

            # Owner of the page uploads a new post
            else:
                new_filename = hash_file_and_save(flask.request.files['file'])
                # insert_post = """INSERT INTO posts(filename, owner) VALUES
                # ('{0}', '{1}')""".format(new_filename, user_url_slug)
                get_db().cursor().execute(
                    "INSERT INTO posts(filename, owner) VALUES (?, ?)",
                    (new_filename, user_url_slug))

        # Current user attempts to follow owner of page
        elif 'follow' in req:
            print(req)
            get_db().cursor().execute(
                "INSERT INTO following(username1, username2) VALUES (?, ?)",
                (flask.session['username'], req['username'],))

        # Current user attempts to unfollow owner of page
        elif 'unfollow' in req:
            get_db().cursor().execute(
                "DELETE FROM following WHERE username1 = ? AND username2 = ?",
                (flask.session['username'], req['username'],))

    # Falls through to here in the case of a GET request

    # Get user's information from user table
    data = (user_url_slug,)
    select_users = 'SELECT * FROM users WHERE username = ?'
    users_info = get_db().cursor().execute(select_users, data).fetchone()

    # print('type: ', type(users_info))
    # print('out: ', users_info)

    # for row in users_info:
    #     print(row,':', users_info[row])

    # Get user's post information
    posts_info = get_db().cursor().execute(
        'SELECT * FROM posts WHERE owner = ?', data).fetchall()

    # print('type: ', type(posts_info))
    # print('out: ', posts_info)

    # for dic in posts_info:
    #     print(row,':', dic)

    # Holds followers/following counts
    follow_info = {}

    # Get follower count
    followers_count = get_db().cursor().execute(
        'SELECT COUNT(*) FROM following WHERE username2 = ?', data).fetchone()
    follow_info['followers'] = followers_count['COUNT(*)']

    # print('followers type: ', type(followers_count))
    # print('followers out: ', followers_count['COUNT(*)'])

    # Get following count
    select_following = 'SELECT COUNT(*) FROM following WHERE username1 = ?'
    following_count = get_db().cursor().execute(
        select_following, data).fetchone()
    follow_info['following'] = following_count['COUNT(*)']

    # Checks if current user follows the owner of the page
    is_following = "SELECT COUNT(*) FROM \
    following WHERE username1 = ? AND username2 = ?"
    follow_data = (flask.session['username'], user_url_slug,)
    does_follow = get_db().cursor().execute(
        is_following, follow_data).fetchone()
    # does_follow['COUNT(*)'] is 1 if current user follows owner, 0 otherwise
    follow_info['does_follow'] = does_follow['COUNT(*)']

    # print('followers type: ', type(following_count))
    # print('followers out: ', following_count['COUNT(*)'])

    # print('follow_info dic: ', follow_info)

    return flask.render_template(
        "user.html",
        users=users_info,
        posts=posts_info,
        follows=follow_info)


@ethanisweird.app.route('/u/<user_url_slug>/followers/', methods=['GET', 'POST'])
def show_user_followers(user_url_slug):
    """Display /u/<user_url_slug>/followers/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for("show_login"))
    user_count = get_db().cursor().execute(
        "SELECT COUNT(*) FROM users where username = ?",
        (user_url_slug,)).fetchone()
    print(user_count['COUNT(*)'])
    if user_count['COUNT(*)'] == 0:
        return flask.redirect(flask.url_for('show_index'))

    # Handles POST requests
    if flask.request.method == 'POST':
        if 'username' not in flask.session:
            flask.abort(403)
        req = flask.request.form.to_dict()

        if 'follow' in req:
            get_db().cursor().execute(
                "INSERT INTO following(username1, username2) VALUES (?, ?)",
                (flask.session['username'], req['username'],))
        if 'unfollow' in req:
            get_db().cursor().execute(
                "DELETE FROM following WHERE username1 = ? AND username2 = ?",
                (flask.session['username'], req['username'],))

    # Get page owner's followers' usernames
    data = (user_url_slug,)
    select_followers = 'SELECT username1 FROM following WHERE username2 = ?'
    followers_names = get_db().cursor().execute(
        select_followers, data).fetchall()

    # print('followers type: ', type(followers_names))
    # print('followers out: ', followers_names)

    # Creates a list of dics containing user info (username, pro pic) from
    # page owner's followers'
    users_list = []
    for dic in followers_names:
        name_in = (dic['username1'],)
        select_users = 'SELECT username, \
        filename FROM users WHERE username = ?'
        users_info = get_db().cursor().execute(
            select_users, name_in).fetchone()
        users_list.append(users_info)

    # print('users_list: ', users_list)

    # Get list of user's that logged in user is following
    logged_in_user = (flask.session['username'],)
    select_following = 'SELECT username2 FROM following WHERE username1 = ?'
    following_names = get_db().cursor().execute(
        select_following, logged_in_user).fetchall()

    # print('following type: ', type(following_names))
    # print('following out: ', following_names)

    following_list = []
    for dic in following_names:
        following_list.append(dic['username2'])

    # print('following_list: ', following_list)

    return flask.render_template(
        "followers.html",
        users=users_list,
        following=following_list)


@ethanisweird.app.route('/u/<user_url_slug>/following/', methods=['GET', 'POST'])
def show_user_following(user_url_slug):
    """Display /u/<user_url_slug>/following/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for("show_login"))
    user_count = get_db().cursor().execute(
        "SELECT COUNT(*) FROM users where username = ?",
        (user_url_slug,)).fetchone()
    if user_count['COUNT(*)'] == 0:
        return flask.redirect(flask.url_for('show_index'))

    # Handles POST requests
    if flask.request.method == 'POST':
        if 'username' not in flask.session:
            flask.abort(403)
        req = flask.request.form.to_dict()
        if 'unfollow' in req:
            get_db().cursor().execute(
                "DELETE FROM following WHERE username1 = ? AND username2 = ?",
                (flask.session['username'], req['username']))
        if 'follow' in req:
            get_db().cursor().execute(
                "INSERT INTO following(username1, username2) VALUES (?, ?)",
                (flask.session['username'], req['username']))

    # Get usernames of users who the page owner followers
    data = (user_url_slug,)
    select_following = 'SELECT username2 FROM following WHERE username1 = ?'
    following_names = get_db().cursor().execute(
        select_following, data).fetchall()

    users_list = []
    for dic in following_names:
        name_in = (dic['username2'],)
        select_users = 'SELECT username, \
        filename FROM users WHERE username = ?'
        users_info = get_db().cursor().execute(
            select_users, name_in).fetchone()
        users_list.append(users_info)

    # Get usernames that logged in user follows
    logged_in_user = (flask.session['username'],)
    select_following_loggedin = 'SELECT \
    username2 FROM following WHERE username1 = ?'
    following_loggedin = get_db().cursor().execute(
        select_following_loggedin, logged_in_user).fetchall()

    following_list = []
    for dic in following_loggedin:
        following_list.append(dic['username2'])

    # print('Users followed:', users_list)

    return flask.render_template(
        "following.html",
        users=users_list,
        following=following_list)
