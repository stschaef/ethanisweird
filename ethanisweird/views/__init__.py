"""Views, one for each Insta485 page."""
from ethanisweird.views.index import download_file, show_index, show_explore
from ethanisweird.views.accounts import show_login, show_logout, show_create
from ethanisweird.views.accounts import show_delete, show_edit, show_password
from ethanisweird.views.user import show_user, show_user_followers
from ethanisweird.views.user import show_user_following
from ethanisweird.views.post import show_post
