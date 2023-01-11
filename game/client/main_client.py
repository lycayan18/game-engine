from client.client_engine import ClientEngine

from core.world import World


class Client(ClientEngine):
    def __init__(self, world: World, ip: str, port: int):
        super(Client, self).__init__(world, ip, port)

        self.client_id = -1
        self.current_entity_id = -1

    def set_client_id(self, id: int):
        self.client_id = id

    def is_authorized(self):
        return self.client_id != -1

    def set_current_entity_id(self, id: int):
        self.current_entity_id = id

    def get_current_entity_id(self) -> int:
        return self.current_entity_id

    def request_client_id(self):
        self.send_command("get_client_id", {}, self.set_client_id)

    def request_current_entity_id(self):
        """
        Requests player's current entity id.\n
        Note: ```request_client_id()``` must be called once before this method to authorize client.
        """

        # Check that we're authorized
        if self.client_id == -1:
            return

        self.send_command("get_current_entity_id",
                          {"client_id": self.client_id},
                          self.set_current_entity_id)
