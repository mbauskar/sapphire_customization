cur_frm.cscript.generate_message = function(doc, dt ,dn){
	frappe.call({
		// method:"core.doctype.notification_setting.credit_days_notification.check_period",
		method: "sapphire_customization.sapphire_customization.doctype.notification_setting.credit_days_notification.check_period",
		callback:function(r){
			console.log("done")
		}
	})
}

cur_frm.cscript.interval = function(doc, dt ,dn){
	frappe.call({
		method:"sapphire_customization.sapphire_customization.doctype.notification_setting.notification_setting.interval",
		args:{interval:doc.interval},
		callback:function(r){
			cur_frm.reload_doc();
			// cur_frm.refresh_field("execution_time");
		}
	})
}
