# Changelog

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
