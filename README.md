# NEO-Switch-
opensource wiregard+openvpn GUI 
# 🔐 NΞO SWITCH
### Ultimate VPN Manager for OpenVPN & WireGuard

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A modern, feature-rich GUI for managing OpenVPN and WireGuard connections with built-in kill switch protection.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

</div>

---

## 🌟 Features

- **🔄 Dual VPN Support** - Seamlessly switch between OpenVPN and WireGuard
- **🛡️ Kill Switch** - Blocks all traffic if VPN disconnects (optional)
- **📁 Easy Config Management** - Browse folders or add individual config files
- **🎨 Modern Dark UI** - Clean, cyberpunk-inspired interface
- **🔒 Secure Auth Storage** - Credentials stored with proper file permissions
- **📊 Real-time Logs** - Monitor connection status and debug issues
- **🖥️ Cross-platform** - Works on Linux, Windows, and macOS
- **⚡ Auto-installer** - Automatically installs dependencies
- **🎯 HTB Compatible** - Perfect for HackTheBox and other VPN labs

## 📋 Requirements

- **Python 3.8+**
- **OpenVPN** (for .ovpn configs)
- **WireGuard** (for .conf configs)
- **Root/Admin privileges** (for kill switch functionality)

### Platform-Specific Requirements

**Linux:**
```bash
sudo apt install openvpn wireguard-tools ufw  # Debian/Ubuntu
sudo pacman -S openvpn wireguard-tools ufw     # Arch
```

**macOS:**
```bash
brew install openvpn wireguard-tools
```

**Windows:**
- Download [OpenVPN](https://openvpn.net/community-downloads/)
- Download [WireGuard](https://www.wireguard.com/install/)

## 🚀 Installation

### Quick Start (Linux/macOS)

```bash
# Clone the repository
git clone https://github.com/yourusername/neoswitch-vpn.git
cd neoswitch-vpn

# Run with auto-install (Linux)
sudo python3 vpngui.py

# Or macOS
sudo python3 vpngui.py
```

### Windows

```powershell
# Clone the repository
git clone https://github.com/yourusername/neoswitch-vpn.git
cd neoswitch-vpn

# Run as Administrator
python vpngui.py
```

### Manual Dependency Installation

```bash
pip install customtkinter psutil --break-system-packages
```

## 💻 Usage

### Basic Operation

1. **Launch the app:**
   ```bash
   sudo python3 vpngui.py  # Linux/macOS
   ```

2. **Select VPN type:**
   - Choose **OpenVPN** or **WireGuard** using radio buttons

3. **Add config files:**
   - Click the big **drop zone** to browse for a config file
   - Click **"Add File"** to import from anywhere
   - Click **"Browse Folder"** to select a folder with multiple configs
   - Click **"Open Folder"** to manually add files to `~/vpn/`

4. **Connect:**
   - Select your config from the dropdown
   - Click **CONNECT**
   - Enter credentials if prompted (OpenVPN only)

5. **Kill Switch:**
   - Enabled by default
   - Blocks all non-VPN traffic
   - Uncheck to disable

### Default Config Location

Configs are stored in: `~/vpn/`
- `.ovpn` files for OpenVPN
- `.conf` files for WireGuard

### Kill Switch Behavior

When enabled, the kill switch:
- ✅ Allows traffic through VPN tunnel (tun/tap/wg interfaces)
- ✅ Allows DNS (port 53)
- ✅ Allows common VPN ports (1194, 51820)
- ❌ Blocks all other traffic
- 🔒 Protects you if VPN disconnects unexpectedly

## 📸 Screenshots

```
┌────────────────────────────────────────┐
│           NΞO SWITCH                   │
│   OpenVPN + WireGuard // Ultimate 2025 │
├────────────────────────────────────────┤
│  ● OpenVPN    ○ WireGuard              │
├────────────────────────────────────────┤
│  📁 CLICK TO ADD CONFIG FILE           │
│     or use buttons below               │
├────────────────────────────────────────┤
│  [my-htb-lab.ovpn          ▼]          │
│  [Browse] [Add File] [Open Folder]     │
├────────────────────────────────────────┤
│            SECURE ✓                    │
├────────────────────────────────────────┤
│       [    DISCONNECT    ]             │
│                                        │
│  ☑ KILL SWITCH (Default ON)           │
├────────────────────────────────────────┤
│  [12:34:56] ✓ Loaded 3 configs        │
│  [12:34:57] 🚀 Executing: openvpn...  │
│  [12:34:58] 🔒 >>> FULL TUNNEL <<<    │
│  [12:34:58] 🛡️ Kill switch ARMED      │
└────────────────────────────────────────┘
```

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'customtkinter'"
Run with sudo to install system-wide:
```bash
sudo pip install customtkinter psutil --break-system-packages
```

### "Kill switch requires ufw"
Install UFW firewall:
```bash
sudo apt install ufw
```

### "OpenVPN not found"
Install OpenVPN:
```bash
sudo apt install openvpn  # Debian/Ubuntu
brew install openvpn      # macOS
```

### VPN connects but no internet
- Make sure **Kill Switch is enabled** (it now allows VPN traffic)
- Check VPN config is valid
- Verify DNS settings

### Permission denied errors
Run with elevated privileges:
```bash
sudo python3 vpngui.py
```

## 🤝 Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Code of conduct
- Development setup
- Pull request process
- Coding standards

### Quick Contribution Guide

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is provided for educational and legitimate VPN management purposes only. Users are responsible for:
- Complying with their VPN provider's terms of service
- Following local laws and regulations
- Using VPN services ethically and legally

The developers are not responsible for misuse of this software.

## 🙏 Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Inspired by the need for a modern VPN management tool
- Thanks to the HackTheBox community for testing feedback

## 📞 Support

- 🐛 [Report a Bug](https://github.com/securitycyber/neoswitch-vpn/issues)
- 💡 [Request a Feature](https://github.com/securitycyber/neoswitch-vpn/issues)
- 💬 [Discussions](https://github.com/securitycyber/neoswitch-vpn/discussions)

## 🗺️ Roadmap

- [ ] Auto-reconnect on disconnect
- [ ] Multiple simultaneous VPN connections
- [ ] Config file encryption
- [ ] Built-in speed test
- [ ] Server location map
- [ ] Connection profiles/favorites
- [ ] System tray integration
- [ ] Import configs from URLs

---

<div align="center">

**Made with ❤️ for the cybersecurity community**

⭐ Star this repo if you find it useful!

</div>
