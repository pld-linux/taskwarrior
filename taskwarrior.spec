%define		shortname	task
%define		crates_ver	3.4.1

Summary:	Taskwarrior is a command-line to do list manager
Summary(hu.UTF-8):	Taskwarrior egy parancssoros ToDo-kezelő
Summary(pl.UTF-8):	Taskwarrior - konsolowy manadżer rzeczy do zrobienia
Name:		taskwarrior
Version:	3.4.1
Release:	1
License:	MIT
Group:		Applications
Source0:	https://github.com/GothenburgBitFactory/taskwarrior/releases/download/v%{version}/task-%{version}.tar.gz
# Source0-md5:	840e8830305d675a9d36526361887e00
Source1:	%{name}-crates-%{crates_ver}.tar.xz
# Source1-md5:	b252f21b4ed995e452214e7e7c0c1aa3
Patch0:		system-sqlite3.patch
URL:		http://taskwarrior.org/
BuildRequires:	cargo
BuildRequires:	clang
BuildRequires:	clang-devel
BuildRequires:	cmake >= 3.22
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	rust
BuildRequires:	rust-bindgen
BuildRequires:	sqlite3-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%{?rust_req}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		vimdir		%{_datadir}/vim/vimfiles

%define		filterout	-fvar-tracking-assignments

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
%setup -q -n %{shortname}-%{version} -a1
%patch -P0 -p1
mv %{shortname}-%{crates_ver}/vendor .

export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"
install -d .cxxbridge
%cargo_install -f --locked --root .cxxbridge cxxbridge-cmd
export PATH=$PATH:$(pwd)/.cxxbridge/bin
export BINDGEN_EXTRA_CLANG_ARGS="%{rpmcflags} %{rpmcppflags}"
export LIBCLANG_PATH="%{_libdir}"
export LIBSQLITE3_SYS_USE_PKG_CONFIG=true
%cmake -B build \
	-DRust_CARGO_TARGET="%rust_target" \
	-DCOR_FROZEN=ON \
	-DENABLE_TLS_NATIVE_ROOTS=ON

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

export CARGO_HOME="$(pwd)/.cargo"
export CC="%{__cc}"
export CXX="%{__cxx}"
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export CPPFLAGS="%{rpmcppflags}"
export LDFLAGS="%{rpmldflags}"
export RUSTFLAGS="${RUSTFLAGS:-%{rpmrustflags}}"
export BINDGEN_EXTRA_CLANG_ARGS="%{rpmcflags} %{rpmcppflags}"
export LIBCLANG_PATH="%{_libdir}"
export LIBSQLITE3_SYS_USE_PKG_CONFIG=true
%{__make} install -C build \
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
%doc AUTHORS ChangeLog DEVELOPER.md README.md doc/rc
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
