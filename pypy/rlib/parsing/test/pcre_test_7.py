# Auto-generated file of regular expressions from PCRE library

# The PCRE library is distributed under the BSD license. We have borrowed some
# of the regression tests (the ones that fit under the DFA scope) in order to
# exercise our regex implementation. Those tests are distributed under PCRE's
# BSD license. Here is the text:

#        PCRE LICENCE
#        ------------
#        
#        PCRE is a library of functions to support regular expressions whose syntax
#        and semantics are as close as possible to those of the Perl 5 language.
#
#        Release 7 of PCRE is distributed under the terms of the "BSD" licence, as
#        specified below. The documentation for PCRE, supplied in the "doc"
#        directory, is distributed under the same terms as the software itself.
#        
#        The basic library functions are written in C and are freestanding. Also
#        included in the distribution is a set of C++ wrapper functions.
#        
#        THE BASIC LIBRARY FUNCTIONS
#        ---------------------------
#        
#        Written by:       Philip Hazel
#        Email local part: ph10
#        Email domain:     cam.ac.uk
#        
#        University of Cambridge Computing Service,
#        Cambridge, England.
#        
#        Copyright (c) 1997-2008 University of Cambridge
#        All rights reserved.
#        
#        THE C++ WRAPPER FUNCTIONS
#        -------------------------
#        
#        Contributed by:   Google Inc.
#        
#        Copyright (c) 2007-2008, Google Inc.
#        All rights reserved.
#        
#        THE "BSD" LICENCE
#        -----------------
#        
#        Redistribution and use in source and binary forms, with or without
#        modification, are permitted provided that the following conditions are met:
#        
#            * Redistributions of source code must retain the above copyright notice,
#              this list of conditions and the following disclaimer.
#        
#            * Redistributions in binary form must reproduce the above copyright
#              notice, this list of conditions and the following disclaimer in the
#              documentation and/or other materials provided with the distribution.
#        
#            * Neither the name of the University of Cambridge nor the name of Google
#              Inc. nor the names of their contributors may be used to endorse or
#              promote products derived from this software without specific prior
#              written permission.
#        
#        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#        AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#        IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#        ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
#        LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#        CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#        SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#        INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#        CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#        ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#        POSSIBILITY OF SUCH DAMAGE.
#        
#        End

suite = []
suite.append(['abc', '', [('abc', ' 0: abc')]])
suite.append(['ab*c', '', [('abc', ' 0: abc'), ('abbbbc', ' 0: abbbbc'), ('ac', ' 0: ac')]])
suite.append(['ab+c', '', [('abc', ' 0: abc'), ('abbbbbbc', ' 0: abbbbbbc'), ('*** Failers', None), ('ac', None), ('ab', None)]])
suite.append(['a*', '', [('a', ' 0: a'), ('aaaaaaaaaaaaaaaaa', ' 0: aaaaaaaaaaaaaaaaa'), ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', ' 0: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')]])
suite.append(['(a|abcd|african)', '', [('a', ' 0: a'), ('abcd', ' 0: abcd'), ('african', ' 0: african')]])
suite.append(['^abc', '', [('abcdef', ' 0: abc'), ('*** Failers', None), ('xyzabc', None), ('xyz\nabc', None)]])
suite.append(['x\\dy\\Dz', '', [('x9yzz', ' 0: x9yzz'), ('x0y+z', ' 0: x0y+z'), ('*** Failers', None), ('xyz', None), ('xxy0z', None)]])
suite.append(['x\\sy\\Sz', '', [('x yzz', ' 0: x yzz'), ('x y+z', ' 0: x y+z'), ('*** Failers', None), ('xyz', None), ('xxyyz', None)]])
suite.append(['x\\wy\\Wz', '', [('xxy+z', ' 0: xxy+z'), ('*** Failers', None), ('xxy0z', None), ('x+y+z', None)]])
suite.append(['x.y', '', [('x+y', ' 0: x+y'), ('x-y', ' 0: x-y'), ('*** Failers', None), ('x\ny', None)]])
suite.append(['a\\d$', '', [('ba0', ' 0: a0'), ('ba0\n', ' 0: a0'), ('*** Failers', None), ('ba0\ncd', None)]])
suite.append(['[^a]', '', [('abcd', ' 0: b')]])
suite.append(['ab?\\w', '', [('abz', ' 0: abz'), ('abbz', ' 0: abb'), ('azz', ' 0: az')]])
suite.append(['x{0,3}yz', '', [('ayzq', ' 0: yz'), ('axyzq', ' 0: xyz'), ('axxyz', ' 0: xxyz'), ('axxxyzq', ' 0: xxxyz'), ('axxxxyzq', ' 0: xxxyz'), ('*** Failers', None), ('ax', None), ('axx', None)]])
suite.append(['x{3}yz', '', [('axxxyzq', ' 0: xxxyz'), ('axxxxyzq', ' 0: xxxyz'), ('*** Failers', None), ('ax', None), ('axx', None), ('ayzq', None), ('axyzq', None), ('axxyz', None)]])
suite.append(['x{2,3}yz', '', [('axxyz', ' 0: xxyz'), ('axxxyzq', ' 0: xxxyz'), ('axxxxyzq', ' 0: xxxyz'), ('*** Failers', None), ('ax', None), ('axx', None), ('ayzq', None), ('axyzq', None)]])
suite.append(['[^a]+', '', [('bac', ' 0: b'), ('bcdefax', ' 0: bcdef'), ('*** Failers', ' 0: *** F'), ('aaaaa', None)]])
suite.append(['[^a]*', '', [('bac', ' 0: b'), ('bcdefax', ' 0: bcdef'), ('*** Failers', ' 0: *** F'), ('aaaaa', ' 0: ')]])
suite.append(['[^a]{3,5}', '', [('xyz', ' 0: xyz'), ('awxyza', ' 0: wxyz'), ('abcdefa', ' 0: bcdef'), ('abcdefghijk', ' 0: bcdef'), ('*** Failers', ' 0: *** F'), ('axya', None), ('axa', None), ('aaaaa', None)]])
suite.append(['\\d*', '', [('1234b567', ' 0: 1234'), ('xyz', ' 0: ')]])
suite.append(['\\D*', '', [('a1234b567', ' 0: a'), ('xyz', ' 0: xyz')]])
suite.append(['\\d+', '', [('ab1234c56', ' 0: 1234'), ('*** Failers', None), ('xyz', None)]])
suite.append(['\\D+', '', [('ab123c56', ' 0: ab'), ('*** Failers', ' 0: *** Failers'), ('789', None)]])
suite.append(['\\d?A', '', [('045ABC', ' 0: 5A'), ('ABC', ' 0: A'), ('*** Failers', None), ('XYZ', None)]])
suite.append(['\\D?A', '', [('ABC', ' 0: A'), ('BAC', ' 0: BA'), ('9ABC', ' 0: A'), ('*** Failers', None)]])
suite.append(['a+', '', [('aaaa', ' 0: aaaa')]])
suite.append(['^.*xyz', '', [('xyz', ' 0: xyz'), ('ggggggggxyz', ' 0: ggggggggxyz')]])
suite.append(['^.+xyz', '', [('abcdxyz', ' 0: abcdxyz'), ('axyz', ' 0: axyz'), ('*** Failers', None), ('xyz', None)]])
suite.append(['^.?xyz', '', [('xyz', ' 0: xyz'), ('cxyz', ' 0: cxyz')]])
suite.append(['^\\d{2,3}X', '', [('12X', ' 0: 12X'), ('123X', ' 0: 123X'), ('*** Failers', None), ('X', None), ('1X', None), ('1234X', None)]])
suite.append(['^[abcd]\\d', '', [('a45', ' 0: a4'), ('b93', ' 0: b9'), ('c99z', ' 0: c9'), ('d04', ' 0: d0'), ('*** Failers', None), ('e45', None), ('abcd', None), ('abcd1234', None), ('1234', None)]])
suite.append(['^[abcd]*\\d', '', [('a45', ' 0: a4'), ('b93', ' 0: b9'), ('c99z', ' 0: c9'), ('d04', ' 0: d0'), ('abcd1234', ' 0: abcd1'), ('1234', ' 0: 1'), ('*** Failers', None), ('e45', None), ('abcd', None)]])
suite.append(['^[abcd]+\\d', '', [('a45', ' 0: a4'), ('b93', ' 0: b9'), ('c99z', ' 0: c9'), ('d04', ' 0: d0'), ('abcd1234', ' 0: abcd1'), ('*** Failers', None), ('1234', None), ('e45', None), ('abcd', None)]])
suite.append(['^a+X', '', [('aX', ' 0: aX'), ('aaX', ' 0: aaX')]])
suite.append(['^[abcd]?\\d', '', [('a45', ' 0: a4'), ('b93', ' 0: b9'), ('c99z', ' 0: c9'), ('d04', ' 0: d0'), ('1234', ' 0: 1'), ('*** Failers', None), ('abcd1234', None), ('e45', None)]])
suite.append(['^[abcd]{2,3}\\d', '', [('ab45', ' 0: ab4'), ('bcd93', ' 0: bcd9'), ('*** Failers', None), ('1234', None), ('a36', None), ('abcd1234', None), ('ee45', None)]])
suite.append(['^(abc)*\\d', '', [('abc45', ' 0: abc4'), ('abcabcabc45', ' 0: abcabcabc4'), ('42xyz', ' 0: 4'), ('*** Failers', None)]])
suite.append(['^(abc)+\\d', '', [('abc45', ' 0: abc4'), ('abcabcabc45', ' 0: abcabcabc4'), ('*** Failers', None), ('42xyz', None)]])
suite.append(['^(abc)?\\d', '', [('abc45', ' 0: abc4'), ('42xyz', ' 0: 4'), ('*** Failers', None), ('abcabcabc45', None)]])
suite.append(['^(abc){2,3}\\d', '', [('abcabc45', ' 0: abcabc4'), ('abcabcabc45', ' 0: abcabcabc4'), ('*** Failers', None), ('abcabcabcabc45', None), ('abc45', None), ('42xyz', None)]])
suite.append(['^(a*\\w|ab)=(a*\\w|ab)', '', [('ab=ab', ' 0: ab=ab')]])
suite.append(['^abc', '', [('abcdef', ' 0: abc'), ('*** Failers', None)]])
suite.append(['^(a*|xyz)', '', [('bcd', ' 0: '), ('aaabcd', ' 0: aaa'), ('xyz', ' 0: xyz'), ('*** Failers', ' 0: ')]])
suite.append(['xyz$', '', [('xyz', ' 0: xyz'), ('xyz\n', ' 0: xyz'), ('*** Failers', None)]])
suite.append(['^abcdef', '', [('*** Failers', None)]])
suite.append(['^a{2,4}\\d+z', '', [('*** Failers', None)]])
suite.append(['^abcdef', '', []])
suite.append(['(ab*(cd|ef))+X', '', []])
suite.append(['the quick brown fox', '', [('the quick brown fox', ' 0: the quick brown fox'), ('The quick brown FOX', None), ('What do you know about the quick brown fox?', ' 0: the quick brown fox'), ('What do you know about THE QUICK BROWN FOX?', None)]])
suite.append(['abcd\\t\\n\\r\\f\\a\\e\\071\\x3b\\$\\\\\\?caxyz', '', [('abcd\t\n\r\x0c\x07\x1b9;$\\?caxyz', ' 0: abcd\t\n\r\x0c\x07\x1b9;$\\?caxyz')]])
suite.append(['a*abc?xyz+pqr{3}ab{2,}xy{4,5}pq{0,6}AB{0,}zz', '', [('abxyzpqrrrabbxyyyypqAzz', ' 0: abxyzpqrrrabbxyyyypqAzz'), ('abxyzpqrrrabbxyyyypqAzz', ' 0: abxyzpqrrrabbxyyyypqAzz'), ('aabxyzpqrrrabbxyyyypqAzz', ' 0: aabxyzpqrrrabbxyyyypqAzz'), ('aaabxyzpqrrrabbxyyyypqAzz', ' 0: aaabxyzpqrrrabbxyyyypqAzz'), ('aaaabxyzpqrrrabbxyyyypqAzz', ' 0: aaaabxyzpqrrrabbxyyyypqAzz'), ('abcxyzpqrrrabbxyyyypqAzz', ' 0: abcxyzpqrrrabbxyyyypqAzz'), ('aabcxyzpqrrrabbxyyyypqAzz', ' 0: aabcxyzpqrrrabbxyyyypqAzz'), ('aaabcxyzpqrrrabbxyyyypAzz', ' 0: aaabcxyzpqrrrabbxyyyypAzz'), ('aaabcxyzpqrrrabbxyyyypqAzz', ' 0: aaabcxyzpqrrrabbxyyyypqAzz'), ('aaabcxyzpqrrrabbxyyyypqqAzz', ' 0: aaabcxyzpqrrrabbxyyyypqqAzz'), ('aaabcxyzpqrrrabbxyyyypqqqAzz', ' 0: aaabcxyzpqrrrabbxyyyypqqqAzz'), ('aaabcxyzpqrrrabbxyyyypqqqqAzz', ' 0: aaabcxyzpqrrrabbxyyyypqqqqAzz'), ('aaabcxyzpqrrrabbxyyyypqqqqqAzz', ' 0: aaabcxyzpqrrrabbxyyyypqqqqqAzz'), ('aaabcxyzpqrrrabbxyyyypqqqqqqAzz', ' 0: aaabcxyzpqrrrabbxyyyypqqqqqqAzz'), ('aaaabcxyzpqrrrabbxyyyypqAzz', ' 0: aaaabcxyzpqrrrabbxyyyypqAzz'), ('abxyzzpqrrrabbxyyyypqAzz', ' 0: abxyzzpqrrrabbxyyyypqAzz'), ('aabxyzzzpqrrrabbxyyyypqAzz', ' 0: aabxyzzzpqrrrabbxyyyypqAzz'), ('aaabxyzzzzpqrrrabbxyyyypqAzz', ' 0: aaabxyzzzzpqrrrabbxyyyypqAzz'), ('aaaabxyzzzzpqrrrabbxyyyypqAzz', ' 0: aaaabxyzzzzpqrrrabbxyyyypqAzz'), ('abcxyzzpqrrrabbxyyyypqAzz', ' 0: abcxyzzpqrrrabbxyyyypqAzz'), ('aabcxyzzzpqrrrabbxyyyypqAzz', ' 0: aabcxyzzzpqrrrabbxyyyypqAzz'), ('aaabcxyzzzzpqrrrabbxyyyypqAzz', ' 0: aaabcxyzzzzpqrrrabbxyyyypqAzz'), ('aaaabcxyzzzzpqrrrabbxyyyypqAzz', ' 0: aaaabcxyzzzzpqrrrabbxyyyypqAzz'), ('aaaabcxyzzzzpqrrrabbbxyyyypqAzz', ' 0: aaaabcxyzzzzpqrrrabbbxyyyypqAzz'), ('aaaabcxyzzzzpqrrrabbbxyyyyypqAzz', ' 0: aaaabcxyzzzzpqrrrabbbxyyyyypqAzz'), ('aaabcxyzpqrrrabbxyyyypABzz', ' 0: aaabcxyzpqrrrabbxyyyypABzz'), ('aaabcxyzpqrrrabbxyyyypABBzz', ' 0: aaabcxyzpqrrrabbxyyyypABBzz'), ('>>>aaabxyzpqrrrabbxyyyypqAzz', ' 0: aaabxyzpqrrrabbxyyyypqAzz'), ('>aaaabxyzpqrrrabbxyyyypqAzz', ' 0: aaaabxyzpqrrrabbxyyyypqAzz'), ('>>>>abcxyzpqrrrabbxyyyypqAzz', ' 0: abcxyzpqrrrabbxyyyypqAzz'), ('*** Failers', None), ('abxyzpqrrabbxyyyypqAzz', None), ('abxyzpqrrrrabbxyyyypqAzz', None), ('abxyzpqrrrabxyyyypqAzz', None), ('aaaabcxyzzzzpqrrrabbbxyyyyyypqAzz', None), ('aaaabcxyzzzzpqrrrabbbxyyypqAzz', None), ('aaabcxyzpqrrrabbxyyyypqqqqqqqAzz', None)]])
suite.append(['^(abc){1,2}zz', '', [('abczz', ' 0: abczz'), ('abcabczz', ' 0: abcabczz'), ('*** Failers', None), ('zz', None), ('abcabcabczz', None), ('>>abczz', None)]])
suite.append(['^(b+|a){1,2}c', '', [('bc', ' 0: bc'), ('bbc', ' 0: bbc'), ('bbbc', ' 0: bbbc'), ('bac', ' 0: bac'), ('bbac', ' 0: bbac'), ('aac', ' 0: aac'), ('abbbbbbbbbbbc', ' 0: abbbbbbbbbbbc'), ('bbbbbbbbbbbac', ' 0: bbbbbbbbbbbac'), ('*** Failers', None), ('aaac', None), ('abbbbbbbbbbbac', None)]])
suite.append(['^\\ca\\cA\\c[\\c{\\c:', '', [('\x01\x01\x1b;z', ' 0: \x01\x01\x1b;z')]])
suite.append(['^[ab\\]cde]', '', [('athing', ' 0: a'), ('bthing', ' 0: b'), (']thing', ' 0: ]'), ('cthing', ' 0: c'), ('dthing', ' 0: d'), ('ething', ' 0: e'), ('*** Failers', None), ('fthing', None), ('[thing', None), ('\\thing', None)]])
suite.append(['^[]cde]', '', [(']thing', ' 0: ]'), ('cthing', ' 0: c'), ('dthing', ' 0: d'), ('ething', ' 0: e'), ('*** Failers', None), ('athing', None), ('fthing', None)]])
suite.append(['^[^ab\\]cde]', '', [('fthing', ' 0: f'), ('[thing', ' 0: ['), ('\\thing', ' 0: \\'), ('*** Failers', ' 0: *'), ('athing', None), ('bthing', None), (']thing', None), ('cthing', None), ('dthing', None), ('ething', None)]])
suite.append(['^[^]cde]', '', [('athing', ' 0: a'), ('fthing', ' 0: f'), ('*** Failers', ' 0: *'), (']thing', None), ('cthing', None), ('dthing', None), ('ething', None)]])
suite.append(['^\\\x81', '', [('\x81', ' 0: \x81')]])
suite.append(['^\xff', '', [('\xff', ' 0: \xff')]])
suite.append(['^[0-9]+$', '', [('0', ' 0: 0'), ('1', ' 0: 1'), ('2', ' 0: 2'), ('3', ' 0: 3'), ('4', ' 0: 4'), ('5', ' 0: 5'), ('6', ' 0: 6'), ('7', ' 0: 7'), ('8', ' 0: 8'), ('9', ' 0: 9'), ('10', ' 0: 10'), ('100', ' 0: 100'), ('*** Failers', None), ('abc', None)]])
suite.append(['^.*nter', '', [('enter', ' 0: enter'), ('inter', ' 0: inter'), ('uponter', ' 0: uponter')]])
suite.append(['^xxx[0-9]+$', '', [('xxx0', ' 0: xxx0'), ('xxx1234', ' 0: xxx1234'), ('*** Failers', None), ('xxx', None)]])
suite.append(['^.+[0-9][0-9][0-9]$', '', [('x123', ' 0: x123'), ('xx123', ' 0: xx123'), ('123456', ' 0: 123456'), ('*** Failers', None), ('123', None), ('x1234', ' 0: x1234')]])
suite.append(['^([^!]+)!(.+)=apquxz\\.ixr\\.zzz\\.ac\\.uk$', '', [('abc!pqr=apquxz.ixr.zzz.ac.uk', ' 0: abc!pqr=apquxz.ixr.zzz.ac.uk'), ('*** Failers', None), ('!pqr=apquxz.ixr.zzz.ac.uk', None), ('abc!=apquxz.ixr.zzz.ac.uk', None), ('abc!pqr=apquxz:ixr.zzz.ac.uk', None), ('abc!pqr=apquxz.ixr.zzz.ac.ukk', None)]])
suite.append([':', '', [('Well, we need a colon: somewhere', ' 0: :'), ("*** Fail if we don't", None)]])
suite.append(['^.*\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})$', '', [('.1.2.3', ' 0: .1.2.3'), ('A.12.123.0', ' 0: A.12.123.0'), ('*** Failers', None), ('.1.2.3333', None), ('1.2.3', None), ('1234.2.3', None)]])
suite.append(['^(\\d+)\\s+IN\\s+SOA\\s+(\\S+)\\s+(\\S+)\\s*\\(\\s*$', '', [('1 IN SOA non-sp1 non-sp2(', ' 0: 1 IN SOA non-sp1 non-sp2('), ('1    IN    SOA    non-sp1    non-sp2   (', ' 0: 1    IN    SOA    non-sp1    non-sp2   ('), ('*** Failers', None), ('1IN SOA non-sp1 non-sp2(', None)]])
suite.append(['^[a-zA-Z\\d][a-zA-Z\\d\\-]*(\\.[a-zA-Z\\d][a-zA-z\\d\\-]*)*\\.$', '', [('a.', ' 0: a.'), ('Z.', ' 0: Z.'), ('2.', ' 0: 2.'), ('ab-c.pq-r.', ' 0: ab-c.pq-r.'), ('sxk.zzz.ac.uk.', ' 0: sxk.zzz.ac.uk.'), ('x-.y-.', ' 0: x-.y-.'), ('*** Failers', None), ('-abc.peq.', None)]])
suite.append(['^\\*\\.[a-z]([a-z\\-\\d]*[a-z\\d]+)?(\\.[a-z]([a-z\\-\\d]*[a-z\\d]+)?)*$', '', [('*.a', ' 0: *.a'), ('*.b0-a', ' 0: *.b0-a'), ('*.c3-b.c', ' 0: *.c3-b.c'), ('*.c-a.b-c', ' 0: *.c-a.b-c'), ('*** Failers', None), ('*.0', None), ('*.a-', None), ('*.a-b.c-', None), ('*.c-a.0-c', None)]])
suite.append(['^\\".*\\"\\s*(;.*)?$', '', [('"1234"', ' 0: "1234"'), ('"abcd" ;', ' 0: "abcd" ;'), ('"" ; rhubarb', ' 0: "" ; rhubarb'), ('*** Failers', None), ('"1234" : things', None)]])
suite.append(['^$', '', [('', ' 0: '), ('*** Failers', None)]])
suite.append(['^(a(b(c)))(d(e(f)))(h(i(j)))(k(l(m)))$', '', [('abcdefhijklm', ' 0: abcdefhijklm')]])
suite.append(['^a*\\w', '', [('z', ' 0: z'), ('az', ' 0: az'), ('aaaz', ' 0: aaaz'), ('a', ' 0: a'), ('aa', ' 0: aa'), ('aaaa', ' 0: aaaa'), ('a+', ' 0: a'), ('aa+', ' 0: aa')]])
suite.append(['^a+\\w', '', [('az', ' 0: az'), ('aaaz', ' 0: aaaz'), ('aa', ' 0: aa'), ('aaaa', ' 0: aaaa'), ('aa+', ' 0: aa')]])
suite.append(['^\\d{8}\\w{2,}', '', [('1234567890', ' 0: 1234567890'), ('12345678ab', ' 0: 12345678ab'), ('12345678__', ' 0: 12345678__'), ('*** Failers', None), ('1234567', None)]])
suite.append(['^[aeiou\\d]{4,5}$', '', [('uoie', ' 0: uoie'), ('1234', ' 0: 1234'), ('12345', ' 0: 12345'), ('aaaaa', ' 0: aaaaa'), ('*** Failers', None), ('123456', None)]])
suite.append(['^From +([^ ]+) +[a-zA-Z][a-zA-Z][a-zA-Z] +[a-zA-Z][a-zA-Z][a-zA-Z] +[0-9]?[0-9] +[0-9][0-9]:[0-9][0-9]', '', [('From abcd  Mon Sep 01 12:33:02 1997', ' 0: From abcd  Mon Sep 01 12:33')]])
suite.append(['^From\\s+\\S+\\s+([a-zA-Z]{3}\\s+){2}\\d{1,2}\\s+\\d\\d:\\d\\d', '', [('From abcd  Mon Sep 01 12:33:02 1997', ' 0: From abcd  Mon Sep 01 12:33'), ('From abcd  Mon Sep  1 12:33:02 1997', ' 0: From abcd  Mon Sep  1 12:33'), ('*** Failers', None), ('From abcd  Sep 01 12:33:02 1997', None)]])
suite.append(['^[ab]{1,3}(ab*|b)', '', [('aabbbbb', ' 0: aabbbbb')]])
suite.append(['abc\\0def\\00pqr\\000xyz\\0000AB', '', [('abc\x00def\x00pqr\x00xyz\x000AB', ' 0: abc\x00def\x00pqr\x00xyz\x000AB'), ('abc456 abc\x00def\x00pqr\x00xyz\x000ABCDE', ' 0: abc\x00def\x00pqr\x00xyz\x000AB')]])
suite.append(['abc\\x0def\\x00pqr\\x000xyz\\x0000AB', '', [('abc\ref\x00pqr\x000xyz\x0000AB', ' 0: abc\ref\x00pqr\x000xyz\x0000AB'), ('abc456 abc\ref\x00pqr\x000xyz\x0000ABCDE', ' 0: abc\ref\x00pqr\x000xyz\x0000AB')]])
suite.append(['^[\\000-\\037]', '', [('\x00A', ' 0: \x00'), ('\x01B', ' 0: \x01'), ('\x1fC', ' 0: \x1f')]])
suite.append(['\\0*', '', [('\x00\x00\x00\x00', ' 0: \x00\x00\x00\x00')]])
suite.append(['A\\x00{2,3}Z', '', [('The A\x00\x00Z', ' 0: A\x00\x00Z'), ('An A\x00\x00\x00Z', ' 0: A\x00\x00\x00Z'), ('*** Failers', None), ('A\x00Z', None), ('A\x00\x00\x00\x00Z', None)]])
suite.append(['^\\s', '', [(' abc', ' 0:  '), ('\x0cabc', ' 0: \x0c'), ('\nabc', ' 0: \n'), ('\rabc', ' 0: \r'), ('\tabc', ' 0: \t'), ('*** Failers', None), ('abc', None)]])
suite.append(['ab{1,3}bc', '', [('abbbbc', ' 0: abbbbc'), ('abbbc', ' 0: abbbc'), ('abbc', ' 0: abbc'), ('*** Failers', None), ('abc', None), ('abbbbbc', None)]])
suite.append(['([^.]*)\\.([^:]*):[T ]+(.*)', '', [('track1.title:TBlah blah blah', ' 0: track1.title:TBlah blah blah')]])
suite.append(['^[W-c]+$', '', [('WXY_^abc', ' 0: WXY_^abc'), ('*** Failers', None), ('wxy', None)]])
suite.append(['^abc$', '', [('abc', ' 0: abc'), ('*** Failers', None), ('qqq\nabc', None), ('abc\nzzz', None), ('qqq\nabc\nzzz', None)]])
suite.append(['[-az]+', '', [('az-', ' 0: az-'), ('*** Failers', ' 0: a'), ('b', None)]])
suite.append(['[az-]+', '', [('za-', ' 0: za-'), ('*** Failers', ' 0: a'), ('b', None)]])
suite.append(['[a\\-z]+', '', [('a-z', ' 0: a-z'), ('*** Failers', ' 0: a'), ('b', None)]])
suite.append(['[a-z]+', '', [('abcdxyz', ' 0: abcdxyz')]])
suite.append(['[\\d-]+', '', [('12-34', ' 0: 12-34'), ('*** Failers', None), ('aaa', None)]])
suite.append(['[\\d-z]+', '', [('12-34z', ' 0: 12-34z'), ('*** Failers', None), ('aaa', None)]])
suite.append(['\\x5c', '', [('\\', ' 0: \\')]])
suite.append(['\\x20Z', '', [('the Zoo', ' 0:  Z'), ('*** Failers', None), ('Zulu', None)]])
suite.append(['ab{3cd', '', [('ab{3cd', ' 0: ab{3cd')]])
suite.append(['ab{3,cd', '', [('ab{3,cd', ' 0: ab{3,cd')]])
suite.append(['ab{3,4a}cd', '', [('ab{3,4a}cd', ' 0: ab{3,4a}cd')]])
suite.append(['{4,5a}bc', '', [('{4,5a}bc', ' 0: {4,5a}bc')]])
suite.append(['abc$', '', [('abc', ' 0: abc'), ('abc\n', ' 0: abc'), ('*** Failers', None), ('abc\ndef', None)]])
suite.append(['(abc)\\223', '', [('abc\x93', ' 0: abc\x93')]])
suite.append(['(abc)\\323', '', [('abc\xd3', ' 0: abc\xd3')]])
suite.append(['ab\\idef', '', [('abidef', ' 0: abidef')]])
suite.append(['a{0}bc', '', [('bc', ' 0: bc')]])
suite.append(['abc[\\10]de', '', [('abc\x08de', ' 0: abc\x08de')]])
suite.append(['abc[\\1]de', '', [('abc\x01de', ' 0: abc\x01de')]])
suite.append(['[^a]', '', [('Abc', ' 0: A')]])
suite.append(['[^a]+', '', [('AAAaAbc', ' 0: AAA')]])
suite.append(['[^a]+', '', [('bbb\nccc', ' 0: bbb\nccc')]])
suite.append(['[^k]$', '', [('abc', ' 0: c'), ('*** Failers', ' 0: s'), ('abk', None)]])
suite.append(['[^k]{2,3}$', '', [('abc', ' 0: abc'), ('kbc', ' 0: bc'), ('kabc', ' 0: abc'), ('*** Failers', ' 0: ers'), ('abk', None), ('akb', None), ('akk', None)]])
suite.append(['^\\d{8,}\\@.+[^k]$', '', [('12345678@a.b.c.d', ' 0: 12345678@a.b.c.d'), ('123456789@x.y.z', ' 0: 123456789@x.y.z'), ('*** Failers', None), ('12345678@x.y.uk', None), ('1234567@a.b.c.d', None)]])
suite.append(['[^a]', '', [('aaaabcd', ' 0: b'), ('aaAabcd', ' 0: A')]])
suite.append(['[^az]', '', [('aaaabcd', ' 0: b'), ('aaAabcd', ' 0: A')]])
suite.append(['\\000\\001\\002\\003\\004\\005\\006\\007\\010\\011\\012\\013\\014\\015\\016\\017\\020\\021\\022\\023\\024\\025\\026\\027\\030\\031\\032\\033\\034\\035\\036\\037\\040\\041\\042\\043\\044\\045\\046\\047\\050\\051\\052\\053\\054\\055\\056\\057\\060\\061\\062\\063\\064\\065\\066\\067\\070\\071\\072\\073\\074\\075\\076\\077\\100\\101\\102\\103\\104\\105\\106\\107\\110\\111\\112\\113\\114\\115\\116\\117\\120\\121\\122\\123\\124\\125\\126\\127\\130\\131\\132\\133\\134\\135\\136\\137\\140\\141\\142\\143\\144\\145\\146\\147\\150\\151\\152\\153\\154\\155\\156\\157\\160\\161\\162\\163\\164\\165\\166\\167\\170\\171\\172\\173\\174\\175\\176\\177\\200\\201\\202\\203\\204\\205\\206\\207\\210\\211\\212\\213\\214\\215\\216\\217\\220\\221\\222\\223\\224\\225\\226\\227\\230\\231\\232\\233\\234\\235\\236\\237\\240\\241\\242\\243\\244\\245\\246\\247\\250\\251\\252\\253\\254\\255\\256\\257\\260\\261\\262\\263\\264\\265\\266\\267\\270\\271\\272\\273\\274\\275\\276\\277\\300\\301\\302\\303\\304\\305\\306\\307\\310\\311\\312\\313\\314\\315\\316\\317\\320\\321\\322\\323\\324\\325\\326\\327\\330\\331\\332\\333\\334\\335\\336\\337\\340\\341\\342\\343\\344\\345\\346\\347\\350\\351\\352\\353\\354\\355\\356\\357\\360\\361\\362\\363\\364\\365\\366\\367\\370\\371\\372\\373\\374\\375\\376\\377', '', [('\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff', ' 0: \x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff')]])
suite.append(['(\\.\\d\\d[1-9]?)\\d+', '', [('1.230003938', ' 0: .230003938'), ('1.875000282', ' 0: .875000282'), ('1.235', ' 0: .235')]])
suite.append(['foo(.*)bar', '', [('The food is under the bar in the barn.', ' 0: food is under the bar in the bar')]])
suite.append(['(.*)(\\d*)', '', [('I have 2 numbers: 53147', ' 0: I have 2 numbers: 53147')]])
suite.append(['(.*)(\\d+)', '', [('I have 2 numbers: 53147', ' 0: I have 2 numbers: 53147')]])
suite.append(['(.*)(\\d+)$', '', [('I have 2 numbers: 53147', ' 0: I have 2 numbers: 53147')]])
suite.append(['(.*\\D)(\\d+)$', '', [('I have 2 numbers: 53147', ' 0: I have 2 numbers: 53147')]])
suite.append(['^[W-]46]', '', [('W46]789', ' 0: W46]'), ('-46]789', ' 0: -46]'), ('*** Failers', None), ('Wall', None), ('Zebra', None), ('42', None), ('[abcd]', None), (']abcd[', None)]])
suite.append(['^[W-\\]46]', '', [('W46]789', ' 0: W'), ('Wall', ' 0: W'), ('Zebra', ' 0: Z'), ('Xylophone', ' 0: X'), ('42', ' 0: 4'), ('[abcd]', ' 0: ['), (']abcd[', ' 0: ]'), ('\\backslash', ' 0: \\'), ('*** Failers', None), ('-46]789', None), ('well', None)]])
suite.append(['\\d\\d\\/\\d\\d\\/\\d\\d\\d\\d', '', [('01/01/2000', ' 0: 01/01/2000')]])
suite.append(['^(a){0,0}', '', [('bcd', ' 0: '), ('abc', ' 0: '), ('aab', ' 0: ')]])
suite.append(['^(a){0,1}', '', [('bcd', ' 0: '), ('abc', ' 0: a'), ('aab', ' 0: a')]])
suite.append(['^(a){0,2}', '', [('bcd', ' 0: '), ('abc', ' 0: a'), ('aab', ' 0: aa')]])
suite.append(['^(a){0,3}', '', [('bcd', ' 0: '), ('abc', ' 0: a'), ('aab', ' 0: aa'), ('aaa', ' 0: aaa')]])
suite.append(['^(a){0,}', '', [('bcd', ' 0: '), ('abc', ' 0: a'), ('aab', ' 0: aa'), ('aaa', ' 0: aaa'), ('aaaaaaaa', ' 0: aaaaaaaa')]])
suite.append(['^(a){1,1}', '', [('bcd', None), ('abc', ' 0: a'), ('aab', ' 0: a')]])
suite.append(['^(a){1,2}', '', [('bcd', None), ('abc', ' 0: a'), ('aab', ' 0: aa')]])
suite.append(['^(a){1,3}', '', [('bcd', None), ('abc', ' 0: a'), ('aab', ' 0: aa'), ('aaa', ' 0: aaa')]])
suite.append(['^(a){1,}', '', [('bcd', None), ('abc', ' 0: a'), ('aab', ' 0: aa'), ('aaa', ' 0: aaa'), ('aaaaaaaa', ' 0: aaaaaaaa')]])
suite.append(['.*\\.gif', '', [('borfle\nbib.gif\nno', ' 0: bib.gif')]])
suite.append(['.{0,}\\.gif', '', [('borfle\nbib.gif\nno', ' 0: bib.gif')]])
suite.append(['.*$', '', [('borfle\nbib.gif\nno', ' 0: no')]])
suite.append(['.*$', '', [('borfle\nbib.gif\nno\n', ' 0: no')]])
suite.append(['^.*B', '', [('**** Failers', None), ('abc\nB', None)]])
suite.append(['^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]', '', [('123456654321', ' 0: 123456654321')]])
suite.append(['^\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d\\d', '', [('123456654321', ' 0: 123456654321')]])
suite.append(['^[\\d][\\d][\\d][\\d][\\d][\\d][\\d][\\d][\\d][\\d][\\d][\\d]', '', [('123456654321', ' 0: 123456654321')]])
suite.append(['^[abc]{12}', '', [('abcabcabcabc', ' 0: abcabcabcabc')]])
suite.append(['^[a-c]{12}', '', [('abcabcabcabc', ' 0: abcabcabcabc')]])
suite.append(['^(a|b|c){12}', '', [('abcabcabcabc', ' 0: abcabcabcabc')]])
suite.append(['^[abcdefghijklmnopqrstuvwxy0123456789]', '', [('n', ' 0: n'), ('*** Failers', None), ('z', None)]])
suite.append(['abcde{0,0}', '', [('abcd', ' 0: abcd'), ('*** Failers', None), ('abce', None)]])
suite.append(['ab[cd]{0,0}e', '', [('abe', ' 0: abe'), ('*** Failers', None), ('abcde', None)]])
suite.append(['ab(c){0,0}d', '', [('abd', ' 0: abd'), ('*** Failers', None), ('abcd', None)]])
suite.append(['a(b*)', '', [('a', ' 0: a'), ('ab', ' 0: ab'), ('abbbb', ' 0: abbbb'), ('*** Failers', ' 0: a'), ('bbbbb', None)]])
suite.append(['ab\\d{0}e', '', [('abe', ' 0: abe'), ('*** Failers', None), ('ab1e', None)]])
suite.append(['"([^\\\\"]+|\\\\.)*"', '', [('the "quick" brown fox', ' 0: "quick"'), ('"the \\"quick\\" brown fox"', ' 0: "the \\"quick\\" brown fox"')]])
suite.append(['a[^a]b', '', [('acb', ' 0: acb'), ('a\nb', ' 0: a\nb')]])
suite.append(['a.b', '', [('acb', ' 0: acb'), ('*** Failers', None), ('a\nb', None)]])
suite.append(['\\x00{ab}', '', [('\x00{ab}', ' 0: \x00{ab}')]])
suite.append(['(A|B)*CD', '', [('CD', ' 0: CD')]])
suite.append(['(\\d+)(\\w)', '', [('12345a', ' 0: 12345a'), ('12345+', ' 0: 12345')]])
suite.append(['(a+|b+|c+)*c', '', [('aaabbbbccccd', ' 0: aaabbbbcccc')]])
suite.append(['(abc|)+', '', [('abc', ' 0: abc'), ('abcabc', ' 0: abcabc'), ('abcabcabc', ' 0: abcabcabc'), ('xyz', ' 0: ')]])
suite.append(['([a]*)*', '', [('a', ' 0: a'), ('aaaaa', ' 0: aaaaa')]])
suite.append(['([ab]*)*', '', [('a', ' 0: a'), ('b', ' 0: b'), ('ababab', ' 0: ababab'), ('aaaabcde', ' 0: aaaab'), ('bbbb', ' 0: bbbb')]])
suite.append(['([^a]*)*', '', [('b', ' 0: b'), ('bbbb', ' 0: bbbb'), ('aaa', ' 0: ')]])
suite.append(['([^ab]*)*', '', [('cccc', ' 0: cccc'), ('abab', ' 0: ')]])
suite.append(['The following tests are taken from the Perl 5.005 test suite; some of them', '', [("/are compatible with 5.004, but I'd rather not have to sort them out./", None)]])
suite.append(['abc', '', [('abc', ' 0: abc'), ('xabcy', ' 0: abc'), ('ababc', ' 0: abc'), ('*** Failers', None), ('xbc', None), ('axc', None), ('abx', None)]])
suite.append(['ab*c', '', [('abc', ' 0: abc')]])
suite.append(['ab*bc', '', [('abc', ' 0: abc'), ('abbc', ' 0: abbc'), ('abbbbc', ' 0: abbbbc')]])
suite.append(['.{1}', '', [('abbbbc', ' 0: a')]])
suite.append(['.{3,4}', '', [('abbbbc', ' 0: abbb')]])
suite.append(['ab{0,}bc', '', [('abbbbc', ' 0: abbbbc')]])
suite.append(['ab+bc', '', [('abbc', ' 0: abbc'), ('*** Failers', None), ('abc', None), ('abq', None)]])
suite.append(['ab{1,}bc', '', []])
suite.append(['ab+bc', '', [('abbbbc', ' 0: abbbbc')]])
suite.append(['ab{1,}bc', '', [('abbbbc', ' 0: abbbbc')]])
suite.append(['ab{1,3}bc', '', [('abbbbc', ' 0: abbbbc')]])
suite.append(['ab{3,4}bc', '', [('abbbbc', ' 0: abbbbc')]])
suite.append(['ab{4,5}bc', '', [('*** Failers', None), ('abq', None), ('abbbbc', None)]])
suite.append(['ab?bc', '', [('abbc', ' 0: abbc'), ('abc', ' 0: abc')]])
suite.append(['ab{0,1}bc', '', [('abc', ' 0: abc')]])
suite.append(['ab?bc', '', []])
suite.append(['ab?c', '', [('abc', ' 0: abc')]])
suite.append(['ab{0,1}c', '', [('abc', ' 0: abc')]])
suite.append(['^abc$', '', [('abc', ' 0: abc'), ('*** Failers', None), ('abbbbc', None), ('abcc', None)]])
suite.append(['^abc', '', [('abcc', ' 0: abc')]])
suite.append(['^abc$', '', []])
suite.append(['abc$', '', [('aabc', ' 0: abc'), ('*** Failers', None), ('aabc', ' 0: abc'), ('aabcd', None)]])
suite.append(['^', '', [('abc', ' 0: ')]])
suite.append(['$', '', [('abc', ' 0: ')]])
suite.append(['a.c', '', [('abc', ' 0: abc'), ('axc', ' 0: axc')]])
suite.append(['a.*c', '', [('axyzc', ' 0: axyzc')]])
suite.append(['a[bc]d', '', [('abd', ' 0: abd'), ('*** Failers', None), ('axyzd', None), ('abc', None)]])
suite.append(['a[b-d]e', '', [('ace', ' 0: ace')]])
suite.append(['a[b-d]', '', [('aac', ' 0: ac')]])
suite.append(['a[-b]', '', [('a-', ' 0: a-')]])
suite.append(['a[b-]', '', [('a-', ' 0: a-')]])
suite.append(['a]', '', [('a]', ' 0: a]')]])
suite.append(['a[]]b', '', [('a]b', ' 0: a]b')]])
suite.append(['a[^bc]d', '', [('aed', ' 0: aed'), ('*** Failers', None), ('abd', None), ('abd', None)]])
suite.append(['a[^-b]c', '', [('adc', ' 0: adc')]])
suite.append(['a[^]b]c', '', [('adc', ' 0: adc'), ('*** Failers', None), ('a-c', ' 0: a-c'), ('a]c', None)]])
suite.append(['\\w', '', [('a', ' 0: a')]])
suite.append(['\\W', '', [('-', ' 0: -'), ('*** Failers', ' 0: *'), ('-', ' 0: -'), ('a', None)]])
suite.append(['a\\sb', '', [('a b', ' 0: a b')]])
suite.append(['a\\Sb', '', [('a-b', ' 0: a-b'), ('*** Failers', None), ('a-b', ' 0: a-b'), ('a b', None)]])
suite.append(['\\d', '', [('1', ' 0: 1')]])
suite.append(['\\D', '', [('-', ' 0: -'), ('*** Failers', ' 0: *'), ('-', ' 0: -'), ('1', None)]])
suite.append(['[\\w]', '', [('a', ' 0: a')]])
suite.append(['[\\W]', '', [('-', ' 0: -'), ('*** Failers', ' 0: *'), ('-', ' 0: -'), ('a', None)]])
suite.append(['a[\\s]b', '', [('a b', ' 0: a b')]])
suite.append(['a[\\S]b', '', [('a-b', ' 0: a-b'), ('*** Failers', None), ('a-b', ' 0: a-b'), ('a b', None)]])
suite.append(['[\\d]', '', [('1', ' 0: 1')]])
suite.append(['[\\D]', '', [('-', ' 0: -'), ('*** Failers', ' 0: *'), ('-', ' 0: -'), ('1', None)]])
suite.append(['ab|cd', '', [('abc', ' 0: ab'), ('abcd', ' 0: ab')]])
suite.append(['()ef', '', [('def', ' 0: ef')]])
suite.append(['$b', '', []])
suite.append(['a\\(b', '', [('a(b', ' 0: a(b')]])
suite.append(['a\\(*b', '', [('ab', ' 0: ab'), ('a((b', ' 0: a((b')]])
suite.append(['a\\\\b', '', []])
suite.append(['((a))', '', [('abc', ' 0: a')]])
suite.append(['(a)b(c)', '', [('abc', ' 0: abc')]])
suite.append(['a+b+c', '', [('aabbabc', ' 0: abc')]])
suite.append(['a{1,}b{1,}c', '', [('aabbabc', ' 0: abc')]])
suite.append(['(a+|b)*', '', [('ab', ' 0: ab')]])
suite.append(['(a+|b){0,}', '', [('ab', ' 0: ab')]])
suite.append(['(a+|b)+', '', [('ab', ' 0: ab')]])
suite.append(['(a+|b){1,}', '', [('ab', ' 0: ab')]])
suite.append(['(a+|b)?', '', [('ab', ' 0: a')]])
suite.append(['(a+|b){0,1}', '', [('ab', ' 0: a')]])
suite.append(['[^ab]*', '', [('cde', ' 0: cde')]])
suite.append(['abc', '', [('*** Failers', None), ('b', None)]])
suite.append(['a*', '', []])
suite.append(['([abc])*d', '', [('abbbcd', ' 0: abbbcd')]])
suite.append(['([abc])*bcd', '', [('abcd', ' 0: abcd')]])
suite.append(['a|b|c|d|e', '', [('e', ' 0: e')]])
suite.append(['(a|b|c|d|e)f', '', [('ef', ' 0: ef')]])
suite.append(['abcd*efg', '', [('abcdefg', ' 0: abcdefg')]])
suite.append(['ab*', '', [('xabyabbbz', ' 0: ab'), ('xayabbbz', ' 0: a')]])
suite.append(['(ab|cd)e', '', [('abcde', ' 0: cde')]])
suite.append(['[abhgefdc]ij', '', [('hij', ' 0: hij')]])
suite.append(['^(ab|cd)e', '', []])
suite.append(['(abc|)ef', '', [('abcdef', ' 0: ef')]])
suite.append(['(a|b)c*d', '', [('abcd', ' 0: bcd')]])
suite.append(['(ab|ab*)bc', '', [('abc', ' 0: abc')]])
suite.append(['a([bc]*)c*', '', [('abc', ' 0: abc')]])
suite.append(['a([bc]*)(c*d)', '', [('abcd', ' 0: abcd')]])
suite.append(['a([bc]+)(c*d)', '', [('abcd', ' 0: abcd')]])
suite.append(['a([bc]*)(c+d)', '', [('abcd', ' 0: abcd')]])
suite.append(['a[bcd]*dcdcde', '', [('adcdcde', ' 0: adcdcde')]])
suite.append(['a[bcd]+dcdcde', '', [('*** Failers', None), ('abcde', None), ('adcdcde', None)]])
suite.append(['(ab|a)b*c', '', [('abc', ' 0: abc')]])
suite.append(['((a)(b)c)(d)', '', [('abcd', ' 0: abcd')]])
suite.append(['[a-zA-Z_][a-zA-Z0-9_]*', '', [('alpha', ' 0: alpha')]])
suite.append(['^a(bc+|b[eh])g|.h$', '', [('abh', ' 0: bh')]])
suite.append(['(bc+d$|ef*g.|h?i(j|k))', '', [('effgz', ' 0: effgz'), ('ij', ' 0: ij'), ('reffgz', ' 0: effgz'), ('*** Failers', None), ('effg', None), ('bcdd', None)]])
suite.append(['((((((((((a))))))))))', '', [('a', ' 0: a')]])
suite.append(['(((((((((a)))))))))', '', [('a', ' 0: a')]])
suite.append(['multiple words of text', '', [('*** Failers', None), ('aa', None), ('uh-uh', None)]])
suite.append(['multiple words', '', [('multiple words, yeah', ' 0: multiple words')]])
suite.append(['(.*)c(.*)', '', [('abcde', ' 0: abcde')]])
suite.append(['\\((.*), (.*)\\)', '', [('(a, b)', ' 0: (a, b)')]])
suite.append(['[k]', '', []])
suite.append(['abcd', '', [('abcd', ' 0: abcd')]])
suite.append(['a(bc)d', '', [('abcd', ' 0: abcd')]])
suite.append(['a[-]?c', '', [('ac', ' 0: ac')]])
suite.append(['((foo)|(bar))*', '', [('foobar', ' 0: foobar')]])
suite.append(['^(.+)?B', '', [('AB', ' 0: AB')]])
suite.append(['^([^a-z])|(\\^)$', '', [('.', ' 0: .')]])
suite.append(['^[<>]&', '', [('<&OUT', ' 0: <&')]])
suite.append(['^(){3,5}', '', [('abc', ' 0: ')]])
suite.append(['^(a+)*ax', '', [('aax', ' 0: aax')]])
suite.append(['^((a|b)+)*ax', '', [('aax', ' 0: aax')]])
suite.append(['^((a|bc)+)*ax', '', [('aax', ' 0: aax')]])
suite.append(['(a|x)*ab', '', [('cab', ' 0: ab')]])
suite.append(['(a)*ab', '', [('cab', ' 0: ab')]])
suite.append(['foo\\w*\\d{4}baz', '', [('foobar1234baz', ' 0: foobar1234baz')]])
suite.append(['^b', '', []])
suite.append(['(\\w+:)+', '', [('one:', ' 0: one:')]])
suite.append(['([\\w:]+::)?(\\w+)$', '', [('abcd', ' 0: abcd'), ('xy:z:::abcd', ' 0: xy:z:::abcd')]])
suite.append(['^[^bcd]*(c+)', '', [('aexycd', ' 0: aexyc')]])
suite.append(['(a*)b+', '', [('caab', ' 0: aab')]])
suite.append(['([\\w:]+::)?(\\w+)$', '', [('abcd', ' 0: abcd'), ('xy:z:::abcd', ' 0: xy:z:::abcd'), ('*** Failers', ' 0: Failers'), ('abcd:', None), ('abcd:', None)]])
suite.append(['^[^bcd]*(c+)', '', [('aexycd', ' 0: aexyc')]])
suite.append(['(>a+)ab', '', []])
suite.append(['([[:]+)', '', [('a:[b]:', ' 0: :[')]])
suite.append(['([[=]+)', '', [('a=[b]=', ' 0: =[')]])
suite.append(['([[.]+)', '', [('a.[b].', ' 0: .[')]])
suite.append(['((Z)+|A)*', '', [('ZABCDEFG', ' 0: ZA')]])
suite.append(['(Z()|A)*', '', [('ZABCDEFG', ' 0: ZA')]])
suite.append(['(Z(())|A)*', '', [('ZABCDEFG', ' 0: ZA')]])
suite.append(['^[a-\\d]', '', [('abcde', ' 0: a'), ('-things', ' 0: -'), ('0digit', ' 0: 0'), ('*** Failers', None), ('bcdef', None)]])
suite.append(['^[\\d-a]', '', [('abcde', ' 0: a'), ('-things', ' 0: -'), ('0digit', ' 0: 0'), ('*** Failers', None), ('bcdef', None)]])
suite.append(['[\\s]+', '', [('> \t\n\x0c\r\x0b<', ' 0:  \t\n\x0c\r')]])
suite.append(['\\s+', '', [('> \t\n\x0c\r\x0b<', ' 0:  \t\n\x0c\r')]])
suite.append(['\\M', '', [('M', ' 0: M')]])
suite.append(['(a+)*b', '', [('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', None)]])
suite.append(['\xc5\xe6\xe5\xe4[\xe0-\xff\xc0-\xdf]+', '', [('\xc5\xe6\xe5\xe4\xe0', ' 0: \xc5\xe6\xe5\xe4\xe0'), ('\xc5\xe6\xe5\xe4\xff', ' 0: \xc5\xe6\xe5\xe4\xff'), ('\xc5\xe6\xe5\xe4\xc0', ' 0: \xc5\xe6\xe5\xe4\xc0'), ('\xc5\xe6\xe5\xe4\xdf', ' 0: \xc5\xe6\xe5\xe4\xdf')]])
suite.append(['line\\nbreak', '', [('this is a line\nbreak', ' 0: line\nbreak'), ('line one\nthis is a line\nbreak in the second line', ' 0: line\nbreak')]])
suite.append(['1234', '', []])
suite.append(['1234', '', []])
suite.append(['Content-Type\\x3A[^\\r\\n]{6,}', '', [('Content-Type:xxxxxyyy', ' 0: Content-Type:xxxxxyyy')]])
suite.append(['Content-Type\\x3A[^\\r\\n]{6,}z', '', [('Content-Type:xxxxxyyyz', ' 0: Content-Type:xxxxxyyyz')]])
suite.append(['Content-Type\\x3A[^a]{6,}', '', [('Content-Type:xxxyyy', ' 0: Content-Type:xxxyyy')]])
suite.append(['Content-Type\\x3A[^a]{6,}z', '', [('Content-Type:xxxyyyz', ' 0: Content-Type:xxxyyyz')]])
suite.append(['^\\w+=.*(\\\\\\n.*)*', '', [('abc=xyz\\\npqr', ' 0: abc=xyz\\\npqr')]])
suite.append(['^(a()*)*', '', [('aaaa', ' 0: aaaa')]])
suite.append(['^(a()+)+', '', [('aaaa', ' 0: aaaa')]])
suite.append(['(a|)*\\d', '', [('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', None), ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa4', ' 0: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa4')]])
suite.append(['.+foo', '', [('afoo', ' 0: afoo'), ('** Failers', None), ('\r\nfoo', None), ('\nfoo', None)]])
suite.append([' End of testinput7 ', '', []])
