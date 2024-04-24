from utils.db_utils import get_mongo_db

def get_user_by_username_password(username,password):
    query = {
                'username':username,
                'password':password
            }
    db = get_mongo_db()
    user_collection = db['users']
    return user_collection.find_one(query)