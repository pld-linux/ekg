%define		snapshot	20020102
Summary:	A client compatible with Gadu-Gadu
Summary(pl):	Eksperymentalny Klient Gadu-Gadu
Name:		ekg
Version:	0.9.0.%{snapshot}
Release:	1
License:	GPL
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narzêdzia
Group(pt_BR):	Rede/Utilitários
Source0:	http://dev.null.pl/ekg/%{name}-%{snapshot}.tar.gz
Source1:	ekg.1.man
Patch0:		ekg-man_bug.patch
URL:		http://dev.null.pl/ekg/
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A client compatible with Gadu-Gadu.

%description -l pl
Eksperymentalny Klient Gadu-Gadu.

%package -n libgg
Summary:	libgg library
Summary(pl):	Biblioteka libgg
Group:		Libraries
Group(pl):	Biblioteki

%description -n libgg
libgg is intended to make it easy to add Gadu-Gadu communication
support to your software.

%description -n libgg -l pl
libgg umo¿liwia ³atwe dodanie do ró¿nych aplikacji komunikacji
bazuj±cej na protokole Gadu-Gadu.

%package -n libgg-devel
Summary:	libgg library development
Summary(pl):	Czê¶æ biblioteki libgg dla programistów
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	libgg

%description -n libgg-devel
The libgg-devel package contains the header files and some
documentation needed to develop application with libgg.

%description -n libgg-devel -l pl
Pakiet libgg-devel zawiera pliki nag³ówkowe i dokumentacjê, potrzebne
do kompilowania aplikacji korzystaj±cych z libgg.

%package -n libgg-static
Summary:	Static libgg Library
Summary(pl):	Statyczna biblioteka libgg
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	libgg-devel

%description -n libgg-static
Static libgg library.

%description -n libgg-static -l pl
Statyczna biblioteka libgg.

%prep
%setup -q -n %{name}-%{snapshot}
%patch0 -p0

%build
%configure \
	%{?!debug:--without-debug}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir}} \
	$RPM_BUILD_ROOT{%{_mandir}/{,pl/}man1,%{_datadir}/ekg}

install src/ekg $RPM_BUILD_ROOT%{_bindir}
install lib/libgg.h $RPM_BUILD_ROOT%{_includedir}
install lib/libgg.a $RPM_BUILD_ROOT%{_libdir}
install lib/libgg.so.* $RPM_BUILD_ROOT%{_libdir}

install themes/*.theme $RPM_BUILD_ROOT%{_datadir}/ekg

install docs/ekg.man $RPM_BUILD_ROOT%{_mandir}/pl/man1/ekg.1
install %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1/ekg.1

gzip -9nf ChangeLog docs/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libgg -p /sbin/ldconfig
%postun -n libgg -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/ekg
%doc docs/{7thguard,dcc,themes,vars}.txt.gz
%doc ChangeLog.gz docs/{FAQ,README,TODO,ekl.pl}.gz
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*

%files -n libgg
%attr(755,root,root) %{_libdir}/libgg.so.*

%files -n libgg-devel
%defattr(644,root,root,755)
%{_includedir}/libgg.h
%doc docs/{7thguard,api,protocol}.txt.gz
%doc ChangeLog.gz docs/{README,TODO}.gz

%files -n libgg-static
%attr(644,root,root) %{_libdir}/libgg.a
