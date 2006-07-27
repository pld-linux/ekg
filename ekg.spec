#
# Conditional build:
%bcond_without	aspell		# without spell checking
%bcond_without	voip		# without VoIP support
%bcond_without	python		# with python support
%bcond_without	pthread		# build with Posix threads support
%bcond_with	ioctl_daemon	# with ioctl_daemon (suid root)
#
Summary:	A client compatible with Gadu-Gadu
Summary(de):	Ein Cliente kompatibel mit Gadu-Gadu
Summary(es):	Un cliente compatible con Gadu-Gadu
Summary(it):	Un cliente compatibile con Gadu-Gadu
Summary(pl):	Klient kompatybilny z Gadu-Gadu
Name:		ekg
Version:	1.6
Release:	1
Epoch:		4
License:	GPL v2
Group:		Applications/Communications
Source0:	http://ekg.chmurka.net/%{name}-%{version}.tar.gz
# Source0-md5:	1094eee5062d9b9900c4b28bd68fb564
Source1:	%{name}.conf
Patch0:		%{name}-jpeg.patch
URL:		http://ekg.chmurka.net/
BuildRequires:	%{_bindir}/perl
%{?with_aspell:BuildRequires:	aspell-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_voip:BuildRequires:	libgsm-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel >= 0.9.7d
%if %{with python}
BuildRequires:	python
BuildRequires:	python-devel
%endif
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
Requires:	libgadu = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
EKG ("Eksperymentalny Klient Gadu-Gadu") is an open source gadu-gadu
client for UNIX systems. Gadu-Gadu is an instant messaging program,
very popular in Poland.

EKG features include:
  - irssi-like ncurses interface
  - sending and receiving files
  - voice conversations
  - launching shell commands on certain events
  - reading input from pipe
  - python scripting support
  - speech synthesis (using an external program)
  - encryption support

Please note that the program is not internationalized and all messages
are in Polish (although the commands are in English).

%description -l de
Ein Cliente kompatibel mit Gadu-Gadu.

%description -l es
Un cliente compatible con Gadu-Gadu.

%description -l it
Un cliente compatibile con Gadu-Gadu.

%description -l pl
EKG ("Eksperymentalny Klient Gadu-Gadu") jest open source'owym
klientem gadu-gadu dla systemów uniksowych. Gadu-Gadu to popularny w
Polsce komunikator internetowy.

Mo¿liwo¶ci EKG:
  - interfejs u¿ytkownika podobny do irssi,
  - wysy³anie i odbieranie plików,
  - rozmowy g³osowe,
  - uruchamianie poleceñ pow³oki w okre¶lonych sytuacjach,
  - wczytywanie wej¶cia z potoku,
  - wsparcie dla skryptów w jêzyku Python,
  - synteza mowy (z u¿yciem zewnêtrznego programu),
  - wsparcie dla szyfrowania.

Program nie jest umiêdzynarodowiony i wszystkie komunikaty s± po
polsku (jednak komendy s± w jêzyku angielskim).

%package -n libgadu
Summary:	libgadu library
Summary(es):	Biblioteca libgadu
Summary(pl):	Biblioteka libgadu
License:	LGPL v2.1
Group:		Libraries
Obsoletes:	libgg

%description -n libgadu
libgadu is intended to make it easy to add Gadu-Gadu communication
support to your software.

%description -n libgadu -l de
Mit libgadu ist es Ihnen möglich auf einfache Weise Gadu-Gadu
Kommunikations-Unterstützung in Ihre Software einzubinden.

%description -n libgadu -l es
libgadu está pensada para facilitar añadirle comunicación vía
Gadu-Gadu a su software.

%description -n libgadu -l pl
libgadu umo¿liwia ³atwe dodanie do ró¿nych aplikacji komunikacji
bazuj±cej na protokole Gadu-Gadu.

%package -n libgadu-devel
Summary:	libgadu development library
Summary(es):	Biblioteca de desarrollo de libgadu
Summary(pl):	Czê¶æ biblioteki libgadu dla programistów
License:	LGPL v2.1
Group:		Development/Libraries
Requires:	libgadu = %{epoch}:%{version}-%{release}
Requires:	openssl-devel
Obsoletes:	libgg-devel

%description -n libgadu-devel
The libgadu-devel package contains the header files and some
documentation needed to develop application with libgadu.

%description -n libgadu-devel -l de
Das libgadu-devel Paket enthält Header-Files (Kopfzeilenordner) und
die Dokumentation die Sie benötigen um mit libgadu Anwendungen zu
entwickeln.

%description -n libgadu-devel -l es
El paquete libgadu-devel contiene los ficheros de cabecera, juntos con
una documentación, necesarios para desarrollar aplicaciones que usar
libgadu.

%description -n libgadu-devel -l pl
Pakiet libgadu-devel zawiera pliki nag³ówkowe i dokumentacjê,
potrzebne do kompilowania aplikacji korzystaj±cych z libgadu.

%package -n libgadu-static
Summary:	Static libgadu library
Summary(es):	Biblioteca libgadu estática
Summary(pl):	Statyczna biblioteka libgadu
License:	LGPL v2.1
Group:		Development/Libraries
Requires:	libgadu-devel = %{epoch}:%{version}-%{release}
Obsoletes:	libgg-static

%description -n libgadu-static
Static libgadu library.

%description -n libgadu-static -l de
Statisches libgadu Archiv.

%description -n libgadu-static -l es
Biblioteca libgadu estática.

%description -n libgadu-static -l pl
Statyczna biblioteka libgadu.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%configure \
	--enable-dynamic \
	--enable-shared \
	--enable-static \
%if %{with pthread}
	--with-pthread \
%else
	--without-pthread \
%endif
	--without-bind \
	%{?with_python:--with-python} \
	%{!?with_voip:--without-libgsm} \
	%{?with_aspell:--enable-aspell} \
	%{?with_ioctl_daemon:--enable-ioctld}

%{__make} \
	CC="%{__cc} %{rpmcflags} -Wall -I/usr/include/ncurses"

%if %{with ioctl_daemon}
%{__make} -C src ioctld
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install install-ekl2 \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

# For libgadu-devel

rm -f examples/Makefile examples/Makefile.in examples/.cvsignore
rm -rf examples/CVS

install -d $RPM_BUILD_ROOT%{_examplesdir}/libgadu-%{version}
cp -af examples/* $RPM_BUILD_ROOT%{_examplesdir}/libgadu-%{version}

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
%{?with_aspell:%doc docs/slownik.txt}
%doc ChangeLog docs/{FAQ,README,TODO,ULOTKA} docs/emoticons.{ansi,sample}
%attr(755,root,root) %{_bindir}/e*
%{?with_ioctl_daemon:%attr(4755,root,root) %{_bindir}/ioctld}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.conf
%{_datadir}/ekg
%{_mandir}/man1/*
%lang(pl) %{_mandir}/pl/man1/*

%files -n libgadu
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgadu.so.*.*

%files -n libgadu-devel
%defattr(644,root,root,755)
%doc docs/{7thguard,ui,devel-hints,przenosny-kod}.txt docs/protocol.html
%doc ChangeLog docs/{README,TODO}
%attr(755,root,root) %{_libdir}/libgadu.so
%{_includedir}/libgadu.h
%{_includedir}/libgadu-config.h
%{_pkgconfigdir}/libgadu.pc
%{_examplesdir}/libgadu-%{version}

%files -n libgadu-static
%defattr(644,root,root,755)
%{_libdir}/libgadu.a
