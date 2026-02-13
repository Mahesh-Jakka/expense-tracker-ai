import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base
from src.core.dependencies import get_db
from src.main import app


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden dependencies."""
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_schema():
    """Sample schema data for testing."""
    return {
        "source_system": "test_system",
        "source_schema": {"fields": [{"name": "id", "type": "integer"}]},
    }


@pytest.fixture
def sample_subscription():
    """Sample subscription data for testing."""
    return {
        "gcp_subscription_id": "projects/test/subscriptions/test-sub",
        "subscription_name": "Test Subscription",
        "project_id": "test-project",
        "topic_id": "test-topic",
    }


@pytest.fixture
def sample_pipeline():
    """Sample pipeline data for testing."""
    return {
        "pipeline_name": "test-pipeline",
        "description": "A test pipeline",
        "connector_id": "connector-123",
        "steps": [
            {
                "step_name": "step1",
                "service_endpoint_url": "http://localhost:8001/process",
                "step_order": 1,
            },
            {
                "step_name": "step2",
                "service_endpoint_url": "http://localhost:8002/transform",
                "step_order": 2,
            },
        ],
    }


@pytest.fixture
def sample_subscription_filter(client, sample_subscription):
    """Create a subscription and return filter data."""
    # First create a subscription
    response = client.post("/subscriptions", json=sample_subscription)
    subscription_id = response.json()["id"]

    return {
        "subscription_id": subscription_id,
        "filter_name": "test-filter",
        "filter_attributes": {"event_type": "CREATE", "source": "system-a"},
    }
