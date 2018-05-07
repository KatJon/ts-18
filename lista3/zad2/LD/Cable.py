class Cable:
    def __init__(self, length):
        self.length = length
        self.devices = []
    #end __init__

    def connect(self, device, pos):
        self.devices += [(device, pos)]
    #end connect

    def print(self):
        cable = ''
        devices = ''
        for i in range(self.length):
            cable += '_'
            for _,pos in self.devices:
                if pos == i:
                    devices += '^'
                    break
            else:
                devices += ' '
            
        print(cable)
        print(devices)
    #end print

    def iteration(self):
        for p in self.packets:
            p.propagate()
            pass
    #end iteration