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


async def gather_responses(response_dict):
    cors = list(response_dict.values())
    results = away asyncio.gather(*cors)
    return dict(zip(dict.keys(), results))