"""Helper function for checking if logged in user."""
import flask
import ethanisweird


def get_logged_in():
    """Return 403 if not logged in."""
    if "username" not in flask.session:
        return False

    return True

def out_of_range(postid):
    """Return 404 if pageid is out of range."""
    connection = ethanisweird.model.get_db()

    cur_maxpostid = connection.execute("SELECT MAX(postid) FROM posts")

    if postid > cur_maxpostid.fetchone()['MAX(postid)']:
        return True
    return False
