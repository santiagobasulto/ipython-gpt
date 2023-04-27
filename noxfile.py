"""All the process that can be run using nox.

The nox run are build in isolated environment that will be stored in .nox. to force the venv update, remove the .nox/xxx folder.
"""
import tempfile
from pathlib import Path

import nox


def install_poetry_groups(session: nox.Session, *groups: str) -> None:
    """Install dependencies from poetry groups.

    Related to https://github.com/cjolowicz/nox-poetry/issues/663
    """
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            *[f"--only={group}" for group in groups],
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        print(Path(requirements.name).read_text())
        session.install("-r", requirements.name)


@nox.session(reuse_venv=True)
def lint(session):
    """Apply the pre-commits."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--a", *session.posargs)


@nox.session(reuse_venv=True)
def test(session):
    """Run all the test using the environment varialbe of the running machine."""
    session.install(".")
    install_poetry_groups(session, "test")
    test_files = session.posargs or ["tests"]
    session.run("pytest", "--color=yes", *test_files)


@nox.session(reuse_venv=True)
def docs(session):
    """Build a static version of the documentation"""
    build = session.posargs.pop() if session.posargs else "html"
    session.install(".")
    install_poetry_groups(session, "docs")
    session.run("sphinx-apidoc", "-o", "docs/api", "ipython_gpt")
    session.run("sphinx-build", "-v", "-b", build, "docs", f"docs/_build/{build}")
