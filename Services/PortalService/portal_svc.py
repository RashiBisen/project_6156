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

def find_skill(uni, template = None):
    result = db.find_record(uni, template)
    skill_set = []
    if len(result) != 0:
        if 'Skills' in result[0]:
            for skill in result[0]['Skills']:
                skill_set.append(skill)
    return skill_set

def update_student_skill(uni, data):
    # data: json object with key:'Skills' and value:list of json object of skills
    result = db.find_record(uni)
    if len(result) != 0:
        result[0]['Skills'] = data
        result[0].pop('uni', None)
        rsp = db.update_by_key(uni, data)
    return rsp
