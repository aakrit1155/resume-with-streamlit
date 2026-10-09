"""Run from this directory: python -m streamlit run resume_app.py"""

from functools import partial

import streamlit as st

from theme import theme_controls

from portfolio import (
    ROOT,
    background_page,
    contact_page,
    experience_page,
    footer,
    load_content,
    overview_page,
    projects_page,
)

st.set_page_config(
    page_title="Aakrit Sharma Lamsal | Software & AI",
    page_icon=":material/code:",
    layout="wide",
)

try:
    content = load_content(ROOT / "data" / "portfolio.json")
except (OSError, ValueError) as exc:
    st.error("Portfolio content could not be loaded.")
    st.caption("Check data/portfolio.json and restart the application.")
    # The full diagnostic stays in the server log.
    import logging

    logging.getLogger(__name__).exception("Invalid portfolio content: %s", exc)
    st.stop()

stylesheet = ROOT / "style.css"
if stylesheet.is_file():
    st.html(stylesheet)

# Native navigation provides real page URLs, keyboard access, and mobile menus.
projects_route = st.Page(partial(projects_page, content), title="Projects", url_path="projects")
pages = [
    st.Page(partial(overview_page, content, projects_route), title="Overview", default=True),
    projects_route,
    st.Page(partial(experience_page, content), title="Experience", url_path="experience"),
    st.Page(partial(background_page, content), title="Background", url_path="background"),
    st.Page(partial(contact_page, content), title="Contact", url_path="contact"),
]
page = st.navigation(pages, position="top")
theme_controls()
page.run()
footer(content)
