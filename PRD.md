# PRD: thegent-cli-share — CLI Coordination for Multi-Agent Orchestration

## Overview
`thegent-cli-share` is a Python library providing multi-agent CLI coordination primitives: command deduplication, task queue management, smart merge, and agent synchronization for the thegent system.

## Problem Statement
When multiple thegent agents run concurrently, they may issue duplicate CLI commands, create conflicting file edits, or deadlock on shared resources. `thegent-cli-share` prevents these problems by providing a shared coordination layer.

## Goals
1. Prevent duplicate command execution across concurrent agents
2. Provide a shared task queue for work distribution
3. Smart merge: detect and resolve conflicting file edits
4. Agent-to-agent synchronization primitives (locks, semaphores, barriers)
5. Audit log for all coordinated operations

## Epics

### E1: Command Deduplication
- E1.1: Command identity hashing (deterministic ID for equivalent commands)
- E1.2: In-flight command registry (prevent duplicate execution)
- E1.3: Result caching (share results of idempotent commands)
- E1.4: TTL-based cache invalidation

### E2: Task Queue
- E2.1: Priority queue with agent-assigned work items
- E2.2: Work stealing for idle agents
- E2.3: Task dependency graph (DAG) with execution ordering
- E2.4: Dead letter queue for failed tasks

### E3: Smart Merge
- E3.1: Detect concurrent edits to the same file
- E3.2: Three-way merge for text files
- E3.3: Conflict escalation to human/operator when auto-merge fails
- E3.4: Merge audit log

### E4: Synchronization Primitives
- E4.1: Distributed lock (mutex for critical sections)
- E4.2: Semaphore (rate limiting concurrent operations)
- E4.3: Barrier (coordinate multiple agents to a sync point)

### E5: Audit Log
- E5.1: Structured event log for all coordination operations
- E5.2: Agent identity tracking per operation
- E5.3: Queryable log for debugging coordination issues
