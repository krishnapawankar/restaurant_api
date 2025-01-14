# tests/test_restaurants.py
def test_create_restaurant_unauthorized(client):
    # Attempt to create restaurant without JWT
    r = client.post("/api/restaurants", json={
        "name": "Gullu dada Biryani",
        "cuisine_type": "Hyderabadi Biryani",
        "address": "New Sangvi Pune",
        "price_range": "MEDIUM"
    })
    # Expect 401 Unauthorized
    assert r.status_code == 401


def test_create_restaurant_as_admin(client):
    # Login as admin
    r = client.post("/api/auth/login", json={"username": "admin", "password": "adminpass"})
    token = r.json["access_token"]

    # Create restaurant
    r = client.post("/api/restaurants",
                    json={
                        "name": "Krishna's Biryani",
                        "cuisine_type": "Hyderabadi Biryani",
                        "address": "New Sangvi Pune",
                        "price_range": "MEDIUM"
                    },
                    headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 201
    assert r.json["name"] == "Krishna's Biryani"
