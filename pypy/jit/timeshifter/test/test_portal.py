from pypy import conftest
from pypy.translator.translator import graphof
from pypy.jit.timeshifter.test.test_timeshift import hannotate
from pypy.jit.timeshifter.rtyper import HintRTyper
from pypy.rpython.llinterp import LLInterpreter
from pypy.objspace.flow.model import checkgraph

from pypy.rpython.objectmodel import hint


class TestPortal(object):
    from pypy.jit.codegen.llgraph.rgenop import RGenOp

    def setup_class(cls):
        cls._cache = {}
        cls._cache_order = []

    def teardown_class(cls):
        del cls._cache
        del cls._cache_order

    def timeshift_from_portal(self, main, portal, main_args,
                              inline=None, policy=None,
                              backendoptimize=False):

        key = main, portal, inline, policy, backendoptimize
        try:
            maingraph, rtyper = self._cache[key]
        except KeyError:
            if len(self._cache_order) >= 3:
                del self._cache[self._cache_order.pop(0)]

            hs, ha, rtyper = hannotate(main, main_args, portal=portal,
                                       policy=policy, inline=inline,
                                       backendoptimize=backendoptimize)

            # make the timeshifted graphs
            hrtyper = HintRTyper(ha, rtyper, self.RGenOp)
            t = rtyper.annotator.translator
            origportalgraph = graphof(t, portal)
            hrtyper.specialize(origportalgraph=origportalgraph,
                               view = conftest.option.view)

            for graph in ha.translator.graphs:
                checkgraph(graph)
                t.graphs.append(graph)

            if conftest.option.view:
                t.view()
            maingraph = graphof(t, main)
            self._cache[key] = maingraph, rtyper
            self._cache_order.append(key)

        llinterp = LLInterpreter(rtyper)
        return llinterp.eval_graph(maingraph, main_args)

    def test_simple(self):

        def main(code, x):
            return evaluate(code, x)

        def evaluate(y, x):
            hint(y, concrete=True)
            z = y+x
            return z

        res = self.timeshift_from_portal(main, evaluate, [3, 2])
        assert res == 5

        res = self.timeshift_from_portal(main, evaluate, [3, 5])
        assert res == 8

        res = self.timeshift_from_portal(main, evaluate, [4, 7])
        assert res == 11
    
