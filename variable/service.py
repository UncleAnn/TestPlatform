import re
import json
from flask import jsonify
from common.mongo import MyMongo
from common import generate_id


class Service:
    def __init__(self):
        self._db = MyMongo('127.0.0.1', 27017)

    def keyword_debug(self, data):
        if not data.get('mock'):
            return jsonify({
                'status_code': 400,
                'message': 'invalid parameter {mock}',
                'data': data
            })
        mock = {'data': json.loads(data['mock'])}
        snippet = data.get('snippet')
        if not snippet:
            return jsonify({
                'status_code': 400,
                'message': 'invalid parameter {snippet}',
                'data': data
            })
        func = re.findall(r'def\s+(.+?):', data['snippet'])
        if func:
            snippet += '\n' + 'result=' + func[0]
        try:
            exec(snippet, mock)
        except Exception as e:
            return ({
                'status_code': 200,
                'message': str(e),
            })
        return jsonify({
            'status_code': 200,
            'message': 'ok',
            'data': mock['result']
        })

    def keyword_save(self, data):
        if not data.get('mock'):
            return jsonify({
                'status_code': 400,
                'message': 'invalid parameter {mock}',
                'data': data
            })
        mock = {'data': json.loads(data['mock'])}
        snippet = data.get('snippet')
        if not snippet:
            return jsonify({
                'status_code': 400,
                'message': 'invalid parameter {snippet}',
                'data': data
            })
        name = re.findall(r'def\s+(.+?)\(', data['snippet'])
        name = name[0] if name else ""
        func = re.findall(r'def\s+(.+?):', data['snippet'])
        if func:
            snippet += '\n' + 'result=' + func[0]
        keyword = {
            '_id': generate_id(),
            'name': name,
            'mock': mock,
            'snippet': snippet
        }
        self._db.insert("variable", "keywords", keyword)
        return jsonify({
            'status_code': 200,
            'message': 'ok',
        })

    def aggregate(self, data):
        key = data['key']
        pipeline = [{'$group': {'_id': f'${key}'}}]
        return self._db.aggregate('variable', data['type'], pipeline)

    def insert(self, data):
        data['_id'] = generate_id()
        return self._db.insert('variable', 'variables', data)

    def update(self, data):
        return self._db.update('variable', 'variables', {'_id': data['_id']}, data)

    def delete(self, filter_condition):
        return self._db.delete('variable', 'variables', filter_condition)

    def search_project(self, data):
        return self._db.search('variable', data['type'], {'team': data['team']})

    def search(self, data):
        return self._db.search('variable', data['type'], {})

if __name__ == '__main__':
    service = Service()
    data = {
        'type': 'team',
        'key': 'team'
    }
    print(service.aggregate(data))