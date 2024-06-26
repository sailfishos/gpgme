Name:    gpgme
Summary: GnuPG Made Easy - high level crypto API
Version: 1.2.0
Release: 0

License: LGPLv2+
URL:     https://github.com/sailfishos/gpgme
Source0: %{name}-%{version}.tar.gz

Patch1: 0001-Allow-gpgsm-to-start-agent-on-demand-during-signing-.patch
Patch2: 0002-doc-Update-gpl.texi-to-match-version-from-gnupg.patch
Patch3: 0003-configure.ac-Make-largefile-check-more-robust.patch

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
Requires: %{name} = %{version}-%{release}
Requires: libgpg-error-devel
# /usr/share/aclocal ownership
#Requires: automake

%description devel
%{summary}

%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

%description doc
Info pages for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}/trunk

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

%make_build

%install
%make_install

# unpackaged files
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}/common-lisp/source/gpgme/

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m0644 -t $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
        AUTHORS ChangeLog NEWS README* THANKS TODO

%check
# expect 1(+?) errors with gnupg < 1.2.4
# gpgme-1.1.6 includes one known failure (FAIL: t-sign)
make -C tests check ||:

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post doc
%install_info  --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz ||:

%postun doc
if [ $1 -eq 0 ] ; then
  %install_info_delete  --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz ||:
fi

%files
%license COPYING*
%{_libdir}/libgpgme*.so.*

%files devel
%{_bindir}/gpgme-config
%{_includedir}/*
%{_libdir}/libgpgme*.so
%{_datadir}/aclocal/gpgme.m4

%files doc
%{_infodir}/%{name}.*
%{_docdir}/%{name}-%{version}
