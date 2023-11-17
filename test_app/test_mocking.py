import urllib.parse


def getssh():
    return urllib.parse.urljoin("https://docs.pytest.org/", "en/7.1.x/how-to/monkeypatch.html")


def test_url(monkeypatch):
    def mockreturn(*args, **kwargs):
        return "https://9999pytest.org/en/7.1.x/how-to/monkeypatch.html"

    monkeypatch.setattr(urllib.parse, 'urljoin', mockreturn)
    print(getssh())

