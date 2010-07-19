# TODO:
# - zsh completion subpackage (I don't know, what is the correct place)
%define	shortname task
Summary:	Taskwarrior is a command-line to do list manager
Summary(hu.UTF-8):	Taskwarrior egy parancssoros ToDo-kezelő
Name:		taskwarrior
Version:	1.9.2
Release:	0.9
License:	GPL v2
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

%package -n bash-completion-taskwarrior
Summary:	bash-completion for taskwarrior
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}

%description -n bash-completion-taskwarrior
bash-completion for taskwarrior.

%package -n vim-syntax-taskwarrior
Summary:	Vim-syntax: taskwarrior
Group:		Applications/Editors/Vim
Requires:	%{name} = %{version}-%{release}

%description -n vim-syntax-taskwarrior
Vim-syntax: taskwarrior.

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
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{shortname}

install -d $RPM_BUILD_ROOT%{bashdir}
install scripts/bash/task_completion.sh $RPM_BUILD_ROOT%{bashdir}/%{shortname}

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
%{bashdir}/%{shortname}

%files -n vim-syntax-taskwarrior
%defattr(644,root,root,755)
%{vimdir}/ftdetect/*
%{vimdir}/syntax/*
