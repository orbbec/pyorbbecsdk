"""One-file overview of a run, for hand-over and quick review.

``junit-all.xml`` already carries the totals, but they are spread over a dozen
``<testsuite>`` elements and the skip reasons are buried inside ``longrepr``
strings.  This writes ``summary.md``: the headline numbers, a per-module
breakdown, every skip reason, and any failures - the things a reviewer actually
asks for.  It is also the place to state the run's caveats, so nobody reads a
green total as "everything was exercised".
"""

from __future__ import annotations

import re
import socket
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from pathlib import Path

#: Statuses counted in the headline table, in display order.
_STATUSES = ("passed", "failed", "errors", "skipped")


def _reason(text):
    """Turn a pytest ``longrepr`` string into a short skip/failure reason."""
    if not text:
        return ""
    text = text.replace("\\n", " ").replace("\n", " ")
    match = re.search(r"(?:Skipped|Failed|Error):\s*(.+?)(?:'|\)\s*$|$)", text)
    if match:
        return match.group(1).strip()
    return text.strip()[:160]


def _case_status(case):
    if case.find("failure") is not None:
        return "failed", case.find("failure")
    if case.find("error") is not None:
        return "errors", case.find("error")
    if case.find("skipped") is not None:
        return "skipped", case.find("skipped")
    return "passed", None


def _module_of(classname):
    """Module name from a JUnit classname.

    conftest writes the source path with separators normalised to dots, so
    ``test_unit_cpp.py`` arrives as ``...auto_tests.test_unit_cpp.py``: the
    ``.py`` suffix must be removed before taking the last dot-separated part.
    """
    name = classname or ""
    if name.endswith(".py"):
        name = name[:-3]
    return name.rsplit(".", 1)[-1]


def collect(junit_xml):
    """Return (per-module rows, skipped list, failed list)."""
    root = ElementTree.parse(junit_xml).getroot()

    modules = {}
    skipped = []
    failed = []

    for case in root.iter("testcase"):
        classname = _module_of(case.get("classname"))
        name = case.get("name") or ""
        status, node = _case_status(case)

        row = modules.setdefault(classname, {"passed": 0, "failed": 0, "errors": 0, "skipped": 0, "time": 0.0})
        row[status] += 1
        try:
            row["time"] += float(case.get("time") or 0)
        except ValueError:
            pass

        if status == "skipped":
            skipped.append((classname, name, _reason(node.get("message"))))
        elif status in ("failed", "errors"):
            failed.append((classname, name, _reason(node.get("message"))))

    return modules, skipped, failed


def total_counts(junit_xml):
    """Aggregate counts straight from the suite elements."""
    root = ElementTree.parse(junit_xml).getroot()
    suites = root.findall("testsuite") if root.tag == "testsuites" else [root]
    totals = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0}
    for suite in suites:
        for key in totals:
            try:
                totals[key] += int(suite.get(key, 0) or 0)
            except ValueError:
                pass
    return totals


def write_summary(results_dir, junit_xml, context):
    """Write ``summary.md`` beside the other artifacts; returns its path."""
    results_dir = Path(results_dir)
    junit_xml = Path(junit_xml)
    if not junit_xml.is_file():
        return None

    totals = total_counts(junit_xml)
    modules, skipped, failed = collect(junit_xml)
    passed = max(totals["tests"] - totals["failures"] - totals["errors"] - totals["skipped"], 0)

    lines = [
        "# auto_tests run summary",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Host: {socket.gethostname()}",
        f"- Config: `{context.get('config', 'n/a')}`",
        f"- Suites: {context.get('suites', 'n/a')}",
        f"- Network tests: {'enabled' if context.get('network') else 'disabled'}",
        f"- Device health: {context.get('health', 'n/a')}",
        f"- SDK: pyorbbecsdk {context.get('sdk_version', 'unknown')}",
    ]
    device = context.get("device")
    if device:
        lines.append(f"- Device: {device}")
    duration = context.get("duration_seconds")
    if duration is not None:
        lines.append(f"- Wall clock: {int(duration // 60)}m {int(duration % 60)}s")
    lines.append(f"- Exit code: {context.get('exit_code', 'n/a')}")
    lines.append("")

    lines += [
        "## Totals",
        "",
        "| Result | Count |",
        "|---|---:|",
        f"| Total cases selected | {totals['tests']} |",
        f"| Passed | {passed} |",
        f"| Failed | {totals['failures']} |",
        f"| Errors | {totals['errors']} |",
        f"| Skipped | {totals['skipped']} |",
        "",
        "> A skip means the device or this pyorbbecsdk build does not provide the "
        "capability, or the case needed an external resource. It is not a pass: "
        "see the skip table below before reading the totals as coverage.",
        "",
        "## Per module",
        "",
        "| Module | Passed | Failed | Skipped | Time (s) |",
        "|---|---:|---:|---:|---:|",
    ]
    for module in sorted(modules):
        row = modules[module]
        lines.append(
            f"| `{module}` | {row['passed']} | {row['failed'] + row['errors']} | "
            f"{row['skipped']} | {row['time']:.1f} |"
        )
    lines.append("")

    if failed:
        lines += ["## Failures", ""]
        for classname, name, reason in failed:
            lines.append(f"- `{name}` ({classname}): {reason}")
        lines.append("")

    if skipped:
        lines += ["## Skipped cases and why", ""]
        grouped = {}
        for classname, name, reason in skipped:
            grouped.setdefault(reason, []).append((classname, name))
        for reason in sorted(grouped, key=lambda item: -len(grouped[item])):
            entries = grouped[reason]
            lines.append(f"### {reason or '(no reason recorded)'} - {len(entries)} case(s)")
            lines.append("")
            for classname, name in entries[:12]:
                lines.append(f"- `{name}`")
            if len(entries) > 12:
                lines.append(f"- ... and {len(entries) - 12} more")
            lines.append("")

    lines += [
        "## Artifacts",
        "",
        "- `junit-all.xml` - machine-readable results, one `<testcase>` per case",
        "- `run-all.log` - full console transcript (SDK logs interleaved)",
        "- `OrbbecSDK.log.txt` - SDK file log at DEBUG level",
        "",
    ]

    target = results_dir / "summary.md"
    target.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    return target
