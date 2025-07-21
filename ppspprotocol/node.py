import random


class Node:
    def __init__(
        self,
        name,
        env,
        inbox,
        downstream=None,
        steal_prob=0.0
    ):
        self.name = name
        self.env = env
        self.inbox = inbox
        self.downstream = downstream
        self.steal_prob = steal_prob

    def stamp_fingerprint(self, pkt):
        pkt.fingerprint_chain.append((self.name, self.env.now))

    def send_pass(self, pkt):
        pkt.hops += 1
        self.downstream.inbox.put(pkt)

    def send_steal(self, pkt):
        pkt.hops += 1
        # 'Steal' behavior: re-encrypt (simulated as stamp)
        self.stamp_fingerprint(pkt)
        self.downstream.inbox.put(pkt)

    def send_ack(self, pkt):
        pkt.clap_flag = True
        # reverse path via fingerprint chain
        while pkt.fingerprint_chain:
            _, _ = pkt.fingerprint_chain.pop()
            pkt.hops += 1

    def on_receive(self, pkt):
        self.stamp_fingerprint(pkt)
        if self.name == pkt.destination.name:
            # reached destination
            return True

        if random.random() < self.steal_prob:
            self.send_steal(pkt)
        else:
            self.send_pass(pkt)

        return False
