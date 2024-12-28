from Plugins.Map.utils import prefab_helpers
from Plugins.Map.utils import math_helpers
import ETS2LA.variables as variables
from Plugins.Map import classes as c
from typing import List, TypeVar
import numpy as np
import logging
import math

T = TypeVar('T')

def get_connecting_item_uid(node_1, node_2) -> int:
    """Will return the connecting item between two nodes, or None if they are not connected.

    :param c.Node node_1: The first node.
    :param c.Node node_2: The second node.
    
    :return: The UID of the connecting item.
    """
    node_1_forward_item = node_1.forward_item_uid
    node_1_backward_item = node_1.backward_item_uid
    node_2_forward_item = node_2.forward_item_uid
    node_2_backward_item = node_2.backward_item_uid
    
    if node_1_forward_item == node_2_backward_item:
        return node_1_forward_item
    elif node_1_backward_item == node_2_forward_item:
        return node_1_backward_item
    elif node_1_forward_item == node_2_forward_item:
        return node_1_forward_item
    elif node_1_backward_item == node_2_backward_item:
        return node_1_backward_item
    
    return None

def rotate_left(arr: List[T], count: int) -> List[T]:
    assert 0 <= count < len(arr), "count must be within the range of the array length"
    if count == 0:
        return arr

def get_connecting_lanes_by_item(node_1, node_2, item, map_data) -> list[int]:
    if type(item) == c.Road:
        left_lanes = len(item.road_look.lanes_left)
        right_lanes = len(item.road_look.lanes_right)
        start_node = item.start_node_uid
        if start_node == node_1.uid:
            return [i for i in range(left_lanes, left_lanes + right_lanes)]
        else:
            if left_lanes > 0:
                return [i for i in range(0, left_lanes)]
            else:
                return [i for i in range(0, right_lanes)]
            
    elif type(item) == c.Prefab:
        description = item.prefab_description
        item_nodes = [map_data.get_node_by_uid(uid) for uid in item.node_uids]
        rotated_nodes = rotate_left( # match the nodes to the nodes in the prefab description
            item_nodes, item.origin_node_index
        )
        
        
    else:
        return []