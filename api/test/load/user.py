from locust import HttpLocust, TaskSet, task, between


class UserBehavior(TaskSet):
    def on_start(self):
        pass

    @task(1)
    def create_user(self):
        # FIXME still need skip unique email check
        headers = {"X-API-Key": "123"}
        data = {"email": "test@gmail.com", "project_id": "100"}
        self.client.post(
            "/api/user/add", data=data, headers=headers, name="Create new user"
        )


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 15)
