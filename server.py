'''Server module responsible for entertaining the requests'''

import json
from flask import jsonify
from itertools import starmap
from http import HTTPStatus
from flask import Flask, request

from lang_exch.setup.setup import config
from lang_exch.db.db_manager import DatabaseManager
from lang_exch.const import serverSection, confSection
from lang_exch.conf.log.lang_exch_logging import logger

app = Flask(__name__)
existing_language = {"1": "Gujarati", "9": "Gujarati"}

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
    message = None
    if lang_name is not None:
        message = jsonify(error='', data=jsonify(lang_id=lang_id, lang_name=lang_name))
    if lang_obj is not None:
        message = jsonify(error='', data=lang_obj)
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
        logger.info(f"Received a request to create a new language with input as: {lang_input}")
        lang_name = lang_input['lang_name']
    except (ValueError, KeyError, TypeError) as json_err:
        logger.error(f"Can not process request, Invalid JSON format: {json_err}")
        return error_response(f'Invalid JSON: {json_err}', HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    if lang_name == '' or not isinstance(lang_name, str):
        logger.error(f"Can not process request, Invalid input. language name must not be empty and non string")
        return error_response('Invalid input', HTTPStatus.UNPROCESSABLE_ENTITY)
    if lang_name in existing_language.values():
        logger.error(f"Can not process request, language name already exists. language name must be unique")
        return error_response('Language already exists', HTTPStatus.CONFLICT)
    _db_manager = DatabaseManager()
    if _db_manager is not None:
        lang_id = _db_manager.add_language(lang_name) or None
        if lang_id is not None:
            logger.info(f"language {lang_name} successfully added with ID: {lang_id}. \
                Now updating in memory store")
            existing_language[lang_id] = lang_name
        else:
            logger.error(f"Failed to add language {lang_name} in the database")
            return error_response('Some problem occured. Failed to add new language entry')
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
    logger.info(f"Received a request to delete the language: {lang_id}")
    if lang_id not in existing_language.keys():
        logger.error(f'Language does not exist with ID:{lang_id}')
        return error_response('Language does not exist', HTTPStatus.NOT_FOUND)
    _db_manager = DatabaseManager()
    if _db_manager is not None:
        _db_manager.delete_language(lang_id)
        logger.info(f"language with ID: {lang_id} successfully deleted.\
                Now updating in memory store for respective entry")
        del existing_language[lang_id]
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
        logger.info(f"Received a request to update a language with input as: {lang_input}")
        lang_name = lang_input['lang_name']
    except (ValueError, KeyError, TypeError) as json_err:
        logger.error(f"Can not process request, Invalid JSON format: {json_err}")
        return error_response(f'Invalid JSON: {json_err}', HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    if lang_name == '' or not isinstance(lang_name, str):
        logger.error(f"Can not process request, Invalid input. language name must not be empty and non string")
        return error_response('Invalid input', HTTPStatus.UNPROCESSABLE_ENTITY)
    if lang_id not in existing_language.keys():
        logger.error(f"Can not process request, language ID does not exist to update")
        return error_response('Language does not exist', HTTPStatus.NOT_FOUND)
    if lang_name in existing_language.values():
        logger.error(f"Can not process request, language name already exists. language name must be unique")
        return error_response('Language name must be unique', HTTPStatus.CONFLICT)
    _db_manager = DatabaseManager()
    if _db_manager is not None:
        _db_manager.update_language(lang_id, lang_name)
        logger.info(f"language ID: {lang_id} successfully updated with: {lang_name}. \
                Now updating in memory store")
        existing_language[lang_id] = lang_name
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
    logger.info(f"Received a request to get the language details for ID: {lang_id}")
    if lang_id not in existing_language.keys():
        logger.error(f"No data found for reqested language with ID: {lang_id}")
        return error_response('Language does not exist', HTTPStatus.NOT_FOUND)
    _db_manager = DatabaseManager()
    if _db_manager is not None:
        if _db_manager.get_a_language(lang_id) is None:
            return error_response('Language does not exist', HTTPStatus.NOT_FOUND)
        else:
            lang_name = _db_manager.get_a_language(lang_id)
        logger.info(f"data succesfully fetched: {lang_id}: {lang_name}")
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
    try:
        languages = []
        def sp(x,y):
            languages.append({'lang_id': x, 'lang_name': y})
        lang_append = languages.append
        logger.info(f"Received a request to fetch all languages")
        _db_manager = DatabaseManager()
        if _db_manager is not None:
            id_name_map = _db_manager.get_languages() or {}
        if id_name_map:
            logger.info(f"Fetched languages: {id_name_map}")
            list(starmap(sp, list(id_name_map.items())))
        return success_response(HTTPStatus.OK, lang_obj=languages)
    except:
        error_response(status_code=500)


if __name__ == '__main__':

    server_section = confSection.SERVER_SECTION.value
    app.run(host=config[server_section][serverSection.SERVER_IP_KEY.value], \
            port=config[server_section][serverSection.SERVER_PORT_KEY.value])
