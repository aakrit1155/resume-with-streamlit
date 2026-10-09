"""Run with: python -m unittest discover -s tests -v"""

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from streamlit.testing.v1 import AppTest

from portfolio import ROOT, asset_path, filter_projects, load_content, safe_url


class ContentTests(unittest.TestCase):
    def setUp(self):
        self.data = load_content(ROOT / "data/portfolio.json")

    def test_search_combines_terms_category_and_technologies(self):
        matches = filter_projects(self.data["projects"], "  NEWS python ",
                                  "Applied AI", ["LangChain"])
        self.assertEqual([p["id"] for p in matches], ["agentic_chat_assistant"])
        self.assertEqual(filter_projects(self.data["projects"], "YOLO", technologies=["Django"]), [])

    def test_hidden_project_is_never_returned(self):
        projects = copy.deepcopy(self.data["projects"])
        projects[0]["visible"] = False
        self.assertNotIn(projects[0], filter_projects(projects))
        self.assertNotIn(projects[0], filter_projects(projects, featured_only=True))

    def test_all_technology_selections_must_match(self):
        matches = filter_projects(self.data["projects"], technologies=["Python", "YOLO"])
        self.assertEqual(len(matches), 1)

    def test_assets_stay_inside_project(self):
        self.assertIsNone(asset_path("../upload/resume_app.py"))
        self.assertIsNone(asset_path("assets/does-not-exist.pdf"))
        path = asset_path(self.data["profile"]["resume"])
        self.assertIsNotNone(path)
        self.assertTrue(path.read_bytes().startswith(b"%PDF-"))

    def test_urls_reject_non_web_schemes(self):
        self.assertIsNone(safe_url("javascript:alert(1)"))
        self.assertIsNone(safe_url("file:///etc/passwd"))
        self.assertIsNone(safe_url("https://user:pass@example.com"))
        self.assertEqual(safe_url("https://github.com/aakrit1155"), "https://github.com/aakrit1155")

    def test_duplicate_ids_are_reported(self):
        self.data["projects"].append(copy.deepcopy(self.data["projects"][0]))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "content.json"
            path.write_text(json.dumps(self.data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unique"):
                load_content(path)


class AppTests(unittest.TestCase):
    def render_page(self, name):
        app = AppTest.from_string(
            "from portfolio import ROOT, load_content, " + name + "\n"
            "data = load_content(ROOT / 'data/portfolio.json')\n"
            + name + "(data)\n"
        ).run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        return app

    def test_home_and_download(self):
        app = AppTest.from_file(str(ROOT / "resume_app.py")).run(timeout=30)
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.get("download_button")), 1)
        self.assertEqual(len(app.get("page_link")), 1)

    def test_all_other_pages(self):
        for name in ("projects_page", "experience_page", "background_page", "contact_page"):
            with self.subTest(page=name):
                self.render_page(name)

    def test_search_empty_state_and_reset(self):
        app = self.render_page("projects_page")
        app.text_input(key="project_query").set_value("YOLO").run()
        self.assertIn("1 of 8 projects", [x.value for x in app.caption])
        app.text_input(key="project_query").set_value("no_such_project_zz").run()
        self.assertEqual(len(app.info), 1)
        app.button[0].click().run()
        self.assertEqual(app.text_input(key="project_query").value, "")
        self.assertIn("8 of 8 projects", [x.value for x in app.caption])

    def test_widget_filter_combinations(self):
        app = self.render_page("projects_page")
        app.selectbox(key="project_category").select("Computer Vision").run()
        app.multiselect(key="project_technologies").set_value(["Python", "YOLO"]).run()
        self.assertIn("1 of 8 projects", [x.value for x in app.caption])
        app.toggle(key="project_featured").set_value(True).run()
        self.assertIn("0 of 8 projects", [x.value for x in app.caption])

    def test_private_repository_has_no_source_button(self):
        app = AppTest.from_string(
            "from portfolio import ROOT, load_content, project_card\n"
            "p = load_content(ROOT / 'data/portfolio.json')['projects'][0]\n"
            "p['repository_public'] = False\n"
            "p['demo_url'] = ''\n"
            "project_card(p)\n"
        ).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.get("link_button")), 0)

    def test_missing_assets_do_not_crash(self):
        app = AppTest.from_string(
            "from portfolio import resume_download, optional_image\n"
            "resume_download({'resume': 'assets/missing.pdf'}, 'test_cv')\n"
            "optional_image('assets/missing.jpg', 'Portrait')\n"
        ).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(app.get("download_button")), 0)
        self.assertTrue(any("email" in x.value for x in app.caption))


if __name__ == "__main__":
    unittest.main()
