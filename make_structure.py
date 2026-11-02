import os

structure = {
    "authorities": ["cyber_and_fraud_authorities", "consumer_authorities", "labour_family_authorities", "utilities_authorities"],
    "cyber": ["peca_2016", "ppc_cyber_related"],
    "consumer": ["punjab_consumer_protection_act_2005", "sale_of_goods_act_1930", "province_map"],
    "rent": ["punjab_rented_premises_act_2009", "transfer_of_property_act_1882", "registration_act_1908", "illegal_dispossession_act_2005", "province_map"],
    "police": ["crpc_1898", "police_order_2002", "constitution_articles"],
    "banking": ["ppc_489f", "negotiable_instruments_act_1881", "payment_systems_eft_act_2007", "banking_mohtasib_order_2006"],
    "employment": ["payment_of_wages_act_1936", "industrial_relations_act_2012", "standing_orders_ordinance_1968", "punjab_domestic_workers_act_2019", "eobi_act_1976"],
    "harassment": ["workplace_harassment_act_2010"],
    "family": ["mflo_1961", "family_courts_act_1964", "dissolution_of_muslim_marriages_act_1939", "guardians_and_wards_act_1890", "muslim_personal_law_shariat_act_1962", "dowry_and_bridal_gifts_act_1976", "punjab_womens_property_rights_act_2021", "punjab_protection_of_women_act_2016"],
    "property": ["specific_relief_act_1877", "punjab_land_revenue_act_1967", "cooperative_societies_act_1925", "punjab_real_estate_regulatory_act_2020"],
    "business": ["partnership_act_1932"],
    "utilities": ["nepra_act_1997", "ogra_ordinance_2002", "electricity_act_1910", "gas_theft_control_act_2016"],
    "telecom": ["pta_reorganization_act_1996"],
    "ombudsman": ["wafaqi_mohtasib_order_1983"],
    "insurance_invest": ["insurance_ordinance_2000", "securities_act_2015", "secp_digital_lending_rules"],
    "education": ["hec_ordinance_2002", "punjab_private_educational_institutions_ordinance_1984"],
    "healthcare": ["punjab_healthcare_commission_act_2010", "pakistan_medical_commission_act_2020"],
    "vehicle": ["motor_vehicles_ordinance_1965"],
    "travel_courier": ["emigration_ordinance_1979", "caa_ordinance_1960", "pakistan_post_office_act_1898"],
    "ip": ["trade_marks_ordinance_2001", "copyright_ordinance_1962"],
    "general": ["contract_act_1872", "limitation_act_1908", "qanun_e_shahadat_1984", "defamation_ordinance_2002"],
}

for folder, files in structure.items():
    os.makedirs(os.path.join("database", folder), exist_ok=True)
    for name in files:
        path = os.path.join("database", folder, name + ".txt")
        if not os.path.exists(path):
            open(path, "w", encoding="utf-8").close()

