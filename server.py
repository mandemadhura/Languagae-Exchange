'''Server module responsible for entertaining the requests'''

import json
from http import HTTPStatus
from flask import Flask, request

from lang_exch.db.db_manager import DatabaseManager


app = Flask(__name__)
existing_language = {"1": "Marathi"}

def success_response(status_code=None, lang_id=None, lang_name=None, lang_obj=None) -> (dict, int):
    '''
    Creates a success response with message and status_code

    Args:
        status_code: HTTP status code
        lang_id: language id
        lang_name: language name
        lang_obj: Language objecti

    Returns:
        message: dict: A dictionary formed of success response with language details,
        status_code: HTTP staus code
    '''
    message = {"error": '', "data": {"lang_id": lang_id}}
    if lang_name is not None:
        message['data']['lang_name'] = lang_name
    if lang_obj is not None:
        message['data'] = lang_obj
    return message, status_code

def error_response(error_string=None, status_code=None) -> (dict, str):
    '''
    Creates an error response with message and status_code

    Args:
        error_string: error which got generated
        status_code: HTTP status code

    Returns:
        message: dict: A dictionary formed of error response with language details,
        status_code: HTTP staus code
    '''
    message = {"error": error_string, "data": ''}
    return message, status_code

@app.route('/languages', methods=['POST'])
def create_language() -> (dict, str):
    '''Handles a POST request for adding a new language to the database

    Args:
        None

    Returns:
        [success_response | error_response]: dict: dictionary with response
        [{error: "", "data": {"lang_id": lang_id}}} |
        {error: <error_string>, "data": ''}
        status_code: int

    Exceptions:
        ValueError, KeyError, TypeError
    '''
    try:
        if request.headers['Content-type'] != 'application/json':
            return error_response('Unsupprted input format', HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
        lang_input = json.loads(request.data)
        lang_name = lang_input['lang_name']
        _db_manager = DatabaseManager()
        if _db_manager is not None:
            lang_id = _db_manager.add_language(lang_name) or None
    except (ValueError, KeyError, TypeError) as json_err:
        return error_response(f'Invalid JSON: {json_err}', HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    if lang_name == '' or not isinstance(lang_name, str):
        return error_response('Invalid input', HTTPStatus.UNPROCESSABLE_ENTITY)
    if lang_name in existing_language.values():
        return error_response('Language already exists', HTTPStatus.CONFLICT)
    return success_response(HTTPStatus.CREATED, lang_id)

@app.route('/languages/<lang_id>', methods=['DELETE'])
def delete_language(lang_id=None) -> (dict, str):
    '''Handles a DELETE request for deleting an existing language
       from the database

    Args:
        None

    Returns:
        [success_response | error_response]: dict: dictionary with response
        [{error: "", "data": {"lang_id": lang_id}}} |
        {error: <error_string>, "data": ''}
        status_code: int
    '''
    if lang_id not in existing_language.keys():
        return error_response('Language does not exist', HTTPStatus.NOT_FOUND)
    # TODO: Handle Language already in use
    return success_response(HTTPStatus.OK, lang_id)

@app.route('/languages/<lang_id>', methods=['PUT'])
def update_language(lang_id: int=None) -> (dict, str):
    '''Handles a PUT request for updating an existing language
       from the database

    Args:
        None

    Returns:
        [success_response | error_response]: dict: dictionary with response
        [{error: "", "data": {"lang_id": lang_id}}} |
        {error: <error_string>, "data": ''}
        status_code: int
    '''
    try:
        if request.headers['Content-type'] != 'application/json':
            return error_response('Unsupprted input format', HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
        lang_input = json.loads(request.data)
        lang_name = lang_input['lang_name']
    except (ValueError, KeyError, TypeError) as json_err:
        return error_response(f'Invalid JSON: {json_err}', HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    if lang_name == '' or not isinstance(lang_name, str):
        return error_response('Invalid input', HTTPStatus.UNPROCESSABLE_ENTITY)
    if lang_id not in existing_language.keys():
        return error_response('Language does not exist', HTTPStatus.NOT_FOUND)
    if lang_name in existing_language.values():
        return error_response('Language name must be unique', HTTPStatus.CONFLICT)
    return success_response(HTTPStatus.OK, lang_id)

@app.route('/languages/<lang_id>', methods=['GET'])
def get_a_language(lang_id: int=None) -> (dict, str):
    '''Handles a GET request to retrieve a language record

    Args:
        None

    Returns:
        [success_response | error_response]: dict: dictionary with response
        [{error: "", "data": {"lang_id": lang_id}}} |
        {error: <error_string>, "data": ''}
        status_code: int
    '''
    if lang_id not in existing_language.keys():
        return error_response('Language does not exist', HTTPStatus.NOT_FOUND)
    lang_name = existing_language[lang_id]
    return success_response(HTTPStatus.OK, lang_id, lang_name)

@app.route('/languages/', methods=['GET'])
def get_languages() -> (dict, str):
    '''Handles a GET request to retrieve a language record

    Args:
        None

    Returns:
        [success_response | error_response]: dict: dictionary with response
        [{error: "", "data": {Languages:[{"lang_id": lang_id, "lang_name": lang_name}]}} |
        {error: <error_string>, "data": ''}
        status_code: int
    '''
    languages = []
    for lang_id, lang_name in existing_language.items():
        languages.append({'lang_id': lang_id, 'lang_name': lang_name})
    return success_response(HTTPStatus.OK, lang_obj=languages)


if __name__ == '__main__':
    app.run()
