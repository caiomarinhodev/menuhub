from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from auth import login_required
from db import get_db

bp = Blueprint("menu", __name__)


@bp.route("/")
def index():
    """Show all the menus, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT *"
        " FROM menu m JOIN user u ON m.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("hub/index.html", posts=posts)


def get_menu(id, check_author=True):
    """Get a menu and its author by id.
    Checks that the id exists and optionally that the current user is
    the author.
    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    menu = (
        get_db()
        .execute(
            "SELECT *"
            " FROM menu m JOIN user u ON m.author_id = u.id"
            " WHERE m.id = ?",
            (id,),
        )
        .fetchone()
    )

    if menu is None:
        abort(404, f"Menu id {id} doesn't exist.")

    if check_author and menu["author_id"] != g.user["id"]:
        abort(403)

    return menu


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO menu (title, author_id) VALUES (?, ?, ?)",
                (title, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("menu.index"))

    return render_template("hub/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_menu(id)

    if request.method == "POST":
        title = request.form["title"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE menu SET title = ? WHERE id = ?", (title, id)
            )
            db.commit()
            return redirect(url_for("menu.index"))

    return render_template("hub/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.
    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_menu(id)
    db = get_db()
    db.execute("DELETE FROM menu WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("menu.index"))
