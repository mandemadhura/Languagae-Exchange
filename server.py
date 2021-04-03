import json
from flask import Flask, request
from http import HTTPStatus
app = Flask(__name__)


existing_language = {"1": "Marathi"}

def success_response(status_code=None, lang_id=None):
    message = {"error": '', "data": {"lang_id": lang_id}}
    return message, status_code

def error_response(error_string=None, status_code=None):
    message = {"error": error_string, "data": ''}
    return message, status_code

@app.route('/languages', methods=['POST'])
def create_language():
    try:
        if request.headers['Content-type'] != 'application/json':
            return error_response('Unsupprted input format', HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
        lang_input = json.loads(request.data)
        lang_id, lang_name = lang_input['lang_id'], lang_input['lang_name']
        print(type(lang_name))
    except (ValueError, KeyError, TypeError) as json_err:
        return error_response(f'Invalid JSON: {json_err}', HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    if lang_name == '' or type(lang_name) != str:
        return error_response('Invalid input', HTTPStatus.UNPROCESSABLE_ENTITY)
    if lang_name in existing_language.values():
        return error_response('Language already exists', HTTPStatus.CONFLICT)
    return success_response(HTTPStatus.CREATED, lang_id)
   
@app.route('/languages/<lang_id>', methods=['DELETE'])
def delete_language(lang_id=None):
    if lang_id not in existing_language.keys(): 
        return error_response('Language does not exist', HTTPStatus.NOT_FOUND) 
    return success_response(HTTPStatus.OK, lang_id)
    
    
if __name__ == '__main__':
    app.run()
  
