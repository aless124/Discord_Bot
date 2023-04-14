import Liste

class User:
    def __init__(self, username):
        self.username = username
        self.history = Liste.doublyLinkedList()

    def add_to_history(self, data):
        self.history.add_node(data)
    