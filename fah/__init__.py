#!/usr/bin/env python2
from __future__ import print_function
from flask import (Flask, render_template, request, redirect, url_for, session)
from flask.ext.socketio import (SocketIO, emit, leave_room, join_room)
from .database import (db, Expansion, BlackCard, WhiteCard)

ROOMS = {
	# room_id: { users: { name: _, cards: [_, _, ...] }, expansions: [_, _, ...] }
}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# TODO: put in witchcraft env vars
app.debug = True
app.secret_key = '\xfepSY)\x836\xea\xfc\xa4\xcd$\xe1aZ\x04' 
db.init_app(app)
socketio = SocketIO(app)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/.room", methods=["POST"])
def room_rd():
	roomname = request.form["room"]
	session['handle'] = request.form["handle"]
	return redirect(url_for("room", name=roomname))

@app.route("/room/<name>")
def room(name):
	expansions = Expansion.query.all()
	return render_template("room.html",
							room=name,
							handle=session.get("handle", ""),
							expansions=expansions)

@socketio.on("connect")
def si_connect():
	emit("chat", "Hello!")

@socketio.on("disconnect")
def si_disconnect():
	pass

@socketio.on("join")
def si_join(data):
	room = data['room']

	join_room(room)
	emit("player.join", {"uuid": "TODO", "handle": data['handle']}, room=room)

	print("-->", data['handle'], "joined room", room)

"""
@socketio.on("leave")
def si_leave(data):
	room_leave(room)
"""
