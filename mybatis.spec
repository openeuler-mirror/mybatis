%bcond_with test
Name:                mybatis
Version:             3.2.8
Release:             1
Summary:             SQL Mapping Framework for Java
License:             Apache 2.0
URL:                 https://github.com/mybatis/mybatis-3
Source0:             https://github.com/mybatis/mybatis-3/archive/%{name}-%{version}.tar.gz
Patch0:              %{name}-%{version}-commons-ognl.patch
Patch1:              mybatis-3.2.8-log4j2.6.patch
BuildRequires:       maven-local mvn(cglib:cglib) mvn(commons-logging:commons-logging)
BuildRequires:       mvn(log4j:log4j:1.2.17) mvn(org.apache.commons:commons-ognl)
BuildRequires:       mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:       mvn(org.apache.logging.log4j:log4j-core)
BuildRequires:       mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:       mvn(org.apache.maven.plugins:maven-site-plugin) mvn(org.javassist:javassist)
BuildRequires:       mvn(org.mybatis:mybatis-parent:pom:) mvn(org.slf4j:slf4j-api)
%if %{with test}
BuildRequires:       mvn(commons-dbcp:commons-dbcp) mvn(junit:junit) mvn(org.apache.derby:derby)
BuildRequires:       mvn(org.apache.geronimo.specs:geronimo-jta_1.1_spec)
BuildRequires:       mvn(org.apache.geronimo.specs:specs:pom:) mvn(org.apache.velocity:velocity)
BuildRequires:       mvn(org.hsqldb:hsqldb) mvn(org.mockito:mockito-core) mvn(postgresql:postgresql)
%endif
BuildArch:           noarch

%description
The MyBatis data mapper framework makes it easier
to use a relational database with object-oriented
applications. MyBatis couples objects with stored
procedures or SQL statements using a XML descriptor
or annotations. Simplicity is the biggest advantage
of the MyBatis data mapper over object relational
mapping tools.
To use the MyBatis data mapper, you rely on your
own objects, XML, and SQL. There is little to
learn that you don't already know. With the
MyBatis data mapper, you have the full power of
both SQL and stored procedures at your fingertips.
The MyBatis project is developed and maintained by
a team that includes the original creators of the
"iBATIS" data mapper. The Apache project was retired
and continued here.

%package javadoc
Summary:             Javadoc for %{name}
%description javadoc
This package contains javadoc for %{name}.

%prep
%autosetup -n %{name}-3-%{name}-%{version} -p1
%pom_remove_dep org.slf4j:slf4j-log4j12
%pom_remove_plugin :maven-pdf-plugin
%pom_remove_plugin :jarjar-maven-plugin
%pom_remove_plugin :cobertura-maven-plugin
sed -i 's/\r//' LICENSE NOTICE
%if %{with test}
%pom_remove_dep javax.transaction:transaction-api
%pom_add_dep org.apache.geronimo.specs:geronimo-jta_1.1_spec::test
rm src/test/java/org/apache/ibatis/parsing/GenericTokenParserTest.java
rm src/test/java/org/apache/ibatis/submitted/multipleresultsetswithassociation/MultipleResultSetTest.java \
 src/test/java/org/apache/ibatis/submitted/includes/IncludeTest.java \
 src/test/java/org/apache/ibatis/submitted/resultmapwithassociationstest/ResultMapWithAssociationsTest.java \
 src/test/java/org/apache/ibatis/submitted/nestedresulthandler_association/NestedResultHandlerAssociationTest.java
rm src/test/java/org/apache/ibatis/logging/LogFactoryTest.java
%endif
%mvn_file :%{name} %{name}

%build
%if %{without test}
opts="-f"
%endif
%mvn_build $opts -- -Dproject.build.sourceEncoding=UTF-8


%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Fri Jan 8 2021 chengzihan <chengzihan2@huawei.com> - 3.2.8-1
- Package init
