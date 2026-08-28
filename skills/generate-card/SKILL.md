---
name: generate-card
description: Create a complete Machi Koro-style card in this repository, from collecting card parameters and generating prompt-driven artwork through a reproducible card command, rendered preview, and user-directed refinements. Use when adding or iterating on a card rather than making an isolated compositor-code change.
---

# Generate Card

Build one card end to end while preserving the repository's prompt, asset, and command conventions.

## Collect the card specification

Inspect existing backgrounds, prompts, icons, fonts, and `card-commands/` first. Ask one concise grouped question for any parameters the user has not already supplied:

- filesystem-safe card slug and displayed title;
- card family/background color;
- activation number and single-digit coin cost;
- exact rules text and intended line breaks;
- central subject and its culturally diagnostic details;
- existing category icon to reuse, a new icon subject, or no icon;
- any requested layout, palette, shadow, or orientation differences.

Do not make paid or time-consuming image-generation calls until the necessary content choices are known. Do not re-ask values already stated by the user. Default to the standard shadow and the closest existing card's typography/layout when the user has no preference.

## Create filled prompts

Create `prompts/central-illustrations/<card-slug>.json` from `prompts/central-illustration.json`. Replace every content placeholder and retain the stable composition/rendering rules. A restrained palette adaptation may harmonize with the selected background.

Central illustrations have an absolute no-text rule. They must contain no letters, numbers, names, prices, menus, labels, signs, logos, graffiti, license-plate characters, or pseudo-writing on any surface. Avoid even blank signboards or menu boards when their presence invites generated text; prefer plain fascia and geometric color panels.

Buildings and storefronts should face slightly to the right, showing their front and right side in a readable three-quarter view. Generate the desired orientation directly. Do not add `--flip-horizontal` merely to correct direction; use it only when the user explicitly requests mirroring during refinement.

For a new icon, create `prompts/icons/<icon-slug>.json` from `prompts/building-type-icon.json`. Follow the v1.1 badge convention: a footer-colored circle covering roughly 82–88% of the square canvas, with a centered white pictogram covering roughly 50–58% of the circle. Sample the unobstructed footer when an exact color is needed. Reuse an existing icon when its category already fits.

Validate every filled JSON and ensure it contains no unresolved `{{...}}` placeholders.

## Generate and validate assets

Use the installed image-generation skill/tool for raster generation and follow its project-save and transparency rules.

Generate the central illustration from scratch from its filled prompt and save the selected RGBA PNG as `buildings/<card-slug>.png`. Inspect it before continuing. Reject and regenerate artwork containing any text-like marks, an opaque backdrop, incorrect orientation, clipped content, or a full-card composition.

When a new icon is needed, generate it from its filled prompt and save it as `icons/<icon-slug>.png`. Confirm actual alpha transparency outside the circular badge and no transparency holes inside the badge. Reject background-removal artifacts, missing circles, low-contrast pictograms, and text.

Do not silently overwrite an existing source asset unless the user requested regeneration or replacement.

## Create the reproducible card command

Create `card-commands/<card-slug>.sh`, using the closest existing command as a layout reference. Commands run from the repository root and must invoke the packaged compositor:

```bash
python skills/generate-card/scripts/card_compositor.py \
  --template backgrounds/<color>.png \
  --overlay buildings/<card-slug>.png \
  --output cards/<card-slug>.png
```

Add the confirmed icon, title, activation number, coin cost, exact rules text, fonts, colors, scale, position, and shadow options. Preserve requested newlines with Bash `$'...\n...'` quoting. Omit `--flip-horizontal` by default because generated buildings should already face right.

Run `bash -n card-commands/<card-slug>.sh`, then execute it. Use the packaged `scripts/card_compositor.py`; when compositor behavior changes, keep the repository-root copy and packaged copy synchronized.

## Preview and refine

Inspect `cards/<card-slug>.png`. Correct objective defects such as missing assets, clipping, overflow, unreadable contrast, wrong orientation, or unintended text before presenting it. Keep every reproducible adjustment in the card command rather than applying it only to the output PNG.

Present the rendered card to the user with links to the filled prompts, generated source assets, card command, and output. Briefly state important defaults or judgment calls, then explicitly ask what they want tweaked. Apply requested tweaks, rerun the command, and present the next preview until accepted.
