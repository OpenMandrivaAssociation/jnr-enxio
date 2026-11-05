Name:		jnr-enxio
Version:	0.33.6
Release:	1
Summary:	Native I/O access for Java
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/jnr/jnr-enxio
Source0:	https://github.com/jnr/jnr-enxio/archive/refs/tags/jnr-enxio-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	jnr-parent
BuildRequires:	jnr-constants
BuildRequires:	jnr-ffi
BuildSystem:	maven

%description
Native I/O access for Java, used by jnr-unixsocket.

%prep
%setup -q -n jnr-enxio-jnr-enxio-%{version}
# Publishing to Central is not part of the package build.
# bnd's wildcard import reads a bundle version from every jar, and ASM has none.
python - <<'PY'
import re
from pathlib import Path
path = Path("pom.xml")
text = path.read_text()
text = re.sub(
	r"\s*<plugin>\s*<groupId>org\.sonatype\.central</groupId>\s*<artifactId>central-publishing-maven-plugin</artifactId>.*?</plugin>",
	"",
	text,
	count=1,
	flags=re.S,
)
text = re.sub(
	r"\s*<plugin>\s*<groupId>org\.apache\.felix</groupId>\s*<artifactId>maven-bundle-plugin</artifactId>.*?</plugin>",
	"",
	text,
	count=1,
	flags=re.S,
)
text = re.sub(r"\s*<manifestFile>.*?</manifestFile>", "", text, count=1, flags=re.S)
text = text.replace(
	"<artifactId>maven-jar-plugin</artifactId>",
	"<artifactId>maven-jar-plugin</artifactId>\n        <version>3.3.0</version>",
	1,
)
# pluginManagement is what a child inherits. An empty configuration
# replaces jnr-parent's JDK toolchain, which runs even when tests are skipped.
text = text.replace(
	"<build>",
	"""<build>
    <pluginManagement>
      <plugins>
        <plugin>
          <artifactId>maven-surefire-plugin</artifactId>
          <configuration combine.self="override"/>
        </plugin>
      </plugins>
    </pluginManagement>""",
	1,
)
path.write_text(text)
PY

%files -f .mfiles
%doc LICENSE README.md
