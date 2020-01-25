import datetime
import sys
import subprocess
from flask import Flask, request
import sqlalchemy as sa

app = Flask(__name__)


template = "<html><head><title>entendre?</title></head><body>{}</body></html>"
input_field = '<form action="." method="POST"><textarea name="text"></textarea><input type="submit" value="add"></form>'

metadata = sa.MetaData()
msgs = sa.Table(
    "msgs",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("text", sa.Text),
    sa.Column("created_at", sa.Date, default=datetime.datetime.now),
)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="entendre",
    password="entendre password",
    hostname="entendre.mysql.pythonanywhere-services.com",
    databasename="entendre$test",
)
engine = sa.create_engine(SQLALCHEMY_DATABASE_URI)
metadata.create_all(engine)


@app.route("/", methods=["GET", "POST"])
def main() -> str:
    try:
        conn = engine.connect()
        if request.method == "POST":
            ins = sa.sql.text("""INSERT INTO msgs (text) VALUES (":text");""")
            conn.execute(ins, text=request.form["text"])
        log = "<br/>".join(str(row[0]) for row in conn.execute("SELECT text FROM msgs"))
        return template.format(log + input_field)
    finally:
        conn.close()


@app.route("/version")
def version() -> str:
    return sys.version


@app.route("/pull_git")
def pull_git() -> str:
    return subprocess.run(
        "git pull origin master".split(), capture_output=True, text=True, check=False
    ).stdout
