import random
import string

import rendezvous


def _random_string(K):
    """Returns a random string upto length K."""
    L = random.choice(range(K))
    ret = []
    for _ in range(L):
        ret.append(random.choice(string.hexdigits))
    return ''.join(ret)


class TestRing(object):
    def setup(self):
        self.ip1 = '1.1.1.1'
        self.ip2 = '2.1.1.2'
        self.ip3 = '3.2.2.2'

    def test_add_remove(self):
        ring = rendezvous.Ring()

        # initially no nodes in the ring
        assert set() == ring.nodes()

        # add some nodes
        ring.add(self.ip1)
        assert {self.ip1} == ring.nodes()

        ring.add(self.ip2)
        ring.add(self.ip3)
        assert {self.ip1, self.ip2, self.ip3} == ring.nodes()

        ring.remove(self.ip2)
        assert {self.ip1, self.ip3} == ring.nodes()
        ring.remove(self.ip1)
        ring.remove(self.ip3)
        assert set() == ring.nodes()

    def test_hash(self):
        ring = rendezvous.Ring({self.ip1})
        keys = [_random_string(100) for _ in range(100)]
        # with only one node, all keys should hash to it
        for k in keys:
            assert self.ip1 == ring.hash(k)

        ring.add(self.ip2)
        ring.add(self.ip3)
        # but with three nodes, keys should hash roughly equally
        counts = {
            self.ip1: 0,
            self.ip2: 0,
            self.ip3: 0,
        }
        for k in keys:
            n = ring.hash(k)
            counts[n] += 1

        assert 3 == len(counts)
        assert 10 <= counts[self.ip1]
        assert 10 <= counts[self.ip2]
        assert 10 <= counts[self.ip3]

        # now remove ip1 and make sure it never appears
        ring.remove(self.ip1)
        for k in keys:
            assert self.ip1 != ring.hash(k)
