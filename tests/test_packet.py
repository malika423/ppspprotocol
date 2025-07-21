"""
test_packet.py

Unit-tests for ppspprotocol.packet.Packet behavior.
"""

from types import SimpleNamespace

from ppspprotocol.packet import Packet


def test_packet_initial_state_and_repr() -> None:
    dummy = SimpleNamespace(name="X")
    pkt = Packet(origin=dummy, destination=dummy)

    assert pkt.hops == 0
    assert pkt.clap_flag is False
    assert pkt.fingerprint_chain == []

    s = repr(pkt)
    assert "from X to X" in s
    assert "hops=0" in s
