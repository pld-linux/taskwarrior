%define		shortname	task
Summary:	Taskwarrior is a command-line to do list manager
Summary(hu.UTF-8):	Taskwarrior egy parancssoros ToDo-kezelő
Summary(pl.UTF-8):	Taskwarrior - konsolowy manadżer rzeczy do zrobienia
Name:		taskwarrior
Version:	2.6.2
Release:	1
License:	MIT
Group:		Applications
Source0:	https://www.taskwarrior.org/download/%{shortname}-%{version}.tar.gz
# Source0-md5:	a9e69fd612e8ad538b9f512c80b18122
URL:		http://taskwarrior.org/
BuildRequires:	cmake >= 3.0
BuildRequires:	gnutls-devel
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
programu task (najlepszego konsolowego menadżera zadań stworzonego
przez Paula Beckinghama) poprzez dodanie interaktywnego interfejsu,
potężnej wyszukiwarki, skrótów klawiszowych, formularzy wprowadzania
danych i wielu innych ulepszeń.

%package -n bash-completion-taskwarrior
Summary:	bash-completion for taskwarrior
Summary(pl.UTF-8):	bashowe uzupełnianie nazw dla taskwarriora
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion
BuildArch:	noarch

%description -n bash-completion-taskwarrior
bash-completion for taskwarrior.

%description -n bash-completion-taskwarrior -l pl.UTF-8
Pakiet ten dostarcza bashowe uzupełnianie nazw dla taskwarriora.

%package -n fish-completion-taskwarrior
Summary:	fish-completion for taskwarrior
Summary(pl.UTF-8):	Uzupełnianie nazw w fish dla taskwarriora
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-taskwarrior
fish-completion for taskwarrior.

%description -n fish-completion-taskwarrior -l pl.UTF-8
Pakiet ten dostarcza uzupełnianie nazw w fish dla taskwarriora.

%package -n vim-syntax-taskwarrior
Summary:	Vim-syntax: taskwarrior
Summary(pl.UTF-8):	Składnia dla Vima: taskwarrior
Group:		Applications/Editors/Vim
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description -n vim-syntax-taskwarrior
Vim-syntax: taskwarrior.

%description -n vim-syntax-taskwarrior -l pl.UTF-8
Ta wtyczka dostarcza podświetlanie składni dla taskwarriora.

%package -n zsh-completion-taskwarrior
Summary:	zsh-completion for taskwarrior
Summary(pl.UTF-8):	Uzupełnianie nazw w zsh dla taskwarriora
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description -n zsh-completion-taskwarrior
zsh-completion for taskwarrior.

%description -n zsh-completion-taskwarrior -l pl.UTF-8
Pakiet ten dostarcza funkcje uzupełniania nazw powłoki zsh dla
taskwarriora.

%prep
%setup -q -n %{shortname}-%{version}

%build
%cmake

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{shortname}

install -d $RPM_BUILD_ROOT{%{bash_compdir},%{fish_compdir},%{zsh_compdir}}
install -p scripts/bash/task.sh $RPM_BUILD_ROOT%{bash_compdir}
install -p scripts/fish/task.fish $RPM_BUILD_ROOT%{fish_compdir}
install -p scripts/zsh/_task $RPM_BUILD_ROOT%{zsh_compdir}

install -d $RPM_BUILD_ROOT%{vimdir}/{ftdetect,syntax}
for dir in ftdetect syntax; do
	install -d $RPM_BUILD_ROOT%{vimdir}/$dir
	install -p scripts/vim/$dir/* $RPM_BUILD_ROOT%{vimdir}/$dir
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog DEVELOPER.md NEWS README.md doc/rc
%attr(755,root,root) %{_bindir}/%{shortname}
%{_mandir}/man1/task.1*
%{_mandir}/man5/task-color.5*
%{_mandir}/man5/task-sync.5*
%{_mandir}/man5/taskrc.5*

%files -n bash-completion-taskwarrior
%defattr(644,root,root,755)
%{bash_compdir}/task.sh

%files -n fish-completion-taskwarrior
%defattr(644,root,root,755)
%{fish_compdir}/task.fish

%files -n vim-syntax-taskwarrior
%defattr(644,root,root,755)
%{vimdir}/ftdetect/*.vim
%{vimdir}/syntax/*.vim

%files -n zsh-completion-taskwarrior
%defattr(644,root,root,755)
%{zsh_compdir}/_task
