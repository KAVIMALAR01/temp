frappe.query_reports["Sales Invoice Report"] = {
    "filters": [
        {
            "fieldname": "item",
            "fieldtype": "Link",
            "label": __("Item"),
            "options": "Item"
        },
        {
            "fieldname": "date",
            "fieldtype": "Date",
            "label": __("Date")
        },
        {
            "fieldname": "quantity_sort",
            "fieldtype": "Select",
            "label": __("Quantity Sort"),
            "options": "Ascending\nDescending"
        }
    ],
   "formatter": function (value, row, column, data, default_formatter) {
    let formatted_value = default_formatter(value, row, column, data);
    if (!data) {
        return formatted_value;
    }
    if (data.amount > 9000) {
        formatted_value = `<span style="background-color:rgb(147, 249, 136);">${formatted_value}</span>`;
		//row.style.backgroundColor = "rgb(147, 249, 136)";
    }
    if (column.fieldname === "quantity" && data.quantity > 5) {
        formatted_value = `<span style="color: green;">${formatted_value}</span>`;
    }
    if (column.fieldname === "quantity" && data.quantity <= 5) {
        formatted_value = `<span style="color: orange;">${formatted_value}</span>`;
    }
    if (column.fieldname === "amount" && data.amount < 8000) {
        formatted_value = `<span style="color: red;">${formatted_value}</span>`;
    }

    return formatted_value;
}
};
