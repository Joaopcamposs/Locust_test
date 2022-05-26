from locust import HttpUser, task


class LocustTester(HttpUser):

    @task
    def root(self):
        self.client.get("/")

    @task
    def show_name(self):
        self.client.post("/name", json={"data": "Joao Pedro"})

    @task
    def show_name_cached(self):
        self.client.post("/name-cached", json={"data": "Joao Pedro"})

    def show_name_count(self):
        self.client.post("/name-count", json={"data": "Joao Pedro"})
