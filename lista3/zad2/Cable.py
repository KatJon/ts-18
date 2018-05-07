from functools import reduce

class Collision(Exception):
    pass

def show_elem(e):
    return '_' if e is None else e[0]

def mkCable(length):
    return list(map(lambda _: None, range(length)))


class Cable:
    def __init__(self, length):
        self.length = length
        self.cable = mkCable(length)

    def __str__(self):
        return reduce(
            lambda p, n: p + show_elem(n), 
            self.cable,
            ''
        )

    def clear(self):
        self.cable = mkCable(self.length)
    
    def emptyL(self):
        return self.cable[0] is None
    
    def emptyR(self):
        return self.cable[-1] is None

    def pushL(self, msg):
        self.cable[0] = msg, 1

    def pushR(self, msg):
        self.cable[-1] = msg, -1

    def tick(self):
        newCable = mkCable(self.length)

        leftRecv = False
        rightRecv = False

        for i,e in enumerate(self.cable):
            if e is not None:
                msg, dir = e
                pos = i + dir
                if 0 <= pos <= self.length - 1:
                    if newCable[pos] is None:
                        if self.cable[pos] is None:
                            newCable[pos] = msg,dir
                        else:
                            msg1, dir1 = self.cable[pos]
                            if dir == dir1:
                                newCable[pos] = msg,dir
                            else:
                                raise Collision()
                    else:
                        raise Collision()
                elif pos < 0:
                    leftRecv = True
                elif pos >= self.length:
                    rightRecv = True
        self.cable = newCable
        return leftRecv, rightRecv
    # end tick