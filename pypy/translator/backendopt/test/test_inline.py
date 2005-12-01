# XXX clean up these tests to use more uniform helpers
import py
import os
from pypy.objspace.flow.model import traverse, Block, Link, Variable, Constant
from pypy.objspace.flow.model import last_exception, checkgraph
from pypy.translator.backendopt.inline import inline_function, CannotInline
from pypy.translator.backendopt.inline import auto_inlining
from pypy.translator.backendopt.inline import collect_called_functions
from pypy.translator.backendopt.inline import measure_median_execution_cost
from pypy.translator.translator import Translator, TranslationContext, graphof
from pypy.rpython.llinterp import LLInterpreter
from pypy.rpython.rarithmetic import ovfcheck
from pypy.translator.test.snippet import is_perfect_number

def no_missing_concretetype(node):
    if isinstance(node, Block):
        for v in node.inputargs:
            assert hasattr(v, 'concretetype')
        for op in node.operations:
            for v in op.args:
                assert hasattr(v, 'concretetype')
            assert hasattr(op.result, 'concretetype')
    if isinstance(node, Link):
        if node.exitcase is not None:
            assert hasattr(node, 'llexitcase')
        for v in node.args:
            assert hasattr(v, 'concretetype')
        if isinstance(node.last_exception, (Variable, Constant)):
            assert hasattr(node.last_exception, 'concretetype')
        if isinstance(node.last_exc_value, (Variable, Constant)):
            assert hasattr(node.last_exc_value, 'concretetype')

def sanity_check(t):
    # look for missing '.concretetype'
    for graph in t.graphs:
        checkgraph(graph)
        traverse(no_missing_concretetype, graph)

def check_inline(func, in_func, sig):
    t = Translator(in_func)
    a = t.annotate(sig)
    a.simplify()
    t.specialize()
    # inline!
    sanity_check(t)    # also check before inlining (so we don't blame it)
    in_func_graph = graphof(t, in_func)
    func_graph = graphof(t, func)
    inline_function(t, func, in_func_graph)
    sanity_check(t)
    interp = LLInterpreter(t.rtyper)
    def eval_func(args):
        return interp.eval_graph(in_func_graph, args)
    return eval_func


def test_inline_simple():
    def f(x, y):
        return (g(x, y) + 1) * x
    def g(x, y):
        if x > 0:
            return x * y
        else:
            return -x * y
    eval_func = check_inline(g, f, [int, int])
    result = eval_func([-1, 5])
    assert result == f(-1, 5)
    result = eval_func([2, 12])
    assert result == f(2, 12)

def test_inline_big():
    def f(x):
        result = []
        for i in range(1, x+1):
            if is_perfect_number(i):
                result.append(i)
        return result
    eval_func = check_inline(is_perfect_number, f, [int])
    result = eval_func([10])
    assert result.length == len(f(10))

def test_inline_raising():
    def f(x):
        if x == 1:
            raise ValueError
        return x
    def g(x):
        a = f(x)
        if x == 2:
            raise KeyError
    def h(x):
        try:
            g(x)
        except ValueError:
            return 1
        except KeyError:
            return 2
        return x
    t = Translator(h)
    a = t.annotate([int])
    a.simplify()
    t.specialize()
    sanity_check(t)    # also check before inlining (so we don't blame it)
    inline_function(t, f, graphof(t, g))
    sanity_check(t)
    interp = LLInterpreter(t.rtyper)
    h_graph = graphof(t, h)
    result = interp.eval_graph(h_graph, [0])
    assert result == 0
    result = interp.eval_graph(h_graph, [1])
    assert result == 1
    result = interp.eval_graph(h_graph, [2])
    assert result == 2    

def test_inline_several_times():
    def f(x):
        return (x + 1) * 2
    def g(x):
        if x:
            a = f(x) + f(x)
        else:
            a = f(x) + 1
        return a + f(x)
    eval_func = check_inline(f, g, [int])
    result = eval_func([0])
    assert result == g(0)
    result = eval_func([42])
    assert result == g(42)

def test_inline_exceptions():
    def f(x):
        if x == 0:
            raise ValueError
        if x == 1:
            raise KeyError
    def g(x):
        try:
            f(x)
        except ValueError:
            return 2
        except KeyError:
            return x+2
        return 1
    eval_func = check_inline(f, g, [int])
    result = eval_func([0])
    assert result == 2
    result = eval_func([1])
    assert result == 3
    result = eval_func([42])
    assert result == 1

def test_inline_var_exception():
    def f(x):
        e = None
        if x == 0:
            e = ValueError()
        elif x == 1:
            e = KeyError()
        if x == 0 or x == 1:
            raise e
    def g(x):
        try:
            f(x)
        except ValueError:
            return 2
        except KeyError:
            return 3
        return 1
    t = Translator(g)
    a = t.annotate([int])
    a.simplify()
    t.specialize()
    auto_inlining(t, threshold=10)
    for graph in t.graphs:
        traverse(no_missing_concretetype, graph)
    interp = LLInterpreter(t.rtyper)
    g_graph = graphof(t, g)
    result = interp.eval_graph(g_graph, [0])
    assert result == 2
    result = interp.eval_graph(g_graph, [1])
    assert result == 3
    result = interp.eval_graph(g_graph, [42])
    assert result == 1

def test_inline_nonraising_into_catching():
    def f(x):
        return x+1
    def g(x):
        try:
            return f(x)
        except KeyError:
            return 42
    eval_func = check_inline(f, g, [int])
    result = eval_func([7654])
    assert result == 7655

def DONOTtest_call_call():
    # for reference.  Just remove this test if we decide not to support
    # catching exceptions while inlining a graph that contains further
    # direct_calls.
    def e(x):
        if x < 0:
            raise KeyError
        return x+1
    def f(x):
        return e(x)+2
    def g(x):
        try:
            return f(x)+3
        except KeyError:
            return -1
    t = Translator(g)
    a = t.annotate([int])
    a.simplify()
    t.specialize()
    sanity_check(t)    # also check before inlining (so we don't blame it)
    inline_function(t, f, t.flowgraphs[g])
    sanity_check(t)
    interp = LLInterpreter(t.flowgraphs, t.rtyper)
    result = interp.eval_function(g, [100])
    assert result == 106
    result = interp.eval_function(g, [-100])
    assert result == -1

def test_for_loop():
    def f(x):
        result = 0
        for i in range(0, x):
            result += i
        return result
    t = Translator(f)
    a = t.annotate([int])
    a.simplify()
    t.specialize()
    for graph in t.graphs:
        if graph.name.startswith('ll_rangenext'):
            break
    else:
        assert 0, "cannot find ll_rangenext_*() function"
    sanity_check(t)    # also check before inlining (so we don't blame it)
    inline_function(t, graph, graphof(t, f))
    sanity_check(t)
    interp = LLInterpreter(t.rtyper)
    result = interp.eval_graph(graphof(t, f), [10])
    assert result == 45

def test_inline_constructor():
    class A:
        def __init__(self, x, y):
            self.bounds = (x, y)
        def area(self, height=10):
            return height * (self.bounds[1] - self.bounds[0])
    def f(i):
        a = A(117, i)
        return a.area()
    eval_func = check_inline(A.__init__.im_func, f, [int])
    result = eval_func([120])
    assert result == 30

def test_cannot_inline_recursive_function():
    def factorial(n):
        if n > 1:
            return n * factorial(n-1)
        else:
            return 1
    def f(n):
        return factorial(n//2)
    py.test.raises(CannotInline, check_inline, factorial, f, [int])

def test_auto_inlining_small_call_big():
    def leaf(n):
        total = 0
        i = 0
        while i < n:
            total += i
            if total > 100:
                raise OverflowError
            i += 1
        return total
    def g(n):
        return leaf(n)
    def f(n):
        try:
            return g(n)
        except OverflowError:
            return -1
    t = Translator(f)
    a = t.annotate([int])
    a.simplify()
    t.specialize()
    auto_inlining(t, threshold=10)
    f_graph = graphof(t, f)
    assert len(collect_called_functions(f_graph)) == 0
    interp = LLInterpreter(t.rtyper)
    result = interp.eval_graph(f_graph, [10])
    assert result == 45
    result = interp.eval_graph(f_graph, [15])
    assert result == -1

def test_inline_exception_catching():
    def f3():
        raise KeyError
    def f2():
        try:
            f3()
        except KeyError:
            return True
        else:
            return False
    def f():
        return f2()
    eval_func = check_inline(f2, f, [])
    result = eval_func([])
    assert result is True

def test_inline_catching_different_exception():
    d = {1: 2}
    def f2(n):
        try:
            return ovfcheck(n+1)
        except OverflowError:
            raise
    def f(n):
        try:
            return f2(n)
        except ValueError:
            return -1
    eval_func = check_inline(f2, f, [int])
    result = eval_func([54])
    assert result == 55

def test_auto_inline_os_path_isdir():
    directory = "./."
    def f():
        return os.path.isdir(directory)
    t = Translator(f)
    a = t.annotate([])
    a.simplify()
    t.specialize()
    auto_inlining(t)
    interp = LLInterpreter(t.rtyper)
    result = interp.eval_graph(graphof(t, f), [])
    assert result is True

def test_inline_raiseonly():
    def f2(x):
        raise KeyError
    def f(x):
        try:
            return f2(x)
        except KeyError:
            return 42
    eval_func = check_inline(f2, f, [int])
    result = eval_func([98371])
    assert result == 42

def test_measure_median_execution_cost():
    def f(x):
        x += 1
        x += 1
        x += 1
        while True:
            x += 1
            x += 1
            x += 1
            if x: break
            x += 1
            x += 1
            x += 1
            x += 1
            x += 1
        x += 1
        return x
    t = TranslationContext()
    graph = t.buildflowgraph(f)
    res = measure_median_execution_cost(graph)
    assert res == 19
