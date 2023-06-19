![Molecule test](https://github.com/pimvh/nsd/actions/workflow/test.yaml/badge.svg)
# Requirements

1. Ansible installed:

```
sudo apt install python3
python3 -m ensurepip --upgrade
pip3 install ansible
```

2. The Ansible controller needs to have `date` installed, see `defaults.yaml`.

This is in order to automagically generate a DNS serial.

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
    dkim_domain: "<< dkim domain >>"
    dkim_keys: "{{ list of dkim_keys }}"
    dnssec_enabled: true
    dnssec_algo: ECDSAP384SHA384
    zsk_validity_period: "7" <-- in days
    zsk_grace_period: "24" <-- in hours
    zsk_rotation_day: "3" <-- weekday starting at 0
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

- Run dependency [systemd-failmail](https://github.com/pimvh/systemd-failmail)
- Validate whether variables are all defined
- Install nsd (nsd_install set)
- Create a bunch of required directories for NSD and ZSK and KSK organisation
- Setup nsd-control with certificates
- Setup zones and move dnssecpls script (when dnssec is enabled)
- Setup dnssecpls service (when dnssec is enabled)

# Future Improvements

- Allow non authorative zones and key directives
- Improve sane defaults of variables (see defaults defined in defaults/main.yaml)
- Allow TTL to be passed in records
- Add automated KSK rollover to dnssecpls script
- Allow duplicates of dnssecpls script with different variables from ZSK rollover etc as specified in nsd_zone_attributes

# Sources

Used as inspiration.

<https://ubuntu.com/server/docs/service-domain-name-service-dns>
<https://www.digitalocean.com/community/tutorials/how-to-configure-nsd-as-a-private-network-dns-server-on-debian-9>
