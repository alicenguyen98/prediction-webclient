import pandas as pd
from collections import namedtuple

# Load data


metal_levels = {
    'bronze': 'Bronze',
    'expanded_bronze': 'Expanded Bronze',
    'silver': 'Silver',
    'gold': 'Gold',
    'platinum': 'Platinum',
    'catastrophic': 'Catastrophic'
}

plan_types = {
    'PPO': 'PPO - Preferred Provider Organization',
    'EPO': 'EPO - Exclusive Provider Organization',
    'POS': 'POS - Point of Service',
    'HMO': 'HMO - Health Maintenance Organization'
}

def get_state_names():
    state_names = df_rate_area[['State Code', 'State Name']].drop_duplicates()
    return list(state_names.itertuples(index=False))

def get_state_name(state_code):
    state_name = df_rate_area.loc[df_rate_area['State Code'] == state_code]['State Name'].drop_duplicates()
    return state_name.values[0]

def get_county_names(state_code):
    county_names = df_rate_area.loc[df_rate_area['State Code'] == state_code][['FIPS','County Name']].drop_duplicates()
    return list(county_names.itertuples(index=False))

def get_metal_levels():
    return [ (x, metal_levels[x]) for x in metal_levels ]

def get_plan_types():
    return [ (x, plan_types[x]) for x in plan_types ]

def get_metal_level(key):
    return metal_levels[key]

def get_plan_type(key):
    return plan_types[key]

def get_rating_area(fips):
    rating_area = df_rate_area.loc[df_rate_area['FIPS'] == fips]['Rating Area'].drop_duplicates()
    if len(rating_area) != 1:
        return None
    return rating_area.values[0]
    
def get_project_index(year, state_code):
    prj_idx = df_project_index.loc[(df_project_index['Year'] == str(year)) & (df_project_index['State Code'] == state_code)]['PRJ_IDX_RT'].drop_duplicates()
    if len(prj_idx) != 1:
        return None
    return prj_idx.values[0]

def check_county_in_state(state_code, fips):
    result = df_rate_area.loc[(df_rate_area['State Code'] == state_code) & (df_rate_area['FIPS'] == fips)]
    return len(result) > 0

def init(conf):
    global df_rate_area
    global df_project_index
    df_rate_area = pd.read_csv(conf['db']['rating_areas'], 
    dtype={
        'Year': 'category',
        'State Code': 'category',
        'State Name': 'category',
        'County Name': 'category',
        'FIPS': 'category'
        })

    df_project_index = pd.read_csv(conf['db']['project_index_rates'], 
    dtype={
        'Year': 'category',
        'State Code': 'category',
        'PRJ_IDX_RT': 'float64'
    })