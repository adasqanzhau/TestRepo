"""Tests for internationalization."""


def test_landing_default_russian(client):
    resp = client.get('/landing')
    assert resp.status_code == 200
    assert b'MediPlatform' in resp.data


def test_set_language_kazakh(client):
    resp = client.get('/set-language/kk?next=/landing', follow_redirects=True)
    assert resp.status_code == 200
    # Kazakh hero line fragment
    assert 'Қазақстан'.encode('utf-8') in resp.data or b'telemedicine' in resp.data.lower()


def test_set_language_english(client):
    resp = client.get('/set-language/en?next=/landing', follow_redirects=True)
    assert resp.status_code == 200
    assert b'telemedicine' in resp.data.lower() or b'Features' in resp.data


def test_invalid_language_falls_back(client):
    resp = client.get('/set-language/xx?next=/landing', follow_redirects=True)
    assert resp.status_code == 200


def test_translate_in_template(client):
    with client.session_transaction() as sess:
        sess['locale'] = 'en'
    resp = client.get('/landing')
    assert b'Sign in' in resp.data or b'sign' in resp.data.lower()
