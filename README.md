# WireGuard

The tunnel, only while it's up. Interface, IP, endpoint on hover. Nothing when you're off.

A quiet chip for the [Omarchy](https://omarchy.org/) Quattro bar. It does not start or stop WireGuard; it just tells you whether a tunnel is actually connected.

Plugin id: `io.github.swadowmaster.wireguard`

## How it works

The QML widget does not talk to WireGuard itself. Every 3 seconds it runs the bundled `status.py` with `python3` and reads one JSON object from stdout:

```json
{ "active": [{ "iface": "wg0", "ip": "10.0.10.2", "endpoint": "203.0.113.10:51820" }] }
```

`status.py` is read-only. It never brings a tunnel up or down, never writes a config, and never uses sudo.

How it decides what is connected:

1. Collect candidate names from `*.conf` in `/etc/wireguard` and `~/.config/wireguard` (the filename without `.conf` is the interface name).
2. Add interfaces that are already running: `wg show interfaces` if `wg` is installed, otherwise `ip link show type wireguard`.
3. Keep a name only if that link is `UP` and has an IPv4 address.
4. Optionally attach the peer endpoint from `wg show <iface> endpoints`.

Commands are called as `/usr/bin/ip` and `/usr/bin/wg`. If `wg` is missing, names and IPs still work via `ip`; endpoints are then omitted.

The bar shows `iface ip` for each active tunnel, separated by `·`. Hover shows the same data plus endpoints. If `active` is empty, the widget sets its width to zero and disappears. It comes back when a tunnel gets an address.

This plugin does not replace Omarchy's network widget. It only reports WireGuard.

## Install

Omarchy 4 (Quattro) only.

```bash
omarchy plugin add https://github.com/SwadowMaster/omarchy-wireguard.git --enable
```

Optional placement:

```bash
omarchy bar move io.github.swadowmaster.wireguard --section right --before omarchy.network
```

## Remove

```bash
omarchy plugin remove io.github.swadowmaster.wireguard
```

That disables the widget and deletes the git checkout. It does not change WireGuard configs or other Omarchy settings.

## Requirements

- Omarchy 4 (Quattro)
- `python3`
- `ip` (iproute2)
- `wg` from `wireguard-tools` (optional; used when present for interface names and endpoints)

## License

MIT. See [LICENSE](LICENSE).
