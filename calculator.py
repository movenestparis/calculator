import numpy as np


def calculate_investment_metrics(
    property_price,
    notary_rate,
    renovation_budget,
    monthly_rent,
    vacancy_months,
    annual_rent_increase,
    annual_charges,
    taxe_fonciere,
    annual_capex,
    annual_charges_increase,
    resale_value_3,
    resale_value_5,
    resale_value_10,
    discount_rate,
    use_loan,
    loan_amount,
    interest_rate,
    loan_duration
):
    total_investment = property_price * (1 + notary_rate / 100) + renovation_budget

    annual_rent = monthly_rent * (12 - vacancy_months)
    annual_expenses = annual_charges + taxe_fonciere + annual_capex

    cash_flows_3 = []
    cash_flows_5 = []
    cash_flows_10 = []

    for year in range(1, 11):
        rent = annual_rent * ((1 + annual_rent_increase / 100) ** (year - 1))
        expenses = annual_expenses * ((1 + annual_charges_increase / 100) ** (year - 1))
        net_cash_flow = rent - expenses

        if year <= 3:
            cash_flows_3.append(net_cash_flow)
        if year <= 5:
            cash_flows_5.append(net_cash_flow)
        cash_flows_10.append(net_cash_flow)

    if resale_value_3:
        cash_flows_3[-1] += resale_value_3
    if resale_value_5:
        cash_flows_5[-1] += resale_value_5
    if resale_value_10:
        cash_flows_10[-1] += resale_value_10

    npv_3 = np.npv(discount_rate / 100, [-total_investment] + cash_flows_3)
    npv_5 = np.npv(discount_rate / 100, [-total_investment] + cash_flows_5)
    npv_10 = np.npv(discount_rate / 100, [-total_investment] + cash_flows_10)

    try:
        irr_3 = np.irr([-total_investment] + cash_flows_3)
    except:
        irr_3 = None
    try:
        irr_5 = np.irr([-total_investment] + cash_flows_5)
    except:
        irr_5 = None
    try:
        irr_10 = np.irr([-total_investment] + cash_flows_10)
    except:
        irr_10 = None

    return {
        "npv_3": round(npv_3, 2),
        "npv_5": round(npv_5, 2),
        "npv_10": round(npv_10, 2),
        "irr_3": round(irr_3 * 100, 2) if irr_3 else None,
        "irr_5": round(irr_5 * 100, 2) if irr_5 else None,
        "irr_10": round(irr_10 * 100, 2) if irr_10 else None,
        "total_investment": round(total_investment, 2),
    }
