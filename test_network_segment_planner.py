import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import smallest_prefix, plan

import ipaddress

def row(segment, hosts):
    return {"segment": segment, "hosts_required": str(hosts)}

class TestSegmentPlanner(unittest.TestCase):
    def test_prefix_for_100_hosts(self):
        self.assertEqual(smallest_prefix(100), 25)
    def test_prefix_for_2_hosts(self):
        self.assertEqual(smallest_prefix(2), 30)
    def test_prefix_exact_fit(self):
        self.assertEqual(smallest_prefix(126), 25)
    def test_first_subnet_starts_at_base(self):
        r = plan([row("Office", 100)])
        self.assertEqual(r[0][2], "10.0.0.0/25")
    def test_usable_range(self):
        r = plan([row("Office", 100)])
        self.assertEqual((r[0][4], r[0][5]), ("10.0.0.1", "10.0.0.126"))
    def test_subnets_do_not_overlap(self):
        r = plan([row("A", 100), row("B", 50), row("C", 10)])
        networks = [ipaddress.ip_network(x[2]) for x in r]
        self.assertTrue(all(not a.overlaps(b) for i, a in enumerate(networks) for b in networks[i + 1:]))
    def test_second_subnet_aligned(self):
        r = plan([row("A", 100), row("B", 50)])
        self.assertEqual(r[1][2], "10.0.0.128/26")
    def test_overflow_raises(self):
        with self.assertRaises(ValueError):
            plan([row("Huge", 70000)], "10.0.0.0/24")
