import pytest


class TestSchemaEndpoints:
    """Tests for schema CRUD endpoints."""

    def test_create_schema(self, client, sample_schema):
        """Test creating a new schema."""
        response = client.post("/schema", json=sample_schema)
        assert response.status_code == 201
        data = response.json()
        assert data["source_system"] == sample_schema["source_system"]
        assert data["source_schema"] == sample_schema["source_schema"]
        assert "id" in data
        assert "created_at" in data

    def test_get_schema(self, client, sample_schema):
        """Test getting a schema by ID."""
        # Create first
        create_response = client.post("/schema", json=sample_schema)
        schema_id = create_response.json()["id"]

        # Get
        response = client.get(f"/schema/{schema_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == schema_id
        assert data["source_system"] == sample_schema["source_system"]

    def test_get_schema_not_found(self, client):
        """Test getting a non-existent schema."""
        response = client.get("/schema/9999")
        assert response.status_code == 404

    def test_get_all_schemas(self, client, sample_schema):
        """Test getting all schemas."""
        # Create two schemas
        client.post("/schema", json=sample_schema)
        schema2 = {**sample_schema, "source_system": "system2"}
        client.post("/schema", json=schema2)

        response = client.get("/schema")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_update_schema(self, client, sample_schema):
        """Test updating a schema."""
        # Create first
        create_response = client.post("/schema", json=sample_schema)
        schema_id = create_response.json()["id"]

        # Update
        update_data = {"source_system": "updated_system"}
        response = client.put(f"/schema/{schema_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["source_system"] == "updated_system"

    def test_update_schema_not_found(self, client):
        """Test updating a non-existent schema."""
        update_data = {"source_system": "updated_system"}
        response = client.put("/schema/9999", json=update_data)
        assert response.status_code == 404
