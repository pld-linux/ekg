%define		snapshot	20020204
Summary:	A client compatible with Gadu-Gadu
Summary(pl):	Eksperymentalny Klient Gadu-Gadu
Name:		ekg
Version:	0.9.0.%{snapshot}
Release:	1
License:	GPL
Group:		Networking/Utilities
Group(de):	Netzwerkwesen/Werkzeuge
Group(es):	Red/Utilitarios
Group(pl):	Sieciowe/Narz�dzia
Group(pt_BR):	Rede/Utilit�rios
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
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Group(pt_BR):	Bibliotecas
Group(ru):	����������
Group(uk):	��̦�����

%description -n libgadu
libgadu is intended to make it easy to add Gadu-Gadu communication
support to your software.

%description -n libgadu -l pl
libgadu umo�liwia �atwe dodanie do r�nych aplikacji komunikacji
bazuj�cej na protokole Gadu-Gadu.

%package -n libgadu-devel
Summary:	libgadu library development
Summary(pl):	Cz�� biblioteki libgadu dla programist�w
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	����������/����������
Group(uk):	��������/��̦�����
Requires:	libgadu

%description -n libgadu-devel
The libgadu-devel package contains the header files and some
documentation needed to develop application with libgadu.

%description -n libgadu-devel -l pl
Pakiet libgadu-devel zawiera pliki nag��wkowe i dokumentacj�,
potrzebne do kompilowania aplikacji korzystaj�cych z libgadu.

%package -n libgadu-static
Summary:	Static libgadu Library
Summary(pl):	Statyczna biblioteka libgadu
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	����������/����������
Group(uk):	��������/��̦�����
Requires:	libgadu-devel

%description -n libgadu-static
Static libgadu library.

%description -n libgadu-static -l pl
Statyczna biblioteka libgadu.

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
	$RPM_BUILD_ROOT{%{_mandir}/{,pl/}man1,%{_datadir}/ekg/themes}

install src/ekg $RPM_BUILD_ROOT%{_bindir}
install src/ioctl_daemon $RPM_BUILD_ROOT%{_bindir}
install docs/ekl.pl $RPM_BUILD_ROOT%{_bindir}
install lib/libgadu.h $RPM_BUILD_ROOT%{_includedir}
install lib/libgadu.a $RPM_BUILD_ROOT%{_libdir}
install lib/libgadu.so.* $RPM_BUILD_ROOT%{_libdir}

install themes/*.theme $RPM_BUILD_ROOT%{_datadir}/ekg/themes

install docs/ekg.man.pl $RPM_BUILD_ROOT%{_mandir}/pl/man1/ekg.1
install docs/ekg.man.en $RPM_BUILD_ROOT%{_mandir}/man1/ekg.1

gzip -9nf ChangeLog docs/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libgadu -p /sbin/ldconfig
%postun -n libgadu -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/e*
%attr(4755,root,root) %{_bindir}/ioctl_daemon
%{_datadir}/ekg
%doc docs/{7thguard,dcc,on,themes,vars}.txt.gz
%doc ChangeLog.gz docs/{FAQ,README,TODO}.gz
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*

%files -n libgadu
%attr(755,root,root) %{_libdir}/libgadu.so.*

%files -n libgadu-devel
%defattr(644,root,root,755)
%{_includedir}/libgadu.h
%doc docs/{7thguard,api,devel-hints,protocol}.txt.gz
%doc ChangeLog.gz docs/{README,TODO}.gz

%files -n libgadu-static
%attr(644,root,root) %{_libdir}/libgadu.a
