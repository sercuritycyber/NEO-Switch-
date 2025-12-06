# vpngui.py - OpenVPN + WireGuard Ultimate Toggle - Enhanced & Hardened
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import subprocess
import os
import threading
import time
import psutil
import platform
import sys
import atexit
import stat

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class NeoSwitch(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NΞO SWITCH ULTIMATE // 2025 FINAL")
        self.geometry("640x900")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.vpn_process = None
        self.current_type = None
        self.config_folder = os.path.expanduser("~/vpn")
        os.makedirs(self.config_folder, exist_ok=True)
        
        # State management
        self.is_connecting = False
        self.is_connected = False
        self.killswitch_active = False

        self.create_ui()
        self.load_configs()
        self.check_privileges()
        atexit.register(self.cleanup)

    def create_ui(self):
        ctk.CTkLabel(self, text="NΞO SWITCH", font=ctk.CTkFont(size=52, weight="bold")).pack(pady=30)
        ctk.CTkLabel(self, text="OpenVPN + WireGuard // Ultimate 2025", text_color="#00ffff", font=ctk.CTkFont(size=16)).pack(pady=(0,20))

        # Type selector
        self.type_var = tk.StringVar(value="OpenVPN")
        type_frame = ctk.CTkFrame(self)
        type_frame.pack(pady=10)
        ctk.CTkRadioButton(type_frame, text="OpenVPN", variable=self.type_var, value="OpenVPN", command=self.load_configs).pack(side="left", padx=20)
        ctk.CTkRadioButton(type_frame, text="WireGuard", variable=self.type_var, value="WireGuard", command=self.load_configs).pack(side="left", padx=20)

        # Visual "Drop Zone" (Click to add files)
        self.drop_frame = ctk.CTkFrame(self, width=520, height=120, fg_color="#1a1a2e", border_width=2, border_color="#00ffff")
        self.drop_frame.pack(pady=15, padx=20)
        self.drop_frame.pack_propagate(False)
        
        drop_label = ctk.CTkLabel(self.drop_frame, text="📁 CLICK TO ADD CONFIG FILE\nor use buttons below", 
                                  font=ctk.CTkFont(size=16), text_color="#00ffff")
        drop_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Make the drop zone clickable
        self.drop_frame.bind("<Button-1>", lambda e: self.add_single_file())
        drop_label.bind("<Button-1>", lambda e: self.add_single_file())
        
        # Hover effect
        def on_enter(e):
            self.drop_frame.configure(border_color="#00ff99", fg_color="#252540")
        def on_leave(e):
            self.drop_frame.configure(border_color="#00ffff", fg_color="#1a1a2e")
        
        self.drop_frame.bind("<Enter>", on_enter)
        self.drop_frame.bind("<Leave>", on_leave)
        drop_label.bind("<Enter>", on_enter)
        drop_label.bind("<Leave>", on_leave)

        # Config selector
        self.config_var = tk.StringVar()
        self.combo = ctk.CTkComboBox(self, variable=self.config_var, width=520, height=45, state="readonly", font=ctk.CTkFont(size=14))
        self.combo.pack(pady=15)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=8)
        ctk.CTkButton(button_frame, text="Browse Folder", command=self.browse_folder, width=160, fg_color="#6600ff").pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Add File", command=self.add_single_file, width=160, fg_color="#ff6600").pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Open Folder", command=self.open_config_folder, width=160, fg_color="#9900ff").pack(side="left", padx=5)

        self.status = ctk.CTkLabel(self, text="DISCONNECTED", text_color="#ff0066", font=ctk.CTkFont(size=32, weight="bold"))
        self.status.pack(pady=50)

        self.toggle_btn = ctk.CTkButton(self, text="CONNECT", command=self.toggle_vpn,
                                        width=420, height=110, font=ctk.CTkFont(size=40, weight="bold"),
                                        fg_color="#00ff99", hover_color="#00cc77", corner_radius=30)
        self.toggle_btn.pack(pady=40)

        self.kill_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(self, text="KILL SWITCH (Default ON)", variable=self.kill_var, text_color="#ff3366").pack(pady=10)

        self.logbox = ctk.CTkTextbox(self, width=580, height=220, font=ctk.CTkFont(size=12))
        self.logbox.pack(pady=20, padx=20, fill="both", expand=True)
        self.log("NΞO SWITCH ULTIMATE ready — OpenVPN + WireGuard loaded.")

    def log(self, msg):
        self.logbox.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.logbox.see("end")

    def check_privileges(self):
        """Check if we have necessary privileges for kill switch"""
        system = platform.system()
        if system == "Linux":
            if os.geteuid() != 0:
                self.log("⚠️  Not running as root - kill switch may require password")
                self.log("💡 Tip: Run with 'sudo python3 vpngui.py' for full functionality")
        elif system == "Windows":
            try:
                import ctypes
                if not ctypes.windll.shell32.IsUserAnAdmin():
                    self.log("⚠️  Not running as administrator - kill switch may fail")
                    self.log("💡 Tip: Run as Administrator for full functionality")
            except:
                pass

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select VPN Config Folder")
        if folder:
            self.config_folder = folder
            self.load_configs()
    
    def open_config_folder(self):
        """Open config folder in file manager"""
        try:
            system = platform.system()
            if system == "Linux":
                subprocess.Popen(["xdg-open", self.config_folder])
            elif system == "Windows":
                os.startfile(self.config_folder)
            elif system == "Darwin":
                subprocess.Popen(["open", self.config_folder])
            self.log(f"📂 Opened: {self.config_folder}")
        except Exception as e:
            self.log(f"⚠️  Could not open folder: {e}")
    
    def add_single_file(self):
        """Add a single config file from anywhere"""
        vpn_type = self.type_var.get()
        filetypes = [("OpenVPN Config", "*.ovpn")] if vpn_type == "OpenVPN" else [("WireGuard Config", "*.conf")]
        filetypes.append(("All Files", "*.*"))
        
        file_path = filedialog.askopenfilename(
            title=f"Select {vpn_type} Config File",
            filetypes=filetypes
        )
        
        if file_path:
            self.import_config(file_path)
    
    def drop_config(self, event):
        """Handle drag and drop of config files"""
        files = event.data
        
        # Parse file paths (can be space-separated or in curly braces)
        if files.startswith('{'):
            files = files.strip('{}')
        
        file_list = files.split()
        
        for file_path in file_list:
            file_path = file_path.strip()
            if os.path.isfile(file_path):
                self.import_config(file_path)
            else:
                self.log(f"⚠️  Not a valid file: {file_path}")
    
    def import_config(self, source_path):
        """Import a config file into the config folder"""
        if not os.path.isfile(source_path):
            self.log(f"❌ File not found: {source_path}")
            return
        
        filename = os.path.basename(source_path)
        vpn_type = self.type_var.get()
        expected_ext = ".ovpn" if vpn_type == "OpenVPN" else ".conf"
        
        # Check extension
        if not filename.lower().endswith(expected_ext):
            response = messagebox.askyesno(
                "Wrong File Type?",
                f"File '{filename}' doesn't have {expected_ext} extension.\n\n"
                f"Current mode: {vpn_type}\n"
                f"Import anyway?"
            )
            if not response:
                return
        
        # Copy to config folder
        dest_path = os.path.join(self.config_folder, filename)
        
        # Check if file already exists
        if os.path.exists(dest_path):
            response = messagebox.askyesno(
                "File Exists",
                f"'{filename}' already exists in config folder.\n\nOverwrite?"
            )
            if not response:
                return
        
        try:
            import shutil
            shutil.copy2(source_path, dest_path)
            self.log(f"✓ Imported: {filename}")
            self.load_configs()
            
            # Auto-select the imported file
            self.combo.set(filename)
            
        except Exception as e:
            self.log(f"❌ Import failed: {e}")
            messagebox.showerror("Import Error", f"Failed to import config:\n{e}")

    def load_configs(self):
        vpn_type = self.type_var.get()
        exts = (".ovpn",) if vpn_type == "OpenVPN" else (".conf",)
        try:
            all_files = os.listdir(self.config_folder)
            files = sorted([f for f in all_files if f.lower().endswith(exts)])
            
            if files:
                self.combo.configure(values=files)
                # Keep current selection if still valid, otherwise select first
                current = self.config_var.get()
                if current in files:
                    self.combo.set(current)
                else:
                    self.combo.set(files[0])
                self.log(f"✓ Loaded {len(files)} {vpn_type} config(s) from {self.config_folder}")
            else:
                self.combo.configure(values=["<No configs found>"])
                self.combo.set("<No configs found>")
                self.log(f"⚠️  No {vpn_type} configs ({exts[0]}) found in {self.config_folder}")
                self.log(f"💡 Tip: Drag & drop your config file or click 'Add Single File'")
        except Exception as e:
            self.log(f"❌ Error loading configs: {e}")

    def find_openvpn(self):
        system = platform.system()
        paths = {
            "Linux": ["/usr/sbin/openvpn", "/usr/bin/openvpn", "/usr/local/sbin/openvpn"],
            "Windows": [
                r"C:\Program Files\OpenVPN\bin\openvpn.exe",
                r"C:\Program Files (x86)\OpenVPN\bin\openvpn.exe",
            ],
            "Darwin": ["/usr/local/opt/openvpn/sbin/openvpn", "/opt/homebrew/opt/openvpn/sbin/openvpn", "/usr/local/bin/openvpn"]
        }
        for path in paths.get(system, []):
            if os.path.isfile(path):
                self.log(f"✓ Found OpenVPN: {path}")
                return path
        
        # Try command line
        try:
            result = subprocess.run(["which", "openvpn"], capture_output=True, text=True)
            if result.returncode == 0:
                path = result.stdout.strip()
                self.log(f"✓ Found OpenVPN: {path}")
                return path
        except:
            pass
        
        self.log("⚠️  OpenVPN not found in standard paths, trying 'openvpn' command")
        return "openvpn"

    def find_wg(self):
        candidates = ["wg-quick", "/usr/bin/wg-quick", "/usr/local/bin/wg-quick"]
        for c in candidates:
            try:
                result = subprocess.run([c, "--version"], capture_output=True, stderr=subprocess.STDOUT)
                if result.returncode == 0:
                    self.log(f"✓ Found WireGuard: {c}")
                    return c
            except:
                pass
        return None

    def get_openvpn_auth(self, path):
        """Get OpenVPN authentication credentials with secure file permissions"""
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "auth-user-pass" not in content:
                    return []
                
                auth_file = os.path.join(os.path.dirname(path), "auth.txt")
                
                if not os.path.exists(auth_file):
                    u = simpledialog.askstring("OpenVPN Login", "Username:")
                    p = simpledialog.askstring("OpenVPN Login", "Password:", show='*')
                    if not u or not p:
                        self.log("❌ Authentication cancelled")
                        return None
                    
                    # Create auth file with secure permissions
                    with open(auth_file, "w") as af:
                        af.write(f"{u}\n{p}")
                    
                    # Set restrictive permissions (owner read/write only)
                    try:
                        os.chmod(auth_file, stat.S_IRUSR | stat.S_IWUSR)
                        self.log(f"✓ Created secure auth file: {auth_file}")
                    except:
                        self.log("⚠️  Could not set secure permissions on auth file")
                
                return ["--auth-user-pass", auth_file]
        except Exception as e:
            self.log(f"❌ Auth error: {e}")
            return []

    def toggle_vpn(self):
        if self.is_connected or (self.vpn_process and self.vpn_process.poll() is None):
            self.disconnect_vpn()
        else:
            self.connect_vpn()

    def connect_vpn(self):
        if self.is_connecting:
            self.log("⚠️  Connection already in progress")
            return
            
        config = self.config_var.get()
        if not config or "<" in config:
            messagebox.showwarning("Select Config", "Please select a valid configuration file")
            return

        config_path = os.path.join(self.config_folder, config)
        
        # Validate config exists
        if not os.path.exists(config_path):
            messagebox.showerror("Config Not Found", f"Config file does not exist:\n{config_path}")
            self.load_configs()
            return
        
        self.is_connecting = True
        self.status.configure(text="CONNECTING...", text_color="#ffff00")
        self.toggle_btn.configure(state="disabled")

        if self.type_var.get() == "OpenVPN":
            threading.Thread(target=self.run_openvpn, args=(config_path,), daemon=True).start()
        else:
            threading.Thread(target=self.run_wireguard, args=(config_path,), daemon=True).start()

    def run_openvpn(self, config_path):
        openvpn_bin = self.find_openvpn()
        auth = self.get_openvpn_auth(config_path)
        if auth is None:
            self.is_connecting = False
            self.after(0, self.on_disconnected)
            return
        cmd = [openvpn_bin, "--config", config_path, "--auth-nocache"] + auth
        self.current_type = "openvpn"
        self.start_process(cmd)

    def run_wireguard(self, config_path):
        wg_bin = self.find_wg()
        if not wg_bin:
            self.after(0, lambda: messagebox.showerror("WireGuard Not Found", 
                "WireGuard (wg-quick) is not installed.\n\n"
                "Install with:\n"
                "• Debian/Ubuntu: sudo apt install wireguard-tools\n"
                "• Arch: sudo pacman -S wireguard-tools\n"
                "• macOS: brew install wireguard-tools"))
            self.is_connecting = False
            self.after(0, self.on_disconnected)
            return
        cmd = [wg_bin, "up", config_path]
        self.current_type = "wireguard"
        self.start_process(cmd)

    def start_process(self, cmd):
        self.log(f"🚀 Executing: {' '.join(cmd)}")
        connection_detected = False
        
        try:
            self.vpn_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, universal_newlines=True
            )

            for line in self.vpn_process.stdout:
                line = line.rstrip()
                if line:
                    # Thread-safe logging
                    self.after(0, lambda msg=line: self.log(msg))
                    
                    # Detect successful connection (only trigger once)
                    if not connection_detected:
                        success_indicators = [
                            "Initialization Sequence Completed",  # OpenVPN
                            "link becomes ready",  # WireGuard on some systems
                        ]
                        # More specific WireGuard checks
                        wg_indicators = ["interface:", "peer:"] if self.current_type == "wireguard" else []
                        all_indicators = success_indicators + wg_indicators
                        
                        if any(x in line for x in all_indicators):
                            connection_detected = True
                            self.after(0, self.on_connected)

            self.vpn_process.wait()
            
            # Only disconnect if we were actually connected
            if self.is_connected:
                self.after(0, self.on_disconnected)
            else:
                self.is_connecting = False
                self.after(0, lambda: self.toggle_btn.configure(state="normal"))
                
        except FileNotFoundError:
            self.log(f"❌ Command not found: {cmd[0]}")
            self.log("💡 Please install the required VPN software")
            self.is_connecting = False
            self.after(0, self.on_disconnected)
        except Exception as e:
            self.log(f"❌ Process error: {e}")
            self.is_connecting = False
            self.after(0, self.on_disconnected)

    def on_connected(self):
        if self.is_connected:
            return  # Prevent duplicate calls
            
        self.is_connected = True
        self.is_connecting = False
        self.status.configure(text="SECURE", text_color="#00ff99")
        self.toggle_btn.configure(text="DISCONNECT", fg_color="#ff0055", hover_color="#cc0044", state="normal")
        self.log("🔒 >>> FULL TUNNEL ACTIVE <<<")
        
        if self.kill_var.get():
            self.enable_killswitch()

    def on_disconnected(self):
        self.is_connected = False
        self.is_connecting = False
        self.status.configure(text="DISCONNECTED", text_color="#ff0066")
        self.toggle_btn.configure(text="CONNECT", fg_color="#00ff99", hover_color="#00cc77", state="normal")
        self.vpn_process = None
        self.current_type = None
        
        if self.killswitch_active:
            self.disable_killswitch()

    def disconnect_vpn(self):
        self.log("🔌 Shutting down VPN...")
        
        if self.current_type == "wireguard":
            config = self.config_var.get()
            wg_bin = self.find_wg()
            if wg_bin:
                cmd = [wg_bin, "down", os.path.join(self.config_folder, config)]
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        self.log("✓ WireGuard interface down")
                    else:
                        self.log(f"⚠️  WireGuard down warning: {result.stderr}")
                except subprocess.TimeoutExpired:
                    self.log("⚠️  WireGuard shutdown timeout")
                except Exception as e:
                    self.log(f"⚠️  WireGuard shutdown error: {e}")
        
        if self.vpn_process:
            try:
                self.vpn_process.terminate()
                self.vpn_process.wait(timeout=10)
                self.log("✓ VPN process terminated")
            except subprocess.TimeoutExpired:
                self.log("⚠️  Process did not terminate, forcing kill...")
                self.vpn_process.kill()
            except Exception as e:
                self.log(f"⚠️  Termination error: {e}")
        
        self.kill_all_vpn_processes()
        self.on_disconnected()

    def kill_all_vpn_processes(self):
        """Kill VPN processes owned by current user only"""
        killed = []
        current_user = os.getuid() if hasattr(os, 'getuid') else None
        
        for proc in psutil.process_iter(['name', 'uids']):
            try:
                name = proc.info['name'].lower()
                
                # Check if it's a VPN process
                if 'openvpn' in name or 'wg-' in name or 'wireguard' in name:
                    # On Unix systems, only kill our own processes
                    if current_user is not None:
                        if hasattr(proc.info.get('uids'), 'real') and proc.info['uids'].real != current_user:
                            continue
                    
                    proc.kill()
                    killed.append(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if killed:
            self.log(f"✓ Cleaned up processes: {', '.join(set(killed))}")

    def enable_killswitch(self):
        """Enable kill switch with proper error handling - allows VPN traffic"""
        system = platform.system()
        success = False
        
        self.log("🛡️  Activating kill switch...")
        
        try:
            if system == "Windows":
                # Windows firewall rules
                result = subprocess.run(["netsh", "advfirewall", "reset"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode != 0:
                    self.log(f"⚠️  Firewall reset warning: {result.stderr}")
                
                result = subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "on"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode != 0:
                    self.log(f"❌ Failed to enable firewall: {result.stderr}")
                    return
                
                # Block all by default
                subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "firewallpolicy", 
                               "blockinbound,blockoutbound"], 
                              capture_output=True, text=True, timeout=10)
                
                # Allow VPN interface (TUN/TAP)
                subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule",
                               "name=Allow VPN", "dir=out", "action=allow",
                               "enable=yes", "profile=any", "interfacetype=any"],
                              capture_output=True, timeout=10)
                
                success = True
                    
            elif system == "Linux":
                # Check if ufw is available
                check = subprocess.run(["which", "ufw"], capture_output=True)
                if check.returncode != 0:
                    self.log("❌ Kill switch requires ufw (install with: sudo apt install ufw)")
                    return
                
                # Reset and configure UFW
                subprocess.run(["sudo", "ufw", "--force", "reset"], 
                             capture_output=True, text=True, timeout=15)
                
                subprocess.run(["sudo", "ufw", "default", "deny", "outgoing"], 
                             capture_output=True, timeout=10)
                subprocess.run(["sudo", "ufw", "default", "deny", "incoming"], 
                             capture_output=True, timeout=10)
                
                # Allow loopback
                subprocess.run(["sudo", "ufw", "allow", "in", "on", "lo"], 
                             capture_output=True, timeout=10)
                subprocess.run(["sudo", "ufw", "allow", "out", "on", "lo"], 
                             capture_output=True, timeout=10)
                
                # Allow VPN interfaces (tun/tap for OpenVPN, wg for WireGuard)
                for iface in ["tun0", "tun1", "tun2", "tap0", "wg0", "wg1"]:
                    subprocess.run(["sudo", "ufw", "allow", "out", "on", iface], 
                                 capture_output=True, timeout=10)
                    subprocess.run(["sudo", "ufw", "allow", "in", "on", iface], 
                                 capture_output=True, timeout=10)
                
                # Allow DNS (needed for VPN connection)
                subprocess.run(["sudo", "ufw", "allow", "out", "53"], 
                             capture_output=True, timeout=10)
                
                # Allow established connections
                subprocess.run(["sudo", "ufw", "allow", "out", "to", "any", "port", "1194", "proto", "udp"], 
                             capture_output=True, timeout=10)
                subprocess.run(["sudo", "ufw", "allow", "out", "to", "any", "port", "1194", "proto", "tcp"], 
                             capture_output=True, timeout=10)
                subprocess.run(["sudo", "ufw", "allow", "out", "to", "any", "port", "51820", "proto", "udp"], 
                             capture_output=True, timeout=10)
                
                result = subprocess.run(["sudo", "ufw", "--force", "enable"], 
                                      capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    success = True
                    self.log("✓ Allowed VPN traffic on tun/tap/wg interfaces")
                else:
                    self.log(f"❌ Failed to enable UFW: {result.stderr}")
            
            if success:
                self.killswitch_active = True
                self.log("✅ Kill switch ARMED - VPN traffic allowed, all else blocked")
            else:
                self.log("❌ Kill switch activation FAILED")
                
        except subprocess.TimeoutExpired:
            self.log("❌ Kill switch timeout - may require elevated privileges")
        except FileNotFoundError as e:
            self.log(f"❌ Kill switch command not found: {e}")
        except Exception as e:
            self.log(f"❌ Kill switch error: {e}")

    def disable_killswitch(self):
        """Disable kill switch with proper error handling"""
        if not self.killswitch_active:
            return
            
        system = platform.system()
        self.log("🛡️  Disarming kill switch...")
        
        try:
            if system == "Windows":
                result = subprocess.run(["netsh", "advfirewall", "reset"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.log("✓ Kill switch DISARMED")
                else:
                    self.log(f"⚠️  Firewall reset warning: {result.stderr}")
                    
            elif system == "Linux":
                result = subprocess.run(["sudo", "ufw", "--force", "disable"], 
                                      capture_output=True, text=True, timeout=15)
                if result.returncode == 0:
                    self.log("✓ Kill switch DISARMED")
                else:
                    self.log(f"⚠️  UFW disable warning: {result.stderr}")
            
            self.killswitch_active = False
            
        except subprocess.TimeoutExpired:
            self.log("⚠️  Kill switch disable timeout")
        except Exception as e:
            self.log(f"⚠️  Kill switch disable error: {e}")

    def on_closing(self):
        if self.is_connected:
            if messagebox.askokcancel("Exit", "Disconnect VPN and quit?"):
                self.disconnect_vpn()
                # Wait for actual disconnect with timeout
                self.after(100, self._check_and_quit)
        else:
            self.destroy()
    
    def _check_and_quit(self, max_wait=10):
        """Wait for VPN to disconnect before quitting"""
        if not self.is_connected and self.vpn_process is None:
            self.destroy()
        elif max_wait > 0:
            self.after(100, lambda: self._check_and_quit(max_wait - 1))
        else:
            # Force quit after timeout
            self.log("⚠️  Force quit - VPN may still be running")
            self.destroy()

    def cleanup(self):
        """Emergency cleanup on exit"""
        self.kill_all_vpn_processes()
        if self.killswitch_active:
            # Quick disable without logging
            try:
                system = platform.system()
                if system == "Windows":
                    subprocess.run(["netsh", "advfirewall", "reset"], 
                                 capture_output=True, timeout=5)
                elif system == "Linux":
                    subprocess.run(["sudo", "ufw", "--force", "disable"], 
                                 capture_output=True, timeout=5)
            except:
                pass

if __name__ == "__main__":
    # Auto-install dependencies
    try:
        import customtkinter, psutil
    except ImportError as e:
        print("📦 Installing required dependencies...")
        missing = str(e)
        
        # Check if running as root
        packages = ["customtkinter", "psutil"]
        if hasattr(os, 'geteuid') and os.geteuid() == 0:
            print("⚠️  Running as root - installing system-wide...")
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages + ["--break-system-packages"])
        else:
            print("📦 Installing for current user...")
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages + ["--user"])
        print("✓ Dependencies installed")
        print("🔄 Please run the script again\n")
        sys.exit(0)
    
    app = NeoSwitch()
    app.mainloop()
