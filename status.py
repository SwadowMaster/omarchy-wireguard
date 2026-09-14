#!/usr/bin/env python3
"""One-shot JSON status for active WireGuard interfaces."""
import json
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    if cmd and cmd[0] in {"ip", "wg"}:
        cmd[0] = f"/usr/bin/{cmd[0]}"
    return subprocess.run(cmd, capture_output=True, text=True)


def configured_interfaces() -> list[str]:
    names: set[str] = set()
    for directory in (Path("/etc/wireguard"), Path.home() / ".config/wireguard"):
        if not directory.is_dir():
            continue
        for conf in directory.glob("*.conf"):
            names.add(conf.stem)
    return sorted(names)


def running_interfaces() -> list[str]:
    result = run(["wg", "show", "interfaces"])
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip().split()

    names: list[str] = []
    result = run(["ip", "-o", "link", "show", "type", "wireguard"])
    for line in result.stdout.splitlines():
        if ": " not in line:
            continue
        iface = line.split(": ", 1)[1].split("@")[0].split()[0]
        if iface:
            names.append(iface)
    return names


def sort_key(name: str) -> tuple:
    if name.startswith("wg") and name[2:].isdigit():
        return (0, int(name[2:]))
    return (1, name)


def is_up(iface: str) -> bool:
    result = run(["ip", "link", "show", iface])
    return result.returncode == 0 and "UP" in result.stdout


def ipv4(iface: str) -> str | None:
    result = run(["ip", "-4", "-o", "addr", "show", "dev", iface])
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 4:
            return parts[3].split("/")[0]
    return None


def endpoint(iface: str) -> str | None:
    result = run(["wg", "show", iface, "endpoints"])
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            return parts[1]
    return None


def main() -> None:
    active: list[dict[str, str | None]] = []
    names = sorted(set(configured_interfaces()) | set(running_interfaces()), key=sort_key)

    for iface in names:
        if not is_up(iface):
            continue
        ip = ipv4(iface)
        if not ip:
            continue
        active.append({"iface": iface, "ip": ip, "endpoint": endpoint(iface)})

    active.sort(key=lambda entry: sort_key(str(entry["iface"])))
    print(json.dumps({"active": active}, ensure_ascii=False))


if __name__ == "__main__":
    main()
