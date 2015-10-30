# -*- coding: utf-8 -*-
# Copyright (c) 2015, sapphire_customization and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import now, get_datetime, cint, cstr
from datetime import datetime, timedelta

class NotificationSetting(Document):
	pass

@frappe.whitelist()
def interval(interval):
	doc = frappe.get_doc("Notification Setting", "Notification Setting")
	doc.execution_time = (datetime.now()+timedelta(hours=cint(interval))).strftime('%Y-%m-%d %H:%M:%S')
	doc.interval = interval
	# frappe.db.set_value("Notification Setting", "Notification Setting", "execution_time", 
	# 	(datetime.now()+timedelta(hours=cint(interval))).strftime('%Y-%m-%d %H:%M:%S'))
	doc.save(ignore_permissions=True)
