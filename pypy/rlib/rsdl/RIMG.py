from pypy.rpython.lltypesystem import lltype, rffi
from pypy.rpython.tool import rffi_platform as platform
from pypy.translator.tool.cbuild import ExternalCompilationInfo
from pypy.rlib.rsdl import RSDL

eci = ExternalCompilationInfo(
    includes=['SDL_image.h'],
    libraries=['SDL_image'],
    )
eci = eci.merge(RSDL.eci)

def external(name, args, result):
    return rffi.llexternal(name, args, result, compilation_info=eci)

Load = external('IMG_Load', [rffi.CCHARP], RSDL.SurfacePtr)
