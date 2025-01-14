# tests/test_reviews.py
def test_create_review(client):
    # Login as user
    r = client.post(
                        "/api/auth/login",
                        json={"username": "user", "password": "user"}
    )
    user_token = r.json["access_token"]

    # First, create a restaurant as admin
    r = client.post(
                        "/api/auth/login",
                        json={"username": "admin", "password": "adminpass"}
    )
    admin_token = r.json["access_token"]
    res = client.post("/api/restaurants",
                      json={
                          "name": "Sairat Biryani",
                          "cuisine_type": "Hyderabadi Biryani",
                          "address": "New Sangvi Pune",
                          "price_range": "LOW"
                      },
                      headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == 201
    restaurant_id = res.json["id"]

    # Now submit a review as user
    r = client.post(
                        "/api/reviews",
                        json={
                            "restaurant_id": restaurant_id,
                            "rating": 4,
                            "comment": "Great place!"
                        },
                        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert r.status_code == 201
    assert r.json["rating"] == 4
