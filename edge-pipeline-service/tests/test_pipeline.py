import pytest


class TestPipelineEndpoints:
    """Tests for pipeline CRUD endpoints."""

    def test_create_pipeline(self, client, sample_pipeline):
        """Test creating a new pipeline with initial version."""
        response = client.post("/pipeline", json=sample_pipeline)
        assert response.status_code == 201
        data = response.json()
        assert data["pipeline_name"] == sample_pipeline["pipeline_name"]
        assert data["description"] == sample_pipeline["description"]
        assert len(data["versions"]) == 1
        assert len(data["versions"][0]["steps"]) == 2

    def test_create_pipeline_without_steps(self, client):
        """Test creating a pipeline without initial steps."""
        pipeline_data = {
            "pipeline_name": "empty-pipeline",
            "description": "Pipeline without steps",
        }
        response = client.post("/pipeline", json=pipeline_data)
        assert response.status_code == 201
        data = response.json()
        assert len(data["versions"]) == 0

    def test_create_duplicate_pipeline(self, client, sample_pipeline):
        """Test creating a pipeline with duplicate name."""
        client.post("/pipeline", json=sample_pipeline)
        response = client.post("/pipeline", json=sample_pipeline)
        assert response.status_code == 409

    def test_get_pipeline(self, client, sample_pipeline):
        """Test getting a pipeline by ID."""
        create_response = client.post("/pipeline", json=sample_pipeline)
        pipeline_id = create_response.json()["id"]

        response = client.get(f"/pipeline/{pipeline_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == pipeline_id
        assert len(data["versions"]) == 1

    def test_get_pipeline_not_found(self, client):
        """Test getting a non-existent pipeline."""
        response = client.get("/pipeline/9999")
        assert response.status_code == 404

    def test_get_all_pipelines(self, client, sample_pipeline):
        """Test getting all pipelines."""
        client.post("/pipeline", json=sample_pipeline)
        pipeline2 = {**sample_pipeline, "pipeline_name": "pipeline-2"}
        client.post("/pipeline", json=pipeline2)

        response = client.get("/pipeline")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_create_new_version(self, client, sample_pipeline):
        """Test creating a new version for a pipeline."""
        create_response = client.post("/pipeline", json=sample_pipeline)
        pipeline_id = create_response.json()["id"]

        new_version_data = {
            "steps": [
                {
                    "step_name": "new-step",
                    "service_endpoint_url": "http://localhost:8003/new",
                    "step_order": 1,
                }
            ]
        }
        response = client.post(f"/pipeline/{pipeline_id}", json=new_version_data)
        assert response.status_code == 201
        data = response.json()
        assert data["version"] == 2
        assert len(data["steps"]) == 1

    def test_get_version(self, client, sample_pipeline):
        """Test getting a specific version."""
        create_response = client.post("/pipeline", json=sample_pipeline)
        pipeline_id = create_response.json()["id"]

        response = client.get(f"/pipeline/{pipeline_id}/version/1")
        assert response.status_code == 200
        data = response.json()
        assert data["version"] == 1

    def test_activate_version(self, client, sample_pipeline):
        """Test activating a pipeline version."""
        create_response = client.post("/pipeline", json=sample_pipeline)
        pipeline_id = create_response.json()["id"]

        # Activate version 1
        update_data = {"status": "active"}
        response = client.put(f"/pipeline/{pipeline_id}/version/1", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "active"

    def test_only_one_active_version(self, client, sample_pipeline):
        """Test that only one version can be active at a time."""
        create_response = client.post("/pipeline", json=sample_pipeline)
        pipeline_id = create_response.json()["id"]

        # Create second version
        new_version_data = {
            "steps": [
                {"step_name": "step", "service_endpoint_url": "http://test", "step_order": 1}
            ]
        }
        client.post(f"/pipeline/{pipeline_id}", json=new_version_data)

        # Activate version 1
        client.put(f"/pipeline/{pipeline_id}/version/1", json={"status": "active"})

        # Activate version 2
        client.put(f"/pipeline/{pipeline_id}/version/2", json={"status": "active"})

        # Check version 1 is now inactive
        response = client.get(f"/pipeline/{pipeline_id}/version/1")
        assert response.json()["status"] == "inactive"

        # Check version 2 is active
        response = client.get(f"/pipeline/{pipeline_id}/version/2")
        assert response.json()["status"] == "active"
