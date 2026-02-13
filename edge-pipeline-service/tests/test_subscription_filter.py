import pytest


class TestSubscriptionFilterEndpoints:
    """Tests for subscription filter CRUD endpoints."""

    def test_create_filter(self, client, sample_subscription_filter):
        """Test creating a new subscription filter."""
        response = client.post("/subscription_filter", json=sample_subscription_filter)
        assert response.status_code == 201
        data = response.json()
        assert data["filter_name"] == sample_subscription_filter["filter_name"]
        assert data["filter_attributes"] == sample_subscription_filter["filter_attributes"]
        assert data["pipelines"] == []

    def test_create_filter_invalid_subscription(self, client):
        """Test creating a filter with invalid subscription ID."""
        filter_data = {
            "subscription_id": 9999,
            "filter_name": "test-filter",
            "filter_attributes": {"key": "value"},
        }
        response = client.post("/subscription_filter", json=filter_data)
        assert response.status_code == 404

    def test_get_filter(self, client, sample_subscription_filter):
        """Test getting a filter by ID."""
        create_response = client.post("/subscription_filter", json=sample_subscription_filter)
        filter_id = create_response.json()["id"]

        response = client.get(f"/subscription_filter/{filter_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == filter_id

    def test_get_filter_not_found(self, client):
        """Test getting a non-existent filter."""
        response = client.get("/subscription_filter/9999")
        assert response.status_code == 404

    def test_get_all_filters(self, client, sample_subscription_filter):
        """Test getting all filters."""
        client.post("/subscription_filter", json=sample_subscription_filter)
        filter2 = {**sample_subscription_filter, "filter_name": "filter-2"}
        client.post("/subscription_filter", json=filter2)

        response = client.get("/subscription_filter")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_filters_by_subscription(self, client, sample_subscription_filter):
        """Test getting filters for a specific subscription."""
        create_response = client.post("/subscription_filter", json=sample_subscription_filter)
        subscription_id = create_response.json()["subscription_id"]

        response = client.get(f"/subscription_filter?subscription_id={subscription_id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_update_filter(self, client, sample_subscription_filter):
        """Test updating a filter."""
        create_response = client.post("/subscription_filter", json=sample_subscription_filter)
        filter_id = create_response.json()["id"]

        update_data = {"filter_name": "updated-filter"}
        response = client.put(f"/subscription_filter/{filter_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["filter_name"] == "updated-filter"

    def test_attach_pipelines(self, client, sample_subscription_filter, sample_pipeline):
        """Test attaching pipelines to a filter."""
        # Create filter
        filter_response = client.post("/subscription_filter", json=sample_subscription_filter)
        filter_id = filter_response.json()["id"]

        # Create pipeline
        pipeline_response = client.post("/pipeline", json=sample_pipeline)
        pipeline_id = pipeline_response.json()["id"]

        # Attach pipeline to filter
        attach_data = {"pipeline_ids": [pipeline_id]}
        response = client.put(f"/subscription_filter/{filter_id}/attach", json=attach_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data["pipelines"]) == 1
        assert data["pipelines"][0]["id"] == pipeline_id

    def test_attach_invalid_pipeline(self, client, sample_subscription_filter):
        """Test attaching a non-existent pipeline."""
        filter_response = client.post("/subscription_filter", json=sample_subscription_filter)
        filter_id = filter_response.json()["id"]

        attach_data = {"pipeline_ids": [9999]}
        response = client.put(f"/subscription_filter/{filter_id}/attach", json=attach_data)
        assert response.status_code == 422

    def test_replace_attached_pipelines(self, client, sample_subscription_filter, sample_pipeline):
        """Test that attaching pipelines replaces existing ones."""
        # Create filter
        filter_response = client.post("/subscription_filter", json=sample_subscription_filter)
        filter_id = filter_response.json()["id"]

        # Create two pipelines
        pipeline1_response = client.post("/pipeline", json=sample_pipeline)
        pipeline1_id = pipeline1_response.json()["id"]

        pipeline2_data = {**sample_pipeline, "pipeline_name": "pipeline-2"}
        pipeline2_response = client.post("/pipeline", json=pipeline2_data)
        pipeline2_id = pipeline2_response.json()["id"]

        # Attach first pipeline
        client.put(f"/subscription_filter/{filter_id}/attach", json={"pipeline_ids": [pipeline1_id]})

        # Attach second pipeline (should replace first)
        response = client.put(
            f"/subscription_filter/{filter_id}/attach", json={"pipeline_ids": [pipeline2_id]}
        )
        data = response.json()
        assert len(data["pipelines"]) == 1
        assert data["pipelines"][0]["id"] == pipeline2_id
