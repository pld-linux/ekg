#
# Conditional build:
# _with_ioctl_daemon - with ioctl_daemon (suid-root!)
#
Summary:	A client compatible with Gadu-Gadu
Summary(de):	Einen client kompatibel zu Gadu-Gadu
Summary(it):	Esperimentale cliente di Gadu-Gadu
Summary(pl):	Eksperymentalny Klient Gadu-Gadu
Name:		ekg
Version:	20020717
Release:	0.1
Epoch:		1
License:	GPL
Group:		Applications/Communications
Source0:	http://dev.null.pl/ekg/%{name}-%{version}.tar.gz
URL:		http://dev.null.pl/ekg/
BuildRequires:	autoconf
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	libgsm-devel
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
Mit libgadu ist es Ihnen m�glich auf einfache Weise Gadu-Gadu
Kommunikations-Unterst�tzung in Ihre Software einzubinden.

%description -n libgadu -l pl
libgadu umo�liwia �atwe dodanie do r�nych aplikacji komunikacji
bazuj�cej na protokole Gadu-Gadu.

%package -n libgadu-devel
Summary:	libgadu library development
Summary(pl):	Cz�� biblioteki libgadu dla programist�w
Group:		Development/Libraries
Requires:	libgadu
Obsoletes:	libgg-devel
License:	LGPL

%description -n libgadu-devel
The libgadu-devel package contains the header files and some
documentation needed to develop application with libgadu.

%description -n libgadu-devel -l de
Das libgadu-devel Paket enth�lt Header-Files (Kopfzeilenordner) und
die Dokumentation die Sie ben�tigen um mit libgadu Anwendungen zu
entwickeln.

%description -n libgadu-devel -l pl
Pakiet libgadu-devel zawiera pliki nag��wkowe i dokumentacj�,
potrzebne do kompilowania aplikacji korzystaj�cych z libgadu.

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
%{__autoconf}
%configure \
	--with-shared \
	%{?!debug:--without-debug} \
	%{?!_with_ioctl_daemon:--without-ioctld}

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
install docs/ekl2.man.pl $RPM_BUILD_ROOT%{_mandir}/pl/man1/ekl2.1
install docs/ekl2.man.en $RPM_BUILD_ROOT%{_mandir}/man1/ekl2.1
install docs/ekg.man.en $RPM_BUILD_ROOT%{_mandir}/man1/ekg.1

# For libgadu-devel

rm examples/Makefile examples/Makefile.in

%if %{?_with_ioctl_daemon:1}%{?!_with_ioctl_daemon:0}
install src/ioctld $RPM_BUILD_ROOT%{_bindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libgadu -p /sbin/ldconfig
%postun -n libgadu -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/e*
%doc docs/{7thguard,dcc,emoticons,on,themes,ui,vars,voip}.txt
%doc ChangeLog docs/{FAQ,README,TODO,ULOTKA} docs/emoticons.sample
%{?_with_ioctl_daemon:%attr(4755,root,root) %{_bindir}/ioctld}
%{_datadir}/ekg
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*

%files -n libgadu
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgadu.so.*

%files -n libgadu-devel
%defattr(644,root,root,755)
%doc docs/{7thguard,api,dcc-protocol,devel-hints,http}.txt docs/protocol.html
%doc ChangeLog docs/{README,TODO} examples
%{_includedir}/libgadu.h

%files -n libgadu-static
%defattr(644,root,root,755)
%attr(644,root,root) %{_libdir}/libgadu.a
