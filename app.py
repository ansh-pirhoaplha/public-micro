from flask import Flask, jsonify , request
from dataservice import *
from datetime import datetime,timedelta
from utils import *
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/view/latest/sensor/data/public/*": {"origins": "*"}})

@app.route('/view/latest/sensor/data/public/', methods=['GET'])
def get_latest_sensor_log():
    response = {}
    response["data_logs"] = []

    #Fetching url info
    unique_id = request.args.get('unique_id')
    url_info = get_url_info(unique_id)

    # Attaching indoor data
    grouped_average = url_info.get("grouped_avg")
    if grouped_average :
        group_logs(url_info)
    else :
        attach_device_logs(response,url_info)

    #Attaching outdoor data
    outdoor_device = url_info.get("external_device")
    if outdoor_device is not None :
        response["outdoor_params"] = url_info.get("outdoor_params")
        response["external_device_log"] = get_latest_log(outdoor_device,node_addr=outdoor_device)

    #Attaching the partner logo/images or static content
    client_id = url_info.get("client_id")
    client_info = get_client_info(client_id)
    partner_id = url_info.get("partner_id")
    partner_info = get_partner_info(partner_id)
    response = handle_images(response,client_info,partner_info)

    #Appending other keys in response
    response["display_logo"] = url_info.get("display_logo")
    response["indoor_params"] = url_info.get("indoor_params")
    response["partner_id"] = client_info.get("partner_id")
    response["display_name"] = url_info.get("display_name","Public URL")
    response["display_date_time"] = url_info.get("display_date_time",True)
    response["custom_styles"] = url_info.get("custom_styles",{})
    response["grouped_avg"] = grouped_average

    return jsonify(response)


@log_exceptions
def handle_images(response,client_info,partner_info):
    
    background_image = client_info.get("public_background_image")
    if background_image in [None,""] :
        response["background_image_url"] = DEFAULT_BG_IMAGE
    else :
        response["background_image_url"] = S3_BASE + background_image

    client_logo = client_info.get("client_logo")
    if client_logo in [None,""] :
        response["client_logo_url"] = DEFAULT_CLIENT
    else :
        response["client_logo_url"] = CLIENT_BASE + background_image

    partner_logo = partner_info.get("partner_logo")
    if partner_logo in [None,""] :
        response["partner_logo_url"] = DEFAULT_CLIENT
    else :
        response["partner_logo_url"] = CLIENT_BASE + background_image

    response["default_image"] = DEFAULT_BG_IMAGE

    return response


@log_exceptions
def group_logs(url_info):
    average = {}
    indoor_devices = url_info.get("device_list")
    expiry_date = url_expiry_date(device_info)
    expired = is_expired(expiry_date)
    notify = put_notification(expiry_date)

    for index,device in enumerate(indoor_devices):
        log = get_latest_log(device,node_addr=device)
        parameters = log.get("params")
        if index == 0 :
            average.append(log)
        else:
            for parameter in parameters:
                average_value = average.get(parameter) 
                current_value = log[parameter]
                calculated_value = average_value + current_value // 2
                average[parameter] = calculated_value

    threshold_data = get_threshold_data(threshold_id)
    proceed_incident_level(average,threshold_data)
    
    return average

@log_exceptions
def proceed_incident_level(data,threshold_data):
    pass


@log_exceptions
def attach_device_logs(response,url_info):

    indoor_devices = url_info.get("device_list")
    for device in indoor_devices:
        device_info = get_device_info(device,node_addr=device)
        expiry_date = device_expiry_date(device_info)
        expired = is_expired(expiry_date)
        notify = put_notification(expiry_date)

        log = get_latest_log(device,node_addr=device)
        if expired :
            log["status"] = False
            log["alert_msg"] = "Device Validity is Expired.Please renew its AMC."
        elif notify :
            log["status"] = True 
            log["alert_msg"] = "Device AMC going to expire.Please renew it."
        else :
            log["status"] = True 
            log["alert_msg"] = None
            
        response["data_logs"].append(log)

    return response


@log_exceptions
def url_expiry_date(url_info):
    default = datetime.today() + timedelta(days=10)
    expiry_date = url_info.get("validity_date",default)
    return expiry_date


@log_exceptions
def device_expiry_date(device_info):
    default = datetime.today() + timedelta(days=10)
    expiry_date = device_info.get("expiry_date",default)
    return expiry_date

@log_exceptions
def is_expired(expiry_date):
    current_date = datetime.today()
    if current_date >= expiry_date :
        return True
    return False

def put_notification(expiry_date,notify_before=7):
    current_date = datetime.today()
    notification_date = expiry_date - timedelta(days=notify_before)
    if notification_date <= current_date :
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True)