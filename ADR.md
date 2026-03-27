# ADR: thegent-cli-share

## ADR-001: Python over Rust for CLI Coordination Layer

**Status**: Accepted

**Context**: thegent-cli-share needs to coordinate Python-based agent processes. Implementation language choices: Rust (for performance), Python (for ecosystem fit), Go.

**Decision**: Python, implemented as a library that other Python agent processes import directly.

**Rationale**: thegent agents are Python processes. A Python library is directly importable without IPC overhead. Rust would require a separate daemon process. Python asyncio is sufficient for coordination at the expected scale (< 100 concurrent agents).

**Consequences**: Coordination is in-process for single-host deployments. Multi-host coordination would require a separate service layer (future work).

---

## ADR-002: File-Based State Store for Coordination Primitives

**Status**: Accepted

**Context**: Distributed locks, task queues, and command caches need a shared state store. Options: Redis, PostgreSQL, filesystem with fcntl locks.

**Decision**: Filesystem-based state store using atomic file operations and fcntl advisory locks for single-host deployments.

**Rationale**: No external service dependency. thegent is a local developer tool; Redis/PostgreSQL is overkill. fcntl locks are reliable on Linux/macOS. Filesystem state is inspectable for debugging.

**Consequences**: Not suitable for multi-host deployments without a storage backend swap. Backend is abstracted via a `StateStore` protocol for future Redis adapter.

---

## ADR-003: CQRS for Command and Query Separation

**Status**: Accepted

**Context**: Coordination operations are a mix of state-mutating commands (enqueue, acquire_lock) and queries (get_task_status, list_in_flight). Mixing these leads to complex APIs.

**Decision**: Separate command and query interfaces following CQRS pattern. `CommandBus` for mutations, `QueryBus` for reads.

**Rationale**: Clean separation simplifies testing (queries are read-only and easier to mock). Aligns with thegent hexagonal architecture standard.

**Consequences**: More initial API surface. Justified by the complexity of the coordination domain.
