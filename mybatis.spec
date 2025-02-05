%bcond_with test
Name:                mybatis
Version:             3.5.8
Release:             1
Summary:             SQL Mapping Framework for Java
License:             Apache 2.0
URL:                 https://github.com/mybatis/mybatis-3
Source0:             https://github.com/mybatis/mybatis-3/archive/%{name}-%{version}.tar.gz
Source1:             mssql-jdbc-9.4.0.jre8.jar
Source2:             ognl-3.3.0.jar
Source3:             mybatis-parent-33.pom
Source4:             oss-parent-9.pom
Source5:             xmvn-reactor
Patch0:              0001-add-javadoc-plugin-in-pom-file.patch
BuildRequires:       maven maven-local java-1.8.0-openjdk-devel
Requires:            java-1.8.0-openjdk javapackages-tools
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
mvn install:install-file -DgroupId=org.mybatis -DartifactId=mybatis-parent -Dversion=33 -Dpackaging=pom -Dfile=%{SOURCE3}
mvn install:install-file -DgroupId=org.sonatype.oss -DartifactId=oss-parent -Dversion=9 -Dpackaging=pom -Dfile=%{SOURCE4}
%autosetup -n %{name}-3-%{name}-%{version} -p1
%pom_remove_dep org.slf4j:slf4j-log4j12
%pom_remove_plugin :maven-pdf-plugin
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
mvn install:install-file -DgroupId=com.microsoft.sqlserver -DartifactId=mssql-jdbc -Dversion=9.4.0.jre8 -Dpackaging=jar -Dfile=%{SOURCE1}
mvn install:install-file -DgroupId=ognl -DartifactId=ognl -Dversion=3.3.0 -Dpackaging=jar -Dfile=%{SOURCE2}
cp %{SOURCE5} ./.xmvn-reactor
echo `pwd` > absolute_prefix.log
sed -i 's/\//\\\//g' absolute_prefix.log
absolute_prefix=`head -n 1 absolute_prefix.log`
sed -i 's/absolute-prefix/'"$absolute_prefix"'/g' .xmvn-reactor

%build
mvn -Dproject.build.sourceEncoding=UTF-8 -DskipTests package

%install
%mvn_install
install -d -m 0755 %{buildroot}/%{_javadocdir}/%{name}
install -m 0755 target/mybatis-3.5.8-javadoc.jar %{buildroot}/%{_javadocdir}/%{name}

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc
%{_javadocdir}/mybatis
%license LICENSE NOTICE

%changelog
* Tue Apr 19 2022 wangkai <wangkai385@h-partners.com> - 3.5.8-1
- Upgrade 3.5.8

* Sat Jun 19 2021 lingsheng <lingsheng@huawei.com> - 3.2.8-2
- Fix CVE-2020-26945

* Fri Jan 8 2021 chengzihan <chengzihan2@huawei.com> - 3.2.8-1
- Package init
