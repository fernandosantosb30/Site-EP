"""Export the Flask templates as a self-contained static site for CDN hosting."""
from datetime import datetime, timezone
from pathlib import Path
import shutil

from flask import render_template
from app import create_app

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "dist"
PAGES = {"main.home": ("/", "index.html"),
         "main.trabalhe_conosco": ("/trabalhe-conosco/", "trabalhe-conosco/index.html")}


def build():
    app = create_app()
    # Build pages first: a template failure must not remove the last successful build.
    def static_url(endpoint, **values):
        if endpoint == "static":
            return "/static/" + values["filename"]
        return PAGES[endpoint][0]

    pages = {}
    for endpoint, (_, filename) in PAGES.items():
        flask_path = "/" if endpoint == "main.home" else "/trabalhe-conosco"
        with app.test_request_context(flask_path):
            pages[filename] = render_template(
                "index.html" if endpoint == "main.home" else "trabalhe-conosco.html",
                url_for=static_url,
                static_export=True,
                current_year=datetime.now(timezone.utc).year,
                candidature_url=app.config.get("CANDIDATURE_URL", ""),
                candidature_email=app.config.get("CANDIDATURE_EMAIL", ""),
            )
    OUTPUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "static", OUTPUT / "static", dirs_exist_ok=True)
    for filename, html in pages.items():
        target = OUTPUT / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
    print(f"Static site generated in {OUTPUT}")


if __name__ == "__main__":
    build()
