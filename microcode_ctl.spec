Summary:	Intel / AMD CPU Microcode Utility
Name:		microcode_ctl
Version:	1.17
Release:	18
Group:		System/Kernel and hardware
License:	GPLv2
Url:		http://www.urbanmyth.org/microcode/
Source0:	http://www.urbanmyth.org/microcode/%name-%version.tar.bz2
Source1:	microcode_ctl
# Intel firmware downloader (Debian)
Source2:	update-intel-microcode
Source3:	update-intel-microcode.8
# AMDl firmware downloader
Source4:	update-amd-microcode
Source5:	update-amd-microcode.8
# monthly cron
Source6:	update-microcode
Patch0:	microcode_ctl.patch
ExclusiveArch:	%ix86 x86_64
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
%setup -q
%apply_patches

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
%makeinstall_std INSDIR=%{_sbindir} MANDIR=%{_mandir}/man8
# replace upstream initscript with our own
rm -rf %{buildroot}%{_sysconfdir}/init.d
mkdir -p %{buildroot}/%{_initrddir}
install -m 755 %SOURCE1 %{buildroot}/%{_initrddir}
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
mkdir -p %{buildroot}/lib/firmware/intel-microcode


%files
%{_sbindir}/*
%{_mandir}/man8/*
%{_initrddir}/%name
%{_sysconfdir}/cron.monthly/update-microcode
/lib/firmware/amd-ucode
/lib/firmware/intel-microcode

%post
# Only enable on Intel 686's and above or AMD family 0x10 and above
vendor=`cat /proc/cpuinfo | grep "^vendor_id" | sort -u | awk -F ":	" '{ print $2 }'`
family=`cat /proc/cpuinfo | grep "^cpu family" | sort -u | awk -F ":	" '{ print $2 }'`
if [ "$vendor" = "GenuineIntel" ]; then
 [ $family -lt 6 ] && exit 0
elif [ "$vendor" = "AuthenticAMD" ]; then
 [ $family -lt 16 ] && exit 0
else
 exit 0
fi
%_post_service %{name}

%preun
%_preun_service %{name}

