#
# Conditional build:
# _with_ioctl_daemon - with ioctl_daemon (suid-root!)
#
%define		snapshot	20020506
Summary:	A client compatible with Gadu-Gadu
Summary(pl):	Eksperymentalny Klient Gadu-Gadu
Name:		ekg
Version:	0.9.0.%{snapshot}
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	http://dev.null.pl/ekg/%{name}-%{snapshot}.tar.gz
URL:		http://dev.null.pl/ekg/
BuildRequires:	autoconf
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A client compatible with Gadu-Gadu.

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

%description -n libgadu-static -l pl
Statyczna biblioteka libgadu.

%prep
%setup -q -n %{name}-%{snapshot}

%build
autoconf
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

%if %{?_with_ioctl_daemon:1}%{?!_with_ioctl_daemon:0}
install src/ioctl_daemon $RPM_BUILD_ROOT%{_bindir}
%endif

gzip -9nf ChangeLog docs/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libgadu -p /sbin/ldconfig
%postun -n libgadu -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/e*
%{?_with_ioctl_daemon:%attr(4755,root,root) %{_bindir}/ioctl_daemon}
%{_datadir}/ekg
%doc docs/{7thguard,dcc,on,themes,vars}.txt.gz
%doc ChangeLog.gz docs/{FAQ,README,TODO,ULOTKA}.gz
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*

%files -n libgadu
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgadu.so.*

%files -n libgadu-devel
%defattr(644,root,root,755)
%{_includedir}/libgadu.h
%doc docs/{7thguard,api,devel-hints,protocol,dcc-protocol}.txt.gz
%doc ChangeLog.gz docs/{README,TODO}.gz

%files -n libgadu-static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/libgadu.a
