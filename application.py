import os
from flask import Flask, session, request, redirect, render_template, flash, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit, send, leave_room, join_room

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# List of users
logged_users = []

# Dictionary for channels. Default channel is general
channel_list = {"general":[]}

# Index page to redirect logged in users
@app.route("/", methods=["GET","POST"])
def index():
    if session.get("user"):
        return redirect("/channels/" + next(iter(channel_list)))
    else:
        return render_template("login.html")

# Login page
@app.route("/login", methods=["GET","POST"])
def login():
    # Get display name from form
    display_name = request.form.get("name")

    if request.method == "POST":
        # Verify if user is already registered
        if display_name in logged_users:
            flash("Username already in use", "warning")
            return redirect (url_for("index"))
        else:
            # Add user to the list
            logged_users.append(display_name)
            session["user"] = display_name

            return render_template("create.html")
    else:
        return render_template("login.html")

# 404 Error if page not found
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

# Logout user from the session
@app.route("/logout")
def logout():
    # Remove user from session
    user = session["user"]
    session.pop("user", None)
    session["user"] = []

    # Remove user from the list
    try:
        logged_users.remove(user)
    except:
        pass

    return redirect(url_for("login"))

# Create a new channel
@app.route("/create", methods=["GET","POST"])
def create():
    # Get channel name from the form
    channel_name = request.form.get("channel")

    if request.method == "POST":
        # Assign session channel to the user provided channel name
        session["channel"] = channel_name

        # Verify if the channel exists
        if channel_name in channel_list:
            flash("Channel already exists. Joining you to current channel", "warning")
        # If not, add it to dictionary
        channel_list[channel_name] = []

        # Redirect user to the channel page
        return redirect("/channels/" + channel_name)

    return render_template("channels.html")

# Delete channel
@app.route("/delete", methods=["GET","POST"])
def delete():

    # Get confirmation from the user
    confirmation = request.form.get("options")
    channel_name = session["existing_channel"]

    if request.method == "POST":
        if confirmation == "Yes":
            del channel_list[channel_name]
        else:
            redirect("/channels/" + channel_name)

    # Redirect user to default channel
    return redirect("/channels/" + next(iter(channel_list)))

# Individual Channels
@app.route("/channels/<channel>", methods=["GET", "POST"])
def channels(channel):
    if not session.get("user"):
        return render_template("login.html")

    session["existing_channel"] = channel

    if request.method == "POST":
        return redirect("/")

    return render_template("channels.html", channels=channel_list, messages=channel_list[channel], user=session["user"], logged_users=logged_users)

# Join user to the channel
@socketio.on("join", namespace="/")
def join():
    channel_room = session.get("existing_channel")
    user_name = session.get("user")
    join_room(channel_room)

# Send message to channel
@socketio.on("send message")
def send_msg(msg, timestamp):

    channel_room = session.get("existing_channel")

    # Count total number of messages
    channel_message_count = len(channel_list[channel_room])

    # If there are more than 100 messages; delete the first message in the list
    if channel_message_count > 100:
        del channel_list[channel_room][0]

    # Append data to channel_list dictionary
    channel_list[channel_room].append([timestamp, session.get("user"), msg])

    emit("announce message", {
        "user": session.get("user"),
        "timestamp": timestamp,
        "msg": msg},
        room=channel_room)
