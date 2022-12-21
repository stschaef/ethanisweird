"""
Insta485 accounts views.

URL:
/accounts/login/
/accounts/logout/
/accounts/create/
/accounts/delete/
/accounts/edit/
/accoutns/password/
"""
import os
import hashlib
import flask
import ethanisweird
from ethanisweird.model import get_db
from ethanisweird.views.view_helper import hash_password
from ethanisweird.views.view_helper import hash_file_and_save


@ethanisweird.app.route('/accounts/login/', methods=['GET', 'POST'])
def show_login():
    """Display /accounts/login/ route."""
    if 'username' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    if flask.request.method == 'POST':
        req = flask.request.form.to_dict()

        get_password = "SELECT password FROM users WHERE username = ?"
        db_password = get_db().cursor().execute(
            get_password, (req['username'],)).fetchone()
        print(req)
        print(db_password)
        algorithm = 'sha512'

        # salt with always be between indices 7 and 39, inclusive
        salt = db_password['password'][7:39]

        hash_obj = hashlib.new(algorithm)
        in_password_salted = salt + req['password']
        hash_obj.update(in_password_salted.encode('utf-8'))
        in_password_hash = hash_obj.hexdigest()
        in_password_string = "$".join([algorithm, salt, in_password_hash])

        if in_password_string != db_password['password']:
            flask.abort(403)

        flask.session['username'] = flask.request.form['username']
        return flask.redirect(flask.url_for('show_index'))
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head><title>Ethan Is Weird</title></head>
        <body>
        <h1><a href = "/">Ethan Is Weird</a></h1>

        <!-- DO NOT CHANGE THIS (aside from styling) -->
        <form action="" method="post" enctype="multipart/form-data">
        <input type="text" name="username" placeholder="Username"/><br>
        <input type="password" name="password" placeholder="Password"/><br>
        <input type="submit" value="login"/>
        </form>

        <p>Don't have an account?</p><b>
        <a href="/accounts/create/">Sign up here</a></b>
        </body>
        </html>'''


@ethanisweird.app.route('/accounts/logout/')
def show_logout():
    """Display /acounts/logout/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for("show_login"))
    flask.session.clear()

    return flask.redirect(flask.url_for("show_login"))


@ethanisweird.app.route('/accounts/create/', methods=['GET', 'POST'])
def show_create():
    """Display /acounts/create/ route."""
    #  Handles POST requests
    if 'username' in flask.session:
        return flask.redirect(flask.url_for("show_edit"))
    if flask.request.method == 'POST':
        req = flask.request.form.to_dict()
        print(req)

        count_username = "SELECT COUNT(1) FROM users WHERE username = ?"
        username_dict = get_db().cursor().execute(
            count_username, (req['username'],)).fetchone()
        username_count = username_dict['COUNT(1)']
        if username_count != 0:
            flask.abort(409)
        if req['password'] == '':
            flask.abort(400)

        # If not the two above errors, then login successful

        password_db_string = hash_password(req['password'])
        new_filename = hash_file_and_save(flask.request.files['file'])

        # Inserts user data into database
        insert_user = "INSERT INTO users(username, fullname, \
        email, filename, password) VALUES (?, ?, ?, ? ,?)"
        data = (
            req['username'],
            req['fullname'],
            req['email'],
            new_filename,
            password_db_string,
        )
        get_db().cursor().execute(insert_user, data)

        # Logs user in and redirects them to '/'
        flask.session['username'] = flask.request.form['username']
        return flask.redirect(flask.url_for("show_index"))

    # TO DO: style this ugly page
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head><title>Insta485</title></head>
        <body>
            <h1><a href = "/">Insta485</a></h1>

            <form action="" method="post" enctype="multipart/form-data">
                Photo <input type="file" id="photo" name="file"><br>
                Name <input type="text" name="fullname"/><br>
                Username <input type="text" name="username"/><br>
                Email <input type="text" name="email"/><br>
                Password <input type="password" name="password"/><br>
                <input type="submit" name="signup" value="sign up"/><br>
            </form>

            <p> Have an account already? </p> <b>
            <a href="/accounts/login/"> Log in </a></b>
        </body>
        </html>'''

# May need GET and POST methods
# TO DO:


@ethanisweird.app.route('/accounts/delete/', methods=['GET', 'POST'])
def show_delete():
    """Display /acounts/delete/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for("show_login"))
    if flask.request.method == 'POST':
        if 'username' not in flask.session:
            flask.abort(403)
        # Delete all relevant files in the filesystem
        get_user_info = 'SELECT * FROM users WHERE username = ?'
        user_info = get_db().cursor().execute(
            get_user_info, (flask.session['username'],),).fetchone()
        prof_pic_path = user_info['filename']

        files_to_delete = [prof_pic_path]

        get_post_pics = 'SELECT filename FROM posts WHERE owner = ?'
        post_pics_dict = get_db().cursor().execute(
            get_post_pics, (flask.session['username'],),).fetchall()

        for post in post_pics_dict:
            files_to_delete.append(post['filename'])

        for old_file in files_to_delete:
            deleted_file = os.path.join(
                ethanisweird.config.UPLOAD_FOLDER, old_file)
            os.remove(deleted_file)

        # Delete all relevant entries in the database
        delete_user = 'DELETE FROM users WHERE username = ?'
        get_db().cursor().execute(delete_user, (flask.session['username'],),)
        delete_post = 'DELETE FROM posts WHERE owner = ?'
        get_db().cursor().execute(delete_post, (flask.session['username'],),)
        delete_follow = 'DELETE FROM following WHERE username1 = ?'
        get_db().cursor().execute(delete_follow, (flask.session['username'],),)
        delete_following = 'DELETE FROM following WHERE username2 = ?'
        get_db().cursor().execute(
            delete_following, (flask.session['username'],),)
        delete_comments = 'DELETE FROM comments WHERE owner = ?'
        get_db().cursor().execute(
            delete_comments, (flask.session['username'],),)
        delete_likes = 'DELETE FROM likes WHERE owner = ?'
        get_db().cursor().execute(delete_likes, (flask.session['username'],),)

        flask.session.clear()

        return flask.redirect(flask.url_for("show_create"))

    # TO DO: style page
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head><title>Insta485</title></head>
        <body>
            <h1><a href = "/">Insta485</a> <a href = "/explore/">explore</a> |
            <a href = "/u/''' + flask.session['username'] + '''/"> \
            ''' + flask.session['username'] + '''</a></h1>

            <h2><b> ''' + flask.session['username'] + ''' </b></h2>

            <!-- DO NOT CHANGE THIS (aside from styling) -->
            <form action="" method="post" enctype="multipart/form-data">
                <input type="submit" name="delete"
                value="confirm delete account"/>
            </form>
        </body>
        </html>'''


@ethanisweird.app.route('/accounts/edit/', methods=['GET', 'POST'])
def show_edit():
    """Display /acounts/edit/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for("show_login"))
    user = (flask.session['username'],)

    get_user_info = 'SELECT * FROM users WHERE username = ?'
    user_info = get_db().cursor().execute(get_user_info, user,).fetchone()

    prof_pic_path = flask.url_for(
        "download_file", filename=user_info['filename'])

    if flask.request.method == 'POST':
        if 'username' not in flask.session:
            flask.abort(403)
        req = flask.request.form.to_dict()
        print(req)

        filename_ = user_info['filename']

        if 'file' in req and req['file'] != "":
            req = flask.request.form.to_dict()
        print(req)

        filename_ = user_info['filename']

        if 'file' in flask.request.files:
            filename_ = hash_file_and_save(flask.request.files['file'])

        # dummy, temp_filename = tempfile.mkstemp()
        # flask.request.files['file'].save(temp_filename)

        # # Compute filename
        # hash_txt = sha256sum(temp_filename)
        # dummy, suffix = os.path.splitext(
        #     flask.request.files['file'].filename)
        # hash_filename_basename = hash_txt + suffix

        # filename_ = hash_filename_basename

        fullname_ = req['fullname']
        email_ = req['email']

        # Inserts user data into database
        update_user = "UPDATE users SET filename = ?, \
        fullname = ?, email = ? WHERE username = ?"
        data = (
            filename_,
            fullname_,
            email_,
            user_info['username']
        )
        get_db().cursor().execute(update_user, data)

        return flask.redirect(flask.url_for("show_edit"))

    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head><title>Insta485</title></head>
        <body>
            <h1><a href = "/">Insta485</a> <a href = "/explore/">explore</a> |
            <a href = "/u/''' + user_info['username'] + '''/"> \
            ''' + user_info['username'] + '''</a></h1>

            <img src ="''' + prof_pic_path + '''"
            alt = "profile pic" style="height:40px;margin-right: 10px">
            <h2><b> ''' + user_info['username'] + ''' </b></h2>

            <form action="" method="post" enctype="multipart/form-data">
                <input type="file" name="file"><br>
                <input type="text" name="fullname" value="''' \
                + user_info['fullname'] + '''"/><br>
                <input type="text" name="email" value="''' \
                + user_info['email'] + '''"/><br>
                <input type="submit" name="update" value="submit"/><br>
            </form>

            <b><a href="/accounts/password/"> Change password </a></b>

            <b><a href="/accounts/delete/"> Delete account </a></b>
        </body>
        </html>'''


@ethanisweird.app.route('/accounts/password/', methods=['GET', 'POST'])
def show_password():
    """Display /acounts/password/ route."""
    if 'username' not in flask.session:
        return flask.redirect(flask.url_for("show_login"))
    user = (flask.session['username'],)

    get_user_info = 'SELECT * FROM users WHERE username = ?'
    user_info = get_db().cursor().execute(get_user_info, user,).fetchone()

    if flask.request.method == 'POST':
        if 'username' not in flask.session:
            flask.abort(403)
        req = flask.request.form.to_dict()

        get_password = "SELECT password FROM users WHERE username = ?"
        db_password = get_db().cursor().execute(
            get_password, (user_info['username'],)).fetchone()

        algorithm = 'sha512'

        # salt with always be between indices 7 and 39, inclusive
        salt = db_password['password'][7:39]

        hash_obj = hashlib.new(algorithm)
        in_password_salted = salt + req['password']
        hash_obj.update(in_password_salted.encode('utf-8'))
        in_password_hash = hash_obj.hexdigest()
        in_password_string = "$".join([algorithm, salt, in_password_hash])

        # Check if current password is correct
        if in_password_string != db_password['password']:
            flask.abort(403)

        # Check if both entries of the new password match
        if req['new_password1'] != req['new_password2']:
            flask.abort(401)

        # Both passwords match, so hash and put into database
        password_db_string = hash_password(req['new_password1'])

        update_password = "UPDATE users SET password = ? WHERE username = ?"

        data = (
            password_db_string,
            user_info['username'],
        )

        get_db().cursor().execute(update_password, data)

        return flask.redirect(flask.url_for('show_edit'))

    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head><title>Insta485</title></head>
        <body>
            <h1><a href = "/">Insta485</a> <a href = "/explore/">explore</a> |
                <a href = "/u/''' + user_info['username'] + '''/"> \
                ''' + user_info['username'] + '''</a></h1>

            <h2><b> ''' + user_info['username'] + ''' </b></h2>

            <form action="" method="post" enctype="multipart/form-data">
                Old password <input type="password" name="password"/><br>
                New password <input type="password" name="new_password1"/><br>
                New password, again <input type="password"
                name="new_password2"/><br>
                <input type="submit" name="update_password"
                value="submit"/><br>
            </form>

            <b><a href="/accounts/edit/"> Back to edit account </a></b>
        </body>
        </html>'''
