class Node:
    ''' Node in circular doubly linked list.
    Holds a next pointer and previous pointer.
    '''
    def __init__(self, value):
        ''' Initialize Node class. '''
        self.next_node = None
        self.prev_node = None
        self.value = value

    def insert(self, node):
        ''' Insert a node after this node. '''
        # Visual for inserting node b.
        # <- a -> <- c ->
        # <- a -> b <- c ->
        # next's previous should point to new node.
        # previous's next should point to new node.
        node.prev_node = self
        node.next_node = self.next_node
        self.next_node.prev_node = node
        self.next_node = node

    def __str__(self):
        ''' Return a string representation of Node. '''
        return str(self.value)


class CyclicList:
    ''' CyclicList is a circular, doubly linked list[0].
    [0]: https://en.wikipedia.org/wiki/Doubly_linked_list#Circular_doubly_linked_lists
    '''
    def __init__(self, values=[]):
        ''' Initialize CyclicList '''
        self.head = None
        self.tail = None
        self.length = 0
        values = values or []
        for value in values:
            self.queue_back(value)

    def queue_back(self, value):
        ''' Queue element at the end of the cyclic list. '''
        if self.length == 0:
            # Handle special case where CyclicList is empty
            node = Node(value)
            node.prev_node = node
            node.next_node = node
            self.head = node
            self.tail = node
        else:
            node = Node(value)
            self.tail.insert(node)
            self.tail = node

        self.length += 1

    def queue_front(self, value):
        ''' Queue element at the front of the cyclic list. '''
        if self.length == 0:
            # Handle special case where CyclicList is empty
            node = Node(value)
            node.prev_node = node
            node.next_node = node
            self.head = node
            self.tail = node
        else:
            node = Node(value)
            self.head.insert(node)
            self.head = node

        self.length += 1

    def clear(self):
        ''' Remove all elements from CyclicList. '''
        self.length = 0
        self.head = None
        self.tail = None

    def delete(self, node):
        ''' Delete element from CyclicList. '''
        if self.length == 1:
            # Handle special case where CyclicList has exactly one element.
            self.clear()
        else:
            # Make the previous pointer's next pointer current node's next pointer
            node.prev_node.next_node = node.next_node
            # Make the next pointer's previous pointer current node's previous pointer
            node.next_node.prev_node = node.prev_node
            if node == self.head:
                self.head = node.next_node
            elif node == self.tail:
                self.tail = node.prev_node

            self.length -= 1

    def search(self, key):
        ''' Search for key in CyclicList. '''
        cycled = False
        cur = self.head
        # Gotta make sure I recognize when I have iterated through the entire
        # list.
        while not cycled:
            if cur.value == key:
                return True
            cur = cur.next_node
            cycled = cur == self.head
        return False

    def __contains__(self, item):
        ''' Returns true if value is contained within CyclicList. '''
        return self.search(item)

    def __len__(self):
        ''' Return the length of a CyclicList. '''
        return self.length

    def __str__(self):
        cur = self.head
        result = ''
        while cur != self.tail:
            result += f'{cur.prev_node.value} <- {cur} -> {cur.next_node.value}, '
            cur = cur.next_node
        result += f'{self.tail.prev_node.value} <- {self.tail} -> {self.tail.next_node.value}'
        return result
