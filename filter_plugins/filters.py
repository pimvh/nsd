#!/usr/bin/python3

import itertools
import ipaddress

from ansible.errors import AnsibleFilterError


class FilterModule:
    """custom filter to check if something is a list"""

    def filters(self):
        return {
            #            'is_list'                   : self.is_list,
            #            'parse_filename'            : self.parse_filename,
            #            'multiline_indent'          : self.multiline_indent,
            "get_rev_dns_origin": self.get_rev_dns_origin,
            "slice_by": self.slice_by,
            "common_start": self.common_start,
            "any": any,
            "all": all,
        }

    def is_list(self, obj):
        """boolean whether something is a list object"""
        if isinstance(obj, list):
            return True
        else:
            return False

    def parse_filename(self, obj):
        """parse filename from string"""
        return obj.split('"')[1]

    def multiline_indent(self, obj, indent=1):
        """fix jinja multiline indentation"""
        out = ""

        if isinstance(obj, list):
            for x in obj:
                out += indent * " " + str(x) + "\n"
            return out

        return indent * " " + str(obj) + "\n"

    def get_rev_dns_origin(self, cidr_range: str, version=4):
        """get reverse dns origin based on CIDR range (v4/v6)"""

        if version == 4:
            ipv4_network = list(ipaddress.IPv4Network(cidr_range, strict=False).hosts())

            rev_start, rev_end = (
                ipv4_network[0].reverse_pointer[::-1],
                ipv4_network[-1].reverse_pointer[::-1],
            )

            return self.common_start(rev_start, rev_end)[::-1][1:]

        elif version == 6:
            addr = next(ipaddress.IPv6Network(cidr_range, strict=False).hosts())
            pointer = str(addr.reverse_pointer[2:])  # slice off 1.

            while True:

                if pointer[:2] == "0.":
                    pointer = pointer[2:]
                else:
                    break

            return pointer  # add starting dot back again
        else:
            raise ValueError("Unkown IP version")

    def slice_by(self, obj, num: int):
        """fix jinja multiline indentation"""

        if not isinstance(num, int):
            num = int(num)

        return obj[num:]

    @staticmethod
    def common_start(sa, sb):
        """returns the longest common substring from the beginning of sa and sb"""

        def _iter():
            for a, b in zip(sa, sb):
                if a == b:
                    yield a
                else:
                    return

        return "".join(_iter())

    def common_ip(self, obj):
        """common substr in range"""

        if not isinstance(obj, str):
            obj = str(obj)

        first_ip, second_ip = obj.split("-")

        return self.common_start(first_ip, second_ip)
