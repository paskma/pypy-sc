import autopath
import py, os
from pypy.config.config import OptionDescription, BoolOption, IntOption, ArbitraryOption, FloatOption
from pypy.config.config import ChoiceOption, StrOption, to_optparse, Config
from pypy.config.config import ConfigError

DEFL_INLINE_THRESHOLD = 32.4    # just enough to inline add__Int_Int()
# and just small enough to prevend inlining of some rlist functions.

DEFL_PROF_BASED_INLINE_THRESHOLD = 32.4
DEFL_CLEVER_MALLOC_REMOVAL_INLINE_THRESHOLD = 32.4
DEFL_LOW_INLINE_THRESHOLD = DEFL_INLINE_THRESHOLD / 2.0

translation_optiondescription = OptionDescription(
        "translation", "Translation Options", [
    BoolOption("stackless", "enable stackless features during compilation",
               default=False, cmdline="--stackless",
               requires=[("translation.type_system", "lltype")]),
    ChoiceOption("type_system", "Type system to use when RTyping",
                 ["lltype", "ootype"], cmdline=None, default="lltype",
                 requires={
                     "ootype": [
                                ("translation.backendopt.constfold", False),
                                ("translation.backendopt.heap2stack", False),
                                ("translation.backendopt.clever_malloc_removal", False),
                                ("translation.list_comprehension_operations", False),
                                ]
                     }),
    ChoiceOption("backend", "Backend to use for code generation",
                 ["c", "llvm", "cli", "jvm", "js"], default="c",
                 requires={
                     "c":      [("translation.type_system", "lltype")],
                     "llvm":   [("translation.type_system", "lltype"),
                                ("translation.backendopt.raisingop2direct_call", True),
                                ],
                     "cli":    [("translation.type_system", "ootype")],
                     "jvm":    [("translation.type_system", "ootype")],
                     "js":     [("translation.type_system", "ootype")],
                     },
                 cmdline="-b --backend"),
    BoolOption("llvm_via_c", "compile llvm via C",
               default=False, cmdline="--llvm-via-c",
               requires=[("translation.backend", "llvm")]),

    # gc
    ChoiceOption("gc", "Garbage Collection Strategy",
                 ["boehm", "ref", "marksweep", "semispace", "statistics",
                  "generation", "hybrid", "none"],
                  "ref", requires={
                     "ref": [("translation.rweakref", False), # XXX
                             ("translation.gctransformer", "ref")],
                     "none": [("translation.rweakref", False), # XXX
                             ("translation.gctransformer", "none")],
                     "semispace": [("translation.gctransformer", "framework")],
                     "marksweep": [("translation.gctransformer", "framework")],
                     "statistics": [("translation.gctransformer", "framework")],
                     "generation": [("translation.gctransformer", "framework")],
                     "hybrid": [("translation.gctransformer", "framework")],
                     "boehm": [("translation.gctransformer", "boehm")],
                     },
                  cmdline="--gc"),
    ChoiceOption("gctransformer", "GC transformer that is used - internal",
                 ["boehm", "ref", "framework", "none"],
                 default="ref", cmdline=None,
                 requires={
                     "boehm": [("translation.gcrootfinder", "n/a")],
                     "ref": [("translation.gcrootfinder", "n/a")],
                     "none": [("translation.gcrootfinder", "n/a")],
                 }),
    ChoiceOption("gcrootfinder",
                 "Strategy for finding GC Roots (framework GCs only)",
                 ["n/a", "shadowstack", "llvmgc", "asmgcc"],
                 "shadowstack",
                 cmdline="--gcrootfinder",
                 requires={
                     "shadowstack": [("translation.gctransformer", "framework")],
                     "llvmgc": [("translation.gctransformer", "framework"),
                                ("translation.backend", "llvm"),
                                ("translation.thread", False)],
                     "asmgcc": [("translation.gctransformer", "framework"),
                                ("translation.backend", "c"),
                                ("translation.thread", False)],
                    },
                 suggests={
                     "shadowstack": [("translation.gc", "generation")],
                     "llvmgc": [("translation.gc", "generation")],
                     "asmgcc": [("translation.gc", "generation")],
                 }),

    # other noticeable options
    BoolOption("thread", "enable use of threading primitives",
               default=False, cmdline="--thread"),
    BoolOption("sandbox", "Produce a fully-sandboxed executable",
               default=False, cmdline="--sandbox",
               requires=[("translation.thread", False)]),
    BoolOption("rweakref", "The backend supports RPython-level weakrefs",
               default=True),

    # misc
    BoolOption("verbose", "Print extra information", default=False),
    BoolOption("debug", "Record extra annotation information",
               cmdline="-d --debug", default=True),
    BoolOption("insist", "Try hard to go on RTyping", default=False,
               cmdline="--insist"),
    StrOption("cc", "Specify compiler to use for compiling generated C", cmdline="--cc"),
    StrOption("profopt", "Specify profile based optimization script",
              cmdline="--profopt"),
    BoolOption("noprofopt", "Don't use profile based optimization",
               default=False, cmdline="--no-profopt", negation=False),
    BoolOption("instrument", "internal: turn instrumentation on",
               default=False, cmdline=None),
    BoolOption("countmallocs", "Count mallocs and frees", default=False,
               cmdline=None),
    ChoiceOption("fork_before",
                 "(UNIX) Create restartable checkpoint before step",
                 ["annotate", "rtype", "backendopt", "database", "source",
                  "hintannotate", "timeshift"],
                 default=None, cmdline="--fork-before"),

    ArbitraryOption("instrumentctl", "internal",
               default=None),
    StrOption("output", "Output file name", cmdline="--output"),

    # portability options
    BoolOption("vanilla",
               "Try to be as portable as possible, which is not much",
               default=False,
               cmdline="--vanilla",
               requires=[("translation.no__thread", True)]),
    BoolOption("no__thread",
               "don't use __thread for implementing TLS",
               default=False, cmdline="--no__thread", negation=False),
    StrOption("compilerflags", "Specify flags for the C compiler",
               cmdline="--cflags"),
    StrOption("linkerflags", "Specify flags for the linker (C backend only)",
               cmdline="--ldflags"),

    # Flags of the TranslationContext:
    BoolOption("simplifying", "Simplify flow graphs", default=True),
    BoolOption("builtins_can_raise_exceptions",
               "When true, assume any call to a 'simple' builtin such as "
               "'hex' can raise an arbitrary exception",
               default=False,
               cmdline=None),
    BoolOption("list_comprehension_operations",
               "When true, look for and special-case the sequence of "
               "operations that results from a list comprehension and "
               "attempt to pre-allocate the list",
               default=False,
               cmdline='--listcompr'),
    IntOption("withsmallfuncsets",
              "Represent groups of less funtions than this as indices into an array",
               default=0),

    # options for ootype
    OptionDescription("ootype", "Object Oriented Typesystem options", [
        BoolOption("mangle", "Mangle names of class members", default=True),
    ]),

    OptionDescription("backendopt", "Backend Optimization Options", [
        # control inlining
        BoolOption("inline", "Do basic inlining and malloc removal",
                   default=True),
        FloatOption("inline_threshold", "Threshold when to inline functions",
                  default=DEFL_INLINE_THRESHOLD, cmdline="--inline-threshold"),
        StrOption("inline_heuristic", "Dotted name of an heuristic function "
                  "for inlining",
                default="pypy.translator.backendopt.inline.inlining_heuristic",
                cmdline="--inline-heuristic"),

        BoolOption("print_statistics", "Print statistics while optimizing",
                   default=False),
        BoolOption("merge_if_blocks", "Merge if ... elif chains",
                   cmdline="--if-block-merge", default=True),
        BoolOption("raisingop2direct_call",
                   "Transform operations that can implicitly raise an "
                   "exception into calls to functions that explicitly "
                   "raise exceptions",
                   default=False, cmdline="--raisingop2direct_call"),
        BoolOption("mallocs", "Remove mallocs", default=True),
        BoolOption("constfold", "Constant propagation",
                   default=True),
        BoolOption("heap2stack", "Escape analysis and stack allocation",
                   default=False,
                   requires=[("translation.stackless", False)]),
        # control profile based inlining
        StrOption("profile_based_inline",
                  "Use call count profiling to drive inlining"
                  ", specify arguments",
                  default=None, cmdline="--prof-based-inline"),
        FloatOption("profile_based_inline_threshold",
                    "Threshold when to inline functions "
                    "for profile based inlining",
                  default=DEFL_PROF_BASED_INLINE_THRESHOLD,
                  cmdline="--prof-based-inline-threshold"),
        StrOption("profile_based_inline_heuristic",
                  "Dotted name of an heuristic function "
                  "for profile based inlining",
                default="pypy.translator.backendopt.inline.inlining_heuristic",
                cmdline="--prof-based-inline-heuristic"),
        # control clever malloc removal
        BoolOption("clever_malloc_removal",
                   "Drives inlining to remove mallocs in a clever way",
                   default=False,
                   cmdline="--clever-malloc-removal"),
        FloatOption("clever_malloc_removal_threshold",
                    "Threshold when to inline functions in "
                    "clever malloc removal",
                  default=DEFL_CLEVER_MALLOC_REMOVAL_INLINE_THRESHOLD,
                  cmdline="--clever-malloc-removal-threshold"),
        StrOption("clever_malloc_removal_heuristic",
                  "Dotted name of an heuristic function "
                  "for inlining in clever malloc removal",
                default="pypy.translator.backendopt.inline.inlining_heuristic",
                cmdline="--clever-malloc-removal-heuristic"),

        BoolOption("remove_asserts",
                   "Remove operations that look like 'raise AssertionError', "
                   "which lets the C optimizer remove the asserts",
                   default=False),

        BoolOption("stack_optimization",
                   "Tranform graphs in SSI form into graphs tailored for "
                   "stack based virtual machines (only for backends that support it)",
                   default=True),

        BoolOption("none",
                   "Do not run any backend optimizations",
                   requires=[('translation.backendopt.inline', False),
                             ('translation.backendopt.inline_threshold', 0),
                             ('translation.backendopt.merge_if_blocks', False),
                             ('translation.backendopt.mallocs', False),
                             ('translation.backendopt.constfold', False)]),

       BoolOption("simplify_disabled",
                  "After rtyping, graph simplifications are disabled",
                  default=False),
    ]),

    OptionDescription("llvm", "GenLLVM options", [
        BoolOption("debug", "Include the llops in the source as comments", default=False),
        BoolOption("logging", "Log how long the various parts of llvm generation take", default=False),
        BoolOption("isolate", "Perform an isolated import", default=True),
        StrOption("opt_options", "Options passed to opt (influences level of optimization in LLVM)",
                     default="-std-compile-opts"),
    ]),

    OptionDescription("cli", "GenCLI options", [
        BoolOption("trace_calls", "Trace function calls", default=False,
                   cmdline="--cli-trace-calls"),
        BoolOption("exception_transformer", "Use exception transformer", default=False),
    ]),
])

def get_combined_translation_config(other_optdescr=None,
                                    existing_config=None,
                                    overrides=None,
                                    translating=False):
    if overrides is None:
        overrides = {}
    d = BoolOption("translating",
                   "indicates whether we are translating currently",
                   default=False, cmdline=None)
    if other_optdescr is None:
        children = []
        newname = ""
    else:
        children = [other_optdescr]
        newname = other_optdescr._name
    if existing_config is None:
        children += [d, translation_optiondescription]
    else:
        children += [child for child in existing_config._cfgimpl_descr._children
                         if child._name != newname]
    descr = OptionDescription("pypy", "all options", children)
    config = Config(descr, **overrides)
    if translating:
        config.translating = True
    if existing_config is not None:
        for child in existing_config._cfgimpl_descr._children:
            if child._name == newname:
                continue
            value = getattr(existing_config, child._name)
            config._cfgimpl_values[child._name] = value
    return config

# ____________________________________________________________

OPT_LEVELS = ['0', '1', 'size', 'mem', '2', '3']
DEFAULT_OPT_LEVEL = '2'

OPT_TABLE_DOC = {
    '0':    'No optimization.  Uses the Boehm GC.',
    '1':    'Enable a default set of optimizations.  Uses the Boehm GC.',
    'size': 'Optimize for the size of the executable.  Uses the Boehm GC.',
    'mem':  'Optimize for run-time memory usage and use a memory-saving GC.',
    '2':    'Enable most optimizations and use a high-performance GC.',
    '3':    'Enable all optimizations and use a high-performance GC.',
    }

OPT_TABLE = {
    #level:  gc          backend optimizations...
    '0':    'boehm       nobackendopt',
    '1':    'boehm       lowinline',
    'size': 'boehm       lowinline     remove_asserts',
    'mem':  'marksweep   lowinline     remove_asserts',
    '2':    'hybrid      extraopts',
    '3':    'hybrid      extraopts     remove_asserts',
    }

def set_opt_level(config, level):
    """Apply optimization suggestions on the 'config'.
    The optimizations depend on the selected level and possibly on the backend.
    """
    # warning: during some tests, the type_system and the backend may be
    # unspecified and we get None.  It shouldn't occur in translate.py though.
    type_system = config.translation.type_system
    backend = config.translation.backend

    try:
        opts = OPT_TABLE[level]
    except KeyError:
        raise ConfigError("no such optimization level: %r" % (level,))
    words = opts.split()
    gc = words.pop(0)

    # set the GC (only meaningful with lltype)
    config.translation.suggest(gc=gc)

    # set the backendopts
    for word in words:
        if word == 'nobackendopt':
            config.translation.backendopt.suggest(none=True)
        elif word == 'lowinline':
            config.translation.backendopt.suggest(inline_threshold=
                                                DEFL_LOW_INLINE_THRESHOLD)
        elif word == 'remove_asserts':
            config.translation.backendopt.suggest(remove_asserts=True)
        elif word == 'extraopts':
            config.translation.suggest(withsmallfuncsets=5)
            config.translation.suggest(list_comprehension_operations=True)
        else:
            raise ValueError(word)

# ----------------------------------------------------------------

PLATFORMS = [
    'host',
    'maemo',
]

def set_platform(config, platform):
    if platform == 'maemo':
        from pypy.translator.tool.cbuild import ExternalCompilationInfo
        # XXX evil hackery
        func_defs = list(ExternalCompilationInfo.__init__.func_defaults)
        func_defs[-1] = 'maemo'
        ExternalCompilationInfo.__init__.im_func.func_defaults = tuple(func_defs)
        
