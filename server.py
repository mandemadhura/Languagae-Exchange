from flask import Flask, request
from http import HTTPStatus
app = Flask(__name__)


def success_response(status_code=None, lang_id=None):
    message = {"error": '', "data": {"lang_id": lang_id}}
    return message, status_code

def error_response(error_string=None, status_code=None):
    message = {"error": error_string, "data": ''}
    return message, status_code

@app.route('/languages', methods=['POST'])
def create_language():
    existing_language = ['Marathi']
    json_data = request.json
    lang_name = json_data['lang_name']
    print(lang_name)
    if lang_name in existing_language:
        return error_response('Language already exists', HTTPStatus.CONFLICT)
    lang_id = json_data['lang_id']
    return success_response(HTTPStatus.CREATED, lang_id)
   

if __name__ == '__main__':
    app.run()
  
