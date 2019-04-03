import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
from kademlia.Contact import *
from kademlia.utils import merge_heaps

def test_push():
    c1 = Contact(4, '0.0.0.0', 12345)
    print("c1_id: ", c1.getId())
    c2 = Contact(8, '0.0.0.0', 12345)
    print("c2_id: ", c2.getId())
    c3 = Contact(16, '0.0.0.0', 12345)
    print("c3_id: ", c3.getId())
    c4 = Contact(32, '0.0.0.0', 12345)
    print("c4_id: ", c4.getId())

    test_heap = ContactHeap(17)
    test_heap.push(c1)
    test_heap.push(c2)
    test_heap.push(c3)
    test_heap.push(c4)

    assert c1 in test_heap
    assert c2 in test_heap  
    assert c3 in test_heap  
    assert c4 in test_heap  

    assert 4 == len(test_heap)


def test_push_all():
    contact_list = []

    for i in range(10):
        contact_list.append(Contact(pow(2, i), '0.0.0.0', 1245))
        print(f"C{i}: {contact_list[i].getId()}")

    test_heap = ContactHeap(0)
    test_heap.push_all(contact_list)

    assert 10 == len(test_heap)

    for i in range(10):
        assert Contact(pow(2, i), '0.0.0.0', 1245) in test_heap


def test_contains():
    print("Running test_contains")
    contact_list = []

    for i in range(10):
        contact_list.append(Contact(pow(2, i), '0.0.0.0', 1245))

    test_heap = ContactHeap(0)
    test_heap.push_all(contact_list)

    # test values that weren't added aren't contained
    assert Contact(5, '0.0.0.0', 12345) not in test_heap
    assert Contact(0, '0.0.0.0', 12345) not in test_heap
    assert Contact(511, '0.0.0.0', 12345) not in test_heap
    assert Contact(None, '0.0.0.0', 12345) not in test_heap

    # test values that were added are contained
    for i in range(10):
        assert Contact(pow(2, i), '0.0.0.0', 12345) in test_heap

def test_merge_heaps():
    contact_list1 = []
    contact_list2 = []

    for i in range(10):
        contact_list1.append(Contact(pow(2, i), '0.0.0.0', 1245))
    
    for i in range(10):
        contact_list2.append(Contact(pow(3, i), '0.0.0.0', 1245))

    test_heap1 = ContactHeap(0)
    test_heap2 = ContactHeap(0)
    
    test_heap1.push_all(contact_list1)
    test_heap2.push_all(contact_list2)

    merged_heap = merge_heaps(test_heap1, test_heap2, 10)

    assert len(merged_heap) == 10

