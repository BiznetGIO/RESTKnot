import random
from locust import HttpLocust, TaskSet, task, between


class UserBehavior(TaskSet):
    def on_start(self):
        pass

    @task(1)
    def create_user(self):

        random_num = int("".join([f"{random.randint(0, 9)}" for num in range(0, 4)]))

        headers = {"X-API-Key": "123"}
        data = {"email": f"test-{random_num}@gmail.com", "project_id": random_num}
        self.client.post(
            "/api/user/add", data=data, headers=headers, name="Create new user"
        )


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 15)
