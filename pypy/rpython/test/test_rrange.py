from pypy.rpython.rrange import *
from pypy.rpython.test.tool import BaseRtypingTest, LLRtypeMixin, OORtypeMixin
from pypy.rpython.rarithmetic import intmask


class BaseTestRrange(BaseRtypingTest):

    def test_rlist_range(self):
        def test1(start, stop, step, varstep):
            expected = range(start, stop, step)
            length = len(expected)
            if varstep:
                l = self.rrange.ll_newrangest(start, stop, step)
                step = l.step
            else:
                RANGE = self.rrange.RangeRepr(step).RANGE
                l = self.rrange.ll_newrange(RANGE,start,stop)
            assert ll_rangelen(l, step) == length
            lst = [ll_rangeitem(dum_nocheck, l, i, step) for i in range(length)]
            assert lst == expected
            lst = [ll_rangeitem_nonneg(dum_nocheck, l, i, step) for i in range(length)]
            assert lst == expected
            lst = [ll_rangeitem(dum_nocheck, l, i-length, step) for i in range(length)]
            assert lst == expected

        for start in (-10, 0, 1, 10):
            for stop in (-8, 0, 4, 8, 25):
                for step in (1, 2, 3, -1, -2):
                    for varstep in False, True:
                        test1(start, stop, step, varstep)

    def test_range(self):
        def dummyfn(N):
            total = 0
            for i in range(N):
                total += i
            return total
        res = self.interpret(dummyfn, [10])
        assert res == 45

    def test_range_is_lazy(self):
        def dummyfn(N, M):
            total = 0
            for i in range(M):
                if i == N:
                    break
                total += i
            return total
        res = self.interpret(dummyfn, [10, 2147418112])
        assert res == 45

    def test_range_item(self):
        def dummyfn(start, stop, i):
            r = range(start, stop)
            return r[i]
        res = self.interpret(dummyfn, [10, 17, 4])
        assert res == 14
        res = self.interpret(dummyfn, [10, 17, -2])
        assert res == 15

    def test_xrange(self):
        def dummyfn(N):
            total = 0
            for i in xrange(N):
                total += i
            return total
        res = self.interpret(dummyfn, [10])
        assert res == 45

    def test_range_len(self):
        def dummyfn(start, stop):
            r = range(start, stop)
            return len(r)
        start, stop = 10, 17
        res = self.interpret(dummyfn, [start, stop])
        assert res == dummyfn(start, stop)

    def test_range2list(self):
        def dummyfn(start, stop):
            r = range(start, stop)
            r.reverse()
            return r[0]
        start, stop = 10, 17
        res = self.interpret(dummyfn, [start, stop])
        assert res == dummyfn(start, stop)

    def check_failed(self, func, *args):
        try:
            self.interpret(func, *args, **kwargs)
        except:
            return True
        else:
            return False

    def test_range_extra(self):
        def failingfn_const():
            r = range(10, 17, 0)
            return r[-1]
        assert self.check_failed(failingfn_const, [])

        def failingfn_var(step):
            r = range(10, 17, step)
            return r[-1]
        step = 3
        res = self.interpret(failingfn_var, [step])
        assert res == failingfn_var(step)
        step = 0
        assert self.check_failed(failingfn_var, [step])

    def test_range_iter(self):
        def fn(start, stop, step):
            res = 0
            if step == 0:
                if stop >= start:
                    r = range(start, stop, 1)
                else:
                    r = range(start, stop, -1)
            else:
                r = range(start, stop, step)
            for i in r:
                res = res * 51 + i
            return res
        for args in [2, 7, 0], [7, 2, 0], [10, 50, 7], [50, -10, -3]:
            res = self.interpret(fn, args)
            assert res == intmask(fn(*args))


class TestLLtype(BaseTestRrange, LLRtypeMixin):
    from pypy.rpython.lltypesystem import rrange 


class TestOOtype(BaseTestRrange, OORtypeMixin):
    from pypy.rpython.ootypesystem import rrange 
