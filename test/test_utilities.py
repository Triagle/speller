from engine import utilities


def test_node():
    # There is only one method for the Node class, therefore only one test.
    node = utilities.Node(3)
    # Test str function works
    assert str(node) == '3'
    node.prev_node = node
    node.next_node = node
    node.insert(utilities.Node(4))
    node.insert(utilities.Node(5))

    # Boilerplate to accumulate each element in the list and ensure it matches
    # the order inserted.
    cur = node
    have_cycled = False
    node_list = []
    while not have_cycled:
        node_list.append(cur.value)
        cur = cur.next_node
        have_cycled = cur == node

    assert node_list == [3, 5, 4]


def test_cyclic_list():
    cyclic_lst = utilities.CyclicList([1, 2, 3, 4])
    assert cyclic_lst.length == 4
    # Ensure they are inserted in the right order
    assert cyclic_lst.head.value == 1
    assert cyclic_lst.tail.value == 4
    # Ensure they are cyclic in both directions
    assert cyclic_lst.head.prev_node == cyclic_lst.tail
    assert cyclic_lst.tail.next_node == cyclic_lst.head
    cyclic_lst.queue_front(0)
    # Ensure queue_front is actually queuing at the front and updating the head
    empty_vals = (None, None, 0)
    assert cyclic_lst.head.value == 0
    cyclic_lst.clear()
    # clear does what it should do.
    assert (cyclic_lst.head, cyclic_lst.tail, cyclic_lst.length) == empty_vals
    cyclic_lst.queue_front(0)
    # Testing special case where cyclic_list is empty.
    assert cyclic_lst.head == cyclic_lst.tail
    assert cyclic_lst.head.value == 0
    assert cyclic_lst.head.prev_node == cyclic_lst.head.next_node

    cyclic_lst.clear()
    cyclic_lst.queue_back(0)
    # Ditto for queue_back
    assert cyclic_lst.head == cyclic_lst.tail
    assert cyclic_lst.head.value == 0
    assert cyclic_lst.head.prev_node == cyclic_lst.head.next_node

    # delete special case where only one element exists
    assert cyclic_lst.length == 1
    cyclic_lst.delete(cyclic_lst.head)
    assert (cyclic_lst.head, cyclic_lst.tail, cyclic_lst.length) == empty_vals

    cyclic_lst.queue_back(0)
    cyclic_lst.queue_back(1)
    cyclic_lst.queue_back(2)
    # list is now [0, 1, 2]
    assert cyclic_lst.length == 3
    cyclic_lst.delete(cyclic_lst.head)
    # list is now [1, 2]
    assert cyclic_lst.tail.value == 2
    assert cyclic_lst.head.value == 1
    assert cyclic_lst.head.next_node.value == 2
    assert cyclic_lst.head.prev_node.value == 2
    assert cyclic_lst.tail.prev_node.value == 1
    assert cyclic_lst.tail.next_node.value == 1
    assert cyclic_lst.length == 2
    assert len(cyclic_lst) == cyclic_lst.length
    # Make sure tail deletion also works
    cyclic_lst.delete(cyclic_lst.tail)
    assert cyclic_lst.head.value == 1
    assert cyclic_lst.head.next_node == cyclic_lst.head
    assert cyclic_lst.head.prev_node == cyclic_lst.head

    cyclic_lst.queue_back(2)

    # search has no special cases
    assert cyclic_lst.search(1)
    assert cyclic_lst.search(2)
    assert not cyclic_lst.search(3)
    # Testing the __contains__ implementation.
    assert 3 not in cyclic_lst
    assert 1 in cyclic_lst

    # Testing that the "clear" method doesn't bork things if called twice.

    cyclic_lst.clear()
    cyclic_lst.clear()
    cyclic_lst.queue_back(3)
    assert cyclic_lst.head.value == 3
