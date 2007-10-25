# ----- mini.image productline -------------------------------
#       NOT relying on order of methods
#       using setup_module(module) now
import py
from pypy.lang.smalltalk import squeakimage
from pypy.lang.smalltalk import model
from pypy.lang.smalltalk import constants
from pypy.lang.smalltalk import interpreter

# lazy initialization of test data, ie ImageReader and Float class

def setup_module(module):
    global mini_image
    global reader
    global image
    mini_image = py.magic.autopath().dirpath().dirpath().join('mini.image')
    reader = open_miniimage()
    reader.initialize()
    image = squeakimage.SqueakImage()
    image.from_reader(get_reader())
    
def open_miniimage():
    return squeakimage.ImageReader(squeakimage.Stream(mini_image.open()))

def get_reader():
    return reader
    
def get_image():
    return image
    
def get_float_class():
    image = get_image()
    return image.special(constants.SO_FLOAT_CLASS)
     
# ------ tests ------------------------------------------
        
def test_miniimageexists():
    assert mini_image.check(dir=False)

def test_read_header():
    reader = open_miniimage()
    reader.read_header()
    assert reader.endofmemory == 0x93174
    assert reader.oldbaseaddress == 0x6649000
    assert reader.specialobjectspointer == 0x6668380

def test_read_all_header(): 
    reader = open_miniimage()
    reader.read_header()
    next = reader.stream.peek()
    assert next != 0 #expects object header, which must not be 0x00000000 
      
      
      
def test_number_of_objects():
    image = get_image()
    objects = image.objects
    assert len(objects) > 0
    assert 15000 < len(objects) < 16000 
    
def test_all_pointers_are_valid():
    reader = get_reader()
    for each in reader.chunks.itervalues():
        if each.format < 5: 
            for pointer in each.data:
                if (pointer & 1) != 1:
                    assert pointer in reader.chunks   
    
    
def test_there_are_31_compact_classes():
    reader = get_reader()
    assert len(reader.compactclasses) == 31
    
def test_invariant():
    image = get_image()
    for each in image.objects:
        each.invariant()
    
def test_float_class_size():
    w_float_class = get_float_class()
    assert w_float_class.size() == 9

def test_float_class_name():
    w_float_class = get_float_class()
    w_float_class_name = w_float_class.fetch(6)
    assert isinstance(w_float_class_name, model.W_BytesObject)
    assert w_float_class_name.bytes == list("Float")
    
def test_str_w_object():
    w_float_class = get_float_class()
    assert str(w_float_class) == "Float class"
    assert str(w_float_class.getclass()) == "a Metaclass" #yes, with article
    assert str(w_float_class.getclass().getclass()) == "Metaclass class"

def test_nil_true_false():
    image = get_image()
    w = image.special(constants.SO_NIL)
    assert str(w) == "a UndefinedObject" #yes, with article
    w = image.special(constants.SO_FALSE)
    assert str(w) == "a False" #yes, with article
    w = image.special(constants.SO_TRUE)
    assert str(w) == "a True" #yes, with article
    
def test_scheduler():
    image = get_image()
    w = image.special(constants.SO_SCHEDULERASSOCIATIONPOINTER)
    w0 = w.fetch(0)
    assert str(w0) == "'Processor'" 
    w0 = w.fetch(1)
    assert str(w0) == "a ProcessorScheduler" 
   
def test_special_classes0():
    image = get_image()
    w = image.special(constants.SO_BITMAP_CLASS)
    assert str(w) == "Bitmap class" 
    w = image.special(constants.SO_SMALLINTEGER_CLASS)
    assert str(w) == "SmallInteger class" 
    w = image.special(constants.SO_STRING_CLASS)
    assert str(w) == "String class" 
    w = image.special(constants.SO_ARRAY_CLASS)
    assert str(w) == "Array class" 
    w = image.special(constants.SO_FLOAT_CLASS)
    assert str(w) == "Float class" 
    w = image.special(constants.SO_METHODCONTEXT_CLASS)
    assert str(w) == "MethodContext class" 
    w = image.special(constants.SO_BLOCKCONTEXT_CLASS)
    assert str(w) == "BlockContext class" 
    w = image.special(constants.SO_POINT_CLASS)
    assert str(w) == "Point class" 
    w = image.special(constants.SO_LARGEPOSITIVEINTEGER_CLASS)
    assert str(w) == "LargePositiveInteger class" 

    # to be continued

    """SO_SMALLTALK = 8
     SO_DISPLAY_CLASS = 14
    SO_MESSAGE_CLASS = 15
    SO_COMPILEDMETHOD_CLASS = 16
    SO_LOW_SPACE_SEMAPHORE = 17
    SO_SEMAPHORE_CLASS = 18
    SO_CHARACTER_CLASS = 19
    SO_DOES_NOT_UNDERSTAND = 20
    SO_CANNOT_RETURN = 21
    # no clue what 22 is doing
    SO_SPECIAL_SELECTORS_ARRAY = 23
    SO_CHARACTER_TABLE_ARRAY = 24
    SO_MUST_BE_BOOLEAN = 25
    SO_BYTEARRAY_CLASS = 26
    SO_PROCESS_CLASS = 27
    SO_COMPACT_CLASSES_ARRAY = 28
    SO_DELAY_SEMAPHORE = 29
    SO_USER_INTERRUPT_SEMAPHORE = 30
    SO_FLOAT_ZERO = 31
    SO_LARGEPOSITIVEINTEGER_ZERO = 32
    SO_A_POINT = 33
    SO_CANNOT_INTERPRET = 34
    SO_A_METHODCONTEXT = 35
    # no clue what 36 is doing
    SO_A_BLOCKCONTEXT = 37
    SO_AN_ARRAY = 38
    SO_PSEUDOCONTEXT_CLASS = 39
    SO_TRANSLATEDMETHOD_CLASS = 40
    SO_FINALIZATION_SEMPAHORE = 41
    SO_LARGENEGATIVEINTEGER_CLASS = 42"""



def test_lookup_abs_in_integer(int=10):
    image = get_image()
    interp = interpreter.Interpreter()

    w_object = model.W_SmallInteger(int)

    # XXX
    # Should get this from w_object
    w_smallint_class = image.special(constants.SO_SMALLINTEGER_CLASS)
    w_method = w_smallint_class.lookup("abs")

    # XXX
    # currently still using highlevel lookup directly pointing to
    # class. Should work using classmirrors when the metaclass of
    # SmallInt is correctly set

    # s_class = w_object.shadow_of_my_class()
    # w_method = s_class.lookup("abs")

    assert w_method
    w_frame = w_method.createFrame(w_object, [])
    interp.w_active_context = w_frame

    print w_method

    while True:
        try:
            interp.step()
            print interp.w_active_context.stack
        except interpreter.ReturnFromTopLevel, e:
            return e.object

def test_lookup_neg_abs_in_integer():
    py.test.skip("TOFIX methodlookup 'negated' fails in shadow SmallInteger")
    # Fails due to same reason because of which
    # classmirror-methodlookup fails
    test_lookup_abs_in_integer(-3)

def test_map_mirrors_to_classtable():
    from pypy.lang.smalltalk import classtable, shadow, objtable
    w_compiledmethod_class = image.special(constants.SO_COMPILEDMETHOD_CLASS)
    assert w_compiledmethod_class is classtable.w_CompiledMethod
    w_nil = image.special(constants.SO_NIL)
    assert w_nil is objtable.w_nil
    w_true = image.special(constants.SO_TRUE)
    assert w_true is objtable.w_true
    w_false = image.special(constants.SO_FALSE)
    assert w_false is objtable.w_false
