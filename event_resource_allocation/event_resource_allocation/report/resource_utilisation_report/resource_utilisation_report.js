// Copyright (c) 2025, Velmurugan and contributors
// For license information, please see license.txt

frappe.query_reports["Resource Utilisation Report"] = {
	filters: [
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Datetime",
			"reqd": 1,
		},
		{
			"fieldname": "to_date",
			"label": "To Date",
			"fieldtype": "Datetime",
			"reqd": 1,
		},
	],
};
