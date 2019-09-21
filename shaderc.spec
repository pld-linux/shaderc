# TODO: glslc docs using asciidoctor
Summary:	Collection of tools, libraries and tests for shader compilation
Summary(pl.UTF-8):	Zestaw narzędzi, bibliotek i testów do kompilacji shaderów
Name:		shaderc
Version:	2019.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/google/shaderc/releases
# TODO:		https://github.com/google/shaderc/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/google/shaderc/archive/v%{version}.tar.gz
# Source0-md5:	8eb2b40712db2762a5cc40b568fd8ad9
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-shared.patch
URL:		https://github.com/google/shaderc
# for docs
#BuildRequires:	asciidoctor
BuildRequires:	cmake >= 2.8.12
BuildRequires:	glslang-devel >= 7.12.3352
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	python3 >= 1:3
BuildRequires:	spirv-tools >= 1:2019.4
BuildRequires:	spirv-tools-devel >= 1:2019.4
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
%setup -q
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
%attr(755,root,root) %{_libdir}/libshaderc.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libshaderc.so
%{_includedir}/shaderc
%{_pkgconfigdir}/shaderc.pc
%{_pkgconfigdir}/shaderc_combined.pc
%{_pkgconfigdir}/shaderc_static.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libshaderc.a
%{_libdir}/libshaderc_combined.a
