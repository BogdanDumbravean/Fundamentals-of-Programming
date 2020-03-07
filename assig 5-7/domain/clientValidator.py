from domain.client import Client

class ClientValidator:
    def validate(self, client):
        if type(client) != Client:
            raise TypeError("Can only validate clients!")

        if client.getID() <= 0 or type(client.getID()) != int:
            raise ValueError("ID must be a natural number!")
  
        if client.getName() == "":
            raise ValueError("The name cannot be null!")

        return True