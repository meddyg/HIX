#!/usr/bin/env bash
# Renders the PlantUML figures into input/images/, where both consumers find
# them: the IG Publisher copies that directory into the site, and pandoc reads
# it from the source tree for the PDF and DOCX.
#
# PlantUML ships inside the IG Publisher jar, so there is nothing else to
# install. Block diagrams set `!pragma layout smetana` because Graphviz is not
# a dependency of this repo.
#
# .drawio sources are not rendered here: draw.io has no headless exporter on
# this machine. Export them from the editor straight into input/images/, with
# the labels set to plain text ("Formatted Text" off), so the SVG carries
# ordinary <text> elements that every renderer draws.
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -f .work/tools/publisher.jar ]; then
  echo "The publisher is missing. Run 'make tools' first." >&2
  exit 1
fi

mkdir -p input/images

java -cp .work/tools/publisher.jar net.sourceforge.plantuml.Run \
  -tsvg -o "$(pwd)/input/images" _diagrams/*.plantuml

# Recent JDKs serialise PlantUML's DOM with xmlns="" on every child element
# (the "not created as namespace-aware" warning). That drops the elements out
# of the SVG namespace and browsers render a blank image. Strip it.
for src in _diagrams/*.plantuml; do
  sed -i 's/ xmlns=""//g' "input/images/$(basename "${src%.plantuml}").svg"
done

ls input/images/*.svg
