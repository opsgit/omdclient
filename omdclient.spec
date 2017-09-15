Name:           omdclient
Group:          System Environment/Libraries
Version:        1.2.0
Release:        1%{?dist}
Summary:        OMD/WATO API check_mk connection tools for puppet
URL:            http://github.com/tskirvin/omdclient.git

License:        Artistic 2.0
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       rsync shyaml moreutils python-beautifulsoup4 python-requests
BuildRequires:  rsync

Source:         omdclient-%{version}-%{release}.tar.gz

%description
Tools to interact with the OMD/WATO API for check_mk, and to tie them 
into puppet.

%prep
%setup -q -c -n omdclient

%build
# Empty build section added per rpmlint

%install
if [[ $RPM_BUILD_ROOT != "/" ]]; then
    rm -rf $RPM_BUILD_ROOT
fi

for i in etc usr; do
    rsync -Crlpt --delete ./${i} ${RPM_BUILD_ROOT}
done

for i in bin sbin; do
    if [ -d ${RPM_BUILD_ROOT}/$i ]; then
        chmod 0755 ${RPM_BUILD_ROOT}
    fi
done

mkdir -p ${RPM_BUILD_ROOT}/usr/share/man/man1
for i in `ls usr/bin`; do
    pod2man --section 1 --center="System Commands" usr/bin/${i} \
        > ${RPM_BUILD_ROOT}/usr/share/man/man1/${i}.1 ;
done

python setup.py install --prefix=${RPM_BUILD_ROOT}/usr

%clean
# Adding empty clean section per rpmlint.  In this particular case, there is 
# nothing to clean up as there is no build process

%files
%defattr(-,root,root)
%config(noreplace) /etc/omdclient/config.yaml
%config(noreplace) /etc/omdclient/place.holder
%{_bindir}/omd-*
/usr/share/man/man1/*
/usr/libexec/omdclient/git-hooks/*
/usr/lib*/python*/site-packages/*
/etc/omdclient/*

%changelog
* Fri Sep 15 2017   Tim Skirvin <tskirvin@fnal.gov>     1.2.0-1
- omd-host-tag - eliminating an extra print statement

* Fri Sep 15 2017   Tim Skirvin <tskirvin@fnal.gov>     1.2.0-0
- omd-host-crud - now prints all listed system tags
- omd-host-tag - new script, set or unset tags for a given host
- updateHost()'s unset_attributes bit should actually work now (tested as
  part of omd-host-tag)

* Tue Sep 12 2017   Tim Skirvin <tskirvin@fnal.gov>     1.1.8-0
- omd-host-crud - read functions only print relevant fields
- listHostsFiltered() function - print hosts where the site matches

* Tue Mar 24 2017   Tim Skirvin <tskirvin@fnal.gov>     1.1.7-0
- omd-nagios-report - now deals with UTF-8 better

* Tue Mar 24 2017   Tim Skirvin <tskirvin@fnal.gov>     1.1.6-0
- omd-nagios-hostlist
- some additional changes from epleterte involving IP addresses

- omdclient/__init.py__ - inventories can now choose to do tabula rasa
- omd-reinventory - allowed to select tabula rasa
- omd-activate - allows us to activate foreign keys

* Tue Jun 21 2016   Tim Skirvin <tskirvin@fnal.gov>     1.1.5-1
- omdclient/__init.py__ - inventories can now choose to do tabula rasa
- omd-reinventory - allowed to select tabula rasa
- omd-activate - allows us to activate foreign keys

* Tue Jun 21 2016   Tim Skirvin <tskirvin@fnal.gov>     1.1.5-0
- omdclient/__init.py__ - inventories now do tabula rasa refresh

* Tue Jun 21 2016   Tim Skirvin <tskirvin@fnal.gov>     1.1.4-0
- omd-nagios-hosts-with-problem - discover hosts with a given problem
- omd-reinventory - start a reinventory of a given host

* Wed Jun 15 2016   Tim Skirvin <tskirvin@fnal.gov>     1.1.3-0
- omd-nagos-report - skips errors on service prints rather than crashing
- omdclient/__init__.py - actually sets downtimes now (I had the required
  date format wrong)

* Thu Jun 25 2015  Tim Skirvin <tskirvin@fnal.gov>      1.1.2-0
- omd-puppet-crud - adds 'inventory' option (kinda cheating)

* Thu Jun 25 2015  Tim Skirvin <tskirvin@fnal.gov>      1.1.2-0
- omd-puppet-enc - sends shyaml errors to stderr

* Thu Jun 25 2015  Tim Skirvin <tskirvin@fnal.gov>      1.1.1-0
- omd-puppet-enc - sends shyaml errors to stderr

* Mon Jun 15 2015  Tim Skirvin <tskirvin@fnal.gov>      1.1.0-0
- added omd-nagios-report, omd-nagios-ack, omd-nagios-downtime
- fixed the git post-receive hook

* Mon Jun 15 2015  Tim Skirvin <tskirvin@fnal.gov>      1.0.0-0
- initial commit
