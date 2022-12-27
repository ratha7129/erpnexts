# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


from frappe.model.document import Document


class ItemSupplier(Document):
	pass


	def __getitem__(self, items):
		print (type(items), items)