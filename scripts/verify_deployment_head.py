#!/usr/bin/env python3
"""Refuser tout déploiement Pages préparé sur un état de main dépassé.

Une demande éditoriale encore non numérotée ou le journal de continuité
n'altèrent pas le rendu déjà validé ; tout autre changement impose de
reconstruire. Le déploiement reste assuré par publish.yml uniquement.
"""
from pathlib import Path
import os
import re
import sys

from publish_site import latest_main, only_pending_requests_or_log


def verify_current_head(repo, published_sha):
    if not re.fullmatch(r"[0-9a-f]{40}", published_sha or ""):
        raise RuntimeError("SHA de publication absent ou invalide")
    head = latest_main(repo)
    if head == published_sha:
        return head
    if only_pending_requests_or_log(repo, published_sha, head):
        print("Nouvelles demandes non attribuées : rendu validé toujours actuel.", flush=True)
        return head
    raise RuntimeError(
        f"Déploiement annulé : main a évolué depuis le rendu validé "
        f"({published_sha[:12]} -> {head[:12]}). La publication suivante reconstruira."
    )


if __name__ == "__main__":
    try:
        verified = verify_current_head(Path.cwd(), os.environ.get("MYTHOS_PUBLISHED_SHA", ""))
        print("Vérification finale du commit public :", verified, flush=True)
    except RuntimeError as error:
        print(f"::error::{error}", file=sys.stderr)
        sys.exit(1)
