# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "sapphire_customization"
app_title = "sapphire_customization"
app_publisher = "sapphire_customization"
app_description = "sapphire_customization"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "makarand.b@indictranstech.com"
app_version = "0.0.1"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sapphire_customization/css/sapphire_customization.css"
# app_include_js = "/assets/sapphire_customization/js/sapphire_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/sapphire_customization/css/sapphire_customization.css"
# web_include_js = "/assets/sapphire_customization/js/sapphire_customization.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "sapphire_customization.install.before_install"
# after_install = "sapphire_customization.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sapphire_customization.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# },
	"Sales Order": {
		"on_submit": "sapphire_customization.sapphire_customization.custom_methods.sales_order_negative_sales_alert"
	},
	"Purchase Receipt": {
		"on_submit": "sapphire_customization.sapphire_customization.custom_methods.purchase_receipt_submit"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"sapphire_customization.sapphire_customization.doctype.notification_setting.credit_days_notification.check_period"
	],
	# "daily": [
	# 	"sapphire_customization.tasks.daily"
	# ],
	# "hourly": [
	# 	"sapphire_customization.tasks.hourly"
	# ],
	# "weekly": [
	# 	"sapphire_customization.tasks.weekly"
	# ]
	# "monthly": [
	# 	"sapphire_customization.tasks.monthly"
	# ]
}

# Testing
# -------

# before_tests = "sapphire_customization.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sapphire_customization.event.get_events"
# }

