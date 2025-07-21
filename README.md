# PPSP Protocol Simulation

Simulates the **Pass-Pass-Steal-Pass (PPSP)** protocol using Python + SimPy.

## What is PPSP?

- Messages traverse a 4-node line (A→B→C→D).
- At each hop, with probability `p`, the node “steals” and re-encrypts (adds a fingerprint).
- Upon reaching D, an ACK retraces the fingerprint chain, stamping a “clap”.

## Setup & Usage

```bash
pip install simpy numpy pandas matplotlib pytest pytest-cov
