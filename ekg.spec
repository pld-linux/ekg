%define        	snapshot	20011027
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
URL:		http://dev.null.pl/ekg/	
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A client compatible with Gadu-Gadu.

%description -l pl
Eksperymentalny Klient Gadu-Gadu.

%prep
%setup -q -n %{name}-%{snapshot} 

%build
./configure \
	%{?!debug:--without-debug}
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install ekg 	$RPM_BUILD_ROOT%{_bindir}

gzip -9nf ChangeLog README docs/* 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz docs/*
%attr(755,root,root) %{_bindir}/* 
