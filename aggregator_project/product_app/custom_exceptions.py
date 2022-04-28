class WrongOffersMicroserviceResponseStatus(Exception):

    def __init__(self, status):
        self.status = status
        self.message = f"Wrong response status code: {self.status}. Allowed only 201 - Created"
        super().__init__(self.message)


class ClientErrorOffersMicroserviceResponseStatus(Exception):

    def __init__(self, status):
        self.status = status
        self.message = f"Offers microservice detected incorrect request {self.status}"
        super().__init__(self.message)
