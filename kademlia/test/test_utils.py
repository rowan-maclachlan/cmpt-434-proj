import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
import pytest

from kademlia.Contact import Contact
from kademlia.utils import distance_to
from kademlia.hashing import hash_function

def test_distance():

    assert distance_to(1234, 4321) == distance_to(4321, 1234)

    assert distance_to(1234, 0) == 1234

    # 3 < 2
    assert distance_to(1, 2) > distance_to(1, 3)
    # 1 < 5
    assert distance_to(2, 3) < distance_to(2, 4)
    # 7 > 6 
    assert distance_to(3, 4) > distance_to(3, 5)
    # 1 < 2 
    assert distance_to(4, 5) < distance_to(4, 6)
    # 3 > 2 
    assert distance_to(5, 6) > distance_to(5, 7)
    # 1 < 14
    assert distance_to(6, 7) < distance_to(6, 8)


def test_hash_function():

    hash01 = hash_function("hello there")
    hash02 = hash_function("hi there")
    hash03 = hash_function("hello there.")

    assert hash01 != hash02
    assert hash01 != hash03
    assert hash02 != hash03

    assert hash01 == hash_function("hello there")
    assert hash02 == hash_function("hi there")
    assert hash03 == hash_function("hello there.")
