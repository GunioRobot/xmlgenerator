#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Nuno Mariz'
__author_email__ = 'nmariz@gmail.com'
__url__ = 'http://mariz.org'
__license__ = 'BSD'
    
from xml.sax.saxutils import escape
from types import NoneType
from decimal import Decimal
from datetime import datetime, date, time
import codecs

class Xml(object):
    """ 
    XML generator class

    Usage:
    >>> xml = Xml(root) # root is a root <Node> object 
    >>> xml.render()

    Writing contents to a file or a writer:
    >>> import cStringIO
    >>> output = cStringIO.StringIO()
    >>> xml = Xml(root) # root is a root <Node> object 
    >>> xml.render(output)
    """

    encoding = 'utf-8'

    def __init__(self, node):
        self._node = node

    def __repr__(self):
        return '<Xml: "Node: %s">' % str(self._node)

    def __unicode__(self):
        return u'<?xml version="1.0" encoding="%s"?>\n%s' % (Xml.encoding, self._node.render())

    @staticmethod
    def set_encoding(encoding):
        Xml.encoding = encoding

    def render(self, writer=None):
        if writer is None:
            return unicode(self)
        writer.write(unicode(self))

    def write(self, filename):
        writer = codecs.open(filename, 'w', Xml.encoding)
        self.render(writer)
        writer.close()


class Node(object):
    """
    Node element class

    Usage:
    Node creation:
    >>> root = Node('root')
    >>> records = Node('blog', 'http://mariz.org', dict(author='Nuno Mariz', title='Nuno Mariz Weblog'))
    
    Append a child node:
    >>> root.append(records)
    or inline:
    >>> root.append_as_node('blog', 'http://mariz.org', dict(author='Nuno Mariz', title='Nuno Mariz Weblog'))
    """

    def __init__(self, name, contents=None, attributes=None, cdata=False):
        self._name = name
        self._contents = contents
        self._attributes = attributes or dict()
        self._cdata = cdata
        self._nodes = []

    def __repr__(self):
        return '<Node: "%s">' % self._name

    def __str__(self):
        return self._name

    def __unicode__(self):
        attributes = u''.join([' %s="%s"' % (key, Node.escape(value)) for key, value in self._attributes.items()])
        contents = None
        if self._contents is not None:
            contents = Node.escape(self._contents, self._cdata)
        elif self._nodes:
            contents = u''.join([unicode(node) for node in self._nodes])
        if contents is not None:
            return u'<%s%s>%s</%s>' % (self._name, attributes, contents, self._name)
        return u'<%s%s />' % (self._name, attributes)

    def __len__(self):
        return len(self._nodes)

    def __getitem__(self, key):
        return self._attributes.get(key)

    def __setitem__(self, key, value):
        self._attributes[key] = value

    def __delitem__(self, key):
        del self._attributes[key]

    @property
    def nodes(self):
        return self._nodes

    @property
    def contents(self):
        return self._contents

    @property
    def has_contents(self):
        return self._contents is None

    @property
    def has_nodes(self):
        return bool(self._nodes)

    @property
    def is_cdata(self):
        return self._cdata

    @staticmethod
    def escape(value, cdata=False):
        if isinstance(value, NoneType):
            return u''
        if isinstance(value, (bool, int, long, datetime, date, time, float, Decimal)):
            return value
        if cdata:
            value = u'<![CDATA[%s]]>' % value
        else:
            value = escape(value)
        if isinstance(value, basestring):
            if not isinstance(value, unicode):
                value = unicode(value, Xml.encoding)
        return value

    def append(self, node):
        assert isinstance(node, Node), '"node" is not a Node instance'
        self._nodes.append(node)

    def append_as_node(self, *args, **kargs):
        self._nodes.append(Node(*args, **kargs))

    def render(self):
        return unicode(self)
