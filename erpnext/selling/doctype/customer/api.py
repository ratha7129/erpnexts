import frappe
from frappe.utils import today
@frappe.whitelist()
def get_customer_loyalty_point(name,company,loyalty_program):
	expiry_date = today()

	total_point_balance = frappe.db.sql(
		"""
		SELECT 
		coalesce(SUM(a.loyalty_points),0) AS loyalty_point,
		coalesce(SUM(a.loyalty_points* b.conversion_factor),0) AS loyalty_point_amount,
		coalesce(min(b.conversion_factor),0) as conversion_factor
		FROM `tabLoyalty Point Entry` a 
			INNER JOIN `tabLoyalty Program` b ON a.loyalty_program = b.name
		WHERE 
			a.customer=%s and 
			a.company = %s and 
			a.loyalty_program = %s and 
			a.expiry_date >%s
		""",
		(name,company,loyalty_program,expiry_date),
		as_dict=True
	)
 
	return total_point_balance[0]