app_name = "motor_insurance_broker"
app_title = "Motor Insurance Broker"
app_publisher = "Haridha"
app_description = "Motor Insurance"
app_email = "haridha.muruganandham@finstein.ai"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "motor_insurance_broker",
# 		"logo": "/assets/motor_insurance_broker/logo.png",
# 		"title": "Motor Insurance Broker",
# 		"route": "/motor_insurance_broker",
# 		"has_permission": "motor_insurance_broker.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/motor_insurance_broker/css/motor_insurance_broker.css"
# app_include_js = "/assets/motor_insurance_broker/js/motor_insurance_broker.js"

# include js, css files in header of web template
# web_include_css = "/assets/motor_insurance_broker/css/motor_insurance_broker.css"
# web_include_js = "/assets/motor_insurance_broker/js/motor_insurance_broker.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "motor_insurance_broker/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "motor_insurance_broker/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "motor_insurance_broker.utils.jinja_methods",
# 	"filters": "motor_insurance_broker.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "motor_insurance_broker.install.before_install"
# after_install = "motor_insurance_broker.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "motor_insurance_broker.uninstall.before_uninstall"
# after_uninstall = "motor_insurance_broker.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "motor_insurance_broker.utils.before_app_install"
# after_app_install = "motor_insurance_broker.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "motor_insurance_broker.utils.before_app_uninstall"
# after_app_uninstall = "motor_insurance_broker.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "motor_insurance_broker.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
doc_events = {
	"Lead": {
		"validate": "motor_insurance_broker.lead_events.set_vehicle_age"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"motor_insurance_broker.tasks.all"
# 	],
# 	"daily": [
# 		"motor_insurance_broker.tasks.daily"
# 	],
# 	"hourly": [
# 		"motor_insurance_broker.tasks.hourly"
# 	],
# 	"weekly": [
# 		"motor_insurance_broker.tasks.weekly"
# 	],
# 	"monthly": [
# 		"motor_insurance_broker.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "motor_insurance_broker.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "motor_insurance_broker.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "motor_insurance_broker.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["motor_insurance_broker.utils.before_request"]
# after_request = ["motor_insurance_broker.utils.after_request"]

# Job Events
# ----------
# before_job = ["motor_insurance_broker.utils.before_job"]
# after_job = ["motor_insurance_broker.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"motor_insurance_broker.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []
fixtures = [
    {"dt": "Client Script"},
    {"dt": "Insurance Provider"},
    {"dt": "Insurance Add-on"}
]
