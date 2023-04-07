class list_chained:
    def __init__(self,first_data):
        self.first_node = Node(first_data)
        self.last_node = self.first_node


    def append(self,data):
        if self.first_node == None:
            self.first_node = Node(data)
        else:
            self.last_node.next_node = Node(data)
            self.last_node = self.last_node.next_node

    def insert_first(self,data):
        if self.first_node == None:
            self.first_node = Node(data)
        else:
            new_node = Node(data)
            new_node.next_node = self.first_node
            self.first_node = new_node

    def size(self):
        current = self.first_node
        count = 0
        while current != None:
            count += 1
            current = current.next_node
        return count
    
    def insert(self,data,index):
        # Add a node at a specific index
        if index == 0:
            self.insert_first(data)
        else:
            current = self.first_node
            count = 0
            while count < index - 1:
                count += 1
                current = current.next_node
            new_node = Node(data)
            new_node.next_node = current.next_node
            current.next_node = new_node


class Node:
    def __init__(self,data) -> None:
        self.data = data
        self.next_node = None


'''       Liste chainé + trié       '''

class list_chained_sorted:
    def __init__(self) -> None:
        self.first_node = Node(data)

    def append(self,data):
        if self.first_node == None:
            self.first_node = Node(data)
        else:
            self.last_node.next_node = Node(data)
            self.last_node = self.last_node.next_node
    def insert_first(self,data):
        if self.first_node == None:
            self.first_node = Node(data)
        else:
            new_node = Node(data)
            new_node.next_node = self.first_node
            self.first_node = new_node
    def size(self):
        current = self.first_node
        count = 0
        while current != None:
            count += 1
            current = current.next_node
        return count
    
    def tri(self):
        current = self.first_node
        while current != None:
            current = current.next_node
            if current.data > current.next_node.data:
                current.data,current.next_node.data = current.next_node.data,current.data
            else:
                current = current.next_node
                    
