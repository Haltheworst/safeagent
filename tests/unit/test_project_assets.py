import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_local_documentation_links_resolve():
    documents = list(ROOT.glob("*.md")) + list((ROOT / "docs").rglob("*.md"))
    for document in documents:
        for destination in re.findall(
            r"\[[^\]]*\]\(([^)]+)\)", document.read_text(encoding="utf-8")
        ):
            if destination.startswith(("http:", "https:", "mailto:", "#")):
                continue
            assert (document.parent / destination.split("#")[0]).exists(), (
                f"Broken link in {document.relative_to(ROOT)}: {destination}"
            )


def test_backlog_has_48_unique_topologically_ordered_local_issues():
    backlog = json.loads((ROOT / "docs/backlog.json").read_text(encoding="utf-8"))
    assert len(backlog["issues"]) == 48
    milestones = {m["id"] for m in backlog["milestones"]}
    labels = set(backlog["labels"])
    seen = set()
    for issue in backlog["issues"]:
        assert issue["planned_id"] not in seen
        assert set(issue["dependencies"]) <= seen
        assert issue["milestone"] in milestones
        assert set(issue["labels"]) <= labels
        assert len(issue["acceptance_criteria"]) >= 3
        assert issue["tests"] and issue["definition_of_done"]
        assert (ROOT / "docs/issues" / f"{issue['planned_id']}.md").exists()
        for document in issue["documentation"]:
            assert (ROOT / document).exists()
        seen.add(issue["planned_id"])
