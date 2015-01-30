#!/usr/bin/env python2
from __future__ import print_function
import os

from gevent import monkey
monkey.patch_all()

from flask import (Flask, render_template, request, redirect, url_for, session,
					make_response)
from flask.ext.socketio import (SocketIO, emit, leave_room, join_room)
from flask.ext.kvsession import KVSessionExtension
from simplekv.db.sql import SQLAlchemyStore
from simplekv.memory import DictStore
import q

from .database import (db, Expansion, BlackCard, WhiteCard)
from .room import (Room, User, rooms)

def create_app():
	app = Flask(__name__)
	# TODO: put in witchcraft env vars
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/xyzzy.db'
	app.debug = bool(os.getenv("FAH_DEBUG", 0))
	app.secret_key = '\xfepSY)\x836\xea\xfc\xa4\xcd$\xe1aZ\x04'

	db.init_app(app)
	socketio = SocketIO(app)

	with app.app_context():
		if app.debug:
			db.drop_all()

		# These two aren't /really/ needed, but in the future perhaps.
		#store = SQLAlchemyStore(db.engine, db.metadata, 'kvsessions')
		store = DictStore()
		kvsession = KVSessionExtension(store, app)

		db.create_all()

	return app, socketio

app, socketio = create_app()

####################

@app.before_request
def setup_user():
	# If we've not got a user setup already, create one.
	# This way we know for a fact there's a user-session.
	if "user" in session:
		return

	session["user"] = User(None)  # No handle, but .uuid is unique per player.

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/.room", methods=["POST"])
def room_rd():
	return redirect(url_for("roomx", name=request.form["room"]))


@app.route("/room/<name>")
def roomx(name):
	room = rooms[name]
	room.users.append(session['user'])
	first = len(room.users) == 1  # ^ race condition 101

	expansions = Expansion.query.all()
	return render_template("room.html",
							room=name,
							user=session['user'],
							expansions=expansions)


@socketio.on("connect")
def si_connect():
	setup_user()

	join_room(session['user'].uuid)

	emit("player.uuid", {"uuid": session['user'].uuid})

	if session['user'].handle is not None:
		emit("player.force-handle", {"handle": session['user'].handle})


@socketio.on("disconnect")
def si_disconnect():
	pass


@socketio.on("join")
def si_join(data):
	room = data['room']

	join_room(room)
	emit("player.join", {"uuid": session['user'].uuid, "handle": session['user'].handle}, room=room)

	print("-->", session['user'].handle, "joined room", room)


@socketio.on("player.rehandle")
def si_rehandle(data):
	q(session)
	session['user'].handle = data['handle']
	session.modified = True
	app.save_session(session, make_response('dummy'))
