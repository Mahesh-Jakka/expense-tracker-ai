import pytest


class TestSubscriptionEndpoints:
    """Tests for subscription CRUD endpoints."""

    def test_create_subscription(self, client, sample_subscription):
        """Test creating a new subscription."""
        response = client.post("/subscriptions", json=sample_subscription)
        assert response.status_code == 201
        data = response.json()
        assert data["gcp_subscription_id"] == sample_subscription["gcp_subscription_id"]
        assert data["subscription_name"] == sample_subscription["subscription_name"]
        assert "id" in data

    def test_create_duplicate_subscription(self, client, sample_subscription):
        """Test creating a subscription with duplicate GCP ID."""
        client.post("/subscriptions", json=sample_subscription)
        response = client.post("/subscriptions", json=sample_subscription)
        assert response.status_code == 409

    def test_get_subscription(self, client, sample_subscription):
        """Test getting a subscription by ID."""
        create_response = client.post("/subscriptions", json=sample_subscription)
        subscription_id = create_response.json()["id"]

        response = client.get(f"/subscriptions/{subscription_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == subscription_id

    def test_get_subscription_not_found(self, client):
        """Test getting a non-existent subscription."""
        response = client.get("/subscriptions/9999")
        assert response.status_code == 404

    def test_get_all_subscriptions(self, client, sample_subscription):
        """Test getting all subscriptions."""
        client.post("/subscriptions", json=sample_subscription)
        sub2 = {**sample_subscription, "gcp_subscription_id": "projects/test/subscriptions/sub2"}
        client.post("/subscriptions", json=sub2)

        response = client.get("/subscriptions")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_update_subscription(self, client, sample_subscription):
        """Test updating a subscription."""
        create_response = client.post("/subscriptions", json=sample_subscription)
        subscription_id = create_response.json()["id"]

        update_data = {"subscription_name": "Updated Name"}
        response = client.put(f"/subscriptions/{subscription_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["subscription_name"] == "Updated Name"

    def test_update_subscription_not_found(self, client):
        """Test updating a non-existent subscription."""
        update_data = {"subscription_name": "Updated Name"}
        response = client.put("/subscriptions/9999", json=update_data)
        assert response.status_code == 404
