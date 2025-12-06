# Contributing to NeoSwitch VPN

First off, thank you for considering contributing to NeoSwitch! 🎉

This document provides guidelines for contributing to this project. Following these guidelines helps maintain quality and makes the contribution process smooth for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)

## 🤝 Code of Conduct

This project follows a simple code of conduct:

- **Be respectful** - Treat everyone with respect and kindness
- **Be constructive** - Provide helpful feedback and suggestions
- **Be patient** - Remember that people have different skill levels and time zones
- **Be inclusive** - Welcome contributors from all backgrounds
- **No harassment** - Zero tolerance for harassment, discrimination, or abuse

By participating, you agree to uphold these principles.

## 🛠️ How Can I Contribute?

### Reporting Bugs

Before creating a bug report:
1. **Check existing issues** to avoid duplicates
2. **Test on the latest version** to ensure the bug still exists
3. **Gather information:**
   - Your OS and version
   - Python version (`python3 --version`)
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages and logs

**Create a bug report:**
- Use the bug report template
- Provide a clear, descriptive title
- Include all relevant information
- Add screenshots if applicable

### Suggesting Enhancements

Feature requests are welcome! Please:
1. **Check if it already exists** in issues or discussions
2. **Explain the use case** - Why is this useful?
3. **Describe the solution** - How should it work?
4. **Consider alternatives** - Are there other approaches?

### Pull Requests

We actively welcome pull requests for:
- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- ⚡ Performance improvements
- 🧪 Test coverage

## 💻 Development Setup

### Prerequisites

```bash
# Python 3.8+
python3 --version

# Git
git --version
```

### Setup Steps

1. **Fork the repository**
   - Click "Fork" on GitHub

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/neoswitch-vpn.git
   cd neoswitch-vpn
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Install dependencies**
   ```bash
   pip install customtkinter psutil
   ```

5. **Make your changes**
   - Write clean, well-commented code
   - Follow the coding standards below
   - Test thoroughly

6. **Test your changes**
   ```bash
   sudo python3 vpngui.py
   ```

## 📤 Pull Request Process

1. **Update documentation** if you're changing functionality
2. **Test on multiple platforms** if possible (Linux, Windows, macOS)
3. **Ensure no merge conflicts** with the main branch
4. **Write a clear PR description:**
   - What does this PR do?
   - Why is this change needed?
   - How has it been tested?
   - Screenshots (for UI changes)

5. **Link related issues** using keywords:
   - `Fixes #123`
   - `Closes #456`
   - `Related to #789`

6. **Wait for review** - Be patient and responsive to feedback

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated (README, docstrings)
- [ ] Tested on at least one platform
- [ ] No new warnings or errors
- [ ] Commit messages follow guidelines

## 🎨 Coding Standards

### Python Style

Follow [PEP 8](https://pep8.org/) with these specifics:

```python
# Good
def connect_vpn(self, config_path):
    """Connect to VPN using the specified config."""
    if not os.path.exists(config_path):
        self.log("❌ Config not found")
        return False
    
    self.is_connecting = True
    # ... rest of code

# Bad
def connectVPN(self,configPath):
    if not os.path.exists(configPath):return False
    self.is_connecting=True
```

### Key Principles

1. **Clarity over cleverness** - Readable code is better than "smart" code
2. **Document the why, not the what** - Comments explain reasoning, not obvious actions
3. **Handle errors gracefully** - Always use try/except for external operations
4. **Log everything** - Use `self.log()` for user-visible events
5. **Thread-safe GUI updates** - Always use `self.after()` for GUI updates from threads

### Naming Conventions

```python
# Variables and functions: snake_case
config_path = "/path/to/config"
def load_configs(self):
    pass

# Classes: PascalCase
class NeoSwitch:
    pass

# Constants: UPPER_CASE
DEFAULT_PORT = 1194
VPN_TIMEOUT = 10

# Private methods: _leading_underscore
def _check_and_quit(self):
    pass
```

### Error Handling

```python
# Good - Specific exceptions, user feedback
try:
    result = subprocess.run(cmd, timeout=10)
    if result.returncode != 0:
        self.log(f"⚠️ Command failed: {result.stderr}")
except subprocess.TimeoutExpired:
    self.log("❌ Operation timed out")
except FileNotFoundError:
    self.log("❌ Command not found")
except Exception as e:
    self.log(f"❌ Unexpected error: {e}")

# Bad - Catches everything, no feedback
try:
    subprocess.run(cmd)
except:
    pass
```

## 📝 Commit Message Guidelines

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance tasks

### Examples

```bash
# Good
feat(killswitch): Add VPN traffic whitelisting
fix(ui): Resolve config dropdown refresh issue
docs(readme): Update installation instructions

# Bad
update stuff
fixed bug
changes
```

### Best Practices

- Use imperative mood ("Add feature" not "Added feature")
- Keep subject line under 50 characters
- Separate subject from body with blank line
- Wrap body at 72 characters
- Reference issues in footer

## 🧪 Testing Guidelines

Before submitting, test:

### Functional Tests

- [ ] OpenVPN connection works
- [ ] WireGuard connection works
- [ ] Kill switch enables/disables correctly
- [ ] Config import works
- [ ] Disconnect works cleanly
- [ ] Error messages are clear

### Platform Tests (if possible)

- [ ] Linux (Debian/Ubuntu/Arch)
- [ ] macOS
- [ ] Windows

### Edge Cases

- [ ] Missing dependencies
- [ ] Invalid config files
- [ ] Network interruption
- [ ] Concurrent connections
- [ ] Kill switch while disconnected

## 🎯 Areas for Contribution

Looking for ideas? Check these:

### Beginner-Friendly
- 📝 Documentation improvements
- 🐛 Bug fixes with clear reproduction steps
- 🎨 UI tweaks and polish
- 🧹 Code cleanup and refactoring

### Intermediate
- ✨ New features from roadmap
- ⚡ Performance optimizations
- 🔒 Security enhancements
- 🧪 Test coverage

### Advanced
- 🏗️ Architecture improvements
- 🌐 Multi-platform compatibility
- 🔌 Plugin system
- 📊 Analytics and telemetry

## 🤔 Questions?

- 💬 Open a [Discussion](https://github.com/securitycyber/neoswitch-vpn/discussions)
- 📧 Email: your.charlie@securitycyber.uk
- 🐛 [Report an Issue]
## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to NeoSwitch!** 🚀
