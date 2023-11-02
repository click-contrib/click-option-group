Name:           python-click-option-group
Version:        0.0.0
Release:        %autorelease
Summary:        Option groups missing in Click

License:        BSD-3-Clause
URL:            https://github.com/click-contrib/click-option-group
Source:         %{pypi_source click-option-group}

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
click-option-group is a Click-extension package that adds option groups missing
in Click.}

%description %_description

%package -n python3-click-option-group
Summary:        %{summary}
%description -n python3-click-option-group %_description


%prep
%autosetup -n click-option-group-%{version}


%generate_buildrequires
%pyproject_buildrequires -x test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files click-option-group


%check
%pytest


%files -n python3-click-option-group -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog
