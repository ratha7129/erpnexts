# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):

	if not filters:
		filters = {}
	if len(filters.item_group) <= 0 and filters.status != "Counted Item":
		frappe.throw("Please select item group.")

	columns = get_columns(filters)
	stock = get_data(filters)

	return columns, stock


def get_columns(filters):
	if filters.status == "Uncounted Item":
		return [
			{"label":"Item", "fieldname":"item_code","fieldtype":"Link","options":"Item","align":"left","sql":"item_code","width":"250"},
			{"label":"Item Name", "fieldname":"item_name","fieldtype":"Data","align":"left","width":"150"},
			{"label":"Supplier", "fieldname":"supplier_name","fieldtype":"Data","align":"left","width":"150"},
			{"label":"Item Group", "fieldname":"item_group","fieldtype":"Data","align":"left","width":"150"},
			{"label":"Min Quantity", "fieldname":"min_quantity","fieldtype":"Data","align":"center","width":"60"},
			{"label":"Max Quantity", "fieldname":"max_quantity","fieldtype":"Data","align":"center","width":"60"},
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
			{"label":"BOH", "fieldname":"current_qty","fieldtype":"Int","width":"100"},
			{"label":"QTY", "fieldname":"qty","fieldtype":"Int","width":"150"},
			{"label":"Diff", "fieldname":"quantity_difference","fieldtype":"Int","width":"150"},
			{"label":"Cost", "fieldname":"valuation_rate","fieldtype":"Currency","width":"150"},
			{"label":"Diff Cost", "fieldname":"amount_difference","fieldtype":"Currency","width":"150"}
		]


def get_data(filters):
	
	
	item_sql = ""
	if len(filters.item_group) > 0:
		all_product_category_sql = """
			select 
				name 
			from `tabItem Group`
			where parent_item_group in %(item_group)s
		"""
	
		category = frappe.db.sql(all_product_category_sql,filters,as_dict=1)
	
		category = [c['name'] for c in category]
	#get Product in category
	if filters.status == "Uncounted Item":
		item_sql = """
			select 
			item.item_code,
			item.item_name,
			item.supplier_name,
			item.item_group,
			item.max_quantity,
			item.min_quantity,
			coalesce(bin.actual_qty,0) actual_qty,
			coalesce(bin.stock_uom,item.stock_uom) stock_uom,
			coalesce(bin.valuation_rate,item.valuation_rate) cost,
			item.standard_rate,
			item.wholesale_price,
			item.max_discount
			from `tabStock Reconciliation Item` ri
			right join `tabItem` item on item.name = ri.name
			left join `tabBin` bin on item.name = bin.item_code
			where 
				item.item_group in %(category)s and 
				item.name not in (select item_code from `tabStock Reconciliation Item` where parent in %(name)s) 

			
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
				valuation_rate,
				amount_difference
			from `tabStock Reconciliation Item`
			where parent in %(name)s

			UNION

			select 
				a.item_code,
				a.item_name,
				a.current_qty,
				a.qty,
				0 quantity_difference,
				b.valuation_rate,
				0 amount_difference
			from `tabNone Change Stock Reconciliation Item` a
			inner join `tabItem` b
			where a.stock_reconciliation in %(name)s
		"""
		stock_reconcill_item = frappe.db.sql(item_sql,{"name":filters.name},as_dict=1)
		
		
		
	return stock_reconcill_item

