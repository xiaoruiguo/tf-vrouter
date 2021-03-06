#
# Copyright (c) 2019 Juniper Networks, Inc. All rights reserved.
#

import os
from object_base import *
from vr_py_sandesh.vr_py.ttypes import *


class Route(ObjectBase, vr_route_req):
    """Base class for creating routes"""

    def __init__(self, family, vrf, prefix=None, prefix_len=None, mac=None,
                 nh_idx=None, h_op=constants.SANDESH_OPER_ADD,
                 rtr_label_flags=None, rtr_label=None, **kwargs):
        super(Route, self).__init__()
        vr_route_req.__init__(self)
        self.h_op = h_op
        self.rtr_family = family
        self.rtr_vrf_id = vrf
        if mac is not None:
            self.rtr_mac = self.vt_mac(mac)
        if prefix is not None:
            if family is constants.AF_INET:
                self.rtr_prefix = self.vt_ipv4_bytes(prefix)
            elif family is constants.AF_INET6:
                self.rtr_prefix = self.vt_ipv6_bytes(prefix)
        self.rtr_prefix_len = prefix_len
        self.rtr_nh_id = nh_idx
        self.rtr_label_flags = rtr_label_flags
        self.rtr_label = rtr_label
        self.sreq_class = vr_route_req.__name__

    def __repr__(self):
        """Display basic details of the route"""
        return "Route(Prefix:{} mac:{})".format(self.rtr_prefix, self.rtr_mac)

    def __str__(self):
        """Display basic details of the route"""
        return "Route(Prefix:{} mac:{})".format(self.rtr_prefix, self.rtr_mac)

    def get(self, key):
        """
        Queries vrouter and return the key value from the response xml file
        """
        self.h_op = constants.SANDESH_OPER_GET
        return super(Route, self).get(key)

    def rtr_nh_idx(self):
        """Returns rtr_nh_id"""
        return self.rtr_nh_idx

    def get_rtr_nh_idx(self):
        """
        Queries vrouter and returns rtr_nh_id value from the response xml file
        """
        return int(self.get('rtr_nh_id'))

    def get_rtr_label_flags(self):
        """
        Queries vrouter and returns rtr_label_flags from response xml file
        """
        return int(self.get('rtr_label_flags'))


class BridgeRoute(Route):
    """
    BridgeRoute class to create bridge route

    Mandatory Parameters:
    --------------------
    vrf : int
        Vrf index
    mac_str: str
        MAC address
    nh_idx : int
        Nexthop id
    """

    def __init__(self, vrf, mac_str, nh_idx, **kwargs):
        super(BridgeRoute, self).__init__(constants.AF_BRIDGE, vrf, None, None,
                                          mac_str, nh_idx, **kwargs)


class InetRoute(Route):
    """
    InetRoute class to create inet route

    Mandatory Parameters:
    --------------------
    vrf : int
        Vrf index
    prefix : str
        IP prefix
    nh_idx : int
        Nexthop id

    Optional Parameters:
    -------------------
    prefix_len : int
        Prefix length
    h_op : int
        Sandesh operation
    rtr_label_flags : int
        Rtr label flags
    rtr_label : int
        Rtr label
    mac_str : str
        Stitched MAC address

    """

    def __init__(self, vrf, prefix, nh_idx, prefix_len=32, mac_str=None,
                 h_op=constants.SANDESH_OPER_ADD, rtr_label_flags=None,
                 rtr_label=None, **kwargs):
        super(InetRoute, self).__init__(
            constants.AF_INET,
            vrf,
            prefix,
            prefix_len,
            mac_str,
            nh_idx,
            h_op,
            rtr_label_flags,
            rtr_label,
            **kwargs)


class Inet6Route(Route):
    """
    Inet6Route class to create inet6 route

    Mandatory Parameters:
    --------------------
    vrf : int
        Vrf index
    prefix : str
        IP prefix
    prefix_len : int
        Nexthop id
    nh_idx : int
        Nexthop id
    """

    def __init__(self, vrf, prefix, prefix_len, nh_idx, mac_str=None,
                 **kwargs):
        super(Inet6Route, self).__init__(
            constants.AF_INET6,
            vrf,
            prefix,
            prefix_len,
            mac_str,
            nh_idx,
            **kwargs)
