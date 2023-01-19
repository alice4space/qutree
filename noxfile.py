"""Define nox sessions for running tests and checks."""

import nox


@nox.session(reuse_venv=True)
def lint(session):
    """Lint everything possible using the pre-commit environment."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--a", *session.posargs)


@nox.session(python=["3.7", "3.8", "3.9"])
def test(session):
    """Run the lib test and export a coverage as html."""
    session.install(".[test]")
    session.run("pytest", "--color=yes", "tests")


@nox.session(reuse_venv=True)
def docs(session):
    """Build the html docs."""
    session.install(".[doc]")
    session.run(
        "sphinx-apidoc",
        "--force",
        "--module-first",
        "-o",
        "docs/source/_api",
        "./qutree",
    )
    session.run("sphinx-build", "-b", "html", "docs/source", "build")
