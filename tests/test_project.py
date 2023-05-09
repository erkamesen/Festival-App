import responses
from apps.models import Team 


def test_home_get(client):
    response = client.get("/")
    assert b"<title>BatKar Festival</title>" in response.data and response.status_code == 200


def test_home_post(client):
    test_data = dict(email="test@mail.com", message="test_message")
    response = client.post("/", data=test_data, follow_redirects=True)
    assert b"Bilet Al" in response.data

def test_join_us(client, app):
    test_data = dict(name="test_name",
                     email="test_mail@mail.com",
                     education="test_University",
                     find_where="test_Instagram",
                     experience="test_Experienced")
    client.post("/bize-katil", data=test_data,
                           follow_redirects=True)
    with app.app_context():
        assert Team.query.count() == 1
        assert Team.query.first().email == "test_mail@mail.com"


def test_ticket_(client, app):
    response = client.get("/ticket", follow_redirects=True)
    assert b"<h1>Bilet Bulunamadi.</h1>" in response.data

    with app.test_client() as c:
        r = c.get('/ticket', query_string={'ticketNo': '83ad067b62968032'})   
    assert b"static" in r.data
    

def payment(client):
    """   responses.add(
        responses.GET,

    ) """
    ticket_code = "K66"
    response = client.post("/payment/K1")
    assert b"Bilet Kodu Hatasi- Bize Ulas !" in response.data





