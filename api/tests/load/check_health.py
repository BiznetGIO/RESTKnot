from locust import HttpUser, TaskSet, between, task


class ApiUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        pass

    @task
    def check_health(self):
        """Check server health."""
        headers = {"X-API-Key": "123"}
        self.client.get("/health", headers=headers, name="Check health")
