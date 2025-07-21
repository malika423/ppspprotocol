import uuid


class Packet:
    def __init__(self, origin, destination):
        self.id = uuid.uuid4()
        self.origin = origin
        self.destination = destination
        self.hops = 0
        self.clap_flag = False  # ACK path marker
        self.fingerprint_chain = []

    def __repr__(self):
        return (
            f"<Packet {self.id.hex[:6]} "
            f"from {self.origin.name} to {self.destination.name}, "
            f"hops={self.hops}, clap={self.clap_flag}, "
            f"fp={self.fingerprint_chain}>"
        )
