import asyncio

def distance_to(node1_id, node2_id):
    """
    Gets the distance to node2_id from node1_id.

    Parameters
    ----------
    node1_id : int
        The first node_id.
    node2_id :int
        The second node_id.

    Return
    ------
    int : the distance to the second node id from the first
    """
    return int(node1_id) ^ int(node2_id)


async def gather_responses(query_dict):
    """
    Waits runs all RPC calls that are stored in the response_dict and stores
    there result in along with the sender's ID in a new dict that is returned.
    """
    queries = list(query_dict.values())
    results = await asyncio.gather(*queries)
    return tuple(zip(query_dict.keys(),  results))


def merge_heaps(heap1, heap2, n_ell):
    """
    Merges heap1 and heap2 together creating a single list of length len.

    Parameters
    ----------
    heap1 : :class: `ContactHeap`
        The first list.
    list2 : :class: `ContactHeap`
        The second list.
    n_ell : int
        Length of the resulting list
    """
    merged_list = []
    while len(heap1) and len(heap2) and len(merged_list) < n_ell:
        if heap1.peek_first() < heap2.peek_first():
            merged_list.append(heap1.pop())
        else:
            merged_list.append(heap2.pop()) 

    if len(heap1) == 0:
        while len(heap2) > 0 and len(merged_list) < n_ell:
            merged_list.append(heap2.pop())
    else:
        while len(heap1) > 0 and len(merged_list) < n_ell:
            merged_list.append(heap1.pop())

    return merged_list
