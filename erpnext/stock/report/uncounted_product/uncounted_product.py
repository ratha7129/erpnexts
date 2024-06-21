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
	if filters.status == "Uncounted Item":
		return [
			{"label":"Item", "fieldname":"item_code","fieldtype":"Link","options":"Item","align":"left","sql":"item_code","width":"250"},
			{"label":"Item Name", "fieldname":"item_name","fieldtype":"Data","align":"left","width":"150"},
			{"label":"Supplier", "fieldname":"supplier_name","fieldtype":"Data","align":"left","width":"150"},
			{"label":"Min Quantity", "fieldname":"min_quantity","fieldtype":"Data","align":"left","width":"60"},
			{"label":"Max Quantity", "fieldname":"max_quantity","fieldtype":"Data","align":"left","width":"60"},
			{"label":"BOH", "fieldname":"actual_qty","fieldtype":"Int","width":"100"},
			{"label":"UOM", "fieldname":"stock_uom","fieldtype":"Data","width":"150"},
			{"label":"Cost", "fieldname":"cost","fieldtype":"Currency","width":"150"},
			{"label":"Wholesale Price", "fieldname":"wholesale_price","fieldtype":"Currency","width":"150"},
			{"label":"Price", "fieldname":"standard_rate","fieldtype":"Currency","width":"150"},
			{"label":"Disc.", "fieldname":"max_discount","fieldtype":"Currency","width":"150"}
		]
	else:
		return [
			{"label":"Item", "fieldname":"item_code","fieldtype":"Link","options":"Item","align":"left","sql":"item_code","width":"250"},
			{"label":"Item Name", "fieldname":"item_name","fieldtype":"Data","align":"left","width":"150"},
			{"label":"BOH", "fieldname":"current_quantity","fieldtype":"Int","width":"100"},
			{"label":"QTY", "fieldname":"qty","fieldtype":"Data","width":"150"},
			{"label":"Diff", "fieldname":"quantity_difference","fieldtype":"Currency","width":"150"},
			{"label":"Cost", "fieldname":"valuation_rate","fieldtype":"Currency","width":"150"},
			{"label":"Diff Cost", "fieldname":"amount_difference","fieldtype":"Currency","width":"150"}
		]


def get_data(filters):
	all_product_category_sql = """
		select 
			name 
		from `tabItem Group`
		where parent_item_group = %(item_group)s
	"""
	category = frappe.db.sql(all_product_category_sql,filters,as_dict=1)
	item_sql = ""
	if len(category) > 0:
		category = [c['name'] for c in category]
	#get Product in category
	if filters.status == "Uncounted Item":
		item_sql = """
			select 
			item.item_code,
			item.item_name,
			item.supplier_name,
			item.max_quantity,
			item.min_quantity,
			coalesce(bin.actual_qty,0) actual_qty,
			coalesce(bin.stock_uom,item.stock_uom) stock_uom,
			coalesce(bin.valuation_rate,item.valuation_rate) cost,
			item.standard_rate,
			item.wholesale_price,
			item.max_discount
			from `tabItem` item 
			left join `tabBin` bin on item.name = bin.item_code
			where 
				item.item_group in %(category)s and 
				item.name not in (select item_code from `tabStock Reconciliation Item` where parent = %(name)s) 

			UNION

			select 
				a.item_code,
				a.item_name,
				b.supplier_name,
				b.max_quantity,
				b.min_quantity,
				a.current_qty,
				b.stock_uom,
				a.valuation_rate cost,
				b.standard_rate,
				b.wholesale_price,
				b.max_discount
			from `tabNone Change Stock Reconciliation Item` a
			inner join `tabItem` b
			where a.stock_reconciliation = %(name)s
		"""
		stock_reconcill_item = frappe.db.sql(item_sql,{"category":category,"name":filters.name},as_dict=1)
	else:
		item_sql = """
			select 
				item_code,
				item_name,
				current_qty,
				qty,
				quantity_difference,
				valuation_rate
			from `tabStock Reconciliation Item`
			where parent = %(name)s
		"""
		stock_reconcill_item = frappe.db.sql(item_sql,{"name":filters.name},as_dict=1)
	
	
	
	return stock_reconcill_item

