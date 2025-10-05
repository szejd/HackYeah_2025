"""Unit tests for health check endpoint."""

from fastapi import status


class TestHealthCheck:
    """Test cases for the health check endpoint."""

    def test_health_check_returns_200(self, client):
        """Test that health check endpoint returns 200 OK status."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK

    def test_health_check_returns_json(self, client):
        """Test that health check endpoint returns JSON response."""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"

    def test_health_check_returns_correct_structure(self, client):
        """Test that health check endpoint returns correct JSON structure."""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert isinstance(data, dict)

    def test_health_check_status_value(self, client):
        """Test that health check endpoint returns status 'ok'."""
        response = client.get("/health")
        data = response.json()

        assert data["status"] == "ok"

    def test_health_check_method_not_allowed(self, client):
        """Test that POST method is not allowed on health check endpoint."""
        response = client.post("/health")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_health_check_accessibility(self, client):
        """Test that health check is accessible without authentication."""
        # This test ensures the endpoint doesn't require auth
        response = client.get("/health")
        # Should succeed without any authorization headers
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "ok"}


class TestHealthCheckEdgeCases:
    """Edge case tests for health check endpoint."""

    def test_health_check_with_query_params(self, client):
        """Test that health check ignores query parameters."""
        response = client.get("/health?test=value")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "ok"}

    def test_health_check_multiple_requests(self, client):
        """Test that multiple health check requests work consistently."""
        for _ in range(5):
            response = client.get("/health")
            assert response.status_code == status.HTTP_200_OK
            assert response.json() == {"status": "ok"}

    def test_health_check_response_time(self, client):
        """Test that health check responds quickly."""
        import time

        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()

        assert response.status_code == status.HTTP_200_OK
        # Health check should respond in less than 1 second
        assert (end_time - start_time) < 1.0
