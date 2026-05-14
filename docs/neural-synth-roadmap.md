# Neural Synth Toggle Roadmap

Neural Synth is a future visualization page for AI Desk Meter. It should be added after the Arc-RAR backend provider and tests are stable.

## Rule

Neural Synth must visualize real provider state. It should not fabricate cognitive activity, receipt links, archive health, or backend status.

## Proposed mappings

| Visual element | Data source |
|---|---|
| Nodes | Providers, sessions, archives, receipts, devices |
| Edges | Receipt/event/session relationships |
| White beads | Normal data flow |
| Yellow beads | Intent/checkpoint matched |
| Red beads | Validation issue or warning |
| Cluster groups | Provider/device/archive categories |

## Views

- Classic Meter View
- Provider Health View
- Archive Timeline View
- Neural Synth View

## Implementation order

1. Add read-only visualization fed by the same `UsagePayload`
2. Add provider/device node rendering
3. Add warning/error bead states
4. Add Arc-RAR archive/receipt graph
5. Add Omnibinary event-spine timeline after the Omnibinary adapter exists
