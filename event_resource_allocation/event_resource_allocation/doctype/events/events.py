# Copyright (c) 2025, Velmurugan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_datetime

class Events(Document):
    
    def on_submit(self):
        start = get_datetime(self.start_date)
        end = get_datetime(self.end_date)
        if start == end:
            frappe.throw("Start Date Time & End Date Time cannot be same")
        if start  < now_datetime():
            frappe.throw("Cannot Create Past Events")

        if end < start:
            frappe.throw("End date is lesser than Start")
        

    def validate(self):
        start = get_datetime(self.start_date)
        end = get_datetime(self.end_date)
        existing = frappe.get_all(
            "Events",
            filters={
                "docstatus": 1,
                "name": ["!=", self.name]
            },
            fields=["name", "event_title", "start_date", "end_date"]
        )

        for a in existing:
            if  self.event_title == a["event_title"] and start ==get_datetime(a["start_date"]) and end ==get_datetime(a["end_date"]):
                frappe.throw("Same Event Title and Time range already exists")

@frappe.whitelist()
def update_event_after_submit(name, event_title, start_date, end_date, description):
    event = frappe.get_doc("Events", name)
    start = get_datetime(start_date)
    end = get_datetime(end_date)

    doc = frappe.get_all(
        "Events", filters={"name": ["!=", name]}, fields=["name", "event_title", "start_date", "end_date", "description"]
    )

    for i in doc:
        e_start = get_datetime(i["start_date"])
        e_end = get_datetime(i["end_date"])
        if event.event_title == i["event_title"] and start == e_start and end == e_end:
            frappe.throw("Same Event Title and Time range already exists")

    event.event_title = event_title
    event.start_date = start_date
    event.end_date = end_date
    event.description = description
    event.flags.ignore_validate_update_after_submit = True

    event.save(ignore_permissions=True)
    frappe.db.commit()





    





