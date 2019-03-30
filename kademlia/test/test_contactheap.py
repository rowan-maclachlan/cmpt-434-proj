import sys
sys.path.append('/home/silentknight/School/CS434/434proj/cmpt-434-proj')
from kademlia.Contact import *

def test_push(node_id):
	print(f"Running test_push with node_id: {node_id}")
	c1 = Contact(4, '0.0.0.0', 12345)
	print("c1_id: ", c1._dict['id'])
	c2 = Contact(8, '0.0.0.0', 12345)
	print("c2_id: ", c2._dict['id'])
	c3 = Contact(16, '0.0.0.0', 12345)
	print("c3_id: ", c3._dict['id'])
	c4 = Contact(32, '0.0.0.0', 12345)
	print("c4_id: ", c4._dict['id'])

	test_heap = ContactHeap(node_id)
	test_heap.push(c1)
	test_heap.push(c2)
	test_heap.push(c3)
	test_heap.push(c4)

	for ell in test_heap._heap:
		print(ell[1]._dict['id'])
	print()

def test_add(node_id):
	print(f"Running test_add with node_id: {node_id}")
	contact_list = []

	for i in range(10):
		contact_list.append(Contact(pow(2, i), '0.0.0.0', 1245))
		print(f"C{i}: {contact_list[i]._dict['id']}")

	test_heap = ContactHeap(node_id)
	test_heap.add(contact_list)

	for ell in test_heap._heap:
		print(f"id: {ell[1]._dict['id']} distance: {ell[0]}")
	print()



test_push(17)
test_push(32)
test_push(0)

test_add(0)
test_add(256)
