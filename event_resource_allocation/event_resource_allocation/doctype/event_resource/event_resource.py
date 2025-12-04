# Copyright (c) 2025, Velmurugan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EventResource(Document):
    def on_submit(self):
        existing = frappe.get_all("Event Resource",{
            "docstatus":1,
            "name":["!=",self.name]},
            ["resource_type","resource_name"]
        )
        for i in existing:
            if self.resource_type == i["resource_type"] and self.resource_name == i["resource_name"]:
                frappe.throw("Resource Type and Name already exists")


@frappe.whitelist()
def update_resource_after_submit(name, resource_name, resource_type):
    doc1 = frappe.get_all("Event Resource",{"docstatus":1,"name":["!=",name]},["resource_type","resource_name"])

    for a in doc1:
        if a["resource_type"] == resource_type and a["resource_name"] == resource_name:
            frappe.throw("Resource Type and Name already exists")
    doc = frappe.get_doc("Event Resource", name)
    doc.resource_name = resource_name
    doc.resource_type = resource_type
    doc.flags.ignore_validate_update_after_submit = True
    doc.save(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist()
def delete_event(name):
    doc = frappe.get_doc("Event Resource", name)
    doc.flags.ignore_validate_update_after_submit = True
    if doc.docstatus == 1:
        doc.cancel()
        frappe.db.commit()
        if doc.docstatus == 2:
            workflow_state = "Not Active"
            frappe.db.set_value("Event Resource", name, "workflow_state", workflow_state)
            frappe.db.commit()