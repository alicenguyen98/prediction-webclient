from flask import render_template, jsonify, request, send_from_directory
from datetime import datetime as dt

from . import app
from . import data_lookup as lookup
from .request import make_requests
from .utils import convert_to_value_label, try_parse_int

@app.route('/', methods=['GET'])
def home():
    return send_from_directory('static', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():

    # Retrieve form data
    data = request.json
    
    # Validate form data
    try:
        state = data['state']

        fips = data['county']

        year = dt.today().year

        # Check whether the county is inside the state
        if not lookup.check_county_in_state(state, fips):
            raise Exception('Invalid state/county pair')

        tobacco = 1 if data['smoker'] else 0

        # Check age
        age = data.get('age', None)
        if isinstance(age, type(None)):
            raise Exception("Age not provided")

        age = try_parse_int(age)
        if isinstance(age, type(None)):
            raise Exception("Age is not a valid integer")

        age = max(min(age, 64), 14)
        
        # Check rating area
        rating_area = lookup.get_rating_area(data['county'])
        if not rating_area:
            raise Exception(f"Failed to get rating area for the selected county ({fips})")
        
        # Check project index
        prj_idx_rt = lookup.get_project_index(year, data['state'])
        if not prj_idx_rt:
            raise Exception(f"No database for the selected state ({lookup.get_state_name(state)})")

        metal_level = lookup.get_metal_level(data['metal_level'])

        plan_type = data['plan_type']

    except Exception as e:
        app.logger.error(e)
        return jsonify({"error" : str(e)})

    # Prepare payload
    req_payload = {
        "Year": year,
        "State Code": state,
        "Rating Area": rating_area,
        "Metal Level": metal_level,
        "Plan Type": plan_type,
        "PRJ_IDX_RT": prj_idx_rt,
        "Tobacco": tobacco,
        "Age": age
    }

    try:
        # Request prediction from all endpoints
        response = make_requests(req_payload)
        
        # If we cannot get a single valid response, return an error
        if not response:
            raise Exception("No valid response")
    
    except Exception as e:
        app.logger.error(e)
        return jsonify({"error": "There is no service available at the moment. Please try again later."})

    return jsonify(response)

#region Vue

@app.route('/vue/form', methods=['GET'])
def form():
    try:
        state_names = convert_to_value_label(lookup.get_state_names())
        metal_levels = convert_to_value_label(lookup.get_metal_levels())
        plan_types = convert_to_value_label(lookup.get_plan_types())
        county_names = convert_to_value_label(lookup.get_county_names(state_names[0]['value']))

        payload = {
            # Initial values
            "state": state_names[0]['value'],
            "county": county_names[0]['value'],
            "smoker": False,
            "metal_level": metal_levels[0]['value'],
            "plan_type": plan_types[0]['value'],
            # Select fields
            "select_fields":{
                "states": state_names,
                "counties": county_names,
                "metal_levels": metal_levels,
                "plan_types": plan_types
            }
        }
    except Exception as e:
        app.logger.error(e)
        return jsonify({})
        
    return jsonify(payload)
    

@app.route('/vue/counties', methods=['GET'])
def county():
    try:
        state = request.args['state']
        payload = {
            "counties": convert_to_value_label(lookup.get_county_names(state))
        }
    except Exception as e:
        app.logger.error(e)
        return jsonify({})

    return jsonify(payload)

#endregion