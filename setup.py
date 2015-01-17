"""
"""
from setuptools import setup

kw = {
	"name": "fah",
	"version": "0.1.0",
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
	],
	"zip_safe": False,
}

if __name__ == "__main__":
	setup(**kw)
