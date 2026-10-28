Name:       sailqemu-qemu-net
Version:    10.2.4
Release:    2
Summary:    QEMU 10.2.4 x86_64 emulator with D-Bus, SDL and NAT for SailQEMU
Group:      Applications/System
License:    GPL-2.0-or-later
URL:        https://www.qemu.org/
Source0:    %{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: meson
BuildRequires: ninja
BuildRequires: python3-base
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(pixman-1)
BuildRequires: pkgconfig(sdl2)
BuildRequires: pkgconfig(zlib)
BuildRequires: sailqemu-libslirp >= 4.9.5
Requires:      sailqemu-libslirp >= 4.9.5

%description
QEMU system emulation compiled from pinned upstream QEMU 10.2.4 source,
installed independently under /opt/sailqemu/qemu-10.2.4-net.

%prep
%setup -q
test -x upstream/configure || { echo 'Pinned upstream source missing'; exit 1; }
test "$(cat upstream/VERSION)" = 10.2.4 || exit 1

%build
PREFIX=/opt/sailqemu/qemu-10.2.4-net
SLIRP=/opt/sailqemu/libslirp-4.9.5
export PKG_CONFIG_PATH="$SLIRP/lib64/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
export LDFLAGS="${LDFLAGS:+$LDFLAGS }-Wl,-rpath,$SLIRP/lib64"
mkdir -p _build
cd _build
../upstream/configure --prefix="$PREFIX" --libdir=lib64 \
 --target-list=x86_64-softmmu --enable-system --disable-user \
 --enable-tcg --disable-kvm --enable-sdl --enable-dbus-display \
 --enable-gio --enable-pixman --enable-slirp \
 --disable-gtk --disable-opengl --disable-spice --disable-vnc \
 --disable-rust --disable-modules --disable-guest-agent \
 --disable-docs --disable-werror --disable-download -Dtests=disabled
make -j 2

%install
make -C _build DESTDIR=%{buildroot} install

%files
/opt/sailqemu/qemu-10.2.4-net
