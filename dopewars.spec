#
# Conditional build:
# _without_gtk				don't build gtk client
# _without_curses			don't build curses client
# _without_sdl				don't use sdl sound output
# _without_esd				don't use esd sound output

Summary:	Drug dealing game
Summary(pl):	Gra polegaj�ca na handlowaniu narkotykami
Name:		dopewars
Version:	1.5.8
Release:	1
License:	GPL
Group:		Applications/Games
Source0:	http://prdownloads.sourceforge.net/dopewars/%{name}-%{version}.tar.gz
URL:		http://dopewars.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_esd:BuildRequires:	esound-devel >= 0.0.20}
Buildrequires:	glib2-devel >= 2.0.0
%{!?_without_gtk:BuildRequires:	gtk+2-devel >= 2.0.0}
%{!?_without_curses:BuildRequires:	ncurses-devel}
%{!?_without_sdl:BuildRequires:	SDL-devel >= 1.0.0}
%{!?_without_sdl:BuildRequires:	SDL_mixer-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Based on John E. Dell's old Drug Wars game, dopewars is a simulation
of an imaginary drug market. dopewars is an All-American game which
features buying, selling, and trying to get past the cops!

The first thing you need to do is pay off your debt to the Loan Shark.
After that, your goal is to make as much money as possible (and stay
alive)! You have one month of game time to make your fortune.

dopewars supports multiple players via. TCP/IP. Chatting to and
fighting with other players (computer or human) is supported; check
the command line switches (via dopewars -h) for further information.

%description -l pl
dopewars jest symulacj� wyimaginowanego narkotykowego rynku, bazuj�c�
na starej grze Johna E. Dell Drug Wars. Jest to gra w ameryka�skim
stylu polegaj�ca na kupowaniu, sprzedawaniu i omijaniu policji!

Pierwsz� rzecz� jak� musisz zrobi� jest sp�acenie d�ugu. Potem celem
jest zdobycie jak najwi�kszej ilo�ci pieni�dzy (i prze�ycie)! Masz
jeden miesi�c gry aby zdoby� fortun�.

W dopewars mo�na gra� z wieloma graczami poprzez TCP/IP. Mo�na tak�e z
nimi rozmawia� i walczy�; u�yj dopewars -h aby zdoby� dalsze
informacje.

%prep
%setup -q

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
		--enable-plugins \
		--enable-networking \
    %{!?_without_esd:--with-esd} \
    %{!?_without_sdl:--with-sdl} \
		%{!?_without_curses:--enable-curses-client} \
		%{!?_without_gtk:--enable-gui-client} \
		%{!?_without_gtk:--enable-gui-server}

%{__make} CFLAGS="%{rpmcflags} -Wall -I/usr/include/ncurses"

%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}%{_applnkdir}/Games

%{__make} install DESTDIR=${RPM_BUILD_ROOT}

# I think this could be done somehow prettier
mv ${RPM_BUILD_ROOT}%{_datadir}/gnome/apps/Games/dopewars.desktop ${RPM_BUILD_ROOT}%{_applnkdir}/Games

rm -f doc/help/Makefile*

%find_lang %{name}

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
%{_bindir}/dopewars -C %{_datadir}/dopewars.sco

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog LICENCE README doc/{*.html,help}
%attr(2755,root,games) %{_bindir}/*
%attr(0660,root,games) %config %{_datadir}/dopewars.sco
%{_mandir}/man6/*
%{_libdir}/%{name}
%{_applnkdir}/Games/*
%{_datadir}/pixmaps/*
%{_datadir}/%{name}
