# tests/test_async.py
def test_async_demo_endpoint(client):
    r = client.get("/api/async-demo/hello")
    assert r.status_code == 200
    assert r.json["message"] == "Hello from async endpoint!"
