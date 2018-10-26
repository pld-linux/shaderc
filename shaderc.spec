# TODO: glslc docs using asciidoctor
Summary:	Collection of tools, libraries and tests for shader compilation
Summary(pl.UTF-8):	Zestaw narzędzi, bibliotek i testów do kompilacji shaderów
Name:		shaderc
# 2018.0 requires glslang >= 201803xx
#Version:	2018.0
Version:	0
%define	snap	20180209
%define	gitref	d1f763cc3742b93f0fc090493be8ba0588f296da
Release:	0.%{snap}.1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/google/shaderc/releases
Source0:	https://github.com/google/shaderc/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	95a05fcd88a242b2f391cf5d165171be
#Source0:	https://github.com/google/shaderc/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-shared.patch
URL:		https://github.com/google/shaderc
# for docs
#BuildRequires:	asciidoctor
BuildRequires:	cmake >= 2.8.12
BuildRequires:	glslang-devel >= 3.0.s20180205
BuildRequires:	python >= 2
BuildRequires:	spirv-tools
BuildRequires:	spirv-tools-devel >= v2018.1-0.s20180210
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A collection of tools, libraries and tests for shader compilation. At
the moment it includes:
 - glslc, a command line compiler for GLSL/HLSL to SPIR-V, and
 - libshaderc, a library API for doing the same.

Shaderc wraps around core functionality in glslang and SPIRV-Tools.
Shaderc aims to to provide:
 - a command line compiler with GCC- and Clang-like usage, for better
   integration with build systems
 - an API where functionality can be added without breaking existing
   clients
 - an API supporting standard concurrency patterns across multiple
   operating systems
 - increased functionality such as file #include support

%description -l pl.UTF-8
Zestaw narzędzi, bibliotek i testów do kompilacji shaderów. Obecnie
zawiera:
 - glslc - kompilator linii poleceń dla GLSL/HLSL do SPIR-V
 - libshaderc - biblioteka do tego samego

Shaderc obudowuje podstawową funkcjonalność glslang i SPIRV-Tools.
Celem shaderc jest zapewnienie:
 - kompilatora linii poleceń używalnego podobnie do GCC czy Clang
   (w celu lepszej integracji z systemami budowania)
 - API, do którego można dodawać funkcjonalność bez psucia
   istniejących klientów
 - API obsługującego standardowe wzorce współbieżności na wielu
   systemach operacyjnych
 - zwiększonej funkcjonalności, np. obsługi #include

%package devel
Summary:	Header files for shaderc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki shaderc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for shaderc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki shaderc.

%package static
Summary:	Static shaderc libraries
Summary(pl.UTF-8):	Statyczne biblioteki shaderc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static shaderc libraries.

%description static -l pl.UTF-8
Statyczne biblioteki shaderc.

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake .. \
	-DSHADERC_SKIP_TESTS=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES CONTRIBUTORS README.md  glslc/README.asciidoc
%attr(755,root,root) %{_bindir}/glslc
%attr(755,root,root) %{_libdir}/libshaderc.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/shaderc

%files static
%defattr(644,root,root,755)
%{_libdir}/libshaderc.a
%{_libdir}/libshaderc_combined.a
%{_libdir}/libshaderc_util.a
