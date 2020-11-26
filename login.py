from werkzeug.security import check_password_hash
from common import MyMongo

mongo = MyMongo('127.0.0.1', 27017)


def get_user_info(username):
    results = mongo.search('users', 'users', {'username': username})
    if results:
        return results[0]
    return None


if __name__ == '__main__':
    print(get_user_info('liukaian'))