%define		snapshot	20020123
Summary:	A client compatible with Gadu-Gadu
Summary(pl):	Eksperymentalny Klient Gadu-Gadu
Name:		ekg
Version:	0.9.0.%{snapshot}
Release:	2
License:	GPL
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/NarzÍdzia
Group(pt_BR):	Rede/Utilit·rios
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

%package -n libgg
Summary:	libgg library
Summary(pl):	Biblioteka libgg
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	‚…¬Ã…œ‘≈À…
Group(uk):	‚¶¬Ã¶œ‘≈À…

%description -n libgg
libgg is intended to make it easy to add Gadu-Gadu communication
support to your software.

%description -n libgg -l pl
libgg umoøliwia ≥atwe dodanie do rÛønych aplikacji komunikacji
bazuj±cej na protokole Gadu-Gadu.

%package -n libgg-devel
Summary:	libgg library development
Summary(pl):	CzÍ∂Ê biblioteki libgg dla programistÛw
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	libgg

%description -n libgg-devel
The libgg-devel package contains the header files and some
documentation needed to develop application with libgg.

%description -n libgg-devel -l pl
Pakiet libgg-devel zawiera pliki nag≥Ûwkowe i dokumentacjÍ, potrzebne
do kompilowania aplikacji korzystaj±cych z libgg.

%package -n libgg-static
Summary:	Static libgg Library
Summary(pl):	Statyczna biblioteka libgg
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Ú¡⁄“¡¬œ‘À¡/‚…¬Ã…œ‘≈À…
Group(uk):	Úœ⁄“œ¬À¡/‚¶¬Ã¶œ‘≈À…
Requires:	libgg-devel

%description -n libgg-static
Static libgg library.

%description -n libgg-static -l pl
Statyczna biblioteka libgg.

%prep
%setup -q -n %{name}-%{snapshot}

%build
autoconf
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
( 
  cd $RPM_BUILD_ROOT%{_libdir}
  ln -s libgg.so.* libgg.so 
)

install themes/*.theme $RPM_BUILD_ROOT%{_datadir}/ekg

install docs/ekg.man.pl $RPM_BUILD_ROOT%{_mandir}/pl/man1/ekg.1
install docs/ekg.man.en $RPM_BUILD_ROOT%{_mandir}/man1/ekg.1

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
%attr(755,root,root) %{_libdir}/libgg.so
%{_includedir}/libgg.h
%doc docs/{7thguard,api,protocol}.txt.gz
%doc ChangeLog.gz docs/{README,TODO}.gz

%files -n libgg-static
%attr(644,root,root) %{_libdir}/libgg.a
