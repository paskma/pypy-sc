import path
from pypy.tool.build import client
import py
import time
from fake import FakeChannel, FakeServer

class ClientForTests(client.PPBClient):
    def __init__(self, *args, **kwargs):
        super(ClientForTests, self).__init__(*args, **kwargs)
        self._done = []
        
def setup_module(mod):
    mod.temp = temp = py.test.ensuretemp('pypybuilder-client')
    mod.svr = svr = FakeServer(temp)

    import pypy.tool.build
    pypy.tool.build.ppbserver = svr

    mod.c1c = c1c = FakeChannel()
    mod.c1 = c1 = ClientForTests(c1c, {'foo': 1, 'bar': [1,2]})
    svr.register(c1)

    mod.c2c = c2c = FakeChannel()
    mod.c2 = c2 = ClientForTests(c2c, {'foo': 2, 'bar': [2,3]})
    svr.register(c2)

def test_compile():
    info = ({'foo': 1}, {'bar': 2})
    c1c.send(True) # notifying we 'accept' the compile
    accepted = c1.compile(info)
    assert accepted
    ret = c1.channel.receive()
    assert ret == info # this was still in the buffer
    c1.channel.send('foo bar')
    c1.channel.send(None)

    # meanwhile the client starts a thread that waits until there's data 
    # available on its own channel, with our FakeChannel it has data rightaway,
    # though (the channel out and in are the same, and we just sent 'info'
    # over the out one)
    time.sleep(1)
    
    done = svr._done.pop()
    
    assert done[0] == info
    assert done[1] == (temp / 'build-0')

def test_channelwrapper():
    class FakeChannel(object):
        def __init__(self):
            self.buffer = []
        def send(self, data):
            self.buffer.append(data)
    c = FakeChannel()
    cw = client.ChannelWrapper(c)
    assert cw.tell() == 0
    cw.write('foo')
    cw.write('bar')
    assert cw.tell() == 6
    cw.write('baz')
    cw.close()
    assert c.buffer == ['foo', 'bar', 'baz', None]

def test_failed_checker():
    info = ({'foo': 1}, {'bar': 2})
    c1c.send(False) # notifying we _don't_ 'accept' the compile
    accepted = c1.compile(info)
    assert not accepted

