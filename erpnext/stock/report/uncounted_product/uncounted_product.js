// Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Uncounted Product"] = {
	onload: function(report) {
		report.page.add_inner_button("Preview Report", function () {
			frappe.query_report.refresh();
		});
		
	},
	"filters": [
		{
			"fieldname":"name",
			"label": __("Stock Reconciliation"),
			"fieldtype": "MultiSelectList",
			"reqd": 1,
			"on_change": function (query_report) {},
			get_data: function(txt) {
				return frappe.db.get_link_options('Stock Reconciliation', txt);
			},
		},
		{
			fieldname: "item_group",
			label: "Item Group",
			fieldtype: "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Item Group', txt,{"is_group":1});
			},
			"on_change": function (query_report) {},
			 
		},
		{
			fieldname: "status",
			label: "Status",
			fieldtype: "Select",
			options:"Uncounted Item\nCounted Item",
			default:"Uncounted Item",
			on_change: function() {
				let status = frappe.query_report.get_filter_value('status');
				frappe.query_report.toggle_filter_display('item_group', status === 'Counted Item');
				// frappe.query_report.refresh();
			}
			 
		},
	]
};
