
.phony: css

css:
	lessc --clean-css fah/static/less/base.less fah/static/css/app.css
