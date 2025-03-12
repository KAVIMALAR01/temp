import frappe

def get_columns():
    return [
        {"label": "Invoice Number", "fieldname": "parent", "fieldtype": "Link", "options": "Sales Invoice", "width": 200},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 200},
        {"label": "Quantity", "fieldname": "quantity", "fieldtype": "Float", "width": 100},
        {"label": "Rate", "fieldname": "rate", "fieldtype": "Currency", "width": 100},
        {"label": "UOM", "fieldname": "uom", "fieldtype": "Data", "width": 80},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
    ]

def get_data(filters=None):
    filters_dict = {"docstatus": 1}

    if filters and filters.get("item"):
        filters_dict["item_code"] = filters["item"]

    if filters and filters.get("date"):
        sales_invoices = frappe.get_all(
            "Sales Invoice",
            fields=["name"],
            filters={"posting_date": filters["date"], "docstatus": 1},
        )
        invoice_names = [si["name"] for si in sales_invoices]
        if invoice_names:
            filters_dict["parent"] = ["in", invoice_names]
        else:
            return []

    sales_invoice_items = frappe.get_all(
        "Sales Invoice Item",
        fields=["parent", "item_name", "item_code", "qty as quantity", "rate", "uom", "amount"],
        filters=filters_dict,
    )

    if not sales_invoice_items:
        return []

    if filters and filters.get("quantity_sort"):
        sales_invoice_items.sort(
            key=lambda x: x["quantity"], 
            reverse=(filters["quantity_sort"] == "Descending")
        )

    return sales_invoice_items

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data
