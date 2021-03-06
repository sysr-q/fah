"""
"""
from setuptools import setup

kw = {
	"name": "fah",
	"version": "0.1.2",
	"description": "Flask Against Humanity (copyright infringement pending).",
	"long_description": __doc__,
	"url": "https://github.com/sysr-q/fah",
	"author": "sysr-q",
	"author_email": "chris@gibsonsec.org",
	"license": "MIT",
	"packages": [
		"fah",
	],
	"package_dir": {
		"fah": "fah",
	},
	"install_requires": [
		"flask",
		"flask-socketio",
		"flask-sqlalchemy",
		"flask-kvsession",
	],
	"zip_safe": False,
}

if __name__ == "__main__":
	setup(**kw)
