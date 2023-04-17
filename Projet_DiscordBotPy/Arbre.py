class node:
    def __init__(self, data):
        self.data = data
        self.right_node = None
        self.left_node = None


class binary_tree:
    def __init__(self,data):
        self.first_node = node(data)

    def append(self,data):
        new_node = node(data)
        if self.first_node is None:
            self.first_node = new_node
        else:
            n = self.first_node
            while n is not None:
                if data < n.data:
                    if n.left_node is None:
                        n.left_node = new_node
                        break
                    else:
                        n = n.left_node
                else:
                    if n.right_node is None:
                        n.right_node = new_node
                        break
                    else:
                        n = n.right_node
        
    def size(self):
        return self.size