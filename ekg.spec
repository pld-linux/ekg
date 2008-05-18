#
# Conditional build:
%bcond_without	aspell		# without spell checking
%bcond_without	voip		# without VoIP support
%bcond_without	python		# with python support
%bcond_without	pthread		# build with Posix threads support
%bcond_with	ioctl_daemon	# with ioctl_daemon (suid root)
%bcond_with	lock_reason	# with lock_reason patch
#
Summary:	A client compatible with Gadu-Gadu
Summary(de.UTF-8):	Ein Cliente kompatibel mit Gadu-Gadu
Summary(es.UTF-8):	Un cliente compatible con Gadu-Gadu
Summary(it.UTF-8):	Un cliente compatibile con Gadu-Gadu
Summary(pl.UTF-8):	Klient kompatybilny z Gadu-Gadu
Name:		ekg
Version:	1.7
%define		snap 20071225
Release:	4.20071225
Epoch:		4
License:	GPL v2
Group:		Applications/Communications
Source0:	http://ekg.chmurka.net/%{name}-%{snap}.tar.gz
# Source0-md5:	34b541bb6c58695dee2b9aea0a5d6d74
Source1:	%{name}.conf
Patch0:		%{name}-LDFLAGS.patch
Patch1:		%{name}-lock_reason.patch
URL:		http://ekg.chmurka.net/
BuildRequires:	%{_bindir}/perl
%{?with_aspell:BuildRequires:	aspell-devel}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libgadu-devel >= 4:1.7.0
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
Requires:	libgadu >= 4:1.7.0
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

%description -l de.UTF-8
Ein Cliente kompatibel mit Gadu-Gadu.

%description -l es.UTF-8
Un cliente compatible con Gadu-Gadu.

%description -l it.UTF-8
Un cliente compatibile con Gadu-Gadu.

%description -l pl.UTF-8
EKG ("Eksperymentalny Klient Gadu-Gadu") jest open source'owym
klientem gadu-gadu dla systemów uniksowych. Gadu-Gadu to popularny w
Polsce komunikator internetowy.

Możliwości EKG:
  - interfejs użytkownika podobny do irssi,
  - wysyłanie i odbieranie plików,
  - rozmowy głosowe,
  - uruchamianie poleceń powłoki w określonych sytuacjach,
  - wczytywanie wejścia z potoku,
  - wsparcie dla skryptów w języku Python,
  - synteza mowy (z użyciem zewnętrznego programu),
  - wsparcie dla szyfrowania.

Program nie jest umiędzynarodowiony i wszystkie komunikaty są po
polsku (jednak komendy są w języku angielskim).

%prep
%setup -q -n %{name}-%{snap}
%patch0 -p0
%if %{with lock_reason}
%patch1 -p1
%endif

%build
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%configure \
	CFLAGS_LIBGADU="%{rpmcflags}" \
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

%{__make}

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

%if %{with ioctl_daemon}
install src/ioctld $RPM_BUILD_ROOT%{_bindir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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
