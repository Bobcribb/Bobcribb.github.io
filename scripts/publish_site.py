#!/usr/bin/env python3
"""Publier un rendu vérifié ; reconstruire si ses sources ont changé."""
from pathlib import Path
import hashlib
import json
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


def only_pending_requests_or_log(repo, base, tip):
    """True only for new, valid inbox requests and the non-rendered journal.

    These additions cannot change already allocated numbers or built pages.
    Changes to an existing request, any registry, source, media or generator
    still require a fresh allocation and complete build.
    """
    if git(repo, "merge-base", "--is-ancestor", base, tip, check=False).returncode:
        return False
    fields = git(repo, "diff", "--no-renames", "--name-status", "-z", base, tip).stdout.split("\0")
    fields = fields[:-1] if fields and fields[-1] == "" else fields
    if len(fields) % 2:
        return False
    from editorial_queue import parse_request
    with tempfile.TemporaryDirectory(prefix="mythos-incoming-") as tmp:
        for status, name in zip(fields[::2], fields[1::2]):
            if name == "EDITORIAL_CONTINUITY.md" and status in {"A", "M"}:
                pass  # No generator reads this editorial journal.
            elif status == "A" and Path(name).parent == Path("editorial/inbox") and Path(name).suffix == ".json":
                request = Path(tmp) / Path(name).name
                request.write_text(git(repo, "show", tip + ":" + name).stdout, encoding="utf-8")
                try:
                    parse_request(request)
                except (ValueError, TypeError, KeyError):
                    return False
            else:
                return False
            if not git(repo, "ls-tree", tip, "--", name).stdout.startswith("100644 blob "):
                return False
    return True


def push_validated_render(repo, worktree, source_sha):
    for _ in range(5):
        pushed = git(worktree, "push", "origin", "HEAD:refs/heads/main", check=False)
        if not pushed.returncode:
            return git(worktree, "rev-parse", "HEAD").stdout.strip()
        print(pushed.stderr, flush=True)
        tip = latest_main(repo)
        if tip == source_sha:
            raise RuntimeError("Push refusé sans modification de main : vérifier les droits ou le réseau")
        if not only_pending_requests_or_log(repo, source_sha, tip):
            return None
        # Only disjoint, unallocated inbox additions or journal changes can
        # reach this merge. No rendered source or allocation is rebased.
        git(worktree, "-c", "user.name=github-actions[bot]", "-c",
            "user.email=41898282+github-actions[bot]@users.noreply.github.com",
            "merge", "--no-edit", "-m", "Conserver les nouvelles demandes en attente [skip ci]", tip)
        print("Nouvelles demandes conservées pour la prochaine exécution ; rendu vérifié inchangé.", flush=True)
    return None


def guard_render_commit(worktree, allocated=None):
    """Only rendered files and exactly verified new allocations may change."""
    allocated = allocated or {}
    for name, expected in allocated.items():
        staged = subprocess.check_output(["git", "-C", str(worktree), "show", ":" + name])
        if hashlib.sha256(staged).hexdigest() != expected:
            raise RuntimeError("Publication refusée : attribution modifiée par le générateur : " + name)
    deleted = git(worktree, "diff", "--cached", "--name-only", "--diff-filter=D").stdout
    if deleted:
        raise RuntimeError("Publication refusée : suppression de fichiers : " + deleted)
    paths = git(worktree, "diff", "--cached", "--name-only", "-z").stdout.split("\0")
    generated = {"search.json", "sitemap.xml", "robots.txt", "CNAME", ".nojekyll",
                 "catalog/comparative-history.json", "catalog/origines-continuity.json", "catalog/numbering.json", "catalog/publication-verification.json", "catalog/entries.json", "catalog/reading-audit.json", "catalog/reading-pdfs.json"}
    for name in filter(None, paths):
        path = Path(name)
        html = (path.suffix == ".html" and not any(p.startswith(".") for p in path.parts)
                and path.parts[0] not in {"scripts", "media", "assets", "tests"})
        if name not in generated and not html and name not in allocated:
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
                # Allocation and source creation use this exact fresh snapshot.
                # A conflicting source change discards this worktree. New inbox
                # requests alone can remain pending without rebasing allocations.
                result = subprocess.check_output(
                    [sys.executable, "scripts/editorial_queue.py", "apply"], cwd=worktree, text=True)
                paths = json.loads(result)["allocated"]
                if paths:
                    paths.append("editorial/numbering.json")
                allocated = {name: hashlib.sha256((worktree / name).read_bytes()).hexdigest()
                             for name in paths}
                subprocess.run([sys.executable, "scripts/build_native.py"], cwd=worktree, check=True)
                # Valider exactement la génération qui sera poussée et déployée,
                # y compris après un refus de push dû à un autre éditeur.
                subprocess.run([sys.executable, "scripts/validate_publication.py"], cwd=worktree, check=True)
                shutil.copytree(worktree / "_site", worktree, dirs_exist_ok=True)
                git(worktree, "add", "-A")
                guard_render_commit(worktree, allocated)
                changed = git(worktree, "diff", "--cached", "--quiet", check=False)
                if changed.returncode not in (0, 1):
                    raise RuntimeError(changed.stderr)
                published_sha = source_sha
                if changed.returncode == 1:
                    git(worktree, "-c", "user.name=github-actions[bot]", "-c",
                        "user.email=41898282+github-actions[bot]@users.noreply.github.com",
                        "commit", "-m", "Actualiser le catalogue GitHub autonome MYTHOS [skip ci]")
                    published_sha = push_validated_render(repo, worktree, source_sha)
                    if published_sha is None:
                        print("main a évolué : nouvelle reconstruction et nouveaux contrôles.", flush=True)
                        continue
                tip = latest_main(repo)
                if tip != published_sha:
                    if not only_pending_requests_or_log(repo, published_sha, tip):
                        print("main a encore évolué : reconstruction avant le déploiement.", flush=True)
                        continue
                    # main already contains the verified render; only later
                    # requests await their own atomic allocation on the next run.
                    published_sha = tip
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
