# tests/test_analytics.py
def test_analytics_endpoints(client):
    # average-ratings
    r = client.get("/api/analytics/average-ratings")
    assert r.status_code == 200
    assert isinstance(r.json, list)

    # top-3 (with a cuisine type, e.g., "mexican")
    r = client.get("/api/analytics/top-3/Hyderabadi Biryani")
    assert r.status_code == 200
    assert isinstance(r.json, list)
