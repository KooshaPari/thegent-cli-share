# thegent-cli-share

CLI share system for multi-agent orchestration - command deduplication, task queue, smart merge, and coordination.

## Architecture

This crate follows **Hexagonal Architecture** (Ports & Adapters) with **Clean Architecture** layers.

## xDD Methodologies Applied

- **TDD**: Tests written first
- **DDD**: Bounded contexts for command cache, task queue, smart merge
- **SOLID**: Single responsibility per module
- **CQRS**: Separate command and query interfaces
- **EDA**: Domain events for state changes

## Domain Services

### Command Deduplication
Prevents duplicate command execution across agents using SHM-based locks.

### Task Queue
Maildir-style queue for distributed task processing.

### Smart Merge
Mergiraf-style AST-aware merging for conflict resolution.

### Coordination
HLC-based distributed coordination.

## Installation

```bash
pip install thegent-cli-share
```

## CLI Usage

```bash
# Command deduplication
thegent-cli-share lock-acquire <cmd_hash>
thegent-cli-share lock-release <cmd_hash> --pid <pid>
thegent-cli-share lock-list

# Task queue
thegent-cli-share queue-enqueue <command> --priority high
thegent-cli-share queue-list
```

## Python API

```python
from thegent_cli_share.adapters.dedup import InMemoryLockAdapter

adapter = InMemoryLockAdapter()
lock = adapter.acquire("cmd_hash", pid=1234)
```

## License

MIT
