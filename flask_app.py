import datetime
import sys
import subprocess
from flask import Flask, request
import sqlalchemy as sa

app = Flask(__name__)
app.config["DEBUG"] = True

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
USERNAME = "entendre"
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=USERNAME,
    password="entendre password",
    hostname="entendre.mysql.pythonanywhere-services.com",
    databasename="entendre$test",
)
CWD = f"/home/{USERNAME}/mysite"

engine = sa.create_engine(SQLALCHEMY_DATABASE_URI)
metadata.create_all(engine)


@app.route("/", methods=["GET", "POST"])
def main() -> str:
    try:
        conn = engine.connect()
        if request.method == "POST":
            ins = msgs.insert().values(text=request.form["text"])
            conn.execute(ins)
        log = "<br/>".join(str(row[0]) for row in conn.execute("SELECT text FROM msgs"))
        return template.format(log + input_field)
    finally:
        conn.close()


@app.route("/version")
def version() -> str:
    commit_version = subprocess.run(
        "git log -1".split(),
        capture_output=True,
        text=True,
        cwd=CWD,
        check=False,
    )
    return f"commit: {commit_version}\n python:{sys.version}"


@app.route("/pull_git")
def pull_git() -> str:
    with open("pull_git_log", "a") as f:
        f.write(datetime.datetime.now().isoformat() + ": pulling git\n")
    txt = subprocess.run(
        "git pull origin master".split(),
        capture_output=True,
        text=True,
        cwd=CWD,
        check=False,
    ).stdout
    with open("pull_git_log", "a") as f:
        f.write(datetime.datetime.now().isoformat() + ": " + txt + "\n")
    assert txt
    return txt
