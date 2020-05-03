# Changelog

## v0.3.2
* DOC: update m2r from a [fork](https://github.com/crossnox/m2r) to support sphinx >= 3

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
