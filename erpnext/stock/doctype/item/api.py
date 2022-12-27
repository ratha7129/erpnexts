import frappe


@frappe.whitelist()
def print_barcode(self):
	frappe.msgprint(self.item_name)


    # # Write to a file-like object:
    # rv = BytesIO()
    # EAN13(str("100000902922"), writer=SVGWriter()).write(rv)

    # # Or to an actual file:
    # with open("somefile.svg", "wb") as f:
    #     EAN13(str(100000011111), writer=SVGWriter()).write(f)