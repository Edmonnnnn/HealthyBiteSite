"""
Lightweight backend smoke tests.

Usage:
    python backend/smoke_test.py

Environment variables:
    BASE_URL (default: http://127.0.0.1:8810)
    LANG     (default: en)

Exit codes:
    0 - all checks passed
    1 - any check failed
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests

TIMEOUT = 10
FALLBACK_SLUG = "healthy-snacking-for-busy-days"


def _shorten(text: str, limit: int = 300) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _normalize_lang(raw: Optional[str]) -> str:
    if not raw:
        return "en"
    lang = raw.split(".", 1)[0]
    lang = lang.split("_", 1)[0]
    lang = lang.strip().lower() or "en"
    return lang


def _print_result(ok: bool, label: str, detail: str = "") -> None:
    status = "[OK]" if ok else "[FAIL]"
    line = f"{status} {label}"
    if detail:
        line += f" - {detail}"
    print(line)


def _request(method: str, url: str, **kwargs: Any) -> requests.Response:
    return requests.request(method, url, timeout=TIMEOUT, **kwargs)


def check_health(base_url: str) -> bool:
    url = f"{base_url}/health"
    try:
        resp = _request("GET", url)
        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        ok = resp.status_code == 200 and data.get("status") == "ok"
        if ok:
            _print_result(True, "GET /health")
        else:
            _print_result(False, "GET /health", f"status={resp.status_code}, body={_shorten(resp.text)}")
        return ok
    except Exception as exc:  # pragma: no cover - runtime safety
        detail = f"error={exc}"
        if isinstance(exc, requests.exceptions.ConnectionError):
            detail += " | Backend not reachable. Start it with: python run_dev.py (port 8810)."
        _print_result(False, "GET /health", detail)
        return False


def _extract_slug(sections: Any) -> Optional[str]:
    if isinstance(sections, list):
        for item in sections:
            if isinstance(item, dict) and item.get("slug"):
                return str(item["slug"])
    elif isinstance(sections, dict):
        for value in sections.values():
            if isinstance(value, dict) and value.get("items") and isinstance(value["items"], list):
                for item in value["items"]:
                    if isinstance(item, dict) and item.get("slug"):
                        return str(item["slug"])
    return None


def check_blog_sections(base_url: str, lang: str) -> Dict[str, Any]:
    url = f"{base_url}/api/v1/blog/sections"
    params = {"lang": lang}
    result = {"ok": False, "slug": None}
    try:
        resp = _request("GET", url, params=params)
        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        has_keys = all(k in data for k in ("lang", "hero", "sections"))
        sections = data.get("sections")
        sections_nonempty = False
        if isinstance(sections, list):
            sections_nonempty = len(sections) > 0
        elif isinstance(sections, dict):
            sections_nonempty = len(sections.keys()) > 0
        slug = _extract_slug(sections)
        ok = resp.status_code == 200 and has_keys and sections_nonempty
        result["ok"] = ok
        result["slug"] = slug
        if ok:
            _print_result(True, "GET /api/v1/blog/sections", f"lang={data.get('lang')}, slug={slug or 'n/a'}")
        else:
            _print_result(
                False,
                "GET /api/v1/blog/sections",
                f"status={resp.status_code}, body={_shorten(resp.text)}",
            )
        return result
    except Exception as exc:  # pragma: no cover - runtime safety
        _print_result(False, "GET /api/v1/blog/sections", f"error={exc}")
        return result


def check_blog_post(base_url: str, slug: str, lang: str) -> bool:
    url = f"{base_url}/api/v1/blog/posts/{slug}"
    params = {"lang": lang}
    try:
        resp = _request("GET", url, params=params)
        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        ok = resp.status_code == 200 and "slug" in data and ("title" in data or "name" in data)
        if ok:
            _print_result(True, "GET /api/v1/blog/posts/{slug}", f"slug={data.get('slug')}")
        else:
            _print_result(
                False,
                "GET /api/v1/blog/posts/{slug}",
                f"status={resp.status_code}, body={_shorten(resp.text)}",
            )
        return ok
    except Exception as exc:  # pragma: no cover
        _print_result(False, "GET /api/v1/blog/posts/{slug}", f"error={exc}")
        return False


def check_contact_support(base_url: str, lang: str) -> bool:
    url = f"{base_url}/api/v1/contact/support"
    payload = {
        "name": "SmokeTest User",
        "email": "smoke@example.com",
        "topic": "smoke-test",
        "message": "Smoke test support message",
        "lang": lang,
    }
    try:
        resp = _request("POST", url, json=payload)
        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        ok = resp.status_code == 200 and (data.get("status") == "ok" or "requestId" in data)
        if ok:
            _print_result(True, "POST /api/v1/contact/support", f"requestId={data.get('requestId', 'n/a')}")
        else:
            _print_result(
                False,
                "POST /api/v1/contact/support",
                f"status={resp.status_code}, body={_shorten(resp.text)}",
            )
        return ok
    except Exception as exc:  # pragma: no cover
        _print_result(False, "POST /api/v1/contact/support", f"error={exc}")
        return False


def check_contact_consult(base_url: str, lang: str) -> bool:
    url = f"{base_url}/api/v1/contact/consult"
    payload = {
        "name": "SmokeTest Consult",
        "email": "smoke@example.com",
        "preferredChannel": "email",
        "preferredTime": "evening",
        "topic": "smoke-test",
        "message": "Smoke test consult message",
        "lang": lang,
    }
    try:
        resp = _request("POST", url, json=payload)
        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        ok = resp.status_code == 200 and (data.get("status") == "ok" or "requestId" in data)
        if ok:
            _print_result(True, "POST /api/v1/contact/consult", f"requestId={data.get('requestId', 'n/a')}")
        else:
            _print_result(
                False,
                "POST /api/v1/contact/consult",
                f"status={resp.status_code}, body={_shorten(resp.text)}",
            )
        return ok
    except Exception as exc:  # pragma: no cover
        _print_result(False, "POST /api/v1/contact/consult", f"error={exc}")
        return False


def check_ai_chat(base_url: str, lang: str) -> bool:
    url = f"{base_url}/api/v1/ai/chat"
    payload = {
        "lang": lang,
        "messages": [
            {"role": "user", "content": "Hello from smoke test"},
        ],
    }
    try:
        resp = _request("POST", url, json=payload)
        data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        ok = resp.status_code == 200 and isinstance(data.get("reply"), str)
        if ok:
            _print_result(True, "POST /api/v1/ai/chat", "reply length={}".format(len(data.get("reply", ""))))
        else:
            _print_result(
                False,
                "POST /api/v1/ai/chat",
                f"status={resp.status_code}, body={_shorten(resp.text)}",
            )
        return ok
    except Exception as exc:  # pragma: no cover
        _print_result(False, "POST /api/v1/ai/chat", f"error={exc}")
        return False


def main() -> int:
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:8810").rstrip("/")
    lang = _normalize_lang(os.getenv("LANG", "en"))

    print(f"Running smoke tests against {base_url} (lang={lang})")

    results: List[bool] = []

    results.append(check_health(base_url))

    sections_result = check_blog_sections(base_url, lang)
    results.append(sections_result.get("ok", False))

    slug = sections_result.get("slug") or FALLBACK_SLUG
    results.append(check_blog_post(base_url, slug, lang))

    results.append(check_contact_support(base_url, lang))
    results.append(check_contact_consult(base_url, lang))
    results.append(check_ai_chat(base_url, lang))

    all_ok = all(results)
    print("\nOverall:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
