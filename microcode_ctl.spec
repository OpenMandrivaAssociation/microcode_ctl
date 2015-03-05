%define upstream_version 2.1-7

Summary:	Intel / AMD CPU Microcode Utility
Name:		microcode_ctl
Version:	2.1
Release:	10
Group:		System/Kernel and hardware
License:	GPLv2
Url:		http://fedorahosted.org/microcode_ctl
Source0:	http://fedorahosted.org/released/microcode_ctl/%{name}-%{upstream_version}.tar.xz
# Intel firmware downloader (Debian)
Source2:	update-intel-microcode
Source3:	update-intel-microcode.8
# AMDl firmware downloader
Source4:	update-amd-microcode
Source5:	update-amd-microcode.8
# monthly cron
Source6:	update-microcode
ExclusiveArch:	%ix86 x86_64 %arm
# needed by firmware downloaders
Suggests:	curl
# we have microcode packaged
Suggests:	microcode
# (fc) 1.17-8 fix paths (Fedora)
Provides:	microcode
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

# do not ship non-free firmware in this package
rm -rf %{buildroot}/lib/firmware
# install intel firmware downloader 
install -m 755 %{SOURCE2} %{buildroot}%{_sbindir}
install -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man8
# install AMD firmware downloader 
install -m 755 %{SOURCE4} %{buildroot}%{_sbindir}
install -m 644 %{SOURCE5} %{buildroot}%{_mandir}/man8
# install monthly cron
mkdir -p %{buildroot}%{_sysconfdir}/cron.monthly
install -m755 %{SOURCE6} %{buildroot}%{_sysconfdir}/cron.monthly
#
mkdir -p %{buildroot}/lib/firmware/amd-ucode 
mkdir -p %{buildroot}/lib/firmware/intel-ucode

%files
%doc README
%{_sbindir}/*
%{_mandir}/man8/*
%{_sysconfdir}/cron.monthly/update-microcode
/lib/firmware/amd-ucode
/lib/firmware/intel-ucode
