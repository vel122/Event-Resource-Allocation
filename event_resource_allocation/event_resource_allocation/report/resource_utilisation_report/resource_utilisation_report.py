import frappe
from frappe.utils import now_datetime, get_datetime

def execute(filters=None):
    filters = filters or {}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    now = now_datetime()

    if not from_date or not to_date:
        frappe.throw("Please select From Date and To Date")

    from_date = get_datetime(from_date)
    to_date = get_datetime(to_date)

    if from_date > to_date:
        frappe.throw("From date is greater than To")

    allocations = frappe.get_all(
        "Event Resource Allocation",
        filters={
            "docstatus": 1,
            "start_date": ["<=", to_date],
            "end_date": [">=", from_date]
        },
        fields=["name", "start_date", "end_date"]
    )

    duration = {}
    for a in allocations:
        start = get_datetime(a["start_date"])
        end = get_datetime(a["end_date"])

        if end >= now:
            continue

        resources = frappe.get_all(
            "Resource",
            filters={
                "parent": a["name"],
                "parenttype": "Event Resource Allocation",
                "parentfield": "resources"
            },
            fields=["resource_id"]
        )

        total_hours = (end - start).total_seconds() / 3600
        for r in resources:
            rid = r["resource_id"]
            duration[rid] = duration.get(rid, 0) + total_hours

    upcoming_allocs = frappe.get_all(
        "Event Resource Allocation",
        filters={
            "docstatus": 1,
            "start_date": [">", now] and ["<=", to_date],
            "end_date": [">=", from_date]
        },
        fields=["name", "event_title", "start_date", "end_date"]
    )

    upcoming = {}
    for u in upcoming_allocs:
        u_start = get_datetime(u["start_date"])
        u_end = get_datetime(u["end_date"])
        u_title = u["event_title"]
        u_current = now_datetime()
        if u_end < u_current:
            continue

        res = frappe.get_all(
            "Resource",
            filters={
                "parent": u["name"],
                "parenttype": "Event Resource Allocation",
                "parentfield": "resources"
            },
            fields=["resource_id"]
        )

        for r in res:
            rid = r["resource_id"]
            booking = f"{u_title} ({u_start} → {u_end})"
            upcoming.setdefault(rid, []).append(booking)

    data = []
    final_keys = set(duration.keys()) | set(upcoming.keys())

    for k in final_keys:
        data.append({
            "resource": k,
            "total_hours": round(duration.get(k, 0), 2),
            "upcoming_events": ",".join(upcoming.get(k, []))
        })

    total_hours_all = sum(duration.values())
    upcoming_count = sum(len(v) for v in upcoming.values())

    summary = [
        {"label": "Total Resources", "value": len(final_keys), "indicator": "Blue"},
        {"label": "Total Hours Utilized", "value": round(total_hours_all, 2), "indicator": "Green"},
        {"label": "Upcoming Bookings", "value": upcoming_count, "indicator": "Red"}
    ]

    columns = [
        {"label": "Resource", "fieldname": "resource", "fieldtype": "Data", "width": 120},
        {"label": "Total Hours", "fieldname": "total_hours", "fieldtype": "Float", "width": 120},
        {"label": "Upcoming", "fieldname": "upcoming_events", "fieldtype": "Data", "width": 1000}
    ]

    return columns, data, None, None, summary
