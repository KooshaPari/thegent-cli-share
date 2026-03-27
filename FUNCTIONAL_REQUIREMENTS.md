# Functional Requirements: thegent-cli-share

## FR-CLI-001: Command Identity
FR-CLI-001a: The library SHALL compute a deterministic command ID by hashing: command string, working directory, and environment variables.
FR-CLI-001b: Command IDs SHALL be stable across agent processes on the same machine.

## FR-CLI-002: Command Deduplication
FR-CLI-002a: When an agent submits a command, the library SHALL check if an identical command is already in-flight.
FR-CLI-002b: If a duplicate in-flight command exists, the submitting agent SHALL wait for the in-flight result instead of executing again.
FR-CLI-002c: Idempotent commands SHALL have their results cached for a configurable TTL (default: 60 seconds).
FR-CLI-002d: Non-idempotent commands (marked with `idempotent=False`) SHALL never be deduplicated.

## FR-CLI-003: Task Queue
FR-CLI-003a: The library SHALL provide `enqueue(task, priority)` and `dequeue() -> Task` operations.
FR-CLI-003b: Tasks with higher priority SHALL be dequeued before lower-priority tasks.
FR-CLI-003c: An idle agent SHALL be able to steal tasks from other agents' assigned queues.
FR-CLI-003d: A failed task SHALL be moved to the dead letter queue after `max_retries` attempts.

## FR-CLI-004: Task Dependencies
FR-CLI-004a: Tasks SHALL support a `depends_on: list[TaskId]` field.
FR-CLI-004b: A task SHALL not be dequeued until all its dependencies have completed successfully.
FR-CLI-004c: Circular dependencies SHALL be detected at enqueue time and rejected with an error.

## FR-CLI-005: Distributed Lock
FR-CLI-005a: `acquire_lock(resource_id, timeout)` SHALL block until the lock is acquired or timeout expires.
FR-CLI-005b: Locks SHALL have a mandatory TTL to prevent deadlock from crashed lock holders.
FR-CLI-005c: Lock acquisition and release SHALL be logged to the audit log.

## FR-CLI-006: Smart Merge
FR-CLI-006a: When two agents attempt to write the same file, the library SHALL detect the conflict.
FR-CLI-006b: The library SHALL attempt a three-way merge using the common ancestor as base.
FR-CLI-006c: If three-way merge fails (conflict), the operation SHALL be flagged for operator review.

## FR-CLI-007: Audit Log
FR-CLI-007a: Every coordination operation SHALL be logged with: timestamp, agent_id, operation_type, resource_id, outcome.
FR-CLI-007b: The audit log SHALL be queryable by agent_id and time range.
FR-CLI-007c: The audit log SHALL be durable (written to disk, not only in-memory).
