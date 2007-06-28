Summary:   Intel P6 CPU Microcode Utility
Name:      microcode_ctl
Version: 1.14
Release:   %mkrel 1
Group:     System/Kernel and hardware
License:   GPL
Url:       http://www.urbanmyth.org/microcode/
Source:    http://www.urbanmyth.org/microcode/%name-%version.tar.bz2
Source1:   microcode_ctl
Patch1:    microcode_ctl-build.diff.bz2
Buildroot: %_tmppath/%name-%version-buildroot
ExclusiveArch: %ix86
BuildRequires: kernel-source

%description
Since PentiumPro, Intel CPU are made of a RISC chip and of a microcode whose
purpose is to decompose "old" ia32 instruction into new risc ones.
P6 familly is concerned: PPro, PII, Celeron, PIII, Celeron2.
Recent kernels have the ability to update this microcode.

The microcode update is volatile and needs to be uploaded on each system
boot. I.e. it doesn't reflash your cpu permanently.
Reboot and it reverts back to the old microcode.

%prep
%setup -q
%patch1 -p0

%build
make

%install
%makeinstall DESTDIR=$RPM_BUILD_ROOT PREFIX=%_prefix MANDIR=%_mandir/man8
mkdir -p $RPM_BUILD_ROOT/%_initrddir
install -m 755 %SOURCE1 $RPM_BUILD_ROOT/%_initrddir
rm -f %buildroot%_sysconfdir/init.d/microcode_ctl

%clean
rm -r $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%_sbindir/microcode_ctl
%_mandir/man8/*
%config(noreplace) %{_sysconfdir}/microcode.dat
%config(noreplace) %_initrddir/%name

%post
/sbin/chkconfig --add %{name}
	
%preun
[[ "$1" = "0" ]] && /sbin/chkconfig --del %name || :
