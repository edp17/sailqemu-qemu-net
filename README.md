# sailqemu-qemu-net 10.2.4 — source RPM recipe (EXPERIMENTAL)

Source build recipe for the tested NAT-enabled QEMU configuration. It is
**not yet tested in Sailfish SDK or OBS** and does not contain compiled binaries.

**Setup after extracting the ZIP**:

```sh
git init -b main
sh scripts/add-upstream.sh
git add .
git commit -m "Package QEMU 10.2.4 from pinned source"
git tag v10.2.4  # local build version; push only after testing
```

The script records upstream QEMU tag `v10.2.4` as a git submodule and
initialises its submodules. Before publication, verify the full commit SHA
and source provenance (`git -C upstream log -1`). The OBS tar_git service
must include the checked-out source/submodules: validate the resulting
source tarball rather than assuming recursive inclusion.

**Build order**: build `sailqemu-libslirp` first and make its `-2` RPM
available inside the SAME selected Sailfish SDK 5.1 target. Then run
`sfdk build` here. Begin with an aarch64 target, then test armv7hl.

Flags closely follow the previously proven on-device networking QEMU build,
including `--enable-slirp=system`, SDL, D-Bus, GIO, Pixman, TCG and the
`x86_64-softmmu` guest target. It installs under the current application
profile path `/opt/sailqemu/qemu-10.2.4-net`.

Before installing this RPM over the known working `10.2.4-1`, verify:
`qemu-system-x86_64 --version`, `readelf -d` RUNPATH,
`qemu-system-x86_64 -netdev help` contains `user`, firmware files are present,
and all guest boot/safe-shutdown tests pass. Confirm the RPM spec's license
metadata and all packaged firmware licenses before publishing.

**Important**: QEMU may need extra SDK dependencies, cross-toolchain fixes,
Meson version changes, or firmware source packages; these cannot be resolved
without the first real SDK build log. A successful compiler run on one arch
is not proof of OBS reproducibility on both arches.

Upstream: https://gitlab.com/qemu-project/qemu
