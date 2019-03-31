from kademlia.KademliaSearch import RPCResponse

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
    return tuple(zip(dict.keys(), map(RPCResponse, results)))