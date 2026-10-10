"""Per-visitor appearance controls for the pinned Streamlit version."""

from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent

PALETTES = {
    "light": {
        "bg": "#FAFAF7", "surface": "#F0F2ED", "text": "#182A31",
        "muted": "#53646B", "border": "#CDD5D0", "accent": "#176B60",
        "accent-text": "#FFFFFF", "hover": "#E3EBE5", "track": "#64756E",
    },
    "dark": {
        "bg": "#10171C", "surface": "#1A242B", "text": "#E9F0F3",
        "muted": "#ADBCC4", "border": "#3C4D57", "accent": "#8BD5C5",
        "accent-text": "#10231F", "hover": "#283A42", "track": "#64756E",
    },
}


def _remember_theme() -> None:
    st.session_state.portfolio_theme = (
        "dark" if st.session_state._portfolio_dark_mode else "light"
    )


def theme_controls() -> None:
    # Keep durable state separate from widget state, which pages may clean up.
    if "portfolio_theme" not in st.session_state:
        st.session_state.portfolio_theme = (
            "light" if st.query_params.get("theme") == "light" else "dark"
        )
    st.session_state._portfolio_dark_mode = st.session_state.portfolio_theme == "dark"

    with st.container(key="theme_controls"):
        dark = st.toggle("Dark mode", key="_portfolio_dark_mode", on_change=_remember_theme)

    mode = "dark" if dark else "light"
    # Preserve the choice on refresh without cookies or a JavaScript dependency.
    st.query_params["theme"] = mode

    tokens = ";".join(f"--pf-{key}:{value}" for key, value in PALETTES[mode].items())
    st.html(f"<style>:root{{{tokens};color-scheme:{mode};}}</style>")
    # CSS is scoped to the components used by this portfolio; no global config mutation.
    st.html(ROOT / "theme.css")
