from __future__ import absolute_import
import warnings

# Import thirt party modules
import yaml
from yaml.nodes import MappingNode
from yaml.constructor import ConstructorError
try:
    yaml.Loader = yaml.CLoader
    yaml.Dumper = yaml.CDumper
except:
    pass

load = yaml.load

class CustomeConstructor(yaml.constructor.SafeConstructor):
    def construct_mapping(self, node, deep=False):
        if not isinstance(node, MappingNode):
            raise ConstructorError(None, None,
                    "expected a mapping node, but found %s" % node.id,
                    node.start_mark)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError, exc:
                raise ConstructorError("while constructing a mapping", node.start_mark,
                        "found unacceptable key (%s)" % exc, key_node.start_mark)
            value = self.construct_object(value_node, deep=deep)
            if key in mapping:
                warnings.warn("Duplicate Key: '{0}'".format(key))
            mapping[key] = value
        return mapping


class CustomLoader(yaml.reader.Reader, yaml.scanner.Scanner, yaml.parser.Parser,
                   yaml.composer.Composer, CustomeConstructor, yaml.resolver.Resolver):
    def __init__(self, stream):
        yaml.reader.Reader.__init__(self, stream)
        yaml.scanner.Scanner.__init__(self)
        yaml.parser.Parser.__init__(self)
        yaml.composer.Composer.__init__(self)
        CustomeConstructor.__init__(self)
        yaml.resolver.Resolver.__init__(self)

