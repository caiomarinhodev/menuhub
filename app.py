import os

from flask import Flask

import auth
import db
import menu

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
)


@app.route("/hello")
def hello():
    return "Hello, World!"


# register the database commands
db.init_app(app)

# apply the blueprints to the app

app.register_blueprint(auth.bp)
app.register_blueprint(menu.bp)

# make url_for('index') == url_for('blog.index')
# in another app, you might define a separate main index here with
# app.route, while giving the blog blueprint a url_prefix, but for
# the tutorial the blog will be the main index
app.add_url_rule("/", endpoint="index")

if __name__ == '__main__':
    app.run()
