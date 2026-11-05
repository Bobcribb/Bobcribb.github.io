"""Policy shared by the MYTHOS publication integrity audit and its regressions.

The audit previously reported broken internal links/fragments as non-fatal
warnings. A green CI could therefore validate pages with missing images,
stylesheets, scripts or anchors. Every warning produced by this focused
auditor represents an actionable integrity or accessibility failure.
"""


def publication_audit_fails(issues, warnings):
    """Reject both hard errors and verified HTML/resource warnings.

    Does not modify editorial sources, assign numbers or touch the site.
    """
    return bool(issues) or bool(warnings)
