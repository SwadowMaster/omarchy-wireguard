# WireGuard

Status widget for the [Omarchy](https://omarchy.org/) Quattro bar.

Shows active WireGuard interfaces and their IPv4 addresses. Hover for endpoint details. The widget hides when no tunnel is up.

Plugin id: `io.github.swadowmaster.wireguard`

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

The widget polls every 3 seconds. It reads interface names from `/etc/wireguard` and `~/.config/wireguard` if those directories exist, then checks which ones are up. It does not start, stop, or edit tunnels, and it does not use sudo.

## License

MIT. See [LICENSE](LICENSE).
