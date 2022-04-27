import random

from locust import HttpUser, TaskSet, between, task


class ApiUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        pass

    @task
    def create_domain(self):
        """Create multiple users with different email address and project id."""
        random_num = int("".join([f"{random.randint(0, 9)}" for num in range(0, 4)]))

        headers = {"X-API-Key": "123"}
        data = {"email": f"test-{random_num}@gmail.com"}
        response = self.client.post(
            "/user/add", data=data, headers=headers, name="Create new user"
        )

        user_id = response["data"]["id"]
        data = {"user_id": "", "zone": f"test-{random-num}.com"}
        self.client.post(
            "/domain/add", data=data, headers=headers, name="Create new domain"
        )
