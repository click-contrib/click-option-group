from functools import wraps

import click
import pytest

from click_option_group import (
    AllOptionGroup,
    GroupedOption,
    MutuallyExclusiveOptionGroup,
    OptionGroup,
    RequiredAllOptionGroup,
    RequiredAnyOptionGroup,
    RequiredMutuallyExclusiveOptionGroup,
    optgroup,
)


def test_basic_functionality_first_api(runner):
    @click.command()
    @click.option("--hello")
    @optgroup("Group 1", help="Group 1 description")
    @optgroup.option("--foo1")
    @optgroup.option("--bar1")
    @click.option("--lol")
    @optgroup.group("Group 2", help="Group 2 description")
    @optgroup.option("--foo2")
    @optgroup.option("--bar2")
    @click.option("--goodbye")
    def cli(hello, foo1, bar1, lol, foo2, bar2, goodbye):
        click.echo(f"{foo1},{bar1},{foo2},{bar2}")

    result = runner.invoke(cli, ["--help"])

    assert not result.exception
    assert "Group 1:" in result.output
    assert "Group 1 description" in result.output
    assert "Group 2:" in result.output
    assert "Group 2 description" in result.output

    result = runner.invoke(cli, ["--foo1", "foo1", "--bar1", "bar1", "--foo2", "foo2", "--bar2", "bar2"])

    assert not result.exception
    assert "foo1,bar1,foo2,bar2" in result.output


def test_noname_group(runner):
    @click.command()
    @optgroup()
    @optgroup.option("--foo")
    def cli(foo):
        pass

    result = runner.invoke(cli, ["--help"])
    assert "Options:\n    --foo" in result.output

    @click.command()
    @optgroup(help="Group description")
    @optgroup.option("--foo")
    def cli(foo):
        pass

    result = runner.invoke(cli, ["--help"])
    assert "Group description" in result.output


def test_mix_decl_first_api():
    with pytest.raises(TypeError, match=r"Check decorator position for \['--hello'\]"):

        @click.command()
        @optgroup("Group 1", help="Group 1 description")
        @optgroup.option("--foo")
        @click.option("--hello")
        @optgroup.option("--bar")
        def cli1(**params):
            pass

    with pytest.raises(TypeError, match=r"Check decorator position for \['--hello'\]"):

        @click.command()
        @optgroup("Group 1", help="Group 1 description")
        @click.option("--hello")
        @optgroup.option("--foo")
        @optgroup.option("--bar")
        def cli2(**params):
            pass

    with pytest.raises(TypeError, match=r"Check decorator position for \['--hello2'\]"):

        @click.command()
        @optgroup("Group 1", help="Group 1 description")
        @click.option("--hello1")
        @optgroup.option("--foo")
        @click.option("--hello2")
        @optgroup.option("--bar")
        def cli3(**params):
            pass


def test_missing_group_decl_first_api(runner):
    @click.command()
    @click.option("--hello1")
    @optgroup.option("--foo")
    @optgroup.option("--bar")
    @click.option("--hello2")
    def cli(**params):
        pass

    # FIXME: https://github.com/click-contrib/click-option-group/issues/65
    #  Now we just do not check not attached options for --help
    #  because handle_parse_result is not called in click >=8.1.8 for --help

    # result = runner.invoke(cli, ["--help"])
    #
    # assert result.exception
    # assert isinstance(result.exception, TypeError)
    # assert "Missing option group decorator" in str(result.exc_info[1])
    # assert "--foo" in str(result.exc_info[1])
    # assert "--bar" in str(result.exc_info[1])

    result = runner.invoke(cli, [])

    assert result.exception
    assert isinstance(result.exception, TypeError)
    assert "Missing option group decorator" in str(result.exc_info[1])
    assert "--foo" in str(result.exc_info[1])
    assert "--bar" in str(result.exc_info[1])

    result = runner.invoke(cli, ["--hello1", "hello1"])

    assert result.exception
    assert isinstance(result.exception, TypeError)
    assert "Missing option group decorator" in str(result.exc_info[1])
    assert "--foo" in str(result.exc_info[1])
    assert "--bar" in str(result.exc_info[1])

    result = runner.invoke(cli, ["--foo", "foo"])

    assert result.exception
    assert isinstance(result.exception, TypeError)
    assert "Missing option group decorator" in str(result.exc_info[1])
    assert "--foo" in str(result.exc_info[1])
    assert "--bar" in str(result.exc_info[1])


def test_missing_grouped_options_decl_first_api(runner):
    with pytest.warns(RuntimeWarning, match=r'The empty option group "Group 1"'):

        @click.command()
        @click.option("--hello1")
        @optgroup("Group 1", help="Group 1 description")
        @click.option("--hello2")
        def cli(**params):
            pass

    result = runner.invoke(cli, ["--help"])

    assert not result.exception
    assert "Group 1:" not in result.output
    assert "Group 1 description" not in result.output
    assert "--hello1" in result.output
    assert "--hello2" in result.output


def test_incorrect_option_group_cls():
    with pytest.raises(TypeError, match=r"must be a subclass of 'OptionGroup' class"):

        @click.command()
        @optgroup(cls=object)
        @optgroup.option("--foo")
        def cli(**params):
            pass


def test_option_group_unexpected_arguments():
    with pytest.raises(
        TypeError,
        match=r"'OptionGroup' constructor got an unexpected keyword argument 'oops'",
    ):

        @click.command()
        @optgroup(oops=True)
        @optgroup.option("--foo")
        def cli(**params):
            pass


def test_incorrect_grouped_option_cls():
    @click.command()
    @optgroup()
    @optgroup.option("--foo", cls=GroupedOption)
    def cli1(**params):
        pass

    with pytest.raises(TypeError, match=r"must be a subclass of 'GroupedOption' class"):

        @click.command()
        @optgroup()
        @optgroup.option("--foo", cls=click.Option)
        def cli2(**params):
            pass


def test_option_group_name_help():
    group = OptionGroup()
    assert group.name == ""
    assert group.help == ""

    group = OptionGroup("Group Name", help="Group description")
    assert group.name == "Group Name"
    assert group.help == "Group description"


def test_basic_functionality_second_api(runner):
    group1 = OptionGroup("Group 1", help="Group 1 description")
    group2 = OptionGroup("Group 2", help="Group 2 description")

    @click.command()
    @click.option("--hello")
    @group1.option("--foo1")
    @group1.option("--bar1")
    @click.option("--lol")
    @group2.option("--foo2")
    @group2.option("--bar2")
    @click.option("--goodbye")
    def cli(hello, foo1, bar1, lol, foo2, bar2, goodbye):
        click.echo(f"{foo1},{bar1},{foo2},{bar2}")

    result = runner.invoke(cli, ["--help"])

    assert not result.exception
    assert "Group 1:" in result.output
    assert "Group 1 description" in result.output
    assert "Group 2:" in result.output
    assert "Group 2 description" in result.output

    result = runner.invoke(cli, ["--foo1", "foo1", "--bar1", "bar1", "--foo2", "foo2", "--bar2", "bar2"])

    assert not result.exception
    assert "foo1,bar1,foo2,bar2" in result.output


def test_mix_decl_second_api():
    group1 = OptionGroup("Group 1", help="Group 1 description")

    with pytest.raises(TypeError, match=r"Check decorator position for \['--hello2'\]"):

        @click.command()
        @click.option("--hello1")
        @group1.option("--foo")
        @click.option("--hello2")
        @group1.option("--bar")
        @click.option("--hello3")
        def cli(**params):
            pass


def test_required_any_option_group(runner):
    group = RequiredAnyOptionGroup()
    assert group.name_extra == ["required_any"]

    @click.command()
    @optgroup(cls=RequiredAnyOptionGroup)
    @optgroup.option("--foo")
    @optgroup.option("--bar")
    def cli(foo, bar):
        click.echo(f"{foo},{bar}")

    result = runner.invoke(cli, ["--help"])
    assert "[required_any]" in result.output

    result = runner.invoke(cli, [])
    assert result.exception
    assert result.exit_code == 2
    assert "At least one of the following options" in result.output
    assert "--foo" in result.output
    assert "--bar" in result.output

    result = runner.invoke(cli, ["--foo", "foo"])
    assert not result.exception
    assert result.exit_code == 0
    assert "foo,None" in result.output

    result = runner.invoke(cli, ["--bar", "bar"])
    assert not result.exception
    assert result.exit_code == 0
    assert "None,bar" in result.output

    result = runner.invoke(cli, ["--foo", "foo", "--bar", "bar"])
    assert not result.exception
    assert result.exit_code == 0
    assert "foo,bar" in result.output


def test_all_option_group(runner):
    group = AllOptionGroup()
    assert group.name_extra == ["all_or_none"]

    @click.command()
    @optgroup.group(cls=AllOptionGroup)
    @optgroup.option("--foo")
    @optgroup.option("--bar")
    def cli(foo, bar):
        click.echo(f"{foo},{bar}")

    result = runner.invoke(cli, ["--help"])
    assert "[all_or_none]" in result.output

    result = runner.invoke(cli, [])
    assert not result.exception
    assert result.exit_code == 0

    result = runner.invoke(cli, ["--foo", "foo"])
    assert result.exception
    assert result.exit_code == 2
    assert "All options from" in result.output
    assert "should be specified or none should be specified" in result.output
    assert "--foo" in result.output
    assert "--bar" in result.output

    result = runner.invoke(cli, ["--foo", "foo", "--bar", "bar"])
    assert not result.exception
    assert result.exit_code == 0
    assert "foo,bar" in result.output


def test_required_all_option_group(runner):
    group = RequiredAllOptionGroup()
    assert group.name_extra == ["required_all"]

    @click.command()
    @optgroup(cls=RequiredAllOptionGroup)
    @optgroup.option("--foo")
    @optgroup.option("--bar")
    def cli(foo, bar):
        click.echo(f"{foo},{bar}")

    result = runner.invoke(cli, ["--help"])
    assert "[required_all]" in result.output

    result = runner.invoke(cli, [])
    assert result.exception
    assert result.exit_code == 2
    assert "Missing required options from" in result.output
    assert "--foo" in result.output
    assert "--bar" in result.output

    result = runner.invoke(cli, ["--foo", "foo"])
    assert result.exception
    assert result.exit_code == 2
    assert "Missing required options from" in result.output
    assert "--foo" not in result.output
    assert "--bar" in result.output

    result = runner.invoke(cli, ["--bar", "bar"])
    assert result.exception
    assert result.exit_code == 2
    assert "Missing required options from" in result.output
    assert "--foo" in result.output
    assert "--bar" not in result.output

    result = runner.invoke(cli, ["--foo", "foo", "--bar", "bar"])
    assert not result.exception
    assert result.exit_code == 0
    assert "foo,bar" in result.output


def test_mutually_exclusive_option_group(runner):
    group = MutuallyExclusiveOptionGroup()
    assert group.name_extra == ["mutually_exclusive"]

    @click.command()
    @optgroup(cls=MutuallyExclusiveOptionGroup)
    @optgroup.option("--foo")
    @optgroup.option("--bar")
    @optgroup.option("--spam")
    def cli(foo, bar, spam):
        click.echo(f"{foo},{bar},{spam}")

    result = runner.invoke(cli, ["--help"])
    assert "[mutually_exclusive]" in result.output

    result = runner.invoke(cli, [])
    assert not result.exception
    assert result.exit_code == 0
    assert "None,None,None" in result.output

    result = runner.invoke(cli, ["--foo", "foo", "--bar", "bar"])
    assert result.exception
    assert result.exit_code == 2
    assert "Mutually exclusive options from" in result.output
    assert "cannot be used at the same time" in result.output
    assert "--foo" in result.output
    assert "--bar" in result.output

    result = runner.invoke(cli, ["--foo", "foo", "--spam", "spam"])
    assert result.exception
    assert result.exit_code == 2
    assert "Mutually exclusive options from" in result.output
    assert "cannot be used at the same time" in result.output
    assert "--foo" in result.output
    assert "--spam" in result.output

    result = runner.invoke(cli, ["--bar", "bar", "--spam", "spam"])
    assert result.exception
    assert result.exit_code == 2
    assert "Mutually exclusive options from" in result.output
    assert "cannot be used at the same time" in result.output
    assert "--bar" in result.output
    assert "--spam" in result.output

    result = runner.invoke(cli, ["--foo", "foo"])
    assert not result.exception
    assert result.exit_code == 0
    assert "foo,None,None" in result.output

    result = runner.invoke(cli, ["--bar", "bar"])
    assert not result.exception
    assert result.exit_code == 0
    assert "None,bar,None" in result.output

    result = runner.invoke(cli, ["--spam", "spam"])
    assert not result.exception
    assert result.exit_code == 0
    assert "None,None,spam" in result.output


def test_required_mutually_exclusive_option_group(runner):
    group = RequiredMutuallyExclusiveOptionGroup()
    assert group.name_extra == ["mutually_exclusive", "required"]

    @click.command()
    @optgroup(cls=RequiredMutuallyExclusiveOptionGroup)
    @optgroup.option("--foo")
    @optgroup.option("--bar")
    @optgroup.option("--spam")
    def cli(foo, bar, spam):
        click.echo(f"{foo},{bar},{spam}")

    result = runner.invoke(cli, ["--help"])
    assert "[mutually_exclusive, required]" in result.output

    result = runner.invoke(cli, [])
    assert result.exception
    assert result.exit_code == 2
    assert "Missing one of the required mutually exclusive options" in result.output
    assert "--foo" in result.output
    assert "--bar" in result.output
    assert "--spam" in result.output


@pytest.mark.parametrize(
    "cls",
    [
        RequiredAnyOptionGroup,
        RequiredAllOptionGroup,
        MutuallyExclusiveOptionGroup,
        RequiredMutuallyExclusiveOptionGroup,
    ],
)
def test_forbidden_option_attrs(cls):
    with pytest.raises(
        TypeError,
        match=f"'required' attribute is not allowed for '{cls.__name__}' option `foo'",
    ):

        @click.command()
        @optgroup(cls=cls)
        @optgroup.option("--foo", required=True)
        @optgroup.option("--bar")
        def cli(foo):
            pass


def test_subcommand_first_api(runner):
    @click.group()
    @optgroup("Group 1", help="Group 1 description")
    @optgroup.option("--foo")
    @optgroup.option("--bar")
    def cli(foo, bar):
        click.echo(f"{foo},{bar}")

    @cli.command()
    @optgroup("Group 2", help="Group 2 description")
    @optgroup.option("--foo")
    @optgroup.option("--bar")
    def command(foo, bar):
        click.echo(f"{foo},{bar}")

    result = runner.invoke(cli, ["--help"])

    assert not result.exception
    assert "Group 1:" in result.output
    assert "Group 1 description" in result.output
    assert "--foo" in result.output
    assert "--bar" in result.output

    result = runner.invoke(cli, ["command", "--help"])

    assert not result.exception

    assert "Group 2:" in result.output
    assert "Group 2 description" in result.output
    assert "--foo" in result.output
    assert "--bar" in result.output

    result = runner.invoke(
        cli,
        ["--foo", "foo", "--bar", "bar", "command", "--foo", "foo1", "--bar", "bar1"],
    )

    assert not result.exception
    assert "foo,bar\nfoo1,bar1" in result.output


def test_subcommand_mix_decl_first_api():
    with pytest.raises(TypeError, match=r"Check decorator position for \['--hello'\] option in 'cli1'"):

        @click.group()
        @optgroup("Group 1", help="Group 1 description")
        @optgroup.option("--foo")
        @click.option("--hello")
        @optgroup.option("--bar")
        def cli1(**params):
            pass

        @cli1.command()
        @optgroup("Group 2", help="Group 2 description")
        @optgroup.option("--foo")
        @optgroup.option("--bar")
        def command1(**params):
            pass

    with pytest.raises(
        TypeError,
        match=r"Check decorator position for \['--hello'\] option in 'command2'",
    ):

        @click.group()
        @optgroup("Group 1", help="Group 1 description")
        @optgroup.option("--foo")
        @optgroup.option("--bar")
        def cli2(**params):
            pass

        @cli2.command()
        @optgroup("Group 2", help="Group 2 description")
        @optgroup.option("--foo")
        @click.option("--hello")
        @optgroup.option("--bar")
        def command2(**params):
            pass


def test_subcommand_second_api(runner):
    group = OptionGroup("Group", help="Group description")

    @click.group()
    @group.option("--foo1")
    @group.option("--bar1")
    def cli(foo1, bar1):
        click.echo(f"{foo1},{bar1}")

    @cli.command()
    @group.option("--foo2")
    @group.option("--bar2")
    def command(foo2, bar2):
        click.echo(f"{foo2},{bar2}")

    result = runner.invoke(cli, ["--help"])

    assert not result.exception
    assert "Group:" in result.output
    assert "Group description" in result.output
    assert "--foo1" in result.output
    assert "--bar1" in result.output

    result = runner.invoke(cli, ["command", "--help"])

    assert not result.exception

    assert "Group:" in result.output
    assert "Group description" in result.output
    assert "--foo2" in result.output
    assert "--bar2" in result.output

    result = runner.invoke(
        cli,
        [
            "--foo1",
            "foo1",
            "--bar1",
            "bar1",
            "command",
            "--foo2",
            "foo2",
            "--bar2",
            "bar2",
        ],
    )

    assert not result.exception
    assert "foo1,bar1\nfoo2,bar2" in result.output


def test_group_context_second_api(runner):
    group = OptionGroup("My Group")

    @click.command()
    @group.option("--foo1")
    @group.option("--bar1")
    def cli1(foo1, bar1):
        click.echo(f"{foo1},{bar1}")

    @click.command()
    @group.option("--foo2")
    @group.option("--bar2")
    def cli2(foo2, bar2):
        click.echo(f"{foo2},{bar2}")

    result = runner.invoke(cli1, ["--help"])
    assert not result.exception
    assert "My Group:" in result.output
    assert "--foo1" in result.output
    assert "--bar1" in result.output

    result = runner.invoke(cli2, ["--help"])
    assert not result.exception
    assert "My Group:" in result.output
    assert "--foo2" in result.output
    assert "--bar2" in result.output

    result = runner.invoke(cli1, ["--foo1", "foo1", "--bar1", "bar1"])
    assert not result.exception
    assert "foo1,bar1" in result.output

    result = runner.invoke(cli2, ["--foo2", "foo2", "--bar2", "bar2"])
    assert not result.exception
    assert "foo2,bar2" in result.output


def test_subcommand_mix_decl_second_api():
    group = OptionGroup()

    with pytest.raises(TypeError, match=r"Check decorator position for \['--hello'\] option in 'cli1'"):

        @click.group()
        @group.option("--foo")
        @click.option("--hello")
        @group.option("--bar")
        def cli1(**params):
            pass

        @cli1.command()
        @group.option("--foo")
        @group.option("--bar")
        def command1(**params):
            pass

    with pytest.raises(
        TypeError,
        match=r"Check decorator position for \['--hello'\] option in 'command2'",
    ):

        @click.group()
        @group.option("--foo")
        @group.option("--bar")
        def cli2(**params):
            pass

        @cli2.command()
        @group.option("--foo")
        @click.option("--hello")
        @group.option("--bar")
        def command2(**params):
            pass


def test_command_first_api(runner):
    @optgroup("Group 1")
    @optgroup.option("--foo")
    @optgroup.option("--bar")
    @click.command()
    def cli(foo, bar):
        click.echo(f"{foo},{bar}")

    result = runner.invoke(cli, ["--help"])
    assert not result.exception
    assert "Group 1:" in result.output
    assert "--foo" in result.output
    assert "--bar" in result.output

    result = runner.invoke(cli, ["--foo", "foo", "--bar", "bar"])
    assert not result.exception
    assert "foo,bar" in result.output


def test_hidden_option(runner):
    @click.command()
    @click.option("--hello")
    @optgroup("Group 1", help="Group 1 description")
    @optgroup.option("--foo1")
    @optgroup.option("--bar1", hidden=True)
    @click.option("--goodbye")
    def cli(hello, foo1, bar1, goodbye):
        click.echo(f"{foo1},{bar1}")

    result = runner.invoke(cli, ["--help"])

    assert not result.exception
    assert "Group 1:" in result.output
    assert "Group 1 description" in result.output
    assert "bar1" not in result.output

    result = runner.invoke(
        cli,
        [
            "--foo1",
            "foo1",
            "--bar1",
            "bar1",
        ],
    )

    assert not result.exception
    assert "foo1,bar1" in result.output

    with pytest.raises(
        TypeError,
        match="'hidden' attribute is not allowed for 'RequiredAllOptionGroup' option `bar'",
    ):

        @click.command()
        @optgroup(cls=RequiredAllOptionGroup)
        @optgroup.option("--foo")
        @optgroup.option("--bar", hidden=True)
        def cli(foo, bar):
            click.echo(f"{foo},{bar}")

    @click.command()
    @optgroup(cls=RequiredAnyOptionGroup)
    @optgroup.option("--foo", hidden=True)
    @optgroup.option("--bar", hidden=True)
    def cli(foo, bar):
        click.echo(f"{foo},{bar}")

    result = runner.invoke(
        cli,
    )
    assert isinstance(result.exception, TypeError)
    assert "Need at least one non-hidden" in str(result.exception)

    @click.command()
    @optgroup("Group 1", help="Group 1 description")
    @optgroup.option("--foo", hidden=True)
    @optgroup.option("--bar", hidden=True)
    def cli(foo, bar):
        click.echo(f"{foo},{bar}")

    result = runner.invoke(cli, ["--help"])
    assert not result.exception
    assert "Group 1" not in result.output

    @click.command()
    @optgroup("Group 1", help="Group 1 description", hidden=True)
    @optgroup.option("--foo")
    @optgroup.option("--bar")
    def cli(foo, bar):
        click.echo(f"{foo},{bar}")

    result = runner.invoke(cli, ["--help"])
    assert not result.exception
    assert "Group 1" not in result.output
    assert "foo" not in result.output
    assert "bar" not in result.output

    @click.command()
    @optgroup("Group 1", help="Group 1 description", hidden=True)
    @optgroup.option("--foo", hidden=False)  # override hidden of group
    @optgroup.option("--bar")
    def cli(foo, bar):
        click.echo(f"{foo},{bar}")

    result = runner.invoke(cli, ["--help"])
    assert not result.exception
    assert "Group 1" in result.output
    assert "foo" in result.output
    assert "bar" not in result.output


@pytest.mark.parametrize(
    ("param_decls", "options", "output"),
    [
        ((), ["--help"], "--help"),
        (("-h", "--help"), ["-h"], "-h, --help"),
        (("-h", "--help"), ["--help"], "-h, --help"),
    ],
)
def test_help_option(runner, param_decls, options, output):
    @click.command()
    @optgroup("Help Options")
    @optgroup.help_option(*param_decls)
    def cli() -> None:
        click.echo("Running command.")

    result = runner.invoke(cli)
    assert not result.exception
    assert "Running command." in result.output
    assert "Usage:" not in result.output

    result = runner.invoke(cli, options)
    assert not result.exception
    assert "Running command." not in result.output
    assert "Usage:" in result.output
    assert output in result.output


def test_wrapped_functions(runner):
    def make_z():
        """A unified option interface for making a `z`."""

        def decorator(f):
            @optgroup.group("Group xyz")
            @optgroup.option("-x", type=int)
            @optgroup.option("-y", type=int)
            @wraps(f)
            def new_func(*args, x=0, y=0, **kwargs):
                # Here we handle every detail about how to make a `z` from the given options
                f(*args, z=x + y, **kwargs)

            return new_func

        return decorator

    def make_c():
        """A unified option interface for making a `c`."""

        def decorator(f):
            @optgroup.group("Group abc")
            @optgroup.option("-a", type=int)
            @optgroup.option("-b", type=int)
            @wraps(f)
            def new_func(*args, a=0, b=0, **kwargs):
                # Here we do the same, but for another object `c` (and many others to come)
                f(*args, c=a * b, **kwargs)

            return new_func

        return decorator

    # Here I want to create a script that has a commen UI to make a `z`.
    # I want to reuse a common set of options for how to make a `z` and don't want
    # to sweat the details. Also, I've decided that I also want a `c` for this script.
    @click.command()
    @make_z()
    @make_c()
    def f(z, c):
        print(z, c)  # noqa: T201

    # Test
    result = runner.invoke(f, ["--help"])
    assert "Group xyz" in result.output
    assert "-x" in result.output
    assert "-y" in result.output
    assert "Group abc" in result.output
    assert "-a" in result.output
    assert "-b" in result.output
