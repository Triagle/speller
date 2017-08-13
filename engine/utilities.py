class Node:
    def __init__(self, value):
        self.next_node = None
        self.prev_node = None
        self.value = value

    def insert(self, node):
        node.prev_node = self
        node.next_node = self.next_node
        self.next_node.prev_node = node
        self.next_node = node

    def __str__(self):
        return str(self.value)


class CyclicList:
    def __init__(self, values=[]):
        self.head = None
        self.tail = None
        self.length = 0
        values = values or []
        for value in values:
            self.queue_back(value)

    def queue_back(self, value):
        if self.length == 0:
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
        if self.length == 0:
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
        self.length = 0
        self.head = None
        self.tail = None

    def delete(self, node):
        if self.length == 1:
            self.clear()
        else:
            node.prev_node.next_node = node.next_node
            node.next_node.prev_node = node.prev_node
            if node == self.head:
                self.head = node.next_node
            elif node == self.tail:
                self.tail = node.prev_node

            self.length -= 1

    def search(self, key):
        cycled = False
        cur = self.head
        while not cycled:
            if cur.value == key:
                return True
            cur = cur.next_node
            cycled = cur == self.head
        return False

    def __contains__(self, item):
        return self.search(item)

    def __len__(self):
        return self.length

    def __str__(self):
        cur = self.head
        result = ''
        while cur != self.tail:
            result += f'{cur.prev_node.value} <- {cur} -> {cur.next_node.value}, '
            cur = cur.next_node
        result += f'{self.tail.prev_node.value} <- {self.tail} -> {self.tail.next_node.value}'
        return result
