class UnsupportedOffersMicroserviceResponseStatus(Exception):

    def __init__(self, status):
        self.status = status
        self.message = f"Unsupported response status code for the API: {self.status}."
        super().__init__(self.message)


class ErrorOffersMicroserviceResponseStatus(Exception):

    def __init__(self, status):
        self.status = status
        self.message = f"Offers microservice detected incorrect request: {self.status}."
        super().__init__(self.message)
