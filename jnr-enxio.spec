%{?_javapackages_macros:%_javapackages_macros}
%global commit_hash d320a2c
%global tag_hash 8dc2020

Name:           jnr-enxio
Version:        0.3
Release:        4.0%{?dist}
Summary:        Unix sockets for Java

# src/main/java/jnr/enxio/channels/PollSelectionKey.java is LGPLv3
# rest of the source code is ASL 2.0
License:        ASL 2.0 and LGPLv3
URL:            http://github.com/jnr/%{name}/
Source0:        https://github.com/jnr/%{name}/tarball/%{version}/jnr-%{name}-%{version}-0-g%{commit_hash}.tar.gz
BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  jpackage-utils
BuildRequires:  jnr-constants
BuildRequires:  jnr-ffi

BuildRequires:  maven-local
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  maven-surefire-provider-junit4

Requires:       java
Requires:       jpackage-utils
Requires:       jnr-constants
Requires:       jnr-ffi

%description
Unix sockets for Java.

%package javadoc
Summary:        Javadocs for %{name}

Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n jnr-%{name}-%{tag_hash}

find ./ -name '*.jar' -delete
find ./ -name '*.class' -delete

%build
mvn-rpmbuild install javadoc:aggregate

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  \
        $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%doc LICENSE
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}.jar

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 08 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3-3
- Document the multiple licensing scenario.

* Fri Feb 08 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3-2
- The license is in fact ASL 2.0 and LGPLv3.
- Properly use the dist tag.

* Wed Feb 06 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3-1
- Initial package.
