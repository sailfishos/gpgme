
Name:    gpgme
Summary: GnuPG Made Easy - high level crypto API
Version: 1.2.0
Release: 2

License: LGPLv2+
Group:   Applications/System
URL:     http://www.gnupg.org/related_software/gpgme/
Source0: ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/gpgme/gpgme-%{version}.tar.bz2.sig

Patch1: gpgme-1.1.3-config_extras.patch

BuildRequires: gawk
BuildRequires: gnupg2
BuildRequires: libgpg-error-devel
#BuildRequires: pth-devel

Requires: gnupg2

%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.  It provides a high-level crypto API for
encryption, decryption, signing, signature verification and key
management.

%package devel
Summary:  Development headers and libraries for %{name}
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libgpg-error-devel
# /usr/share/aclocal ownership
#Requires: automake
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info
%description devel
%{summary}

%prep
%setup -q

#%patch1 -p1 -b .config_extras

## HACK ALERT
# The config script already suppresses the -L if it's /usr/lib, so cheat and
# set it to a value which we know will be suppressed.
#sed -i -e 's|^libdir=@libdir@$|libdir=@exec_prefix@/lib|g' gpgme/gpgme-config.in

%build
%configure \
  --disable-static \
  --with-gpg=%{_bindir}/gpg2 --disable-gpg-test

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# unpackaged files
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/common-lisp/source/gpgme/

%check
# expect 1(+?) errors with gnupg < 1.2.4
# gpgme-1.1.6 includes one known failure (FAIL: t-sign)
make -C tests check ||:

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
%install_info  --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%postun devel
if [ $1 -eq 0 ] ; then
  %install_info_delete  --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING* README* THANKS VERSION
%{_libdir}/libgpgme*.so.*

%files devel
%defattr(-,root,root,-)
%doc ChangeLog NEWS TODO
%{_bindir}/gpgme-config
%{_includedir}/*
%{_libdir}/libgpgme*.so
%{_datadir}/aclocal/gpgme.m4
%{_infodir}/gpgme.info*
