# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):

	if not filters:
		filters = {}
	columns = get_columns(filters)
	stock = get_data(filters)

	return columns, stock


def get_columns(filters):

		return [
			{"label":"Item", "fieldname":"item_code","fieldtype":"Link","options":"Item","align":"left","sql":"item_code","width":"250"},
			{"label":"Item Name", "fieldname":"item_name","fieldtype":"Data","align":"left"},
			{"label":"Actual Qty", "fieldname":"actual_qty","fieldtype":"Int"},
			{"label":"UOM", "fieldname":"stock_uom","fieldtype":"Data","width":"100"}
		]
	



def get_data(filters):
	all_product_category_sql = """
		select 
			distinct i.item_group 
		from `tabStock Reconciliation Item` s 
		inner join `tabItem` i on s.item_code = i.name
		where s.parent = %(name)s
	"""
	category = frappe.db.sql(all_product_category_sql,filters,as_dict=1)
	if len(category) > 0:
		category = [c['item_group'] for c in category]
	#get Product in category
	item_sql = """
		select 
		item.item_code,
		item.item_name,
		coalesce(bin.actual_qty,0) actual_qty,
		coalesce(bin.stock_uom,item.stock_uom) stock_uom
		from `tabItem` item 
		left join `tabBin` bin on item.name = bin.item_code

		where item.item_group in {} and item.name not in (select item_code from `tabStock Reconciliation Item`)
		
	""".format(tuple(category))
	# frappe.throw(item_sql)
	item = frappe.db.sql(item_sql,as_dict=1)
	
	return item

