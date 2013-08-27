%define		ver	%(echo %{version} | tr . _)
%define		plugin	swfupload
Summary:	JavaScript & Flash Upload Library
Name:		js-%{plugin}
Version:	2.2.0.1
Release:	3
License:	MIT
Group:		Applications/WWW
Source0:	https://swfupload.googlecode.com/files/SWFUpload%20v%{version}%20Core.zip?/SWFUpload_v%{version}_Core.zip
# Source0-md5:	1bf14f5a7a9a3ecc529378ee50f0c59b
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		https://code.google.com/p/swfupload/
BuildRequires:	closure-compiler
BuildRequires:	js
BuildRequires:	rpmbuild(macros) >= 1.553
BuildRequires:	unzip
Requires:	webapps
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{plugin}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
SWFUpload is a JavaScript Library that wraps the Flash Player's upload
function. It brings your uploads to the next level with Multiple File
Selection, Upload Progress and Client-side File Size Checking.

Unlike other Flash upload tools, SWFUpload leaves the UI in the
developer's hands. Using a set of event handlers developers can
display upload progress and status to the user in their own HTML/CSS
UI.

Features:
- Multiple File Selection
- File Upload Progress
- Custom Limits for File Size and Number of Uploads
- Filter by File Type ie. *.jpg
- File Queue
- Customize the Browse Control
- Flash 10 Support (Starting with Version 2.2.0)
- Client-Side Image Resizing (JPG & PNG) (Starting with Version 2.5.0)

%prep
%setup -qc
mv 'SWFUpload v2.2.0.1 Core'/* .

mv 'Core Changelog.txt' Changelog.txt
mv 'swfupload license.txt' license.txt

%undos -f js

%build
install -d build

# compress .js
for js in *.js; do
	out=build/${js#*/}
%if 0%{!?debug:1}
	closure-compiler --js $js --charset UTF-8 --js_output_file $out
	js -C -f $out
%else
	cp -p $js $out
%endif
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}

cp -p build/%{plugin}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.min.js
cp -p %{plugin}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}-%{version}.js
ln -s %{plugin}-%{version}.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}.src.js
ln -s %{plugin}-%{version}.min.js $RPM_BUILD_ROOT%{_appdir}/%{plugin}.js

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -p $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc Changelog.txt license.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}
