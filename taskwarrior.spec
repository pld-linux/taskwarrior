%define		shortname	task
Summary:	Taskwarrior is a command-line to do list manager
Summary(hu.UTF-8):	Taskwarrior egy parancssoros ToDo-kezelő
Summary(pl.UTF-8):	Taskwarrior - konsolowy manadźer rzeczy do zrobienia
Name:		taskwarrior
Version:	1.9.2
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://www.taskwarrior.org/download/%{shortname}-%{version}.tar.gz
# Source0-md5:	be98cc74fe03b8336250e0b7ed3cd8c7
Patch0:		%{name}-flags.patch
Patch1:		%{name}-tinfo.patch
URL:		http://taskwarrior.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	ncurses-ext-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define bashdir	%{_sysconfdir}/bash_completion.d
%define vimdir %{_datadir}/vim/vimfiles

%description
Taskwarrior is an ambitious project to supercharge task (most
excellent CLI task manager by Paul Beckingham) with an interactive
interface, a powerful search tool, hotkeys, forms data entry, and a
host of new features.

%description -l hu.UTF-8
Taskwarrior egy törekvő project, amely a task-ot bővíti ki (a legjobb
CLI feladatkezelő Paul Beckingham-től) egy interaktív felületettel,
hatékony kereső eszközzel, hotkey-ekkel, űrlapokkal és új lehetőségek
tömegeivel.

%description -l pl.UTF-8
Taskwarrior jest ambitnym projektem mającym na celu ulepszenie
programu task (najlepszego konsolowego manadżera zadań stworzonego
przez Paula Beckinghama) poprzez dodanie interaktywnego interfejsu,
potężnej wyszukiwarki, skrótów klawiszowych, formularzy wprowadzania
danych i wiele innych ulepszeń.

%package -n bash-completion-taskwarrior
Summary:	bash-completion for taskwarrior
Summary(pl.UTF-8):	bashowe uzupełnianie nazw dla taskwarriora
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}

%description -n bash-completion-taskwarrior
bash-completion for taskwarrior.

%description -n bash-completion-taskwarrior -l pl.UTF-8
Pakiet ten dostarcza bashowe uzupełnianie nazw dla taskwarriora.

%package -n vim-syntax-taskwarrior
Summary:	Vim-syntax: taskwarrior
Summary(pl.UTF-8):	Składnia dla Vima: taskwarrior
Group:		Applications/Editors/Vim
Requires:	%{name} = %{version}-%{release}

%description -n vim-syntax-taskwarrior
Vim-syntax: taskwarrior.

%description -n vim-syntax-taskwarrior -l pl.UTF-8
Ta wtyczka dostarcza podświetlanie składni dla taskwarriora.

%prep
%setup -q -n %{shortname}-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-ncurses-inc="$(pkg-config --variable=includedir ncurses++w)" \
	--with-ncurses-lib="$(pkg-config --libs ncurses++w)"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	bashscriptsdir=%{_sysconfdir}/bash_completion.d

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{shortname}

install -d $RPM_BUILD_ROOT%{vimdir}/{ftdetect,syntax}
for dir in ftdetect syntax; do
	install -d $RPM_BUILD_ROOT%{vimdir}/$dir
	install scripts/vim/$dir/* $RPM_BUILD_ROOT%{vimdir}/$dir
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README i18n doc/rc
%attr(755,root,root) %{_bindir}/%{shortname}
%{_mandir}/man1/*1*
%{_mandir}/man5/*5*

%files -n bash-completion-taskwarrior
%defattr(644,root,root,755)
%{_sysconfdir}/bash_completion.d/*

%files -n vim-syntax-taskwarrior
%defattr(644,root,root,755)
%{vimdir}/ftdetect/*
%{vimdir}/syntax/*
