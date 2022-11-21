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
nsd_zones_attributes:
  example_zone_name:
    ttl: 300
    dns_refresh: 300
    dns_retry: 300
    dns_expire: 300
    dns_negative_response_cache: 300
    make_ascii: true
    dkim: true
    dnssec:
      enabled: true
      algo: ECDSAP384SHA384
      zsk_rollover: "7" # <-- in days
      zsk_grace_period: "1" <-- in days
      propagation_delay: "24" <-- in hours
    reverse_zone:
      enabled: true
      name_v4: "{{ range_ipv4 | get_rev_dns_origin }}"
      name_v6: "{{ range_ipv6 | get_rev_dns_origin(version=6) }}"

nsd_records:
  example_zone_name:
    - id: "@"
      type: A
      record: "<< ip addr here >>"
      no_ptr: true
    - id: "@"
      type: MX
      value: 10
      record: "{{ zone_name | default('') }}."
    - type: "raw"
      record: >-
        << raw DNS record here >>
```

# TLDR - What will happen if I run this

- validate whether variables are all right
- install nsd (nsd_install set)
- create a bunch of required directories for NSD and ZSK and KSK organisation
- setup nsd-control with certificates
- setup zones and move dnssecpls script
- setup dnssecpls service (with failmail to required addr)

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
