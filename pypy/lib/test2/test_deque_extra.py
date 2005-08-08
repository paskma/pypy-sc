# Deque Tests



n = 10
class Test_deque:
    def setup_method(self,method):
        
        from pypy.lib.collections import deque
        self.d = deque(range(n))
        
    def test_deque(self):
        
        assert len(self.d) == n
        for i in range(n):
            assert i == self.d[i]
        for i in reversed(range(n)):
            assert self.d.pop() == i
            
    def test_deque_iter(self):
        it = iter(self.d)
        assert len(it) == n
        assert it.next() == 0
        assert len(it) == n-1
        self.d.pop()
        raises(RuntimeError,it.next)
        assert len(it) == 0
        assert list(it) == []
        
    def test_deque_reversed(self):
        it = reversed(self.d)
        assert len(it) == n
        assert it.next() == n-1
        assert len(it) == n-1
        self.d.pop()
        raises(RuntimeError,it.next)
        assert len(it) == 0
        assert list(it) == []