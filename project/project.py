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

'''

debug = True


def _parse_path(path):
    """
    Parse a specialized dot-path and return constituent path members
    :param path: a dot-notated epanet model path
    :return: path components tuple (prefix, args, attribute)

    Example:
    >>> _parse_path("links[20].roughness")
    "links", "20", "roughness"

    >>> _parse_path("options.duration")
    "options", "", "duration"
    """
    prefix, attribute = path.split('.')
    prefix, args = prefix.split('[')
    if args is not None:
        args = args.replace(']', '').replace('"', '').replace("'", "")
    return prefix, args, attribute


class LinkModifier:
    def __init__(self, en_project_handle, link_id):
        if link_id is None:
            raise KeyError('must specify a link name')
        self._p = en_project_handle
        self._l = link_id

    def set(self, key, value):
        keys = {
            'status': toolkit.EN_STATUS,
            'setting': toolkit.EN_SETTING,
            'roughness': toolkit.EN_ROUGHNESS
        }
        idx = toolkit.getlinkindex(self._p, self._l)
        toolkit.setlinkvalue(self._p, idx, keys[key], value)
        if debug:
            print("set {} to {} -> epanet value is {}".format(key, value, toolkit.getlinkvalue(self._p, idx, keys[key])))


class NodeModifier:
    def __init__(self, en_project_handle, node_id):
        self._p = en_project_handle
        self._n = node_id

    def set(self, key, value):
        keys = {
            'elevation': toolkit.EN_ELEVATION,
            'base_demand': None
        }
        idx = toolkit.getnodeindex(self._p, self._n)
        toolkit.setnodevalue(self._p, idx, keys[key], value)
        if debug:
            print("set {} to {} -> epanet value is {}".format(key, value, toolkit.getnodevalue(self._p, idx, keys[key])))


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
        prefix, args, attribute = _parse_path(path)
        ModifierType = modifiers[prefix]
        modifier = ModifierType(self._p, args)
        modifier.set(attribute, value)

