#
# Conditional build:
# _with_ioctl_daemon    - with ioctl_daemon (suid-root!)
# _with_python          - with python support
# _without_voip	        - without voip support
#
Summary:	A client compatible with Gadu-Gadu
Summary(de):	Einen client kompatibel zu Gadu-Gadu
Summary(it):	Esperimentale cliente di Gadu-Gadu
Summary(pl):	Eksperymentalny Klient Gadu-Gadu
Name:		ekg
Version:	20030208
Release:	1
Epoch:		1
License:	GPL
Group:		Applications/Communications
Source0:	http://bzium.eu.org/ekg/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
URL:		http://bzium.eu.org/ekg/
BuildRequires:	autoconf
BuildRequires:	automake
%{?!_without_voip:BuildRequires: libgsm-devel}
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	perl
%{?_with_python:BuildRequires: python-devel}
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
License:	LGPL

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
Requires:	libgadu
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
Requires:	libgadu-devel
Obsoletes:	libgg-static
License:	LGPL

%description -n libgadu-static
Static libgadu library.

%description -n libgadu-static -l de
Statisches libgadu Archiv.

%description -n libgadu-static -l pl
Statyczna biblioteka libgadu.

%prep
%setup -q

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%configure \
	--enable-shared \
	--enable-static \
	--with-pthread \
	%{?_with_python:--with-python} \
	%{?_without_voip:--without-libgsm} \
	%{?!_with_ioctl_daemon:--disable-ioctld}
%{__make}

%{?_with_ioctl_daemon: (cd src && %{__make} ioctld )}
( cd docs/api && ./make.pl )

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install contrib/ekl2.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/ekl2.sh $RPM_BUILD_ROOT%{_bindir}
install docs/ekl2.man.pl $RPM_BUILD_ROOT%{_mandir}/pl/man1/ekl2.1
install docs/ekl2.man.en $RPM_BUILD_ROOT%{_mandir}/man1/ekl2.1
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/

# For libgadu-devel

rm examples/Makefile examples/Makefile.in

%if %{?_with_ioctl_daemon:1}%{?!_with_ioctl_daemon:0}
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
%attr(755,root,root) %{_bindir}/e*
%attr(644,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/*.conf
%doc docs/{7thguard,dcc,gdb,python,themes,ui,vars,voip}.txt
%doc ChangeLog docs/{FAQ,README,TODO,ULOTKA} docs/emoticons.{ansi,sample}
%{?_with_ioctl_daemon:%attr(4755,root,root) %{_bindir}/ioctld}
%{_datadir}/ekg
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*

%files -n libgadu
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgadu.so.*.*

%files -n libgadu-devel
%defattr(644,root,root,755)
%doc docs/{7thguard,api,devel-hints,przenosny-kod}.txt docs/protocol.html docs/api/ref.functions.html
%doc ChangeLog docs/{README,TODO} examples
%{_libdir}/libgadu.so
%{_includedir}/libgadu.h
%{_includedir}/libgadu-config.h
%{_pkgconfigdir}/*

%files -n libgadu-static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/libgadu.a
