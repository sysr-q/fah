#!/usr/bin/env python2
from __future__ import print_function
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # NOTE: run db.init_app(app)


class Expansion(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), nullable=False)
	ident = db.Column(db.String(64), unique=True, nullable=False)
	description = db.Column(db.Text, nullable=False)
	# TODO: cascade
	black_cards = db.relationship("BlackCard", backref="expansion", lazy="dynamic")
	white_cards = db.relationship("WhiteCard", backref="expansion", lazy="dynamic")

	def __init__(self, name, ident, description):
		self.name = name
		self.ident = ident
		self.description = description


class BlackCard(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text, nullable=False)
	answers = db.Column(db.Integer)
	# .expansion <- relationship
	expansion_id = db.Column(db.Integer, db.ForeignKey('expansion.id'))

	def __init__(self, text, answers, expansion_id=None):
		self.text = text
		self.answers = answers  # NOTE: actually a number
		self.expansion_id = expansion_id


class WhiteCard(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text, nullable=False)
	trump = db.Column(db.Boolean)
	# .expansion <- relationship
	expansion_id = db.Column(db.Integer, db.ForeignKey('expansion.id'))

	def __init__(self, text, trump, expansion_id=None):
		self.text = text
		self.trump = trump
		self.expansion_id = expansion_id
