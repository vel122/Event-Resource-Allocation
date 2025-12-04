from frappe.model.document import Document
import frappe
import json

class EventResourceAllocation(Document):
        
    def on_submit(self):
        for r in self.resources:
            existing = frappe.get_all("Event Resource Allocation",{
                "docstatus":1,
                "name":["!=",self.name]
                },
                ["name","start_date","end_date"])
            
            for a in existing:
                resource = frappe.get_all("Resource",{
                    "parent":a["name"],
                    "parenttype":"Event Resource Allocation",
                    "parentfield":"resources",
                    "resource_id":r.resource_id
                },["resource_id"])

                if resource:
                    if self.start_date < a["end_date"] and self.end_date > a["start_date"]:
                       frappe.throw("Resource is already allocated to another event at this time Interval")
        


        event = frappe.get_doc("Events",self.event_id)

        allocation = frappe.get_all("Event Resource Allocation",{
            "docstatus":1,
            "event_id":self.event_id
            },
            ["name"]
        )

        for a in allocation:
            alloc = frappe.get_doc("Event Resource Allocation",a["name"])
            for r in alloc.resources:
                child = event.append("resource_allocated",{})
                child.resource_id = r.resource_id
                child.from_date = alloc.start_date
                child.to_date = alloc.end_date
                child.resource_name = r.resource_name
        
        event.flags.ignore_validate_update_after_submit = True
        event.save(ignore_permissions = True)

        frappe.db.commit()
           

    def on_cancel(self):
        event = frappe.get_doc("Events", self.event_id)

        updated_list = []
        for row in event.resource_allocated:
            if row.resource_id not in [r.resource_id for r in self.resources]:
                updated_list.append(row)

        event.set("resource_allocated", updated_list)

        event.flags.ignore_validate_update_after_submit = True
        event.save(ignore_permissions=True)
        frappe.db.commit()

@frappe.whitelist()
def update_resources_from_dialog(docname, resources,):

    if isinstance(resources, str):
        resources = json.loads(resources)

    doc = frappe.get_doc("Event Resource Allocation", docname)

    start_date = doc.start_date
    end_date = doc.end_date

 
    for r in resources:
        existing_allocs = frappe.get_all(
            "Event Resource Allocation",
            filters={
                "docstatus": 1,
                "name": ["!=", doc.name]
            },
            fields=["name", "start_date", "end_date"]
        )

        for alloc in existing_allocs:

            res_found = frappe.get_all(
                "Resource",
                filters={
                    "parent": alloc["name"],
                    "parenttype": "Event Resource Allocation",
                    "parentfield": "resources",
                    "resource_id": r.get("resource_id"),
                },
                fields=["resource_id"]
            )

            if res_found:
                if start_date < alloc["end_date"] and end_date > alloc["start_date"]:
                    frappe.throw(
                        f"Resource  is already allocated to another event "
                    )

    doc.flags.ignore_validate_update_after_submit = True

    doc.set("resources", [])

    for r in resources:
        row = doc.append("resources", {})
        row.resource_id = r.get("resource_id")
        row.resource_type = r.get("resource_type")
        row.resource_name = r.get("resource_name")

    doc.save(ignore_permissions=True)
    frappe.db.commit()
