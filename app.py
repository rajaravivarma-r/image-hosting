import os
import logging

from pathlib import Path
from hashlib import md5
from functools import partial

import peewee
from sanic_session import InMemorySessionInterface
from sanic_jinja2 import SanicJinja2
from sanic import Sanic
from sanic.response import json, html, redirect
from jinja2 import Environment, FileSystemLoader, select_autoescape

from memegram.db.models import Image, Tag

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('./logs/sql.log')
logger.addHandler(file_handler)

UPLOAD_DIRECTORY = "./static/pictures"
VIEWS_PATH = Path(__file__).parent.joinpath("views")

app = Sanic('memegram', inspector=True)

jinja = SanicJinja2(app, loader=FileSystemLoader(str(VIEWS_PATH)))
session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)

jinja.add_env(
    "image_static_url", partial(app.url_for, "static", name="images")
)
# Serve CSS files
app.static("/css", "./static/css", name="css")
# Serve JS files
app.static("/js", "./static/js", name="js")
# Serve Image files
app.static("/images", "./static/pictures", name="images")


def save_image_details(image_file, image_filepath, image_tags=None):
    image_digest = md5(image_file.body).hexdigest()
    try:
        with Image.transaction():
            image = Image.create(
                filename=image_file.name,
                filepath=image_filepath,
                digest=image_digest,
            )
            tags = [Tag.create(name=tag_name) for tag_name in image_tags]
            image.tags = tags
        return True
    except peewee.IntegrityError as e:
        print("Duplicate file detected")
        return False


@app.middleware("request")
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    await session.open(request)


@app.middleware("response")
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    await session.save(request, response)


def render_template(filename, request, **template_variables):
    return jinja.render(
        filename,
        errors=request.get("flash", {}).get("errors", []),
        info=request.get("flash", {}).get("info", []),
        **template_variables,
    )


@app.route("/")
async def test(request):
    return redirect(app.url_for("index"))


@app.route("/upload", methods=["POST"])
async def upload(request):
    picture_file = request.files["picture"][0]
    image_tags = set(request.form.get('tags').split(','))
    if len(picture_file.name) > 0:
        filepath = os.path.join(UPLOAD_DIRECTORY, picture_file.name)

        if save_image_details(picture_file, filepath, image_tags):
            with open(filepath, "wb") as f:
                f.write(picture_file.body)
            jinja.flash(request, "successfully saved image", "success")
        else:
            jinja.flash(request, "Image file already exists", "danger")
    else:
        jinja.flash(request, "Please upload a file", "danger")

    return redirect(app.url_for("index"))


@app.route("/index")
async def index(request):
    image_files = Image.select()
    return jinja.render("layout.html.jinja2", request, image_files=image_files)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
