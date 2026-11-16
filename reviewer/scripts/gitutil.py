"""Git helpers shared by the reviewer scripts. Every call runs in the current directory."""
import os
import re
import shutil
import subprocess
import tempfile

CODE_EXT = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")
STYLE_EXT = (".css", ".scss", ".less")
TEST_PATH_RE = re.compile(r"\.test\.|\.spec\.|(^|/)(tests|__tests__)/")


def sh(*args, env=None):
    try:
        p = subprocess.run(args, capture_output=True, text=True, env=env)
    except FileNotFoundError as e:
        return 127, "", str(e)
    return p.returncode, p.stdout.rstrip(), p.stderr.strip()


def git(*args, env=None):
    code, out, _ = sh("git", *args, env=env)
    return out if code == 0 else None


def toplevel():
    return git("rev-parse", "--show-toplevel")


def repo_name():
    # A linked worktree reports the main checkout's name, so its findings resume from either place.
    common = os.path.abspath(git("rev-parse", "--git-common-dir") or "")
    main = os.path.dirname(common) if os.path.basename(common) == ".git" else toplevel()
    return os.path.basename(main or os.getcwd())


def branch_key(branch):
    return branch.replace("/", "-")


def current_branch():
    return git("rev-parse", "--abbrev-ref", "HEAD")


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def snapshot_tree():
    """Tree of the working tree as it is now, built in a temp index; the real index is untouched."""
    real = git("rev-parse", "--git-path", "index")
    fd, tmp = tempfile.mkstemp(prefix="reviewer-index-")
    os.close(fd)
    try:
        if real and os.path.exists(real):
            shutil.copyfile(real, tmp)
        else:
            os.remove(tmp)
        env = dict(os.environ, GIT_INDEX_FILE=tmp)
        sh("git", "add", "-A", env=env)
        return git("write-tree", env=env)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def snapshot():
    """Uncommitted work as a dangling commit on top of HEAD (no ref moves)."""
    env = dict(os.environ, GIT_AUTHOR_NAME="reviewer", GIT_AUTHOR_EMAIL="reviewer@localhost",
               GIT_COMMITTER_NAME="reviewer", GIT_COMMITTER_EMAIL="reviewer@localhost")
    return git("commit-tree", snapshot_tree(), "-p", "HEAD", "-m", "uncommitted", env=env)
