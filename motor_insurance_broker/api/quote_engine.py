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


def get_third_party_rate(cc_value):
    try:
        cc = float(cc_value)
    except (TypeError, ValueError):
        frappe.throw("Lead CC must be a number for Third-Party Liability.")

    if cc <= 1000:
        return 2094
    if cc <= 1500:
        return 3416
    return 7897


def compute_addons(provider_doc, idv, od_premium):
    total = 0
    breakdown = []
    addons = []

    for row in provider_doc.get("addons") or []:
        addon_name = row.addon or ""
        name_lower = addon_name.lower()
        premium = 0

        if "zero" in name_lower:
            premium = od_premium * (provider_doc.zero_dep_rate or 0) / 100
        elif "engine" in name_lower:
            premium = idv * (provider_doc.engine_protect_rate or 0) / 100
        elif "road" in name_lower or "rsa" in name_lower:
            premium = row.premium or 0
        elif "return" in name_lower or "rti" in name_lower:
            premium = idv * (provider_doc.rti_rate or 0) / 100
        else:
            premium = row.premium or 0

        total += premium
        if addon_name:
            breakdown.append(f"{addon_name}: {premium:.2f}")
            addons.append(
                {
                    "addon": row.addon,
                    "premium": premium,
                    "required": row.required or 0,
                }
            )

    return total, ", ".join(breakdown), addons


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

    coverage_type = lead.get("custom_coverage_type") or lead.get("coverage_type")
    if not coverage_type:
        frappe.throw("Lead coverage type is required to generate quotes.")

    year = None
    vehicle_age = None
    ex_showroom_price = None

    if coverage_type in ("Comprehensive", "Own-Damage"):
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

    cc_value = None
    if coverage_type == "Third-Party Liability":
        cc_value = lead.get("cc") or lead.get("custom_cc")
        if cc_value is None:
            frappe.throw("Lead CC is required for Third-Party Liability quotes.")

    for ins in insurers:
        idv = None
        base_premium = 0
        discount = 0
        gst = 0
        final_premium = 0

        addon_total = 0
        addons_breakdown = ""
        addons_list = []

        if coverage_type == "Third-Party Liability":
            base_premium = get_third_party_rate(cc_value)
            gst = base_premium * 0.18
            final_premium = base_premium + gst
        else:
            provider = frappe.get_doc("Insurance Provider", ins.name)
            dep_percentage = get_depreciation_percentage(provider, vehicle_age)
            idv = calculate_idv(ex_showroom_price, dep_percentage)

            od_rate = provider.od_rate or ins.base_rate or 0
            od_premium = idv * od_rate / 100

            base_rate = ins.base_rate or 0
            base_premium = idv * base_rate / 100

            # Apply NCB on OD premium for OD coverage; on base premium for comprehensive
            if coverage_type == "Own-Damage":
                discount = od_premium * (ins.ncb_discount or 0) / 100
            else:
                discount = base_premium * (ins.ncb_discount or 0) / 100
            addon_total, addons_breakdown, addons_list = compute_addons(provider, idv, od_premium)

            if coverage_type == "Own-Damage":
                # Formula provided: OD = (IDV × OD rate) − NCB − discounts + addons
                # No GST mentioned in the formula, so keep GST as 0 for OD unless required.
                base_premium = od_premium
                final_premium = od_premium - discount + addon_total
            else:
                # Comprehensive
                subtotal = base_premium - discount + addon_total
                gst = subtotal * 0.18
                final_premium = subtotal + gst

        quote.append("motor_quotes", {
            "insurer": ins.name,
            "idv": idv,
            "base_premium": base_premium,
            "addon_premium": addon_total,
            "addons_breakdown": addons_breakdown,
            "final_premium": final_premium,
            "ncb_applied": discount,
            "gst": gst
        })

        for addon in addons_list:
            quote.append(
                "add_on_provided",
                {
                    "insurer": ins.name,
                    "addon": addon["addon"],
                    "premium": addon["premium"],
                    "required": addon["required"],
                },
            )

    quote.insert()
    return quote.name
