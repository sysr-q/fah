#!/usr/bin/env python2
from __future__ import print_function
from collections import defaultdict
import uuid

class Room(object):
	def __init__(self):
		self.name = None
		self.users = {}
		self.expansions = [0]  # 0 -> Base


class User(object):
	def __init__(self, handle, trip=None, first=False):
		self.uuid = uuid.uuid4()
		self.handle = handle
		self.trip = trip
		self.first = first
		self.rooms = []  # {name: _, owner: _}
		self.cards = []  # list of ids (usually 10)

	# NOTE: don't remove these, they might keep shit working. Can't remember.
	#       Sorry, future maintainer(s).
	def __new__(cls, *args, **kwargs):
		return super(User, cls).__new__(cls, *args, **kwargs)

	def __copy__(self):
		return self

	def __deepcopy__(self):
		return self
