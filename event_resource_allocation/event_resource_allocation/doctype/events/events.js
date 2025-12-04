// Copyright (c) 2025, Velmurugan and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Events", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Events",{
    refresh(frm){
        if(frm.doc.docstatus === 1){
            frm.add_custom_button(__('Update Event'), function() {
                let d = new frappe.ui.Dialog({
                    title: __('Update Event'),
                    fields: [
                        {
                            label: __('Event Title'),
                            fieldname: 'event_title',
                            fieldtype: 'Data',
                            default: frm.doc.event_title
                        },
                        {
                            label: __('Start Date'),
                            fieldname: 'start_date',
                            fieldtype: 'Datetime',
                            default: frm.doc.start_date
                        },
                        {
                            label: __('End Date'),
                            fieldname: 'end_date',
                            fieldtype: 'Datetime',
                            default: frm.doc.end_date
                        },
                        {
                            label: __('Description'),
                            fieldname: 'description',
                            fieldtype: 'Long Text',
                            default: frm.doc.description
                        },
                    ],
                    primary_action: function() {
                        let data = d.get_values();
                        d.hide();
                        if(data) {
                            frappe.call({
                                method: "event_resource_allocation.event_resource_allocation.doctype.events.events.update_event_after_submit",
                                args: {
                                    name: frm.doc.name,
                                    event_title: data.event_title,
                                    start_date: data.start_date,
                                    end_date: data.end_date,
                                    description: data.description
                                },
                                callback(r) {
                                    frm.reload_doc();
                                }
                            });
                        }

                    }
                });
                d.show();
            });
            frm.add_custom_button(__("Go to Event Resource Allocation"), ()=>{
                frappe.set_route("List", "Event Resource Allocation");
            })
            if (frm.doc.docstatus === 1){
                frm.add_custom_button(__("Delete Event"), ()=>{
                    frappe.confirm("Are you Sure want to Delete", () => {
                        frappe.call({
                            method: "event_resource_allocation.event_resource_allocation.doctype.events.events.delete_event",
                            args: {
                                name: frm.doc.name
                            },
                            callback: function(r) {
                                frm.reload_doc();
                            }
                        });
                    });
                })
            }
        }
    }
})