frappe.ui.form.on("Event Resource Allocation", {
    refresh(frm) {
        if (frm.fields_dict["resources"] && frm.fields_dict["resources"].grid) {
            frm.fields_dict["resources"].grid.get_field("resource_id").get_query = function () {
                return {
                    filters: {
                        workflow_state: "Active",
                         resource_type: frm.doc.resource_type
                    }
                };
            };
        }
        frm.set_query("event_id", () => ({
            filters:
             {
               docstatus: 1
             }
        }));

        if (frm.doc.docstatus === 1) {

            frm.add_custom_button("Update Resources", () => {

                let dialog = new frappe.ui.Dialog({
                    title: "Update Resources",
                    fields: [
                        {
                            label: "Resource Type",
                            fieldname: "dialog_resource_type",
                            fieldtype: "Select",
                            options: frm.get_field("resource_type").df.options,
                            default: frm.doc.resource_type,
                            read_only:1
                        },
                        {
                            fieldname: "resources",
                            fieldtype: "Table",
                            label: "Resources",
                            in_place_edit: true,
                            fields: [
                                {
                                    fieldname: "resource_id",
                                    label: "Resource ID",
                                    fieldtype: "Link",
                                    options: "Event Resource",
                                    in_list_view: 1,
                                    reqd: 1,
                                    get_query: () => ({
                                        filters: {
                                            workflow_state: "Active",
                                            resource_type: dialog.get_value("dialog_resource_type")
                                        }
                                    })
                                },
                                {
                                    fieldname: "resource_type",
                                    label: "Resource Type",
                                    fieldtype: "Data",
                                    in_list_view: 1,
                                },
                                {
                                    fieldname: "resource_name",
                                    label: "Resource Name",
                                    fieldtype: "Data",
                                    in_list_view: 1
                                }
                            ]
                        }
                    ],

                    primary_action_label: "Update",

                 primary_action(values) {
                    frappe.call({
                        method: "event_resource_allocation.event_resource_allocation.doctype.event_resource_allocation.event_resource_allocation.update_resources_from_dialog",
                        args: {
                            docname: frm.doc.name,
                            resources: values.resources,
                        },
                        callback: function (r) {
                            if (!r.exc) {
                                frm.reload_doc();
                                dialog.hide();
                            }
                        }
                    });
                }

                });
                dialog.$wrapper.on("shown.bs.modal", () => {

                    let table = dialog.fields_dict.resources.grid;
                    table.df.data = frm.doc.resources.map(r => ({
                        resource_id: r.resource_id,
                        resource_type: r.resource_type,
                        resource_name: r.resource_name
                    }));

                    table.refresh();
                });
          
                dialog.show();
            });
        }
    }
});
