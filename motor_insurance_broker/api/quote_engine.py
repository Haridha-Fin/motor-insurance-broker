import frappe
from frappe.utils import getdate, nowdate

# ✅ VEHICLE AGE + IDV CALCULATION
def calculate_vehicle_age(year):
    current_year = getdate(nowdate()).year
    return current_year - int(year)


def extract_year(value):
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit() and len(value) == 4:
        return int(value)
    return getdate(value).year


def age_rule_matches(value, age):
    if value is None:
        return False

    if isinstance(value, (int, float)):
        return int(value) == age

    s = str(value).strip().replace(" ", "")
    if s.isdigit():
        return int(s) == age
    if "-" in s:
        parts = s.split("-")
        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
            return int(parts[0]) <= age <= int(parts[1])
    if s.endswith("+") and s[:-1].isdigit():
        return age >= int(s[:-1])

    return False


def get_depreciation_percentage(provider_doc, vehicle_age):
    for row in provider_doc.get("idv_calucation") or []:
        if age_rule_matches(row.age, vehicle_age):
            return row.depreciation_percentage or 0
    return 0


def calculate_idv(ex_showroom_price, depreciation_percentage):
    depreciation_amount = ex_showroom_price * (depreciation_percentage / 100)
    return ex_showroom_price - depreciation_amount


# ✅ MAIN QUOTE GENERATION
@frappe.whitelist()
def generate_quotes(lead_name):
    lead = frappe.get_doc("Lead", lead_name)

    insurers = frappe.get_all(
        "Insurance Provider",
        fields=["name", "provider_name", "base_rate", "ncb_discount"]
    )

    # Create Quote Doc (you must have created this)
    quote = frappe.new_doc("Motor Quote")
    quote.motor_lead = lead.name

    year_value = lead.get("year") or lead.get("custom_year")
    if not year_value:
        frappe.throw("Lead year is required to calculate IDV.")

    ex_showroom_price = lead.get("custom_price")
    if ex_showroom_price is None:
        frappe.throw("Lead price (ex-showroom) is required to calculate IDV.")

    try:
        ex_showroom_price = float(ex_showroom_price)
    except (TypeError, ValueError):
        frappe.throw("Lead price (ex-showroom) must be a number.")

    year = extract_year(year_value)
    vehicle_age = calculate_vehicle_age(year)

    for ins in insurers:
        provider = frappe.get_doc("Insurance Provider", ins.name)
        dep_percentage = get_depreciation_percentage(provider, vehicle_age)
        idv = calculate_idv(ex_showroom_price, dep_percentage)

        base_rate = ins.base_rate or 0
        base_premium = idv * base_rate / 100

        # Apply NCB
        discount = base_premium * (ins.ncb_discount or 0) / 100
        subtotal = base_premium - discount
        gst = subtotal * 0.18
        final_premium = subtotal + gst

        quote.append("motor_quotes", {
            "insurer": ins.name,
            "idv": idv,
            "base_premium": base_premium,
            "final_premium": final_premium,
            "ncb_applied": discount,
            "gst": gst
        })

    quote.insert()
    return quote.name
