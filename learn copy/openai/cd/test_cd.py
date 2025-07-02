from cd import cd, cd_2

"""
cd(/foo/bar, baz) = /foo/bar/baz
cd(/foo/../, /baz) = /baz
cd(/, foo/bar/../../baz) = /baz
cd(/, ..) = Null
"""
def test_1():
    assert cd('/foo/bar', 'baz') == '/foo/bar/baz'
    assert cd('/foo/../', '/baz') == '/baz'
    assert cd('/', 'foo/bar/../../baz') == '/baz'
    assert cd('/', '..') == None

"""
cd(/foo/bar, baz, {'/foo/bar': '/abc', '/foo/bar/baz': '/xyz'}) = /xyz
"""
def test_2():
    assert cd_2('/foo/bar', 'baz', {'/foo/bar': '/abc', '/foo/bar/baz': '/xyz'}) == '/xyz'
    assert cd_2('/foo/bar', 'baz', {'/foo/bar': '/abc'}) == '/abc/baz'
