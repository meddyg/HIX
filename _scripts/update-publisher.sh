#!/usr/bin/env bash
# Downloads the IG Publisher into .work/tools/.
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p .work/tools

url=https://github.com/HL7/fhir-ig-publisher/releases/latest/download/publisher.jar
echo "Downloading $url"
curl -fL --progress-bar -o .work/tools/publisher.jar "$url"
java -jar .work/tools/publisher.jar -v
