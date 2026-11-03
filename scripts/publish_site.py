#!/usr/bin/env python3
"""Reconstruire sur main à chaque tentative, sans fusionner les rendus générés."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile


def git(repo, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=check,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )


def latest_main(repo):
    # Ref explicite : ne dépend pas du refspec d'un checkout superficiel.
    git(repo, "fetch", "--no-tags", "origin", "refs/heads/main:refs/remotes/origin/main")
    return git(repo, "rev-parse", "refs/remotes/origin/main").stdout.strip()


def guard_render_commit(worktree):
    """Seuls les rendus peuvent changer ; les sources et médias restent identiques."""
    deleted = git(worktree, "diff", "--cached", "--name-only", "--diff-filter=D").stdout
    if deleted:
        raise RuntimeError("Publication refusée : suppression de fichiers : " + deleted)
    paths = git(worktree, "diff", "--cached", "--name-only", "-z").stdout.split("\0")
    generated = {"search.json", "sitemap.xml", "robots.txt", "CNAME", ".nojekyll"}
    for name in filter(None, paths):
        path = Path(name)
        html = (path.suffix == ".html" and not any(p.startswith(".") for p in path.parts)
                and path.parts[0] not in {"scripts", "media", "assets", "tests"})
        if name not in generated and not html:
            raise RuntimeError("Publication refusée : source ou média modifié : " + name)


def synchronize(repo, max_attempts=5):
    repo = Path(repo).resolve()
    # Le checkout de travail n'est jamais réinitialisé ; seuls les worktrees
    # temporaires créés ci-dessous sont nettoyés après chaque tentative.
    if git(repo, "status", "--porcelain", "--untracked-files=normal").stdout:
        raise RuntimeError("Publication refusée : le checkout contient des modifications locales")
    artifact = repo / "_site"
    if artifact.exists():
        shutil.rmtree(artifact)
    for attempt in range(1, max_attempts + 1):
        source_sha = latest_main(repo)
        print(f"Publication MYTHOS : tentative {attempt}/{max_attempts}, source {source_sha}", flush=True)
        with tempfile.TemporaryDirectory(prefix="mythos-publish-", dir=os.environ.get("RUNNER_TEMP")) as tmp:
            worktree = Path(tmp) / "source"
            git(repo, "worktree", "add", "--detach", str(worktree), source_sha)
            try:
                subprocess.run([sys.executable, "scripts/build_native.py"], cwd=worktree, check=True)
                # Valider exactement la génération qui sera poussée et déployée,
                # y compris après un refus de push dû à un autre éditeur.
                subprocess.run([sys.executable, "scripts/validate_publication.py"], cwd=worktree, check=True)
                shutil.copytree(worktree / "_site", worktree, dirs_exist_ok=True)
                git(worktree, "add", "-A")
                guard_render_commit(worktree)
                changed = git(worktree, "diff", "--cached", "--quiet", check=False)
                if changed.returncode not in (0, 1):
                    raise RuntimeError(changed.stderr)
                published_sha = source_sha
                if changed.returncode == 1:
                    git(worktree, "-c", "user.name=github-actions[bot]", "-c",
                        "user.email=41898282+github-actions[bot]@users.noreply.github.com",
                        "commit", "-m", "Actualiser le catalogue GitHub autonome MYTHOS [skip ci]")
                    published_sha = git(worktree, "rev-parse", "HEAD").stdout.strip()
                    pushed = git(worktree, "push", "origin", "HEAD:refs/heads/main", check=False)
                    if pushed.returncode:
                        print(pushed.stderr, flush=True)
                        if latest_main(repo) == source_sha:
                            raise RuntimeError("Push refusé sans modification de main : vérifier les droits ou le réseau")
                        print("main a évolué : nouvelle reconstruction et nouveaux contrôles.", flush=True)
                        continue
                # Même un rendu inchangé doit correspondre au main actuel.
                if latest_main(repo) != published_sha:
                    print("main a encore évolué : reconstruction avant le déploiement.", flush=True)
                    continue
                shutil.copytree(worktree / "_site", artifact)
                print(f"Publication validée : source {source_sha}, rendu {published_sha}", flush=True)
                if os.environ.get("GITHUB_OUTPUT"):
                    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
                        output.write(f"source_sha={source_sha}\npublished_sha={published_sha}\n")
                return published_sha
            finally:
                # Aucun reset, clean ou push forcé sur main. Ce worktree ne
                # contient que les résultats reproductibles de cette tentative.
                git(repo, "worktree", "remove", "--force", str(worktree))
    raise RuntimeError(f"main a changé pendant les {max_attempts} tentatives ; aucun artefact obsolète à déployer")


if __name__ == "__main__":
    try:
        synchronize(Path.cwd())
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(f"::error::{error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(error.stderr, file=sys.stderr)
        sys.exit(1)
