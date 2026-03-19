import frappe
from frappe.utils import getdate, nowdate


def _extract_year(value):
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit() and len(value) == 4:
        return int(value)
    return getdate(value).year


def set_vehicle_age(doc, method=None):
    year_value = doc.get("year") or doc.get("custom_year")
    if not year_value:
        return

    year = _extract_year(year_value)
    current_year = getdate(nowdate()).year
    age = current_year - int(year)

    if doc.meta.has_field("age"):
        doc.set("age", age)
    elif doc.meta.has_field("custom_age"):
        doc.set("custom_age", age)
    else:
        frappe.throw("Lead field 'age' not found. Please add it to Lead.")
