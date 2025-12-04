// Copyright (c) 2025, Velmurugan and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Event Resource", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Event Resource", {
    refresh(frm) {
        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(__('Update Resource'), () => {

                let d = new frappe.ui.Dialog({
                    title: __('Update Resource'),
                    fields: [
                        {
                            label: __("Resource Type"),
                            fieldname: "resource_type",
                            fieldtype: "Select",
                            options: frm.fields_dict.resource_type.df.options, 
                            default: frm.doc.resource_type
                        },
                        {
                            label: __("Resource Name"),
                            fieldname: "resource_name",
                            fieldtype: "Data",
                            default: frm.doc.resource_name
                        }
                    ],
                    primary_action(values) {
                        d.hide();

                        frappe.call({
                            method: "event_resource_allocation.event_resource_allocation.doctype.event_resource.event_resource.update_resource_after_submit",
                            args: {
                                name: frm.doc.name,
                                resource_name: values.resource_name,
                                resource_type: values.resource_type
                            },
                            callback() {
                                frm.reload_doc();
                            }
                        });
                    }
                });

                d.show();
            });
        }
    }
});

