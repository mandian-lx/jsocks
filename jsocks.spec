%{?_javapackages_macros:%_javapackages_macros}

Summary:	A pure Java SOCKS Server
Name:		jsocks
Version:	1.01
Release:	1
License:	Apache Software License
Group:		Development/Java
URL:		http://jsocks.sourceforge.net
#Source0:	https://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}_code%{version}.zip
# mkdir jsocks-code && pushd jsocks-code
# cvs -d:pserver:anonymous@jsocks.cvs.sourceforge.net:/cvsroot/jsocks login
# cvs -z3 -d:pserver:anonymous@jsocks.cvs.sourceforge.net:/cvsroot/jsocks co . -P jsocks
# popd
# cp -far jsocks-code jsocks-1.01
# find jsocks-1.01 -name "CVS*" -type d -exec rm -fr {} \; 2> /dev/null
# tar Jcf jsocks-1.01.tar.xz jsocks-1.01
Source0:	%{name}-%{version}.tar.xz
BuildArch:	noarch

BuildRequires:	jpackage-utils
BuildRequires:	java-devel

Requires:	java-headless
Requires:	jpackage-utils

%description
It is a SOCKS server written entirely in Java, which supports both SOCKS4
and SOCKS5 protocols. 

%files
%{_javadir}/%{name}*.jar

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
BuildArch:	noarch
%description javadoc
API documentation for %{name}.

%files javadoc
%{_javadocdir}/%{name}

#----------------------------------------------------------------------------

%prep
#% setup -q -c %{name}-%{version}
%setup -q
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

%build
# compile
javac -encoding UTF-8 -verbose \
	*.java \
	socks/*.java \
	test/*.java

# jars
%jar cf %{name}.jar \
	socks/*class \
	socks/server/*class

%jar cf %{name}_apps.jar \
		*.class *.properties *.gif

# add the index to the jars
%jar i %{name}.jar
%jar i %{name}_apps.jar

# javadoc
%javadoc \
	-d doc -public \
	`%__find ./socks -name '*java' -and -not -path "test/*java"`

%install
# jars
install -dm 0755 %{buildroot}%{_javadir}/
install -pm 0644 %{name}.jar %{buildroot}%{_javadir}/%{name}.jar
install -pm 0644 %{name}_apps.jar %{buildroot}%{_javadir}/%{name}_apps.jar

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/%{name}/
cp -pr doc/* %{buildroot}%{_javadocdir}/%{name}

