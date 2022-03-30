# Work around incomplete debug packages
%global _empty_manifest_terminate_build 0

%define upstream_version 2.1-13

Summary:	Intel / AMD CPU Microcode Utility
Name:		microcode_ctl
Version:	2.1
Release:	17
Group:		System/Kernel and hardware
License:	GPLv2
Url:		https://pagure.io/microcode_ctl
Source0:	https://releases.pagure.org/microcode_ctl/%{name}-%{upstream_version}.tar.xz
Source1: microcode_ctl.rpmlintrc
ExclusiveArch:	%ix86 x86_64 %armx znver1
# (fc) 1.17-8 fix paths (Fedora)
Provides:	microcode = 0.20140323-4
Obsoletes:	microcode < 0.20140323-4
Requires(post,preun):	rpm-helper

%description
Since PentiumPro, Intel CPU are made of a RISC chip and of a microcode whose
purpose is to decompose "old" ia32 instruction into new risc ones.
P6 familly is concerned: PPro, PII, Celeron, PIII, Celeron2, Core 2, ...
Recent kernels have the ability to update this microcode.

The microcode update is volatile and needs to be uploaded on each system
boot. I.e. it doesn't reflash your cpu permanently.
Reboot and it reverts back to the old microcode.

This package also support updating latest AMD CPU microcode.

%prep
%autosetup -n %{name}-%{upstream_version} -p1

%build
%set_build_flags
%make_build

%install
mkdir -p %{buildroot}%{_mandir}/man8
%make_install INSDIR=%{_sbindir} PREFIX=%{_prefix}

mkdir -p %{buildroot}/lib/firmware/amd-ucode
mkdir -p %{buildroot}/lib/firmware/intel-ucode

%files
%doc README
/lib/firmware/amd-ucode
/lib/firmware/intel-ucode
