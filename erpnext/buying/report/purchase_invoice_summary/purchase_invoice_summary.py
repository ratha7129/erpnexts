import frappe
from frappe.utils import date_diff,today 
from frappe.utils.data import strip
from frappe import _
from py_linq import Enumerable

def execute(filters=None): 
	#run this to update parent_product_group in table sales invoice item

	report_data = []
	skip_total_row=False
 
	
	report_data = get_report_data(filters) 

	return get_columns(filters), report_data, None, None
 

def get_columns(filters):
	return [
		{"label":"Name", "fieldname":"supplier","fieldtype":"Link","options":"Supplier", "align":"left","width":200},
		{"label":"Supplier", "fieldname":"supplier_name","fieldtype":"Data","align":"left","width":200},
		{"label":"Total Amnount", "fieldname":"total_amount","fieldtype":"Currency", "align":"right",},
		{"label":"Total Invoice", "fieldname":"total_invoice","fieldtype":"INT", "align":"right",}
		
	]
 
 


 
def get_conditions(filters,group_filter=None):
	
	conditions = " a.docstatus = 1 "

	conditions += " AND a.posting_date between '{}' AND '{}'".format(filters.start_date,filters.end_date)

	if filters.get("supplier"):
		conditions += " AND supplier in %(supplier)s"
	
	return conditions

def get_report_data(filters,parent_row_group=None,indent=0,group_filter=None):

	data=[]

	sql = """
		SELECT 
			0 as indent,
			supplier ,
			supplier_name,
			SUM(grand_total) AS total_amount,
			COUNT(NAME) total_invoice
		FROM `tabPurchase Invoice` a
		where {}
		GROUP BY supplier
		
	""".format(get_conditions(filters,group_filter))
	parent = frappe.db.sql(sql,filters, as_dict=1)
	for dic_p in parent:
		dic_p["indent"] = 0
		dic_p["is_group"]=1
		data.append(dic_p)
		if filters.show_invoice==1 and len(data) > 0:
			child = frappe.db.sql("""
								select 1 as indent,name supplier,supplier_name,grand_total as total_amount, 1 as total_invoice from `tabPurchase Invoice` a where {0} and supplier = '{1}'
							""".format(get_conditions(filters,group_filter),dic_p.supplier), as_dict=1)
			for dic_c in child:
				dic_c["indent"] = 1
				dic_c["is_group"]=0
				data.append(dic_c)


	return data
 

# def get_report_summary(data,filters):
# 	report_summary = [] 
# 	if filters.show_summary:
# 		report_summary.append({"label":_("Quantity"),"value":Enumerable(data).sum(lambda x: x.total_quantity or 0),"indicator":"blue"})	
# 		report_summary.append({"label":_("Sub Total"),"value":frappe.utils.fmt_money(Enumerable(data).sum(lambda x: x.sub_total or 0)),"indicator":"blue"})	
# 		report_summary.append({"label":_("Discount"),"value":frappe.utils.fmt_money(Enumerable(data).sum(lambda x: x.total_discount or 0)),"indicator":"red"})	
# 		report_summary.append({"label":_("Tax"),"value":frappe.utils.fmt_money(Enumerable(data).sum(lambda x: x.total_tax or 0)),"indicator":"red"})	
# 		report_summary.append({"label":_("Cost"),"value":frappe.utils.fmt_money(Enumerable(data).sum(lambda x: x.total_cost or 0)),"indicator":"orange"})	
# 		report_summary.append({"label":_("Total Amount"),"value":frappe.utils.fmt_money(Enumerable(data).sum(lambda x: x.grand_total or 0)),"indicator":"green"})	
# 		report_summary.append({"label":_("Profit"),"value":frappe.utils.fmt_money(Enumerable(data).sum(lambda x: x.profit or 0)),"indicator":"green"})	

	return report_summary