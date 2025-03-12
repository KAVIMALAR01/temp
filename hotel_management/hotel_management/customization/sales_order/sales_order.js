/*frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        frm.add_custom_button('Get Sales Invoices', function() {
            frappe.call({
                method: "hotel_management.hotel_management.customization.sales_order.sales_order.get_sales_invoices",
                args: {
                    sales_order: frm.doc.name
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        let invoice_links = r.message.map(inv => {
                            return `<a href="#Form/Sales Invoice/${inv}" target="_blank">${inv}</a>`;
                        }).join('<br>');

                        frappe.msgprint({
                            title: __('Sales Invoices Found'),
                            message: __('The linked Sales Invoices are:<br><br>') + invoice_links,
                            indicator: 'green'
                        });

                        frappe.show_alert({
                            message: __('{0} Sales Invoice(s) found!', [r.message.length]),
                            indicator: 'green'
                        });

                    } else {
                        frappe.msgprint({
                            title: __('No Sales Invoices Found'),
                            message: __('No Sales Invoices found for this Sales Order.'),
                            indicator: 'red'
                        });

                        frappe.show_alert({
                            message: __('No Sales Invoices found!'),
                            indicator: 'red'
                        });
                    }
                }
            });
        });
    }
});*/
/*frappe.ui.form.on("Sales Order", {
    refresh: function(frm) {
        if (frm.doc.workflow_state) {
            frm.set_intro("Current Workflow State: <b>" + frm.doc.workflow_state + "</b>", "blue");

            // Send workflow state to the server
            frappe.call({
                method: "hotel_management.hotel_management.customization.sales_order.sales_order.store_workflow_state",
                args: {
                    sales_order: frm.doc.name,
                    workflow_state: frm.doc.workflow_state
                },
                callback: function(r) {
                    if (r.message) {
                        console.log("Workflow state updated successfully.");
                    }
                }
            });
        }
    }
});*/
