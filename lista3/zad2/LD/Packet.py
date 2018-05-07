class Packet:
    def __init__(self, size, dir, pos):
        self.size = size
        self.dir = dir
        self.pos = pos
        self.head = pos
    # end init

    def pr