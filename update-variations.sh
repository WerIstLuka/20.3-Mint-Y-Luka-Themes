#!/bin/bash
colors="Aqua Blue Brown Grey Orange Pink Purple Red Sand Teal"

for color in $colors; do
	./update-variations.py $color &
done
echo
echo "All done"
