"""Reusable presentation helpers. Edit data/portfolio.json to update content."""

from __future__ import annotations

import json
import logging
from datetime import date
from html import escape
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit

import streamlit as st
from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parent
Record = dict[str, Any]
LOGGER = logging.getLogger(__name__)


def safe_url(value: str) -> str | None:
    """Only ordinary web links may be rendered from the content file."""
    try:
        parsed = urlsplit(value)
        if parsed.scheme in {"https", "http"} and parsed.hostname and not parsed.username:
            return value
    except ValueError:
        pass
    return None


def asset_path(value: str) -> Path | None:
    """Resolve local assets relative to the app, independent of the shell's cwd."""
    if not value:
        return None
    path = (ROOT / value).resolve()
    return path if path.is_relative_to(ROOT) and path.is_file() else None


def load_content(path: Path) -> Record:
    # This small file is intentionally read on reruns so edits appear immediately.
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("The content file must contain a JSON object.")
    # Older content files remain valid when no certificates have been added.
    data.setdefault("certifications", [])

    def require(record: Any, schema: dict[str, type], label: str) -> None:
        if not isinstance(record, dict):
            raise ValueError(f"{label} must be an object.")
        for key, kind in schema.items():
            if not isinstance(record.get(key), kind):
                raise ValueError(f"{label}.{key} must be {kind.__name__}.")

    require(data.get("profile"), {
        "name": str, "role": str, "location": str, "email": str,
        "intro": str, "about": str, "resume": str, "resume_label": str,
        "portrait": str, "portrait_caption": str,
        "links": list, "highlights": list, "focus": list,
        "languages": list, "interests": list,
    }, "profile")
    schemas = {
        "projects": {"id": str, "title": str, "category": str, "kind": str,
                     "summary": str, "technologies": list, "details": list,
                     "repository_url": str, "repository_public": bool,
                     "demo_url": str, "image": str, "image_caption": str,
                     "featured": bool, "visible": bool},
        "experience": {"company": str, "role": str, "period": str,
                       "location": str, "summary": str, "highlights": list, "skills": list},
        "education": {"institution": str, "degree": str, "period": str,
                      "location": str, "details": list},
        "skills": {"category": str, "items": list},
        "publications": {"title": str, "year": str, "venue": str, "role": str,
                         "summary": str, "contribution": str, "url": str},
        "achievements": {"title": str, "organization": str, "description": str},
        "certifications": {"title": str, "provider": str, "url": str},
    }
    for section, schema in schemas.items():
        if not isinstance(data.get(section), list):
            raise ValueError(f"{section} must be a list.")
        for index, record in enumerate(data[section]):
            require(record, schema, f"{section}[{index}]")
            for key, kind in schema.items():
                if kind is list and not all(isinstance(x, str) for x in record[key]):
                    raise ValueError(f"{section}[{index}].{key} must contain strings.")
    for index, certificate in enumerate(data["certifications"]):
        for field in ("issued", "expires"):
            if not isinstance(certificate.get(field, ""), str):
                raise ValueError(f"certifications[{index}].{field} must be a string.")
    for index, item in enumerate(data["education"]):
        if not isinstance(item.get("status", ""), str):
            raise ValueError(f"education[{index}].status must be a string.")
        courses = item.get("coursework", [])
        if not isinstance(courses, list) or not all(isinstance(x, str) for x in courses):
            raise ValueError(f"education[{index}].coursework must be a list of strings.")
    for index, role in enumerate(data["experience"]):
        if not isinstance(role.get("kind", ""), str):
            raise ValueError(f"experience[{index}].kind must be a string.")
    for field, schema in {
        "links": {"label": str, "url": str},
        "highlights": {"value": str, "label": str},
        "focus": {"title": str, "text": str},
    }.items():
        for index, record in enumerate(data["profile"][field]):
            require(record, schema, f"profile.{field}[{index}]")
    for field in ("languages", "interests"):
        if not all(isinstance(x, str) for x in data["profile"][field]):
            raise ValueError(f"profile.{field} must contain strings.")
    ids = [project["id"] for project in data["projects"]]
    if len(ids) != len(set(ids)) or any(not value.strip() for value in ids):
        raise ValueError("Project IDs must be unique and nonempty.")
    return data


def filter_projects(
    projects: list[Record], query: str = "", category: str = "All projects",
    technologies: list[str] | None = None, featured_only: bool = False,
) -> list[Record]:
    terms = query.casefold().split()
    required = set(technologies or [])
    matches = []
    for project in projects:
        if not project["visible"]:
            continue
        if category != "All projects" and project["category"] != category:
            continue
        if featured_only and not project["featured"]:
            continue
        if not required.issubset(project["technologies"]):
            continue
        searchable = " ".join([
            project["title"], project["summary"], project["category"],
            project["kind"], *project["technologies"], *project["details"],
        ]).casefold()
        if all(term in searchable for term in terms):
            matches.append(project)
    # Preserve editorial order rather than infer quality from repository stars.
    return matches


def pills(items: list[str]) -> None:
    st.html('<div class="pf-pills">' + "".join(
        f'<span class="pf-pill">{escape(item)}</span>' for item in items
    ) + "</div>")


def section(title: str, description: str = "") -> None:
    st.html(f'<div class="pf-section"><h2>{escape(title)}</h2>'
            f'<p>{escape(description)}</p></div>')


def bullets(items: list[str]) -> None:
    if items:
        st.html('<ul class="pf-list">' + "".join(f"<li>{escape(item)}</li>" for item in items) + "</ul>")


def web_button(label: str, url: str, **kwargs: Any) -> None:
    if safe_url(url):
        st.link_button(label, url, **kwargs)


def optional_image(value: str, caption: str) -> None:
    path = asset_path(value)
    if path is None:
        return
    try:
        with Image.open(path) as image:
            image.load()
            st.image(image.copy(), caption=caption or None, width="stretch")
    except (OSError, ValueError, UnidentifiedImageError):
        LOGGER.warning("Could not display optional image: %s", path.name)


def resume_download(profile: Record, key: str) -> None:
    path = asset_path(profile["resume"])
    try:
        payload = path.read_bytes() if path else b""
    except OSError:
        payload = b""
    if not payload.startswith(b"%PDF-"):
        st.caption("For a copy of my CV, please get in touch by email.")
        return
    st.download_button(
        "Download CV", payload, file_name="Aakrit_Sharma_Lamsal_CV.pdf",
        mime="application/pdf", key=key, icon=":material/download:", on_click="ignore",
    )


def email_url(profile: Record) -> str:
    return f"mailto:{quote(profile['email'], safe='@')}?subject=Portfolio%20enquiry"


def project_card(project: Record, *, compact: bool = False) -> None:
    with st.container(border=True):
        optional_image(project["image"], project["image_caption"] or project["title"])
        st.html(
            f'<div class="pf-card-label">{escape(project["category"])}</div>'
            f'<h3 class="pf-card-title">{escape(project["title"])}</h3>'
            f'<p class="pf-card-description">{escape(project["summary"])}</p>'
        )
        pills(project["technologies"])
        if not compact:
            with st.expander("Project details"):
                st.caption(project["kind"])
                bullets(project["details"])
        with st.container(horizontal=True):
            if project["repository_public"]:
                web_button("Source code", project["repository_url"], icon=":material/code:")
            web_button("Open demo", project["demo_url"], icon=":material/open_in_new:")


def overview_page(data: Record, projects_route: Any) -> None:
    profile = data["profile"]
    # Pair the portrait with the introduction so visitors connect a face to the name.
    intro, portrait = st.columns([2.3, 1], gap="large", vertical_alignment="center")
    with intro:
        st.html(
            '<section class="pf-hero">'
            f'<p class="pf-eyebrow">Software Engineer / {escape(profile["location"])}</p>'
            f'<h1>{escape(profile["name"])}</h1>'
            f'<p class="pf-role">{escape(profile["role"])}</p>'
            f'<p class="pf-intro">{escape(profile["intro"])}</p>'
            '</section>'
        )
        with st.container(horizontal=True, vertical_alignment="center"):
            st.link_button("Get in touch", email_url(profile), type="primary")
            resume_download(profile, "home_cv")
            for link in profile["links"][:2]:
                web_button(link["label"], link["url"])
    with portrait, st.container(key="hero_portrait"):
        optional_image(profile["portrait"], profile["portrait_caption"])

    highlights = profile["highlights"]
    if highlights:
        for column, item in zip(st.columns(len(highlights)), highlights):
            with column:
                st.html(f'<div class="pf-stat"><strong>{escape(item["value"])}</strong>'
                        f'<span>{escape(item["label"])}</span></div>')

    section("Selected work", "A few projects across applied AI and computer vision.")
    featured = filter_projects(data["projects"], featured_only=True)[:3]
    if featured:
        for column, project in zip(st.columns(len(featured)), featured):
            with column:
                project_card(project, compact=True)
    else:
        st.caption("Explore the project collection below.")
    st.page_link(projects_route, label="Explore all projects", icon=":material/arrow_forward:")

    section("From ideas to working systems")
    left, right = st.columns([1.6, 1], gap="large")
    with left:
        st.write(profile["about"])
        for item in profile["focus"]:
            st.html(f'<div class="pf-note"><p><strong>{escape(item["title"])}</strong></p>'
                    f'<p class="pf-muted">{escape(item["text"])}</p></div>')
    with right:
        with st.container(border=True):
            st.caption("CAREER & TEACHING")
            for role in data["experience"]:
                st.markdown(f'**{role["company"]}**')
                st.write(role["role"])
                st.caption(role["period"])


def reset_filters() -> None:
    st.session_state.update(project_query="", project_category="All projects",
                            project_technologies=[], project_featured=False)


def projects_page(data: Record) -> None:
    st.title("Projects")
    st.write("Practical explorations in AI, computer vision, machine learning, and data.")
    visible = filter_projects(data["projects"])
    categories = ["All projects"] + sorted({p["category"] for p in visible})
    technologies = sorted({tag for p in visible for tag in p["technologies"]})
    search_column, category_column = st.columns([2, 1])
    with search_column:
        query = st.text_input("Search projects", placeholder="Try Python, YOLO, or computer vision",
                              key="project_query", max_chars=200)
    with category_column:
        category = st.selectbox("Area", categories, key="project_category")
    selected = st.multiselect("Technologies", technologies, key="project_technologies",
                              help="Projects must include every selected technology.")
    with st.container(horizontal=True, vertical_alignment="center"):
        featured_only = st.toggle("Featured only", key="project_featured")
        st.button("Clear filters", on_click=reset_filters, type="tertiary")
    matches = filter_projects(visible, query, category, selected, featured_only)
    st.caption(f"{len(matches)} of {len(visible)} projects")
    if not matches:
        st.info("No projects match these filters. Try another term or clear the filters.")
    for offset in range(0, len(matches), 2):
        for column, project in zip(st.columns(2, gap="medium"), matches[offset:offset + 2]):
            with column:
                project_card(project)


def experience_page(data: Record) -> None:
    st.title("Experience")
    st.write("Software engineering, applied AI, and graduate teaching.")
    for role in data["experience"]:
        # Stacked cards preserve chronology and leave room for substantive details.
        with st.container(border=True):
            period, details = st.columns([1, 3], gap="large")
            with period:
                st.html(f'<div class="pf-timeline-date">{escape(role["period"])}</div>')
                st.caption(role["location"])
                if role.get("kind"):
                    st.caption(role["kind"])
            with details:
                st.html(f'<p class="pf-card-label">{escape(role["company"])}</p>')
                st.subheader(role["role"])
                st.write(role["summary"])
                bullets(role["highlights"])
                pills(role["skills"])


def certification_card(certificate: Record) -> None:
    with st.container(border=True):
        st.caption(certificate["provider"])
        st.subheader(certificate["title"])
        dates = []
        if certificate.get("issued"):
            dates.append(f'Issued {certificate["issued"]}')
        if certificate.get("expires"):
            dates.append(f'Expires {certificate["expires"]}')
        if dates:
            st.caption(" · ".join(dates))
        web_button("View credential", certificate["url"], icon=":material/open_in_new:")


def background_page(data: Record) -> None:
    st.title("Background")
    st.write("The technical toolkit, education, and research behind my work.")
    section("Technical skills")
    for offset in range(0, len(data["skills"]), 2):
        for column, group in zip(st.columns(2, gap="large"), data["skills"][offset:offset + 2]):
            with column:
                with st.container(border=True):
                    st.markdown(f'**{group["category"]}**')
                    pills(group["items"])
    section("Education")
    for item in data["education"]:
        with st.container(border=True):
            if item.get("status"):
                pills([item["status"]])
            st.subheader(item["institution"])
            st.write(item["degree"])
            st.caption(f'{item["period"]} · {item["location"]}')
            bullets(item["details"])
            if item.get("coursework"):
                st.caption("RELEVANT COURSEWORK")
                pills(item["coursework"])
    if data["publications"]:
        section("Research")
        for paper in data["publications"]:
            with st.container(border=True):
                st.caption(f'{paper["role"]} · {paper["venue"]} · {paper["year"]}')
                st.subheader(paper["title"])
                st.write(paper["summary"])
                st.write(paper["contribution"])
                web_button("Read publication", paper["url"], icon=":material/article:")
    if data["achievements"]:
        section("Recognition")
        for offset in range(0, len(data["achievements"]), 2):
            for column, item in zip(st.columns(2), data["achievements"][offset:offset + 2]):
                with column, st.container(border=True):
                    st.markdown(f'**{item["title"]}**')
                    st.caption(item["organization"])
                    st.write(item["description"])
    certificates = data.get("certifications", [])
    if certificates:
        section("Certifications & training")
        for offset in range(0, len(certificates), 2):
            for column, certificate in zip(st.columns(2), certificates[offset:offset + 2]):
                with column:
                    certification_card(certificate)
    with st.expander("Beyond work"):
        st.markdown("**Languages**")
        pills(data["profile"]["languages"])
        st.markdown("**Interests**")
        pills(data["profile"]["interests"])


def contact_page(data: Record) -> None:
    profile = data["profile"]
    st.title("Let's connect")
    st.write("For engineering opportunities, research conversations, or project collaboration.")
    st.caption(profile["location"])
    st.subheader(profile["email"])
    with st.container(horizontal=True):
        st.link_button("Write an email", email_url(profile), type="primary", icon=":material/mail:")
        resume_download(profile, "contact_cv")
    st.caption(profile["resume_label"])
    section("Find me online")
    with st.container(horizontal=True):
        for link in profile["links"]:
            web_button(link["label"], link["url"], icon=":material/open_in_new:")


def footer(data: Record) -> None:
    st.html(f'<footer class="pf-footer">© {date.today().year} '
            f'{escape(data["profile"]["name"])} · Built with Python &amp; Streamlit'
            '</footer>')
