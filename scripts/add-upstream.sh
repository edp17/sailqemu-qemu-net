#!/bin/sh
set -eu
# Run from this packaging repository AFTER git init, before initial commit.
[ -d .git ] || { echo 'Run git init -b main first'; exit 1; }
[ ! -e upstream ] || { echo 'upstream exists; inspect pinned tag'; exit 1; }
git submodule add https://gitlab.com/qemu-project/qemu.git upstream
git -C upstream fetch --tags
git -C upstream checkout v10.2.4
test "$(cat upstream/VERSION)" = '10.2.4'
# QEMU's build can need pinned nested upstream subprojects.
git -C upstream submodule update --init --recursive
printf 'Pinned QEMU upstream commit: %s\n' "$(git -C upstream rev-parse HEAD)"
