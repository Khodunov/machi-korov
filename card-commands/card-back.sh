#!/usr/bin/env bash
# Shared card back for the whole deck.
#
# Unlike the other card commands this one does not call card_compositor.py:
# the back is a full-bleed card face rather than a template plus a floating
# overlay, so it is drawn directly. Spec: prompts/card-back.json

python card-back/generate_card_back.py
