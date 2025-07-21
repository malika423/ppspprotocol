"""
test_node.py

Unit-tests for ppspprotocol.node.Node behavior.
"""

import simpy

from ppspprotocol.node import Node
from ppspprotocol.packet import Packet


def test_on_receive_pass() -> None:
    env = simpy.Environment()
    store_a = simpy.Store(env)
    store_b = simpy.Store(env)

    node_a = Node("A", env, store_a, steal_prob=0.0)
    node_b = Node("B", env, store_b, steal_prob=0.0)
    node_a.downstream = node_b

    pkt = Packet(origin=node_a, destination=node_b)
    done = node_a.on_receive(pkt)

    assert done is False
    assert len(pkt.fingerprint_chain) == 1
    assert pkt.hops == 1


def test_on_receive_steal() -> None:
    env = simpy.Environment()
    store_a = simpy.Store(env)
    store_b = simpy.Store(env)

    node_a = Node("A", env, store_a, steal_prob=1.0)
    node_b = Node("B", env, store_b, steal_prob=1.0)
    node_a.downstream = node_b

    pkt = Packet(origin=node_a, destination=node_b)
    done = node_a.on_receive(pkt)

    assert done is False
    assert len(pkt.fingerprint_chain) == 2
    assert pkt.hops == 1
