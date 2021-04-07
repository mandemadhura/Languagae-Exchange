import json
from flask import Flask, request
from http import HTTPStatus
app = Flask(__name__)


existing_language = {"1": "Marathi"}

def success_response(status_code=None, lang_id=None, lang_name=None, lang_obj=None):
    message = {"error": '', "data": {"lang_id": lang_id}}
    if lang_name is not None:
        message['data']['lang_name'] = lang_name
    if lang_obj is not None:
        message['data'] = lang_obj
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
    # TODO: Handle Language already in use
    return success_response(HTTPStatus.OK, lang_id)

@app.route('/languages/<lang_id>', methods=['PUT'])
def update_language(lang_id):
    try:
        if request.headers['Content-type'] != 'application/json':
            return error_response('Unsupprted input format', HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
        lang_input = json.loads(request.data)
        lang_name = lang_input['lang_name']
    except (ValueError, KeyError, TypeError) as json_err:
        return error_response(f'Invalid JSON: {json_err}', HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    if lang_name == '' or type(lang_name) != str:
        return error_response('Invalid input', HTTPStatus.UNPROCESSABLE_ENTITY)
    if lang_id not in existing_language.keys():
        return error_response('Language does not exist', HTTPStatus.NOT_FOUND)
    if lang_name in existing_language.values():
        return error_response('Language name must be unique', HTTPStatus.CONFLICT)
    return success_response(HTTPStatus.OK, lang_id)

@app.route('/languages/<lang_id>', methods=['GET'])
def get_a_language(lang_id):
    if lang_id not in existing_language.keys():
        return error_response('Language does not exist', HTTPStatus.NOT_FOUND)
    lang_name = existing_language[lang_id]
    return success_response(HTTPStatus.OK, lang_id, lang_name)

@app.route('/languages/', methods=['GET'])
def get_languages():
    Language = []
    for lang_id, lang_name in existing_language.items():
        Language.append({'lang_id': lang_id, 'lang_name': lang_name})
    return success_response(HTTPStatus.OK, lang_obj=Language)


if __name__ == '__main__':
    app.run()

