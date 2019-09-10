from epanet import toolkit

'''

there are a few different attributes that must be supported:

Create:
- nodes, links (of different types)
- curves
- controls

Update properties / attributes:
- nodes (junctions, tanks, reservoirs)
    - elevation?
- links (pipes, pumps, valves)
    - valve position
    - roughness / roughness category
    - status (open/closed)
- controls
    - lowlevel / highlevel
    - time?
    - access by index/name?




resolve key paths using nested structured dictionaries:

{
    key: key_name
    args: arguments or None
    nested: {
        key: key_name
        args: arguments or None
        nested: ... or None
    }
}



'''

debug = True


class KeyPath:
    def __init__(self):
        self.key = ''
        self.args = None
        self.nested = None


def _parse_path(path):
    """
    Parse a specialized dot-path and return constituent path members
    :param path: a dot-and-bracket-notated epanet model path
    :return: path components dictionary (key,args,nested[...])

    Example:
    >>> _parse_path("links[20].roughness")
    {
        'key': 'links',
        'args': '20',
        'nested': {
            'key': 'roughness',
            'args': None,
            'nested': None
        }
    }

    >>> _parse_path("options.duration")
    "options", "", "duration"
    """
    wrapper = KeyPath()
    components = path.split('.')
    wrapper.nested = KeyPath()
    this_key = wrapper
    for c in components:
        this_key.nested = KeyPath()
        this_key = this_key.nested
        if '[' in c:  # there are arguments
            c, args = c.split('[')
            args = args.replace(']', '')
        this_key.key = c
        this_key.args = args
    # ignore the wrapper
    return wrapper.nested


class LinkModifier:
    _keys = {
            'status': toolkit.STATUS,
            'setting': toolkit.SETTING,
            'roughness': toolkit.ROUGHNESS
        }

    def __init__(self, en_project_handle, link_id):
        if link_id is None:
            raise KeyError('must specify a link name')
        self._p = en_project_handle
        self._l = link_id

    def set(self, key, value):
        k = key.key
        idx = toolkit.getlinkindex(self._p, self._l)
        toolkit.setlinkvalue(self._p, idx, LinkModifier._keys[k], value)
        if debug:
            print("set {} to {} -> epanet value is {}".format(key, value, toolkit.getlinkvalue(self._p, idx, LinkModifier._keys[k])))


class NodeModifier:
    _keys = {
        'elevation': toolkit.ELEVATION,
        'base_demand': toolkit.BASEDEMAND
    }

    def __init__(self, en_project_handle, node_id):
        self._p = en_project_handle
        self._n = node_id

    def set(self, key, value):
        k = key.key
        idx = toolkit.getnodeindex(self._p, self._n)
        toolkit.setnodevalue(self._p, idx, NodeModifier._keys[k], value)
        if debug:
            print("set {} to {} -> epanet value is {}".format(key, value, toolkit.getnodevalue(self._p, idx, NodeModifier._keys[k])))


class Project:
    def __init__(self):
        self._p = toolkit.createproject()

    def open(self, filename):
        toolkit.open(self._p, filename, 'tmp.rpt', 'tmp.out')

    def __del__(self):
        print('deleting')
        toolkit.close(self._p)

    def set_network_attribute(self, path, value):
        """
        Set a Network Attribute
        :param path: a dot-notated path to the model element/option and attribute
        :param value: a new value
        :return: None

        Example:
        >>> p = Project('Net3.inp')
        >>> p.set_network_attribute("links[20].roughness", 200)

        """
        modifiers = {
            'links': LinkModifier,
            'nodes': NodeModifier,
            'controls': None
        }
        key_path = _parse_path(path)
        ModifierType = modifiers[key_path.key]
        modifier = ModifierType(self._p, key_path.args)
        modifier.set(key_path.nested, value)
