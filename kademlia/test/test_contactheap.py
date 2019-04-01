import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
from kademlia.Contact import *

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

	for ell in test_heap._heap:
		print(ell[1].getId())
	print()


def test_push_all():
	contact_list = []

	for i in range(10):
		contact_list.append(Contact(pow(2, i), '0.0.0.0', 1245))
		print(f"C{i}: {contact_list[i].getId()}")

	test_heap = ContactHeap(0)
	test_heap.push_all(contact_list)

	for ell in test_heap._heap:
		print(f"id: {ell[1].getId()} distance: {ell[0]}")
	print()

def test_contains():
	print("Running test_contains")
	contact_list = []

	for i in range(10):
		contact_list.append(Contact(pow(2, i), '0.0.0.0', 1245))

	test_heap = ContactHeap(0)
	test_heap.push_all(contact_list)

	# test values that weren't added aren't contained
	assert not test_heap.contains(Contact(5, '0.0.0.0', 12345))
	assert not test_heap.contains(Contact(0, '0.0.0.0', 12345))
	assert not test_heap.contains(Contact(511, '0.0.0.0', 12345))
	assert not test_heap.contains(Contact(None, '0.0.0.0', 12345))

	# test values that were added are contained
	for i in range(10):
		assert test_heap.contains(Contact(pow(2, i), '0.0.0.0', 12345))
	print("success")
	print()

