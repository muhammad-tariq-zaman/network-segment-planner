# network-segment-planner

Plan subnets for network segments from a CSV: each segment gets the smallest subnet that fits its hosts plus network and broadcast addresses, allocated in order from a base network without overlapping — first and last usable addresses shown.

## How to run

```sh
python3 main.py segments.csv
```

## Example output

```
Office: 10.0.0.0/25 (/25, 100 hosts, usable 10.0.0.1 - 10.0.0.126)
Lab: 10.0.0.128/26 (/26, 50 hosts, usable 10.0.0.129 - 10.0.0.190)
```

Standard library only. Run the tests with `python3 -m unittest discover`.
