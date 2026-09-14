import QtQuick
import Quickshell
import Quickshell.Io
import qs.Ui
import qs.Commons

BarWidget {
  id: root
  moduleName: "io.github.swadowmaster.wireguard"

  property bool opened: false
  property bool popoutSwitchClosing: false
  property var tunnels: []
  property string tooltip: ""

  readonly property bool connected: tunnels.length > 0
  readonly property string label: {
    if (!connected)
      return ""
    const parts = []
    for (let i = 0; i < tunnels.length; i++) {
      const t = tunnels[i]
      parts.push(t.iface + " " + t.ip)
    }
    return "󰖂 " + parts.join(" · ")
  }

  visible: connected
  implicitWidth: connected ? button.implicitWidth : 0
  implicitHeight: button.implicitHeight

  function open() {}
  function close() {}
  function toggle() {}
  function closeForPopoutSwitch() {}

  function pluginDir() {
    return Qt.resolvedUrl(".").toString().replace("file://", "")
  }

  function parseStatus(raw) {
    try {
      const data = JSON.parse(String(raw || "").trim() || "{\"active\":[]}")
      const list = data.active || []
      tunnels = list
      if (!list.length) {
        tooltip = "WireGuard: disconnected"
        return
      }
      const lines = ["WireGuard activo", ""]
      for (let i = 0; i < list.length; i++) {
        const t = list[i]
        lines.push(t.iface)
        lines.push("  IP: " + t.ip)
        if (t.endpoint)
          lines.push("  Endpoint: " + t.endpoint)
        lines.push("")
      }
      tooltip = lines.join("\n").trim()
    } catch (e) {
      tunnels = []
      tooltip = "WireGuard: status error"
    }
  }

  Process {
    id: poll
    running: true
    command: ["python3", root.pluginDir() + "status.py"]
    stdout: StdioCollector {
      waitForEnd: true
      onStreamFinished: root.parseStatus(text)
    }
    stderr: StdioCollector { waitForEnd: true }
  }

  Timer {
    interval: 3000
    running: true
    repeat: true
    triggeredOnStart: true
    onTriggered: {
      poll.running = false
      poll.running = true
    }
  }

  WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: root.label
    tooltipText: root.tooltip
  }
}
