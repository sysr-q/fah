#!/usr/bin/env python2
from __future__ import print_function
from flask import (Flask, render_template, request, redirect, url_for)
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/.room", methods=["POST"])
def room_rd():
	roomname = request.form["room"]
	handle = request.form["handle"]
	return redirect(url_for("room", name=roomname, _anchor=handle))

@app.route("/room/<name>")
def room(name):
	return render_template("room.html", room=name)

@socketio.on("connect")
def si_connect():
	emit("chat", "Hello!")

@socketio.on("disconnect")
def si_disconnect():
	pass

@socketio.on("join")
def si_join(data):
	print("-->", data)

@socketio.on("leave")
def si_leave(data):
	print("<--", data)
