class Device:
    def __init__(self, cable, pos, P, msg):
        self.cable = cable
        self.pos = pos
        self.P = P
        self.msg = msg

        self.cable.connect(self, pos)
    # end __init__

    def recv(self, data):
        print(data)
    #end recv

    def emit(self):
        return []
    #end emit
