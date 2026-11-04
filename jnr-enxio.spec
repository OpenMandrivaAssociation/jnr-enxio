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
# jnr-parent configures surefire with a JDK toolchain that is not installed.
plugin = """      <plugin>
        <artifactId>maven-surefire-plugin</artifactId>
        <configuration combine.self="override"/>
      </plugin>
"""
marker = "</plugins>"
text = text[:text.rfind(marker)] + plugin + text[text.rfind(marker):]
path.write_text(text)
PY

%files -f .mfiles
%doc LICENSE README.md
