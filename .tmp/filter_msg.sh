#!/bin/bash
sed '/⚙️ Generated with ChipAgents/d; /Co-Authored-By: ChipAgents/d' "$1" | sed -e :a -e '/^\n*$/{$d;N;ba}' > "$1.tmp" && mv "$1.tmp" "$1"