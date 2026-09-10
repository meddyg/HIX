#!/usr/bin/env bash
# Builds the site into dist/site. The IG Publisher runs SUSHI itself and renders
# every page through Jekyll, so both have to be reachable on PATH.
set -euo pipefail

cd "$(dirname "$0")/.."

# `gem install --user-install` puts binaries outside the default PATH.
for d in "$HOME"/.local/share/gem/ruby/*/bin; do
  [ -d "$d" ] && PATH="$d:$PATH"
done
export PATH

for tool in sushi jekyll java; do
  command -v "$tool" >/dev/null || { echo "$tool is not on PATH. See README.md." >&2; exit 1; }
done

if [ ! -f .work/tools/publisher.jar ]; then
  echo "The publisher is missing. Run 'make tools' first." >&2
  exit 1
fi

java -Xmx4g -jar .work/tools/publisher.jar publisher -ig .

# The publisher honours path-output and path-tx-cache, but two things have no
# parameter: it drops its terminology QA report into ./output and its schema
# cache into ./input-cache. Both are swept into .work rather than left at the
# root. Nothing is lost -- the schema cache is kept, just moved.
if [ -d output ]; then
  mkdir -p .work/qa
  mv -f output/* .work/qa/ 2>/dev/null || true
  rmdir output 2>/dev/null || true
fi
if [ -d input-cache ]; then
  rm -rf .work/schemas
  mv -f input-cache/schemas .work/schemas 2>/dev/null || true
  rm -rf input-cache
fi

# fsh-generated/ is SUSHI's output and template/ is the expanded template. Both
# are rebuilt from scratch on every run, so they are moved out of the way rather
# than left cluttering the root. Moved, not deleted: nothing here is a source.
for d in fsh-generated template; do
  if [ -d "$d" ]; then
    rm -rf ".work/$d"
    mv -f "$d" ".work/$d"
  fi
done

echo
echo "Open dist/site/index.html"
