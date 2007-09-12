#! /usr/bin/env python

import os, py, sys
from pypy.rpython.lltypesystem import lltype
from pypy.rpython.lltypesystem import rffi
from pypy.rpython.lltypesystem import llmemory
from pypy.translator.tool.cbuild import build_executable
from pypy.tool.udir import udir
import distutils

# ____________________________________________________________
#
# Helpers for simple cases

def getstruct(name, c_header_source, interesting_fields):
    class CConfig:
        _header_ = c_header_source
        STRUCT = Struct(name, interesting_fields)
    return configure(CConfig)['STRUCT']

def getsimpletype(name, c_header_source, ctype_hint=rffi.INT):
    class CConfig:
        _header_ = c_header_source
        TYPE = SimpleType(name, ctype_hint)
    return configure(CConfig)['TYPE']

def getconstantinteger(name, c_header_source):
    class CConfig:
        _header_ = c_header_source
        CONST = ConstantInteger(name)
    return configure(CConfig)['CONST']

def getdefined(macro, c_header_source):
    class CConfig:
        _header_ = c_header_source
        DEFINED = Defined(macro)
    return configure(CConfig)['DEFINED']

def has(name, c_header_source):
    class CConfig:
        _header_ = c_header_source
        HAS = Has(name)
    return configure(CConfig)['HAS']

# ____________________________________________________________
#
# General interface

class ConfigResult:
    def __init__(self, CConfig, info, entries):
        self.CConfig = CConfig
        self.result = {}
        self.info = info
        self.entries = entries
        
    def get_entry_result(self, entry):
        try:
            return self.result[entry]
        except KeyError:
            pass
        name = self.entries[entry]
        info = self.info[name]
        self.result[entry] = entry.build_result(info, self)

    def get_result(self):
        return dict([(name, self.result[entry])
                     for entry, name in self.entries.iteritems()])

class _CWriter(object):
    """ A simple class which aggregates config parts
    """
    def __init__(self, CConfig):
        self.path = uniquefilepath()
        self.f = self.path.open("w")
        self.config = CConfig

    def write_header(self):
        f = self.f
        CConfig = self.config
        print >> f, C_HEADER
        print >> f
        for path in getattr(CConfig, '_includes_', ()):   # optional
            print >> f, '#include <%s>' % (path,)
        print >> f, getattr(CConfig, '_header_', '')      # optional
        print >> f

    def write_entry(self, key, entry):
        f = self.f
        print >> f, 'void dump_section_%s(void) {' % (key,)
        for line in entry.prepare_code():
            if line and line[0] != '#':
                line = '\t' + line
            print >> f, line
        print >> f, '}'
        print >> f

    def write_entry_main(self, key):
        print >> self.f, '\tprintf("-+- %s\\n");' % (key,)
        print >> self.f, '\tdump_section_%s();' % (key,)
        print >> self.f, '\tprintf("---\\n");'

    def start_main(self):
        print >> self.f, 'int main(int argc, char *argv[]) {'

    def close(self):
        f = self.f
        print >> f, '\treturn 0;'
        print >> f, '}'
        f.close()

    def ask_gcc(self, question):
        self.start_main()
        self.f.write(question + "\n")
        self.close()
        include_dirs = getattr(self.config, '_include_dirs_', [])
        build_executable([self.path], include_dirs=include_dirs)
        
def configure(CConfig):
    """Examine the local system by running the C compiler.
    The CConfig class contains CConfigEntry attribues that describe
    what should be inspected; configure() returns a dict mapping
    names to the results.
    """
    entries = []
    for key in dir(CConfig):
        value = getattr(CConfig, key)
        if isinstance(value, CConfigEntry):
            entries.append((key, value))            

    if entries:   # can be empty if there are only CConfigSingleEntries
        writer = _CWriter(CConfig)
        writer.write_header()
        for key, entry in entries:
            writer.write_entry(key, entry)

        f = writer.f
        writer.start_main()
        for key, entry in entries:
            writer.write_entry_main(key)
        writer.close()

        include_dirs = getattr(CConfig, '_include_dirs_', [])
        infolist = list(run_example_code(writer.path, include_dirs))
        assert len(infolist) == len(entries)

        resultinfo = {}
        resultentries = {}
        for info, (key, entry) in zip(infolist, entries):
            resultinfo[key] = info
            resultentries[entry] = key

        result = ConfigResult(CConfig, resultinfo, resultentries)
        for name, entry in entries:
            result.get_entry_result(entry)
        res = result.get_result()
    else:
        res = {}

    for key in dir(CConfig):
        value = getattr(CConfig, key)
        if isinstance(value, CConfigSingleEntry):
            writer = _CWriter(CConfig)
            writer.write_header()
            res[key] = value.question(writer.ask_gcc)

    return res

# ____________________________________________________________


class CConfigEntry(object):
    "Abstract base class."


class Struct(CConfigEntry):
    """An entry in a CConfig class that stands for an externally
    defined structure.
    """
    def __init__(self, name, interesting_fields, ifdef=None):
        self.name = name
        self.interesting_fields = interesting_fields
        self.ifdef = ifdef

    def prepare_code(self):
        if self.ifdef is not None:
            yield '#ifdef %s' % (self.ifdef,)
        yield 'typedef %s platcheck_t;' % (self.name,)
        yield 'typedef struct {'
        yield '    char c;'
        yield '    platcheck_t s;'
        yield '} platcheck2_t;'
        yield ''
        yield 'platcheck_t s;'
        if self.ifdef is not None:
            yield 'dump("defined", 1);'
        yield 'dump("align", offsetof(platcheck2_t, s));'
        yield 'dump("size",  sizeof(platcheck_t));'
        for fieldname, fieldtype in self.interesting_fields:
            yield 'dump("fldofs %s", offsetof(platcheck_t, %s));'%(
                fieldname, fieldname)
            yield 'dump("fldsize %s",   sizeof(s.%s));' % (
                fieldname, fieldname)
            if fieldtype in integer_class:
                yield 's.%s = 0; s.%s = ~s.%s;' % (fieldname,
                                                   fieldname,
                                                   fieldname)
                yield 'dump("fldunsigned %s", s.%s > 0);' % (fieldname,
                                                             fieldname)
        if self.ifdef is not None:
            yield '#else'
            yield 'dump("defined", 0);'
            yield '#endif'

    def build_result(self, info, config_result):
        if self.ifdef is not None:
            if not info['defined']:
                return None
        layout = [None] * info['size']
        for fieldname, fieldtype in self.interesting_fields:
            if isinstance(fieldtype, Struct):
                offset = info['fldofs '  + fieldname]
                size   = info['fldsize ' + fieldname]
                c_fieldtype = config_result.get_entry_result(fieldtype)
                layout_addfield(layout, offset, c_fieldtype, fieldname)
            else:
                offset = info['fldofs '  + fieldname]
                size   = info['fldsize ' + fieldname]
                sign   = info.get('fldunsigned ' + fieldname, False)
                if (size, sign) != rffi.size_and_sign(fieldtype):
                    fieldtype = fixup_ctype(fieldtype, fieldname, (size, sign))
                layout_addfield(layout, offset, fieldtype, fieldname)

        n = 0
        for i, cell in enumerate(layout):
            if cell is not None:
                continue
            layout_addfield(layout, i, rffi.UCHAR, '_pad%d' % (n,))
            n += 1

        # build the lltype Structure
        seen = {}
        fields = []
        for cell in layout:
            if cell in seen:
                continue
            fields.append((cell.name, cell.ctype))
            seen[cell] = True

        name = self.name
        if name.startswith('struct '):
            name = name[7:]
        kwds = {'hints':{'align':info['align'],
                         'size':info['size']}}
        return rffi.CStruct(name, *fields, **kwds)

class SimpleType(CConfigEntry):
    """An entry in a CConfig class that stands for an externally
    defined simple numeric type.
    """
    def __init__(self, name, ctype_hint=rffi.INT, ifdef=None):
        self.name = name
        self.ctype_hint = ctype_hint
        self.ifdef = ifdef
        
    def prepare_code(self):
        if self.ifdef is not None:
            yield '#ifdef %s' % (self.ifdef,)
        yield 'typedef %s platcheck_t;' % (self.name,)
        yield ''
        yield 'platcheck_t x;'
        if self.ifdef is not None:
            yield 'dump("defined", 1);'
        yield 'dump("size",  sizeof(platcheck_t));'
        if self.ctype_hint in integer_class:
            yield 'x = 0; x = ~x;'
            yield 'dump("unsigned", x > 0);'
        if self.ifdef is not None:
            yield '#else'
            yield 'dump("defined", 0);'
            yield '#endif'

    def build_result(self, info, config_result):
        if self.ifdef is not None and not info['defined']:
            return None
        size = info['size']
        sign = info.get('unsigned', False)
        ctype = self.ctype_hint
        if (size, sign) != rffi.size_and_sign(ctype):
            ctype = fixup_ctype(ctype, self.name, (size, sign))
        return ctype


class ConstantInteger(CConfigEntry):
    """An entry in a CConfig class that stands for an externally
    defined integer constant.
    """
    def __init__(self, name):
        self.name = name

    def prepare_code(self):
        yield 'if ((%s) < 0) {' % (self.name,)
        yield '    long long x = (long long)(%s);' % (self.name,)
        yield '    printf("value: %lld\\n", x);'
        yield '} else {'
        yield '    unsigned long long x = (unsigned long long)(%s);' % (
                        self.name,)
        yield '    printf("value: %llu\\n", x);'
        yield '}'

    def build_result(self, info, config_result):
        return info['value']

class DefinedConstantInteger(CConfigEntry):
    """An entry in a CConfig class that stands for an externally
    defined integer constant. If not #defined the value will be None.
    """
    def __init__(self, macro):
        self.name = self.macro = macro

    def prepare_code(self):
        yield '#ifdef %s' % self.macro
        yield 'dump("defined", 1);'
        yield 'if ((%s) < 0) {' % (self.macro,)
        yield '    long long x = (long long)(%s);' % (self.macro,)
        yield '    printf("value: %lld\\n", x);'
        yield '} else {'
        yield '    unsigned long long x = (unsigned long long)(%s);' % (
                        self.macro,)
        yield '    printf("value: %llu\\n", x);'
        yield '}'
        yield '#else'
        yield 'dump("defined", 0);'
        yield '#endif'

    def build_result(self, info, config_result):
        if info["defined"]:
            return info['value']
        return None


class DefinedConstantString(CConfigEntry):
    """
    """
    def __init__(self, macro):
        self.macro = macro
        self.name = macro

    def prepare_code(self):
        yield '#ifdef %s' % self.macro
        yield 'int i;'
        yield 'char *p = %s;' % self.macro
        yield 'dump("defined", 1);'
        yield 'for (i = 0; p[i] != 0; i++ ) {'
        yield '  printf("value_%d: %d\\n", i, (int)(unsigned char)p[i]);'
        yield '}'
        yield '#else'
        yield 'dump("defined", 0);'
        yield '#endif'

    def build_result(self, info, config_result):
        if info["defined"]:
            string = ''
            d = 0
            while info.has_key('value_%d' % d):
                string += chr(info['value_%d' % d])
                d += 1
            return string
        return None


class Defined(CConfigEntry):
    """A boolean, corresponding to an #ifdef.
    """
    def __init__(self, macro):
        self.macro = macro
        self.name = macro

    def prepare_code(self):
        yield '#ifdef %s' % (self.macro,)
        yield 'dump("defined", 1);'
        yield '#else'
        yield 'dump("defined", 0);'
        yield '#endif'

    def build_result(self, info, config_result):
        return bool(info['defined'])

class CConfigSingleEntry(object):
    """ An abstract class of type which requires
    gcc succeeding/failing instead of only asking
    """
    pass

class Has(CConfigSingleEntry):
    def __init__(self, name):
        self.name = name
    
    def question(self, ask_gcc):
        try:
            ask_gcc(self.name + ';')
            return True
        except distutils.errors.CompileError:
            return False

# ____________________________________________________________
#
# internal helpers

def uniquefilepath(LAST=[0]):
    i = LAST[0]
    LAST[0] += 1
    return udir.join('platcheck_%d.c' % i)

integer_class = [rffi.SIGNEDCHAR, rffi.UCHAR, rffi.CHAR,
                 rffi.SHORT, rffi.USHORT,
                 rffi.INT, rffi.UINT,
                 rffi.LONG, rffi.ULONG,
                 rffi.LONGLONG, rffi.ULONGLONG]
# XXX SIZE_T?

float_class = [rffi.DOUBLE]

def _sizeof(tp):
    if isinstance(tp, lltype.Struct):
        return sum([_sizeof(i) for i in tp._flds.values()])
    return rffi.sizeof(tp)

class Field(object):
    def __init__(self, name, ctype):
        self.name = name
        self.ctype = ctype
    def __repr__(self):
        return '<field %s: %s>' % (self.name, self.ctype)

def layout_addfield(layout, offset, ctype, prefix):
    size = _sizeof(ctype)
    name = prefix
    i = 0
    while name in layout:
        i += 1
        name = '%s_%d' % (prefix, i)
    field = Field(name, ctype)
    for i in range(offset, offset+size):
        assert layout[i] is None, "%s overlaps %r" % (fieldname, layout[i])
        layout[i] = field
    return field

def fixup_ctype(fieldtype, fieldname, expected_size_and_sign):
    for typeclass in [integer_class, float_class]:
        if fieldtype in typeclass:
            for ctype in typeclass:
                if rffi.size_and_sign(ctype) == expected_size_and_sign:
                    return ctype
    if isinstance(fieldtype, lltype.FixedSizeArray):
        size, _ = expected_size_and_sign
        return lltype.FixedSizeArray(fieldtype.OF, size/_sizeof(fieldtype.OF))
    raise TypeError("conflicting field type %r for %r" % (fieldtype,
                                                          fieldname))


C_HEADER = """
#include <stdio.h>
#include <stddef.h>   /* for offsetof() */

void dump(char* key, int value) {
    printf("%s: %d\\n", key, value);
}
"""

def run_example_code(filepath, include_dirs=[]):
    executable = build_executable([filepath], include_dirs=include_dirs)
    output = py.process.cmdexec(executable)
    section = None
    for line in output.splitlines():
        line = line.strip()
        if line.startswith('-+- '):      # start of a new section
            section = {}
        elif line == '---':              # section end
            assert section is not None
            yield section
            section = None
        elif line:
            assert section is not None
            key, value = line.split(': ')
            section[key] = int(value)

# ____________________________________________________________

def get_python_include_dir():
    from distutils import sysconfig
    gcv = sysconfig.get_config_vars()
    return gcv['INCLUDEPY']

if __name__ == '__main__':
    doc = """Example:
    
       rffi_platform.py  -h sys/types.h  -h netinet/in.h
                           'struct sockaddr_in'
                           sin_port  INT
    """
    import sys, getopt
    opts, args = getopt.gnu_getopt(sys.argv[1:], 'h:')
    if not args:
        print >> sys.stderr, doc
    else:
        assert len(args) % 2 == 1
        headers = []
        for opt, value in opts:
            if opt == '-h':
                headers.append('#include <%s>' % (value,))
        name = args[0]
        fields = []
        for i in range(1, len(args), 2):
            ctype = getattr(rffi, args[i+1])
            fields.append((args[i], ctype))

        S = getstruct(name, '\n'.join(headers), fields)

        for name in S._names:
            print name, getattr(S, name)