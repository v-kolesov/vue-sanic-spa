import os


def test_user_auth_successfully(app):
    data = {
        'email': os.getenv('API_ADMIN_EMAIL'),
        'password': os.getenv('API_ADMIN_PASSWORD')
    }
    req, res = app.test_client.post('/v1.0/user/auth', json=data)

    assert res.status == 200
    assert res.json['valid']
    assert 'access_token' in res.json['data']
    assert res.json['data']['access_token'] is not None
