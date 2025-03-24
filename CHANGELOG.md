# Changelog

## v0.5.7 (24.03.2025)

* Add return type Decorator (PR [#68](https://github.com/click-contrib/click-option-group/pull/68))
* Update CI/CD config and Python versions (PR [#69](https://github.com/click-contrib/click-option-group/pull/69))
* Fix tests for click>=8.1.8 (PR [#70](https://github.com/click-contrib/click-option-group/pull/70))

## v0.5.6 (09.06.2023)

* Add `optgroup.help_option` decorator to add help option to the group (PR [#50](https://github.com/click-contrib/click-option-group/pull/50))
* Use GitHub Actions instead of Travis CI for CI
* Delete tox runner
* Add Python 3.11 to the setup classifiers

## v0.5.5 (12.10.2022)

* Add `tests/` directory to tarball
* Add `tests_cov` extra dependencies for testing with coverage

## v0.5.4 (12.10.2022)

* Move frame gathering into error code path (PR [#34](https://github.com/click-contrib/click-option-group/pull/34))
* Fix typos (PR [#37](https://github.com/click-contrib/click-option-group/pull/37))
* PEP 561 support (PR [#42](https://github.com/click-contrib/click-option-group/pull/42))
* Update docs dependencies and Travis CI Python version matrix (PR [#43](https://github.com/click-contrib/click-option-group/pull/43))

## v0.5.3 (14.05.2021)

* Update Click dependency version to `<9` (Issue [#33](https://github.com/click-contrib/click-option-group/issues/33))

## v0.5.2 (28.11.2020)

* Do not use default option group name. An empty group name will not be displayed
* Slightly edited error messages
* All arguments except `name` in `optgroup` decorator must be keyword-only

## v0.5.1 (14.06.2020)

* Fix incompatibility with autocomplete: out of the box Click completion and click-repl (Issue [#14](https://github.com/click-contrib/click-option-group/issues/14))

## v0.5.0 (10.06.2020)

* Add `AllOptionGroup` class: all options from the group must be set or none must be set (PR [#13](https://github.com/click-contrib/click-option-group/pull/13))
* Fix type hints
* Update docs

## v0.4.0 (18.05.2020)

* Support multi-layer wrapped functions (PR [#10](https://github.com/click-contrib/click-option-group/pull/10))
* Fix flake8 issues

## v0.3.1

* Add `hidden=True` to `_GroupTitleFakeOption` as a temporary workaroud for issue [#4](https://github.com/click-contrib/click-option-group/issues/4)

## v0.3.0
* Add support for hidden options inside groups (PR [#2](https://github.com/click-contrib/click-option-group/pull/2))

## v0.2.3
* Transfer the repo to click-contrib organisation

## v0.2.2
* Add true lineno in warning when declaring empty option group
* Update readme

## v0.2.1
* Use RuntimeWarning and stacklevel 2 when declaring empty option group
* Update readme

## v0.2.0
* Implement `RequiredMutuallyExclusiveOptionGroup` class instead of `required` argument for `MutuallyExclusiveOptionGroup`
* Add tests with 100% coverage
* Update readme

## v0.1.0
* First public release
