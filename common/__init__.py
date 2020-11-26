from time import strftime
from uuid import uuid1
from common.mongo import MyMongo
from common.email_tool import send_email


def generate_id():
    prefix = strftime("%Y%m%d%H%M%S")
    li = str(uuid1()).split('-')
    suffix = li[0] + li[3]
    case_id = prefix + suffix
    return case_id


if __name__ == '__main__':
    mongo = MyMongo(host='localhost', port=27017)
    db = 'users'
    collection = 'users'
    print(mongo.search(db, collection, {'username': 'liukaian'}))
