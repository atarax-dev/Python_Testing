from locust import HttpUser, task


class WebsiteUser(HttpUser):
    @task
    def main_page(self):
        self.client.get("/")

    @task
    def clubs_page(self):
        self.client.get("/clubs")

    @task
    def login(self):
        self.client.post("/showSummary", data=dict(email="john@simplylift.co"))

    @task
    def book(self):
        self.client.get("/book/Test%20Classic/She%20Lifts")

    @task
    def book_with_wrong_path(self):
        self.client.get("/book/Fake%20Classic/She%20Lifts")

    @task
    def purchase_ok(self):
        self.client.post(
            "/purchasePlaces", data=dict(competition="Test Classic", club="She Lifts", places=2))

    @task
    def purchase_on_past_competitions(self):
        self.client.post(
            "/purchasePlaces", data=dict(competition="Fall Classic", club="She Lifts", places=2))

    @task
    def purchase_more_than_available_places(self):
        self.client.post(
            "/purchasePlaces", data=dict(competition="TestMonkey Classic", club="She Lifts", places=4))

    @task
    def purchase_with_negative_places(self):
        self.client.post(
            "/purchasePlaces", data=dict(competition="TestMonkey Classic", club="She Lifts", places=-4))

    @task
    def purchase_more_than_12_places(self):
        self.client.post(
            "/purchasePlaces", data=dict(competition="Test Classic", club="She Lifts", places=13))
