import simpy

from ppspprotocol.packet import Packet
from ppspprotocol.node import Node


DEFAULT_TIMEOUT = 100


def run_one(steal_prob: float) -> tuple[bool, int]:
    """
    Run a single PPSP packet simulation over a 4-node line (A→B→C→D).
    Returns (delivered, hop_count).
    """
    env = simpy.Environment()

    stores = {
        name: simpy.Store(env)
        for name in ("A", "B", "C", "D")
    }

    nodes: dict[str, Node] = {
        name: Node(
            name=name,
            env=env,
            inbox=stores[name],
            steal_prob=steal_prob,
        )
        for name in ("A", "B", "C", "D")
    }

    # Wire downstream references
    nodes["A"].downstream = nodes["B"]
    nodes["B"].downstream = nodes["C"]
    nodes["C"].downstream = nodes["D"]
    nodes["D"].downstream = None

    pkt = Packet(origin=nodes["A"], destination=nodes["D"])
    stores["A"].put(pkt)

    delivered = False
    hop_count = 0

    def process(store: simpy.Store, node: Node) -> None:
        nonlocal delivered, hop_count
        while True:
            pkt = yield store.get()
            done = node.on_receive(pkt)
            if done:
                delivered = True
                hop_count = pkt.hops
                return

    for name in ("A", "B", "C", "D"):
        env.process(process(stores[name], nodes[name]))

    env.run(until=DEFAULT_TIMEOUT)
    return delivered, hop_count


def main() -> None:
    import sys

    prob = 0.0
    if len(sys.argv) > 1:
        try:
            prob = float(sys.argv[1])
        except ValueError:
            pass

    delivered, hops = run_one(prob)
    print(f"{delivered},{hops}")


if __name__ == "__main__":
    main()
