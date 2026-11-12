"""Plan subnets for network segments from a base network.

Usage: python3 main.py segments.csv [--base 10.0.0.0/16]
CSV columns: segment,hosts_required.
Each segment gets the smallest subnet that fits its hosts
plus the network and broadcast addresses. Subnets are
allocated in order from the base network, aligned to their
size, and never overlap. The first and last usable addresses
are shown for each segment.
"""
import argparse, csv, ipaddress, math, sys

def smallest_prefix(hosts):
    needed = hosts + 2
    bits = math.ceil(math.log2(needed))
    return 32 - bits

def plan(rows, base="10.0.0.0/16"):
    network = ipaddress.ip_network(base)
    cursor = int(network.network_address)
    out = []
    for row in rows:
        hosts = int(row["hosts_required"])
        prefix = smallest_prefix(hosts)
        size = 2 ** (32 - prefix)
        if cursor % size:
            cursor = ((cursor // size) + 1) * size
        subnet = ipaddress.ip_network((cursor, prefix))
        if not subnet.subnet_of(network):
            raise ValueError(f"not enough space in {base} for segment {row['segment'].strip()}")
        out.append((row["segment"].strip(), hosts, str(subnet), prefix,
                    str(subnet.network_address + 1),
                    str(subnet.broadcast_address - 1)))
        cursor += size
    return out

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--base", default="10.0.0.0/16")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = plan(list(csv.DictReader(f)), args.base)
    for segment, hosts, subnet, prefix, first, last in results:
        print(f"{segment}: {subnet} (/{prefix}, {hosts} hosts, usable {first} - {last})")
    return 0

if __name__ == "__main__":
    sys.exit(main())
