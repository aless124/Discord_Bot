import Liste

class User:
    def __init__(self, username):
        self.username = username
        self.history = Liste.DoublyLinkedList()

    def add_to_history(self, data):
        self.history.add_node(data)