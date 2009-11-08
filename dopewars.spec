#
# TODO: move scores file to /var/games!
#
# Conditional build:
%bcond_without	gtk		# don't build GTK+ client
%bcond_without	curses		# don't build curses client
%bcond_without	sdl		# don't use sdl sound output
%bcond_without	esd		# don't use esd sound output
#
Summary:	Drug dealing game
Summary(pl.UTF-8):	Gra polegająca na handlowaniu narkotykami
Name:		dopewars
Version:	1.5.12
Release:	0.1
License:	GPL
Group:		Applications/Games
Source0:	http://dl.sourceforge.net/dopewars/%{name}-%{version}.tar.gz
# Source0-md5:	debf749de9053dc2fb2e74c37ae06206
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-scoredir.patch
URL:		http://dopewars.sourceforge.net/
%{?with_sdl:BuildRequires:	SDL-devel >= 1.0.0}
%{?with_sdl:BuildRequires:	SDL_mixer-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_esd:BuildRequires:	esound-devel >= 0.0.20}
BuildRequires:	glib2-devel >= 2.0.0
%{?with_gtk:BuildRequires:	gtk+2-devel >= 1:2.0.0}
%{?with_curses:BuildRequires:	ncurses-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Based on John E. Dell's old Drug Wars game, dopewars is a simulation
of an imaginary drug market. dopewars is an All-American game which
features buying, selling, and trying to get past the cops!

The first thing you need to do is pay off your debt to the Loan Shark.
After that, your goal is to make as much money as possible (and stay
alive)! You have one month of game time to make your fortune.

dopewars supports multiple players via TCP/IP. Chatting to and
fighting with other players (computer or human) is supported; check
the command line switches (via dopewars -h) for further information.

%description -l pl.UTF-8
dopewars jest symulacją wyimaginowanego narkotykowego rynku, bazującą
na starej grze Drug Wars autorstwa Johna E. Della. Jest to gra w
amerykańskim stylu polegająca na kupowaniu, sprzedawaniu i omijaniu
policji!

Pierwszą rzeczą jaką trzeba zrobić jest spłacenie długu. Potem celem
jest zdobycie jak największej ilości pieniędzy (i przeżycie)! Gracz ma
jeden miesiąc gry na zdobycie fortuny.

W dopewars można grać z wieloma graczami poprzez TCP/IP. Można także z
nimi rozmawiać i walczyć; więcej informacji w opisie parametrów linii
poleceń (pokaże je dopewars -h).

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-plugins \
	--enable-networking \
	%{?with_esd:--with-esd} \
	%{?with_sdl:--with-sdl} \
	%{?with_curses:--enable-curses-client} \
	%{?with_gtk:--enable-gui-client} \
	%{?with_gtk:--enable-gui-server}

%{__make} \
	CFLAGS="%{rpmcflags} -Wall -I/usr/include/ncurses"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	SCOREDIR=$RPM_BUILD_ROOT/var/games/dopewars \
	DESTDIR=${RPM_BUILD_ROOT}

# I think this could be done somehow prettier
mv $RPM_BUILD_ROOT%{_datadir}/gnome/apps/Games/dopewars.desktop $RPM_BUILD_ROOT%{_desktopdir}

rm -f doc/help/Makefile*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/dopewars -C %{_datadir}/dopewars.sco

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog LICENCE README doc/{*.html,help}
%attr(2755,root,games) %{_bindir}/*
%attr(770,root,games) /var/games/dopewars
%{_mandir}/man6/*
%{_libdir}/%{name}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
%{_datadir}/%{name}
