# Aakrit's portfolio

## Run

Use Python 3.12. From the folder containing `resume_app.py`:

With uv:

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
uv run python run_local.py
```

Select the project's `.venv` interpreter in VS Code so Pylance reads the installed
Streamlit version. The steps below are an alternative using standard Python tools.

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
python run_local.py
```

Open http://localhost:8501. No API keys, databases, or system packages are needed.
The local launcher binds to `127.0.0.1` and prints only `http://localhost:8501`.
For another local port, use `uv run python run_local.py --port 8502`.

## Light and dark themes

Open the top-right **⋮ menu → Settings → Choose app theme**. Choose **Dark**,
**Light**, or the custom light theme. The portfolio's accents, cards, tags, and
text follow the active theme immediately, including when using the navigation bar.
Streamlit handles preferences independently for each visitor. In Streamlit 1.50,
opening or refreshing a different page URL can require selecting the theme again.

## Files

| File | Purpose |
| --- | --- |
| `resume_app.py` | Entry point and native page navigation |
| `run_local.py` | Local-only launcher; displays one localhost URL |
| `portfolio.py` | Reusable rendering, filtering, asset handling, and validation |
| `data/portfolio.json` | Profile, projects, experience, skills, education, research |
| `style.css` | Small visual layer over native Streamlit components |
| `.streamlit/config.toml` | Theme and application settings |
| `assets/Aakrit_CV_latest_Jan_2026.pdf` | Downloadable CV supplied with the project |
| `assets/Aakrit_professional_portrait.png` | Portrait displayed on the Overview page |
| `tests/test_portfolio.py` | Content, filtering, and Streamlit smoke tests |

## Update content

Edit `data/portfolio.json`; do not put personal content into the rendering functions.
Save valid JSON, then refresh the app. The `_notes` object records content sources
and is not shown to visitors.

- **Project:** duplicate one project object, assign a unique `id`, and update its
  fields. Keep `visible: true` to display it. `featured: true` adds it to the
  homepage; the first three visible featured projects appear, in file order.
- **Private source code:** set `repository_public: false` to hide its repository
  link. This does not hide the project description; set `visible: false` to hide
  the whole card. Publish only project descriptions you intend to share.
- **Demo:** fill `demo_url` with its public URL, or use `""` to omit the button.
- **Screenshot:** put an image in `assets/`, then set `image` and `image_caption`
  on that project. Leave `image: ""` to keep a text-only card.
- **Portrait:** replace `assets/Aakrit_professional_portrait.png`, or update
  `profile.portrait` and `profile.portrait_caption` to use another local image.
- **Certification:** append an object to `certifications` with `title`, `provider`,
  and `url`. Optional `issued` and `expires` strings can contain a month and year;
  leave them empty if unknown. Use an empty list to hide the section. The provider
  is currently the credential platform; add the issuing institution if confirmed.
- **CV:** replace the PDF, or update `profile.resume` and `profile.resume_label`.
  The original supplied PDF is included unchanged.
- **New role, degree, publication, or award:** append an object to the relevant
  list, following the fields in an existing entry.
- **Graduate education:** `status` and `coursework` are optional education fields.
  The reported GPA is currently shown as `4.1` because its grading scale has not
  been supplied. Coursework is listed without assuming completion status.
- **Teaching assistantship:** the GSU role is marked `Current`; update its `period`
  after confirming its start month and year. Role duties have not been inferred.
- **New page:** add a rendering function in `portfolio.py`, then register it with
  `st.Page` in `resume_app.py`.

An empty string omits an optional image or demo. Missing/corrupt optional images
are skipped; an unavailable CV shows an email fallback. Relative asset paths
resolve from the app directory. The public portfolio does not call GitHub or
external AI services at runtime.

## Deploy on Streamlit Community Cloud

Push this entire folder to a GitHub repository, retaining the `.streamlit` folder
and the PDF under `assets/`. Select the repository, set the entry point to
`resume_app.py`, and select Python 3.12. **Do not select `run_local.py` on Cloud.**
The shared configuration does not set `server.address`, `browser.serverAddress`,
or ports, so Community Cloud can apply its own network settings and public URL.

The Local, Network, and External URLs printed by a default Streamlit launch are
candidate addresses for the same app. A Network URL is for devices on the local
network; an External URL is not a deployment or a guarantee of public reachability.
The local launcher avoids advertising these additional addresses.

## Checks

```bash
python -m unittest discover -s tests -v
```

## Content sources

The January 2026 CV supplies the updated employment dates and profile details.
The old Streamlit app supplies additional internship, AI-COE, research, and demo
details. Eight projects were selected from the supplied repository list after
reviewing their public GitHub metadata, READMEs, and root files on 2026-10-08.
Descriptions do not claim independent performance measurements. The two demo
links come from the previous portfolio; their availability may change.

- Project sources: the `repository_url` field on each project.
- Publication: https://doi.org/10.1155/2022/2767371
- Streamlit navigation: https://docs.streamlit.io/develop/api-reference/navigation/st.navigation

The portrait and five credential titles and links were supplied by the owner on
2026-10-08. Credential dates and issuing institutions are not inferred. The links
open the providers' verification pages; verification pages could not be retrieved
during this update.

The GSU master's degree, January 2026 start, expected December 2027 graduation,
GPA, coursework, and current teaching assistantship were supplied by the owner on
2026-10-08. The downloadable January 2026 PDF remains the supplied original.

Useful additions: GPA scale, assistantship start month, project screenshots,
verified demo links, measured project results, and certificate dates.
