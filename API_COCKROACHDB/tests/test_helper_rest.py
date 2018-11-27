import pytest
from app.helpers.rest import *


class TestHelperRest:
    def test_response_success(self, client):
        assert response(200) == {'code': 200,
                                 'count': 0,
                                 'data': None,
                                 'message': 'Operation succeeded',
                                 'status': 'success'}
                                 
    def test_response_created(self, client):
        assert response(201) == {'code': 201,
                                 'count': 0,
                                 'data': None,
                                 'message': 'Created',
                                 'status': 'success'}
                                 
    def test_response_accepted(self, client):
        assert response(202) == {'code': 202,
                                 'count': 0,
                                 'data': None,
                                 'message': 'Accepted',
                                 'status': 'success'}

    def test_response_reply(self, client):
        assert response(204) == {'code': 204,
                                 'count': 0,
                                 'data': None,
                                 'message': 'Reply does not contain additional content',
                                 'status': 'success'}

    def test_response_not_modified(self, client):
        assert response(304) == {'code': 304,
                                 'count': 0,
                                 'data': None,
                                 'message': 'Not modified',
                                 'status': 'success'}

    def test_response_unauthorized(self, client):
        assert response(401) == {'code': 401,
                                 'count': 0,
                                 'data': None,
                                 'message': 'Unauthorized operation',
                                 'status': 'error'}

    def test_response_other(self, client):
        assert response(999) == {'code': 999,
                                 'count': 0,
                                 'data': None,
                                 'message': 'Internal error occurred - unexpected error caused by request data',
                                 'status': 'error'}

    def test_validate_wrong_token(self, client):
        assert validate('aaaaaaaa') == {
            'code': 404,
            'message': 'Wrong Token'
        }
