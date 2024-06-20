// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Uncounted Product"] = {
	"filters": [
		{
			"fieldname":"name",
			"label": __("Stock Reconciliation"),
			"fieldtype": "Link",
			"reqd": 1,
			"options": "Stock Reconciliation",
		},
		
	]
};
