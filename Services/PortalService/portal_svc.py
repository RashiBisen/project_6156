from Services.DataService import dynamodb as db

def create_student(data):
    uni = data['uni']
    response = db.create(uni, data)
    if response ==  False:
        return False
    else:
        return True

def find_student(uni = None, template = None):
    result = db.find_record(uni, template)
    return result

def update_student(uni, update_data):
    rsp = db.update_by_key(uni, update_data)
    return rsp


