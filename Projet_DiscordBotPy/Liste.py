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
    def __init__(self, data):
        self.item = data
        self.next = None
        self.prev = None

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
        return self.first_node
    
class Stack:
    def __init__(self) -> None:
        self.list = list_chained_sorted()
    def push(self,data):
        self.list.append(data)
    def pop(self):
        self.list.insert_first(None)
    def size(self):
        return self.list.size()
    def tri(self):
        return self.list.tri()
    def peek(self):
        return self.list.first_node.data
    

# Initialise the Node
class Node:
    def __init__(self, data):
        self.item = data
        self.next = None
        self.prev = None
# Class for doubly Linked List
class doublyLinkedList:
    def __init__(self):
        self.start_node = None
    # Insert Element to Empty list
    def InsertToEmptyList(self, data):
        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node
        else:
            print("The list is empty")
    # Insert element at the end
    def InsertToEnd(self, data):
        # Check if the list is empty
        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node
            return
        n = self.start_node
        # Iterate till the next reaches NULL
        while n.next is not None:
            n = n.next
        new_node = Node(data)
        n.next = new_node
        new_node.prev = n
    # Delete the elements from the start
    def DeleteAtStart(self):
        if self.start_node is None:
            print("The Linked list is empty, no element to delete")
            return 
        if self.start_node.next is None:
            self.start_node = None
            return
        self.start_node = self.start_node.next
        self.start_prev = None;
    # Delete the elements from the end
    def delete_at_end(self):
        # Check if the List is empty
        if self.start_node is None:
            print("The Linked list is empty, no element to delete")
            return 
        if self.start_node.next is None:
            self.start_node = None
            return
        n = self.start_node
        while n.next is not None:
            n = n.next
        n.prev.next = None
    # Traversing and Displaying each element of the list
    def Display(self):
        if self.start_node is None:
            print("The list is empty")
            return
        else:
            n = self.start_node
            while n is not None:
                print("Element is: ", n.item)
                n = n.next
        print("\n")
# Create a new Doubly Linked List
NewDoublyLinkedList = doublyLinkedList()
# Insert the element to empty list
NewDoublyLinkedList.InsertToEmptyList(10)
# Insert the element at the end
NewDoublyLinkedList.InsertToEnd(20)
NewDoublyLinkedList.InsertToEnd(30)
NewDoublyLinkedList.InsertToEnd(40)
NewDoublyLinkedList.InsertToEnd(50)
NewDoublyLinkedList.InsertToEnd(60)
# Display Data
NewDoublyLinkedList.Display()
# Delete elements from start
NewDoublyLinkedList.DeleteAtStart()
# Delete elements from end
NewDoublyLinkedList.DeleteAtStart()
# Display Data
NewDoublyLinkedList.Display()