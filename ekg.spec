%bcond_without	voip
%bcond_with	python
%bcond_with	ioctl_daemon

%define	snap	20031001
Summary:	A client compatible with Gadu-Gadu
Summary(de):	Einen client kompatibel zu Gadu-Gadu
Summary(it):	Esperimentale cliente di Gadu-Gadu
Summary(pl):	Eksperymentalny Klient Gadu-Gadu
Name:		ekg
Version:	1.4
Release:	0.%{snap}.1
Epoch:		3
License:	GPL v2
Group:		Applications/Communications
Source0:	http://dev.null.pl/ekg/%{name}-%{snap}.tar.gz
# Source0-md5:	613eaeb65ffca744bff96eafb04f5039
Source1:	%{name}.conf
URL:		http://dev.null.pl/ekg/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_voip:BuildRequires:	libgsm-devel}
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	%{_bindir}/perl
%{?with_python:BuildRequires:	python-devel}
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A client compatible with Gadu-Gadu.

%description -l de
Einen client kompatibel zu Gadu-Gadu.

%description -l it
Esperimentale cliente di Gadu-Gadu.

%description -l pl
Eksperymentalny Klient Gadu-Gadu.

%package -n libgadu
Summary:	libgadu library
Summary(pl):	Biblioteka libgadu
Group:		Libraries
Obsoletes:	libgg
License:	LGPL v2.1

%description -n libgadu
libgadu is intended to make it easy to add Gadu-Gadu communication
support to your software.

%description -n libgadu -l de
Mit libgadu ist es Ihnen möglich auf einfache Weise Gadu-Gadu
Kommunikations-Unterstützung in Ihre Software einzubinden.

%description -n libgadu -l pl
libgadu umo¿liwia ³atwe dodanie do ró¿nych aplikacji komunikacji
bazuj±cej na protokole Gadu-Gadu.

%package -n libgadu-devel
Summary:	libgadu library development
Summary(pl):	Czê¶æ biblioteki libgadu dla programistów
Group:		Development/Libraries
Requires:	libgadu = %{epoch}:%{version}
Obsoletes:	libgg-devel
License:	LGPL

%description -n libgadu-devel
The libgadu-devel package contains the header files and some
documentation needed to develop application with libgadu.

%description -n libgadu-devel -l de
Das libgadu-devel Paket enthält Header-Files (Kopfzeilenordner) und
die Dokumentation die Sie benötigen um mit libgadu Anwendungen zu
entwickeln.

%description -n libgadu-devel -l pl
Pakiet libgadu-devel zawiera pliki nag³ówkowe i dokumentacjê,
potrzebne do kompilowania aplikacji korzystaj±cych z libgadu.

%package -n libgadu-static
Summary:	Static libgadu Library
Summary(pl):	Statyczna biblioteka libgadu
Group:		Development/Libraries
Requires:	libgadu-devel = %{epoch}:%{version}
Obsoletes:	libgg-static
License:	LGPL

%description -n libgadu-static
Static libgadu library.

%description -n libgadu-static -l de
Statisches libgadu Archiv.

%description -n libgadu-static -l pl
Statyczna biblioteka libgadu.

%prep
%setup -q -n %{name}-%{snap}

%build
rm -f missing
%{__aclocal}
%{__autoheader}
%{__autoconf}
%configure \
	--enable-shared \
	--enable-static \
	--with-pthread \
	%{?with_python:--with-python} \
	%{?!with_voip:--without-libgsm} \
	%{?!with_ioctl_daemon:--disable-ioctld}
%{__make}

%if %{with ioctl_daemon}
cd src
%{__make} ioctld
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install install-ekl2 \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/

# For libgadu-devel

rm examples/Makefile examples/Makefile.in examples/.cvsignore

%if %{with ioctl_daemon}
install src/ioctld $RPM_BUILD_ROOT%{_bindir}
%endif

cd $RPM_BUILD_ROOT%{_libdir}
ln -sf libgadu.so.*.* libgadu.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libgadu -p /sbin/ldconfig
%postun -n libgadu -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc docs/{7thguard,dcc,files,gdb,python,sim,themes,ui-ncurses,vars,voip}.txt
%doc ChangeLog docs/{FAQ,README,TODO,ULOTKA} docs/emoticons.{ansi,sample}
%attr(755,root,root) %{_bindir}/e*
%{?with_ioctl_daemon:%attr(4755,root,root) %{_bindir}/ioctld}
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*.conf
%{_datadir}/ekg
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*

%files -n libgadu
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgadu.so.*.*

%files -n libgadu-devel
%defattr(644,root,root,755)
%doc docs/{7thguard,ui,devel-hints,przenosny-kod}.txt docs/protocol.html
%doc ChangeLog docs/{README,TODO} examples
%{_libdir}/libgadu.so
%{_includedir}/libgadu.h
%{_includedir}/libgadu-config.h
%{_pkgconfigdir}/*

%files -n libgadu-static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/libgadu.a
