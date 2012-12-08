# Debug package is empty and rpmlint rejects build
%define _enable_debug_packages %{nil}
%define debug_package %{nil}

Summary:	KON - Kanji ON Linux console
Name:		kon2
Version:	0.3.9b
Release:	16
License:	BSD
Group:		System/Internationalization
Source0:	ftp://ftp.linet.gr.jp/pub/KON/kon2-%{version}.tar.bz2
Source1:	pubfont.a.gz
Source2:	pubfont.k.gz
Source3:	terminfo.kon
Patch0:		kon2-iso8859.diff
Patch1:		kon2-debian_jumbo_patch.diff
BuildRequires:	glibc-static-devel
Requires:	ncurses
Requires:	locales-ja
ExclusiveArch:	%{ix86} x86_64

%description
KON displays kanji characters on Linux console screen.
It is launched like a shell, so you should put at the very
end of your ~/.profile something like:

TTY=`tty | cut -b-8 2> /dev/null`

if [ "$TTY" = "/dev/tty" ]; then
   exec kon
fi

%prep
%setup -q 
%patch0 -p1
%patch1 -p1

cp %{SOURCE1} .

%build
make config 

# Don't use $RPM_OPT_FLAGS
make 

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/fonts
mkdir -p %{buildroot}%{_mandir}/ja/man1
mkdir -p %{buildroot}%{_sysconfdir}

make install TOPDIR=%{buildroot} MANDIR=%{buildroot}/%{_mandir}/ja/man1
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/fonts
install -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/fonts

# create a fake file for %ghost; this could be removed when ncurses
# will include a definition for 'kon'
mkdir -p %{buildroot}%{_datadir}/terminfo/k
touch %{buildroot}%{_datadir}/terminfo/k/kon

# install the English man page
mkdir -p %{buildroot}/%{_mandir}/man1
cp doc/kon.1.eng %{buildroot}/%{_mandir}/man1/kon.1

# remove useless files from doc directory
rm doc/kon.1* doc/*.buffer || :

%post
tic %{_defaultdocdir}/kon2-%{version}/terminfo.kon
if ! grep '^kon|kanji on console' %{_sysconfdir}/termcap >& /dev/null ; then
	 cat %{_defaultdocdir}/kon2-%{version}/termcap.kon >> %{_sysconfdir}/termcap
fi

%files
%defattr(0644,root,root,0755)
%doc doc/* terminfo.kon termcap.kon
%attr(4711,root,root) %{_bindir}/kon
%attr(755,root,root) %{_bindir}/fld
%attr(755,root,root) %{_bindir}/swkon
%attr(755,root,root) %{_bindir}/newvc
%{_mandir}/ja/man1/*
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/kon.cfg
%{_datadir}/fonts/pubfont.a.gz
%{_datadir}/fonts/pubfont.k.gz
%ghost %{_datadir}/terminfo/k/kon




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.3.9b-14mdv2011.0
+ Revision: 666038
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.9b-13mdv2011.0
+ Revision: 606270
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.3.9b-12mdv2010.1
+ Revision: 523158
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.3.9b-11mdv2010.0
+ Revision: 425494
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.3.9b-10mdv2009.1
+ Revision: 351343
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.3.9b-9mdv2009.0
+ Revision: 221928
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Dec 14 2007 Thierry Vignaud <tv@mandriva.org> 0.3.9b-8mdv2008.1
+ Revision: 119983
- it does build on x86_64 (which chmouel didn't know back in 2000)


* Sun Mar 18 2007 Oden Eriksson <oeriksson@mandriva.com> 0.3.9b-7mdv2007.1
+ Revision: 146046
- Import kon2

* Sun Mar 18 2007 Oden Eriksson <oeriksson@mandriva.com> 0.3.9b-7mdv2007.1
- use the %%mrel macro
- removed patches and use one jumbo patch by debian

