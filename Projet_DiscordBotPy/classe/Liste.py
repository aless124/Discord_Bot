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
        self.size = 0
        self.author = None
    
    # Insert Element to Empty list
    def InsertToEmptyList(self, data):
        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node
            self.size += 1
        else:
            print("The list is not empty")
    # Insert element at the end
    def InsertToEnd(self, data):
        # Check if the list is empty
        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node
            self.size += 1
            return
        
        n = self.start_node
        # Iterate till the next reaches NULL
        while n.next is not None:
            n = n.next
        new_node = Node(data)
        self.size += 1
        n.next = new_node # type: ignore
        new_node.prev = n # type: ignore
    # Delete the elements from the start
    def DeleteAtStart(self):
        self.size -= 1
        if self.start_node is None:
            print("The Linked list is empty, no element to delete")
            return 
        if self.start_node.next is None:
            self.start_node = None
            return
        self.start_node = self.start_node.next
        self.start_prev = None
    # Delete the elements from the end
    def delete_at_end(self):
        self.size -= 1
        # Check if the List is empty
        if self.start_node is None:
            print("The Linked list is empty, no element to delete")
            return ("The Linked list is empty, no element to delete")
        else:
            n = self.start_node
            while n.next is not None:
                n = n.next
            n.prev.next = None
    # Delete the elements from the end
        
    # Traversing and Displaying each element of the list
    def DeleteAll(self):       

        if self.start_node is None:
            print("The Linked list is empty, no element to delete")
            return "The Linked list is empty, no element to delete"
        else:
            for _ in range(self.size_liste()):
            #self.size -= 1
                if self.start_node == None:
                    print("The Linked list is empty, no element to delete")
                    return "The Linked list is empty, no element to delete"
                elif self.start_node.next == None:
                    self.start_node = None
            
                else :
                    self.start_node = self.start_node.next
                    self.start_prev = None
        return self
    
    def Display(self):
        if self.start_node is None:
            print("The list is empty")
            return
        else:
            Liste = []
            n = self.start_node
            while n is not None:
                Liste.append(n.item)
                n = n.next
        return Liste
    
    def DisplayLast(self):
        if self.start_node is None:
            print("The list is empty")
            return
        else:
            Liste = []
            n = self.start_node
            while n is not None:
                Liste.append(n.item)
                n = n.next
        return Liste[-1]
    
    def DisplayOne(self, index):
        if self.start_node is None:
            print("The list is empty")
            return
        else:
            Liste = []
            n = self.start_node
            while n is not None:
                Liste.append(n.item)
                n = n.next
        return Liste[index]

    # Size of the list

    def size_liste(self):
        print("Size of the list is: ", self.size)
        return self.size


'''
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
# Delete elements from start
NewDoublyLinkedList.DeleteAtStart()
# Delete elements from end
NewDoublyLinkedList.DeleteAtStart()
# Display Data
NewDoublyLinkedList.Display()
# Delete all elements

print("*"*50)

# Display Data
NewDoublyLinkedList.DeleteAll()
NewDoublyLinkedList.Display()
NewDoublyLinkedList.size_liste()
'''

