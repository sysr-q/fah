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

from .database import (db, Expansion, BlackCard, WhiteCard)
from .room import (Room, User)
from .trip import mktripcode

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

def _get_room():
	# TODO: bad
	# Forgive me, #basedgod, for I have sinned.
	return list(request.namespace.rooms)[-1] if len(request.namespace.rooms) > 0 else None

def _room(r):
	if r in socketio.rooms:
		return socketio.rooms[r]
	if '' in socketio.rooms:
		return socketio.rooms[''].get(r, [])
	return []

def _sync_session():
	room = _get_room()
	uuid = session['user'].uuid

	# These two lines are required to sync the session data.
	session.modified = True
	app.save_session(session, make_response('dummy'))

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
	setup_user()

	room = _room(name)
	session['user'].first = room is None or len(room) == 1

	expansions = Expansion.query.all()
	return render_template("room.html",
							room=name,
							user=session['user'],
							expansions=expansions,
							first=session['user'].first)


@socketio.on("connect")
def si_connect():
	if "user" not in session:
		# Refresh your page, nimrod.
		emit("player.force-refresh")
		return

	join_room(session['user'].uuid)

	emit("player.uuid", {"uuid": session['user'].uuid}, room=session['user'].uuid)

	if session['user'].handle is not None:
		emit("player.force-handle", {"handle": session['user'].handle}, room=session['user'].uuid)


@socketio.on("disconnect")
def si_disconnect():
	room = _get_room()  # TODO
	emit("player.leave", {"uuid": session['user'].uuid}, room=room)


@socketio.on("join")
def si_join(data):
	room = data['room']

	emit("player.join", {"uuid": session['user'].uuid,
						 "handle": session['user'].handle,
						 "trip": session['user'].trip}, room=room)

	joins = []
	for ns in _room(room):
		p = ns.session['user']
		joins.append({
			"uuid": p.uuid,
			"handle": p.handle,
			"trip": p.trip,
		})

	emit("player.joins", joins, room=session['user'].uuid)
	join_room(room)

	#print("-->", session['user'].handle, "joined room", room)


@socketio.on("player.rehandle")
def si_rehandle(data):
	handle, trip_phrase = data['handle'], ""
	if "#" in handle:
		handle, trip_phrase = handle.split("#", 1)

	session['user'].handle = handle
	if trip_phrase:
		session['user'].trip = mktripcode(trip_phrase, salt=app.secret_key)

	room = _get_room()
	emit("player.name-change", {"uuid": session['user'].uuid,
								"handle": handle,
								"trip": session['user'].trip}, room=room)
	emit("player.force-handle", {"handle": handle}, room=session['user'].uuid)

	_sync_session()


@socketio.on("__users")
def si__users(room):
	u = []
	for ns in _room(room):
		p = ns.session['user']
		u.append({
			"uuid": p.uuid,
			"handle": p.handle,
			"trip": p.trip,
		})
	emit("__users", u)

@socketio.on("__room")
def si__room():
	emit("__room", list(request.namespace.rooms))
