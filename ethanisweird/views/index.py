"""
Insta485 index (main) view.

URLs include:
/
/explore/
"""
import flask
import ethanisweird
from ethanisweird.model import get_db
from ethanisweird.views.post_helper import get_post_info


@ethanisweird.app.route('/uploads/<path:filename>')
def download_file(filename):
    """Routes to the path to file file images."""
    return flask.send_from_directory(
        ethanisweird.app.config['UPLOAD_FOLDER'], filename)

# TO DO:


@ethanisweird.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    if 'username' in flask.session:

        if flask.request.method == 'POST':
            if 'username' not in flask.session:
                flask.abort(403)
            # TO DO: This logical structure may be wrong
            req = flask.request.form.to_dict()
            if 'uncomment' in req:
                get_db().cursor().execute(
                    'DELETE FROM comments WHERE commentid = ?',
                    (req['commentid'],))
            elif 'like' in req:
                get_db().cursor().execute(
                    'INSERT INTO likes(owner, postid) VALUES (?, ?)',
                    (flask.session['username'], req['postid'],))
            elif 'comment' in req:
                get_db().cursor().execute(
                    'INSERT INTO \
                    comments(postid, owner, text) VALUES (?, ?, ?)',
                    (req['postid'], flask.session['username'], req['text'],))
            elif 'unlike' in req:
                get_db().cursor().execute(
                    'DELETE FROM likes WHERE owner = ? AND postid= ?',
                    (flask.session['username'], req['postid'],))
            elif 'delete' in req:
                get_db().cursor().execute(
                    'DELETE FROM posts WHERE owner = ? AND postid = ?',
                    (flask.session['username'], req['postid'],))
                # Keep running into FOREIGN KEY constraint violated with the
                # above lines

                # TO DO: Delete everything else related to this file and post
                # from the databsse

                return flask.redirect(flask.url_for('show_index'))

        # Get list of user's that logged in user is following
        logged_in_user = (flask.session['username'],)
        select_following = 'SELECT \
        username2 FROM following WHERE username1 = ?'
        following_names = get_db().cursor().execute(
            select_following, logged_in_user).fetchall()

        following_list = []
        for dic in following_names:
            following_list.append(dic['username2'])

        following_list.append(flask.session['username'])
        # print('following_list: ', following_list)

        # Use the following_list to get the post id's that should appear on
        # user's home page
        select_pids = 'SELECT postid FROM posts WHERE owner \
        IN (%s) ORDER BY postid DESC' % ','.join('?' * len(following_list))
        print(select_pids)
        pid_dic = get_db().cursor().execute(
            select_pids, following_list).fetchall()

        # print('pid_dic type: ', type(pid_dic))
        # print('pid_dic: ', pid_dic)

        # Get info for each post(dic from post_helper) in a list
        post_info = []
        for pid in pid_dic:
            # print(pid['postid'])
            post_info.append(get_post_info(str(pid['postid'])))

        # print('post_info: ', post_info)

        # for post in post_info:
        #     print('########')
        #     print('########')
        #     print('~~~post #: ', post['posts_']['postid'])
        #     print('~~~~~~~~~~')
        #     for part in post:
        #         print(part)

        return flask.render_template("index.html", posts=post_info)
    return flask.redirect(flask.url_for("show_login"))

# TO DO:


@ethanisweird.app.route('/explore/', methods=['GET', 'POST'])
def show_explore():
    """Display /explore/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for("show_login"))
    # Handles POST requests
    if flask.request.method == 'POST':
        if 'username' not in flask.session:
            flask.abort(403)
        req = flask.request.form.to_dict()
        if 'follow' in req:
            get_db().cursor().execute(
                "INSERT INTO following(username1, username2) VALUES (?, ?)",
                (flask.session['username'], req['username']))

    # print('users_possible', users_possible)

    # Get all users that logged in user follows and put them in python list
    data = (flask.session['username'],)
    select_following = 'SELECT username2 FROM following WHERE username1 = ?'
    following_dic = get_db().cursor().execute(
        select_following, data).fetchall()

    following_list = []
    for name in following_dic:
        following_list.append(name['username2'])

    # print('following_names', following_list)

    # get list of all usernames in DB
    all_users_dic = get_db().cursor().execute(
        'SELECT username FROM users').fetchall()

    # print('all users dic: ', all_users_dic)

    # Compare the total list to the followers list and add any that the logged
    # in user isn't following to users_list
    users_list = []
    for dic in all_users_dic:
        if dic['username'] not in following_list \
          and dic['username'] != flask.session['username']:
            name_in = (dic['username'],)
            select_user_info = 'SELECT username, \
            filename FROM users WHERE username = ?'
            users_info = get_db().cursor().execute(
                select_user_info, name_in).fetchone()
            users_list.append(users_info)

    # print('FINAL users list: ', users_list)
    return flask.render_template("explore.html", users=users_list)
