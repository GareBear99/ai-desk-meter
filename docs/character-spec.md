# Pixel Buddy / “Musing...” Character Spec

The small pixel buddy is part of the product identity and should remain recognizable across the docs, dashboard, and firmware demos.

## Baseline appearance

- compact orange/red pixel body
- small blue feet or lower pixels
- simple blocky silhouette
- displayed under the current/weekly meters
- paired with the status text: `✶ Musing...`

## Current meaning

For the open-source pre-3.0 track, `Musing...` is the general loading/responding state. It covers:

- agent responding to prompt input
- action loading
- provider refresh in progress
- local workflow processing

Later versions may split this into more precise states, but the baseline character and Musing label should stay intact.

## CSS reference

The public page uses the `.pixel-buddy` grid. The goal is not high-detail art; it is a consistent tiny hardware-friendly mascot that can be redrawn on ESP32/Arduino-class displays.


## Asset reference

The repo includes `assets/character/pixel-buddy-musing.svg` as the current scalable reference asset for docs, dashboards, and firmware redraws.
