# Package needs to stay arch specific (due to nagios plugins location), but
# there's nothing to extract debuginfo from
%global debug_package %{nil}

%define nagios_plugins_dir %{_libdir}/nagios/plugins

Name:       nagios-plugins-storage-space
Version:    0.0.1
Release:    1%{?dist}
Summary:    Nagios probes to be run remotely against EGI Online endpoints
License:    MIT
Group:      Applications/Internet
URL:        https://github.com/EGI-Federation/nagios-plugins-storage-space
# The source of this package was pulled from upstream's vcs. Use the
# following commands to generate the tarball:
Source0:   %{name}-%{version}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires:  cmake
Requires:   nagios%{?_isa}
Requires:   python36
Requires:   python36-pycurl
Requires:   python3-nap


%description
This package provides the nagios probes for storage free space monitor

%prep
%setup -q -n %{name}-%{version}

%build
%cmake . -DCMAKE_INSTALL_PREFIX=/

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nagios_plugins_dir}/storage-space
%doc LICENSE README.md

%changelog
* Wed 27 September  2023 Andrea Manzi <andrea.manzi@egi.eu> - 0.0.1-0
- first version
