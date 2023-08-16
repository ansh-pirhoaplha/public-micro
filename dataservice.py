from pymongo import MongoClient

HOST = 'localhost'
DATABASE = 'well_sensor_data'

def connect_collection(collection):
    client = MongoClient()
    db = client[DATABASE]
    collection_string = db[collection]
    return collection_string


def get_url_info(unique_id):
    query = {"unique_id":unique_id}
    projection = {"_id":0}

    collection = connect_collection("public_url_info")
    result = collection.find_one(query,projection)
    return result

def get_threshold_data(threshold_id):
    query = {"threshold_id":threshold_id}
    projection = {"_id":0}

    collection = connect_collection("threshold_standard")
    result = collection.find_one(query,projection)
    return result

def get_latest_log(device_id,node_addr):
    query = {"node_addr":node_addr,"device_id":device_id }
    projection = {"_id":0}

    collection = connect_collection("last_sensor_log")
    result = collection.find_one(query,projection)
    return result


def get_device_info(device_id,node_addr):
    query = {"node_addr":node_addr,"device_id":device_id }
    projection = {"_id":0}

    collection = connect_collection("devices")
    result = collection.find_one(query,projection)
    return result


def get_client_info(client_id):
    query = {"client_id":client_id}
    projection = {"_id":0}

    collection = connect_collection("client_details")
    result = collection.find_one(query,projection)
    return result


def get_partner_info(client_id):
    query = {"client_id":client_id}
    projection = {"_id":0}

    collection = connect_collection("client_details")
    result = collection.find_one(query,projection)
    return result