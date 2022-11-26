# Requirements

1. Ansible installed:

```
sudo apt install python3
python3 -m ensurepip --upgrade
pip3 install ansible
```

## Required variables

Review the variables as shown in defaults.

# Example playbook

```
hosts:
  - foo
roles:
  - pimvh.nsd

```

Variable structure:

```
# list of all zones

nsd_zone_attributes:
  - name: "<< zone_name >>"
    ttl: 300
    dns_refresh: 300
    dns_retry: 300
    dns_expire: 300
    dns_negative_response_cache: 300
    make_ascii: true
    dkim_enabled: true
    dkim_domain: bastia.prac.os3.nl
    dkim_keys: "{{ list of dkim_keys }}"
    dnssec_enabled: true
    dnssec_algo: ECDSAP384SHA384
    zsk_rollover: "7" <-- in days
    zsk_grace_period: "1" <-- in days
    dnssec_propagation_delay: "24" <-- in hours
    reverse_zone_enabled: true
    reverse_zone_name_v4: "{{ assigned_range_ipv4 | get_rev_dns_origin }}" <-- Use supplied filter to calculate rev dns for a zone,
    reverse_zone_name_v6: "{{ assigned_range_ipv6 | get_rev_dns_origin(version=6) }}" <-- idem, but for v6.

"nsd_<< your zone with _ instead of . >>_records":
  - id: "@"
    type: NS
    record: "ns1"
  - id: "@"
    type: A
    record: "127.0.0.1"
    no_ptr: true <-- supply no_ptr for it to not show up in the PTR file
  - id: "@"
    type: AAAA
    record: "::1"
    no_ptr: true <-- supply no_ptr for it to not show up in the PTR file
  - id: "@"
    type: MX
    value: 10
    record: "{{ nsd_zone_name | default('') }}." <-- you can use the name of the zone in here
    type: CNAME
    record: "@"
# e.g. SPF record:
  - id: "@"
    type: "TXT"
    record: "v=spf1 ip4:<< ipv4_addr >> ip6:<< ipv6_addr >> ~all" <--
  - type: "raw"
    record: >-
        << some_raw_record, which will be placed in the file directly >>

```

# TLDR - What will happen if I run this

- validate whether variables are all defined
- install nsd (nsd_install set)
- create a bunch of required directories for NSD and ZSK and KSK organisation
- setup nsd-control with certificates
- setup zones and move dnssecpls script
- setup dnssecpls service (with failmail to required addr)

# Future Improvements

- Allow non authorative zones and key directives
- Improve sane defaults of variables (see defaults defined in defaults/main.yaml)
- Allow TTL to be passed in records
- Add automated KSK rollover to dnssecpls script
- Allow duplicates of dnssecpls script with different variables from ZSK rollover etc as specified in nsd_zone_attributes
- Only update serial when required, instead of when running role

# License

The GPLv3 License (GPLv3)

Copyright (c) 2022 Author

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
