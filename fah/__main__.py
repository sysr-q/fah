#!/usr/bin/env python2
import os
from fah import app, socketio

socketio.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
