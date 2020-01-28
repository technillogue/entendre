import datetime
import sys
import subprocess
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit
#import sqlalchemy as sa

app = Flask(__name__)
app.config["DEBUG"] = True
socketio = SocketIO(app)
"""
metadata = sa.MetaData()
msgs = sa.Table(
    "msgs",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    #    sa.Column("author", sa.Text),
    sa.Column("text", sa.Text),
    sa.Column("created_at", sa.Date, default=datetime.datetime.now),
)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=USERNAME,
    password="entendre password",
    hostname="entendre.mysql.pythonanywhere-services.com",
    databasename="entendre$test",
)

engine = sa.create_engine(SQLALCHEMY_DATABASE_URI)
metadata.create_all(engine)
"""

USERNAME = "entendre"
CWD = f"/home/{USERNAME}/mysite"

@app.route("/", methods=["GET", "POST"])
def main() -> str:
    return "hello world"
"""
try:
        conn = engine.connect()
        if request.method == "POST":
            ins = msgs.insert().values(text=request.form["text"])
            conn.execute(ins)
        messages = [str(row[0]) for row in conn.execute("SELECT text FROM msgs")]
        return render_template("simple_main.html", messages=messages)
    finally:
        conn.close()


@app.route("/fancy", methods=["GET", "POST"])
def fancy() -> str:
    return render_template("main.html")

"""
@app.route("/version")
def version() -> str:
    commit_version = subprocess.run(
        "git log -1".split(), capture_output=True, text=True, cwd=CWD, check=False,
    ).stdout
    return f"commit: {commit_version}<br/> python:{sys.version}"

@app.route("/emit_msg", methods=["GET", "POST"])
def emit_msg() -> str:
    message = request.args.get("msg", "poke")
    emit("chat message", message)
    return '<a href="#?msg=hewwo">hewwo??</a>'

@socketio.on("chat message")
def handle_chat_msg(msg):
    emit("chat message", f"you said {msg}")

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
