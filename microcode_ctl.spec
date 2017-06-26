%define upstream_version 2.1-12

Summary:	Intel / AMD CPU Microcode Utility
Name:		microcode_ctl
Version:	2.1
Release:	16
Group:		System/Kernel and hardware
License:	GPLv2
Url:		http://fedorahosted.org/microcode_ctl
Source0:	http://fedorahosted.org/released/microcode_ctl/%{name}-%{upstream_version}.tar.xz
ExclusiveArch:	%ix86 x86_64 %armx
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
%setup -qn %{name}-%{upstream_version}
%apply_patches

%build
%setup_compile_flags
%make

%install
mkdir -p %{buildroot}%{_mandir}/man8
%makeinstall_std INSDIR=%{_sbindir} PREFIX=%{_prefix}

#
mkdir -p %{buildroot}/lib/firmware/amd-ucode
mkdir -p %{buildroot}/lib/firmware/intel-ucode

%files
%doc README
%{_sbindir}/*
/lib/firmware/amd-ucode
/lib/firmware/intel-ucode
