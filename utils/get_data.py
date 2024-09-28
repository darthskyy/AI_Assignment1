from ucimlrepo import fetch_ucirepo
import json
import os
import pandas as pd

# changing from codes to their actual meaning
ATTRIBUTE_MAP = {
    "1": {
        "name": "Status of existing checking account",
        "type": "categorical",
        "categories": [
            "negative_balance",
            "small_balance",
            "large_balance",
            "no_account"
        ],
        "mapping": {
            "A11": "negative_balance",
            "A12": "small_balance",
            "A13": "large_balance",
            "A14": "no_account"
        },
        "identifier": "status_checking_account"
    },
    "2": {
        "name": "Duration",
        "type": "categorical",
        "categories": [
            "short_term",
            "medium_term",
            "long_term"
        ],
        "mapping": {
            "A21": "short_term",
            "A22": "medium_term",
            "A23": "long_term"
        },
        "identifier": "loan_duration"
    },
    "3": {
        "name": "Credit history",
        "type": "categorical",
        "categories": [
            "no_credits",
            "all_credits_paid",
            "existing_credits_paid",
            "delayed_payment",
            "critical_account"
        ],
        "mapping": {
            "A30": "no_credits",
            "A31": "all_credits_paid",
            "A32": "existing_credits_paid",
            "A33": "delayed_payment",
            "A34": "critical_account"
        },
        "identifier": "credit_history"
    },
    "4": {
        "name": "Purpose",
        "type": "categorical",
        "categories": [
            "new_car",
            "used_car",
            "furniture",
            "electronics",
            "appliances",
            "repairs",
            "education",
            "vacation",
            "retraining",
            "business",
            "others"
        ],
        "mapping": {
            "A40": "new_car",
            "A41": "used_car",
            "A42": "furniture",
            "A43": "electronics",
            "A44": "appliances",
            "A45": "repairs",
            "A46": "education",
            "A47": "vacation",
            "A48": "retraining",
            "A49": "business",
            "A410": "others"
        },
        "identifier": "purpose"
    },
    "5": {
        "name": "Credit amount",
        "type": "categorical",
        "categories": [
            "low_credit",
            "medium_credit",
            "high_credit",
            "very_high_credit"
        ],
        "mapping": {
            "A51": "low_credit",
            "A52": "medium_credit",
            "A53": "high_credit",
            "A54": "very_high_credit"
        },
        "identifier": "loan_amount"
    },
    "6": {
        "name": "Savings account/bonds",
        "type": "categorical",
        "categories": [
            "low_savings",
            "medium_savings",
            "high_savings",
            "very_high_savings",
            "no_savings"
        ],
        "mapping": {
            "A61": "low_savings",
            "A62": "medium_savings",
            "A63": "high_savings",
            "A64": "very_high_savings",
            "A65": "no_savings"
        },
        "identifier": "savings_account_bonds"
    },
    "7": {
        "name": "Present employment since",
        "type": "categorical",
        "categories": [
            "unemployed",
            "less_than_1_year",
            "1_to_4_years",
            "4_to_7_years",
            "more_than_7_years"
        ],
        "mapping": {
            "A71": "unemployed",
            "A72": "less_than_1_year",
            "A73": "1_to_4_years",
            "A74": "4_to_7_years",
            "A75": "more_than_7_years"
        },
        "identifier": "employment_duration"
    },
    "8": {
        "name": "Installment rate in percentage of disposable income",
        "type": "numerical",
        "identifier": "installment_rate"
    },
    "9": {
        "name": "Personal status and sex",
        "type": "categorical",
        "categories": [
            "male_divorced",
            "female_divorced",
            "male_single",
            "male_married",
            "female_single"
        ],
        "mapping": {
            "A91": "male_divorced",
            "A92": "female_divorced",
            "A93": "male_single",
            "A94": "male_married",
            "A95": "female_single"
        },
        "identifier": "personal_status_sex"
    },
    "10": {
        "name": "Other debtors / guarantors",
        "type": "categorical",
        "categories": [
            "none",
            "co_applicant",
            "guarantor"
        ],
        "mapping": {
            "A101": "none",
            "A102": "co_applicant",
            "A103": "guarantor"
        },
        "identifier": "other_debtors_guarantors"
    },
    "11": {
        "name": "Present residence since",
        "type": "categorical",
        "categories": [
            "short",
            "medium",
            "long"
        ],
        "mapping": {
            "A111": "short",
            "A112": "medium",
            "A113": "long"
        },
        "identifier": "residence_duration"
    },
    "12": {
        "name": "Property",
        "type": "categorical",
        "categories": [
            "real_estate",
            "savings_agreement",
            "car_or_other",
            "no_property"
        ],
        "mapping": {
            "A121": "real_estate",
            "A122": "savings_agreement",
            "A123": "car_or_other",
            "A124": "no_property"
        },
        "identifier": "property"
    },
    "13": {
        "name": "Age in years",
        "type": "categorical",
        "categories": [
            "young",
            "middle_aged",
            "old"
        ],
        "mapping": {
            "A131": "young",
            "A132": "middle_aged",
            "A133": "old"
        },
        "identifier": "age_years"
    },
    "14": {
        "name": "Other installment plans",
        "type": "categorical",
        "categories": [
            "bank",
            "stores",
            "none"
        ],
        "mapping": {
            "A141": "bank",
            "A142": "stores",
            "A143": "none"
        },
        "identifier": "other_installment_plans"
    },
    "15": {
        "name": "Housing",
        "type": "categorical",
        "categories": [
            "rent",
            "own",
            "for_free"
        ],
        "mapping": {
            "A151": "rent",
            "A152": "own",
            "A153": "for_free"
        },
        "identifier": "housing"
    },
    "16": {
        "name": "Number of existing credits at this bank",
        "type": "numerical",
        "identifier": "existing_credits"
    },
    "17": {
        "name": "Job",
        "type": "categorical",
        "categories": [
            "unemployed",
            "unskilled_resident",
            "skilled_employee",
            "management"
        ],
        "mapping": {
            "A171": "unemployed",
            "A172": "unskilled_resident",
            "A173": "skilled_employee",
            "A174": "management"
        },
        "identifier": "job"
    },
    "18": {
        "name": "Number of people being liable to provide maintenance for",
        "type": "numerical",
        "identifier": "maintenance_people"
    },
    "19": {
        "name": "Telephone",
        "type": "categorical",
        "categories": [
            "none",
            "yes_registered"
        ],
        "mapping": {
            "A191": "none",
            "A192": "yes_registered"
        },
        "identifier": "telephone"
    },
    "20": {
        "name": "foreign worker",
        "type": "categorical",
        "categories": [
            "yes",
            "no"
        ],
        "mapping": {
            "A201": "yes",
            "A202": "no"
        },
        "identifier": "foreign_worker"
    }
}

NUM_2_IDENTIFIER = {
    val: obj["identifier"] for val, obj in ATTRIBUTE_MAP.items()
}
IDENTIFIER_2_NUM = {
    obj["identifier"]: val for val, obj in ATTRIBUTE_MAP.items()
}
## PART 1: Fetching the data

def fetch_data():
    # fetch dataset
    statlog_german_credit_data = fetch_ucirepo(id=144)

    # data (as pandas dataframes)
    X = statlog_german_credit_data.data.features
    y = statlog_german_credit_data.data.targets
    return X, y

def clean_data(X):
    # remove columns with missing values
    # drop columns
    # Atribute8, Attribute9, Attribute10, Attribute11, Attribute12, Attribute14,
    # Attribute15, Attribute16, Attribute18, Attribute19, Attribute20
    X = X.drop(columns=['Attribute8', 'Attribute9', 'Attribute10',
                        'Attribute11', 'Attribute12', 'Attribute14', 'Attribute15',
                        'Attribute16', 'Attribute18', 'Attribute19', 'Attribute20'])

    # get the range of values for Attribute5: loan amount
    min_amount, max_amount = X['Attribute5'].min(), X['Attribute5'].max()

    # dictionary of the range divided into 4 categories of the same width
    amount_bins = {
        "A51": (min_amount,
                min_amount + (max_amount - min_amount) / 4),
        "A52": (min_amount + (max_amount - min_amount) /4,
                min_amount + 2 * (max_amount - min_amount) / 4),
        "A53": (min_amount + 2 * (max_amount - min_amount) / 4,
                min_amount + 3 * (max_amount - min_amount) / 4),
        "A54": (min_amount + 3 * (max_amount - min_amount) / 4,
                max_amount)
    }

    # changing the values of Attribute5 to the corresponding category
    X['Attribute5'] = X['Attribute5'].apply(lambda x: [k for k, v in amount_bins.items() if v[0] <= x <= v[1]][0])

    # get the range of values for Attribute2: duration
    min_duration, max_duration = X['Attribute2'].min(), X['Attribute2'].max()

    # dictionary of the range divided into 3 categories of the same width

    duration_bins = {
        "A21": (min_duration,
                min_duration + (max_duration - min_duration) / 3),
        "A22": (min_duration + (max_duration - min_duration) / 3,
                min_duration + 2 * (max_duration - min_duration) / 3),
        "A23": (min_duration + 2 * (max_duration - min_duration) / 3,
                max_duration)
    }

    # changing the values of Attribute2 to the corresponding category
    X['Attribute2'] = X['Attribute2'].apply(lambda x: [k for k, v in duration_bins.items() if v[0] <= x <= v[1]][0])

    # setting the range of values for Attribute13: age
    # last category is open ended
    # 3 categories: 19-35, 36-55, 56-inf
    age_bins = {
        "A131": (19, 35),
        "A132": (36, 55),
        "A133": (56, float('inf'))
    }
    # changing the values of Attribute13 to the corresponding category
    X['Attribute13'] = X['Attribute13'].apply(lambda x: [k for k, v in age_bins.items() if v[0] <= x <= v[1]][0])

    return X

def map_data(X, attribute_map):
    for col in X.columns:
        number = col.removeprefix('Attribute')
        mapping = attribute_map[number]['mapping']
        X[col] = X[col].map(mapping)
        X = X.rename(columns={col: attribute_map[number]['identifier']})
    return X

def get_probability(X, col):
    return X[col].value_counts(normalize=True)

def get_conditional_probability(X, col1, col2, attribute_map=ATTRIBUTE_MAP):
    # probability of col1|col2
    probabilities = X.groupby(col2)[col1].value_counts(normalize=True)
    
    cats1 = attribute_map[IDENTIFIER_2_NUM[col1]]['categories']
    cats2 = attribute_map[IDENTIFIER_2_NUM[col2]]['categories']
    
    # sort by cats1
    probabilities = probabilities.reindex(pd.MultiIndex.from_product([cats2, cats1], names=[col2, col1])).fillna(0)
    return probabilities


def main():
    import pprint
    if not os.path.exists("data/features.csv"):
        X, y = fetch_data()
        X = clean_data(X)
        X = map_data(X, ATTRIBUTE_MAP)
        y = y.rename(columns={'class': 'credit_risk'})
        y['credit_risk'] = y['credit_risk'].map({1: 'yes', 2: 'no'})
        X['credit_risk'] = y['credit_risk']
        X.to_csv('data/features.csv', index=False)

    X = pd.read_csv("data/features.csv")


    x = get_conditional_probability(X, "credit_history", "age_years")
    print(x)
    print(type(x))
    for condition, prob in x.items():
        print(f"Condition: {condition}, Probability: {prob}")


if __name__ == '__main__':
    main()