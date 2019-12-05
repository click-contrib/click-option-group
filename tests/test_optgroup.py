# -*- coding: utf-8 -*-

import pytest
import click

from click_option_group import (
    optgroup,
    OptionGroup,
    GroupedOption,
    RequiredAnyOptionGroup,
    RequiredAllOptionGroup,
    MutuallyExclusiveOptionGroup
)


def test_basic_functionality_first_api(runner):
    @click.command()
    @click.option('--hello')
    @optgroup('Group 1', help='Group 1 description')
    @optgroup.option('--foo1')
    @optgroup.option('--bar1')
    @click.option('--lol')
    @optgroup.group('Group 2', help='Group 2 description')
    @optgroup.option('--foo2')
    @optgroup.option('--bar2')
    @click.option('--goodbye')
    def cli(hello, foo1, bar1, lol, foo2, bar2, goodbye):
        click.echo(f'{foo1},{bar1},{foo2},{bar2}')

    result = runner.invoke(cli, ['--help'])

    assert not result.exception
    assert 'Group 1:' in result.output
    assert 'Group 1 description' in result.output
    assert 'Group 2:' in result.output
    assert 'Group 2 description' in result.output

    result = runner.invoke(cli, [
        '--foo1', 'foo1', '--bar1', 'bar1',
        '--foo2', 'foo2', '--bar2', 'bar2'])

    assert not result.exception
    assert 'foo1,bar1,foo2,bar2' in result.output


def test_mix_decl_first_api(runner):
    with pytest.raises(TypeError, match=r"Check decorator position for \['--hello'\]"):
        @click.command()
        @optgroup('Group 1', help='Group 1 description')
        @optgroup.option('--foo')
        @click.option('--hello')
        @optgroup.option('--bar')
        def cli(**params):
            pass

    with pytest.raises(TypeError, match=r"Check decorator position for \['--hello'\]"):
        @click.command()
        @optgroup('Group 1', help='Group 1 description')
        @click.option('--hello')
        @optgroup.option('--foo')
        @optgroup.option('--bar')
        def cli(**params):
            pass

    with pytest.raises(TypeError, match=r"Check decorator position for \['--hello2'\]"):
        @click.command()
        @optgroup('Group 1', help='Group 1 description')
        @click.option('--hello1')
        @optgroup.option('--foo')
        @click.option('--hello2')
        @optgroup.option('--bar')
        def cli(**params):
            pass


def test_missing_group_decl_first_api(runner):
    @click.command()
    @click.option('--hello1')
    @optgroup.option('--foo')
    @optgroup.option('--bar')
    @click.option('--hello2')
    def cli(**params):
        pass

    result = runner.invoke(cli, ['--help'])

    assert result.exception
    assert TypeError == result.exc_info[0]
    assert 'Missing option group' in str(result.exc_info[1])
    assert '--foo' in str(result.exc_info[1])
    assert '--bar' in str(result.exc_info[1])


def test_missing_grouped_options_decl_first_api(runner):
    with pytest.warns(UserWarning, match=r'The empty option group "Group 1"'):
        @click.command()
        @click.option('--hello1')
        @optgroup('Group 1', help='Group 1 description')
        @click.option('--hello2')
        def cli(**params):
            pass

    result = runner.invoke(cli, ['--help'])

    assert not result.exception
    assert 'Group 1:' not in result.output
    assert 'Group 1 description' not in result.output
    assert '--hello1' in result.output
    assert '--hello2' in result.output


def test_basic_functionality_second_api(runner):
    group1 = OptionGroup('Group 1', help='Group 1 description')
    group2 = OptionGroup('Group 2', help='Group 2 description')

    @click.command()
    @click.option('--hello')
    @group1.option('--foo1')
    @group1.option('--bar1')
    @click.option('--lol')
    @group2.option('--foo2')
    @group2.option('--bar2')
    @click.option('--goodbye')
    def cli(hello, foo1, bar1, lol, foo2, bar2, goodbye):
        click.echo(f'{foo1},{bar1},{foo2},{bar2}')

    result = runner.invoke(cli, ['--help'])

    assert not result.exception
    assert 'Group 1:' in result.output
    assert 'Group 1 description' in result.output
    assert 'Group 2:' in result.output
    assert 'Group 2 description' in result.output

    result = runner.invoke(cli, [
        '--foo1', 'foo1', '--bar1', 'bar1',
        '--foo2', 'foo2', '--bar2', 'bar2'])

    assert not result.exception
    assert 'foo1,bar1,foo2,bar2' in result.output
