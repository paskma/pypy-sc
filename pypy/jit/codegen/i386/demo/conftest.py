import py, random

Option = py.test.config.Option

option = py.test.config.addoptions("demo options",
        Option('--seed', action="store", type="int",
               default=random.randrange(0, 10000),
               dest="randomseed",
               help="choose a fixed random seed"),
        )