
Name:    gpgme
Summary: GnuPG Made Easy - high level crypto API
Version: 1.2.0
Release: 2

License: LGPLv2+
Group:   Applications/System
URL:     http://www.gnupg.org/related_software/gpgme/
Source0: %{name}-%{version}.tar.gz

BuildRequires: gawk
BuildRequires: gnupg2
BuildRequires: libgpg-error-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: texinfo
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
%setup -q -n %{name}-%{version}/%{name}/trunk

#%patch1 -p1 -b .config_extras

## HACK ALERT
# The config script already suppresses the -L if it's /usr/lib, so cheat and
# set it to a value which we know will be suppressed.
#sed -i -e 's|^libdir=@libdir@$|libdir=@exec_prefix@/lib|g' gpgme/gpgme-config.in

%build
autoreconf -vfi
%configure \
  --enable-maintainer-mode \
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
%install_info  --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz ||:

%postun devel
if [ $1 -eq 0 ] ; then
  %install_info_delete  --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz ||:
fi

%files
%defattr(-,root,root,-)
%doc COPYING*
%{_libdir}/libgpgme*.so.*

%files devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS TODO README* THANKS
%{_bindir}/gpgme-config
%{_includedir}/*
%{_libdir}/libgpgme*.so
%{_datadir}/aclocal/gpgme.m4
%{_infodir}/gpgme.info*
