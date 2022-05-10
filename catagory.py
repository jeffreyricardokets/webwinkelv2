from models import *
from flask import request
from flask_login import current_user

#get data from form
def get_data_from_form():
    cat_name = request.form.get('catagory_name')
    user = current_user
    return cat_name,user

#check if catagory name already exist
def cat_already_exist(name):
    query = Catagories.select().where(Catagories.catagory_name == name)
    if query.exists():
        return True
    else:
        return False

#create the catagory in the database
def create_catagory():
    #get data from from
    cat_name, user = get_data_from_form()
    if user.is_admin:
        if not cat_already_exist(cat_name):
            Catagories.create(catagory_name = cat_name, created_by = user)
            return True
        else:
            #in the future I want to display a message that it already exist
            return False
    else:
        return False



#Select all item in Catagory
def query_all_in_catagories():
    query = Catagories.select()
    if query.exists:
        return query
    else:
        return False

