#
# Conditional build:
# _with_ioctl_daemon - with ioctl_daemon (suid-root!)
#
%define		snapshot	20020528
Summary:	A client compatible with Gadu-Gadu
Summary(de):	Einen client kompatibel zu Gadu-Gadu 
Summary(it):	Esperimentale cliente di Gadu-Gadu
Summary(pl):	Eksperymentalny Klient Gadu-Gadu
Name:		ekg
Version:	0.9.0.%{snapshot}
Release:	2
License:	GPL
Group:		Networking/Utilities
Source0:	http://dev.null.pl/ekg/%{name}-%{snapshot}.tar.gz
Patch0:		%{name}-home_etc.patch
URL:		http://dev.null.pl/ekg/
BuildRequires:	autoconf
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
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
Das libgadu-devel Paket enthält Header-Files (Kopfzeilenordner)
und die Dokumentation die Sie benötigen um mit libgadu
Anwendungen zu entwickeln.

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
%setup -q -n %{name}-%{snapshot}
%patch0 -p1

%build
%{__autoconf}
%configure \
	--with-shared \
	%{?!debug:--without-debug} \
	%{?!_with_ioctl_daemon:--without-ioctl}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{_mandir}/{,pl/}man1,%{_datadir}/ekg/themes}

install src/ekg $RPM_BUILD_ROOT%{_bindir}
install contrib/ekl2.pl $RPM_BUILD_ROOT%{_bindir}
install contrib/ekl2.sh $RPM_BUILD_ROOT%{_bindir}
install lib/libgadu.h $RPM_BUILD_ROOT%{_includedir}
install lib/libgadu.a $RPM_BUILD_ROOT%{_libdir}
install lib/libgadu.so.* $RPM_BUILD_ROOT%{_libdir}

install themes/*.theme $RPM_BUILD_ROOT%{_datadir}/ekg/themes

install docs/ekg.man.pl $RPM_BUILD_ROOT%{_mandir}/pl/man1/ekg.1
install docs/ekg.man.en $RPM_BUILD_ROOT%{_mandir}/man1/ekg.1

# For libgadu-devel

rm examples/Makefile examples/Makefile.in

%if %{?_with_ioctl_daemon:1}%{?!_with_ioctl_daemon:0}
install src/ioctl_daemon $RPM_BUILD_ROOT%{_bindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -n libgadu -p /sbin/ldconfig
%postun -n libgadu -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/e*
%doc docs/{7thguard,dcc,on,themes,vars,emoticons}.txt
%doc ChangeLog docs/{FAQ,README,TODO,ULOTKA} docs/emoticons.sample
%{?_with_ioctl_daemon:%attr(4755,root,root) %{_bindir}/ioctl_daemon}
%{_datadir}/ekg
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*

%files -n libgadu
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgadu.so.*

%files -n libgadu-devel
%defattr(644,root,root,755)
%doc docs/{7thguard,api,devel-hints,dcc-protocol}.txt protocol.html
%doc ChangeLog docs/{README,TODO} examples
%{_includedir}/libgadu.h

%files -n libgadu-static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/libgadu.a
