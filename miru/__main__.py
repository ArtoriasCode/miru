import sys
from argparse import ArgumentParser
from shutil import copy2
from pathlib import Path
from re import compile, IGNORECASE


def setup() -> None:
    """
    Setups Miru for the Vue project.

    Parameters:
    - None.

    Returns:
    - None.
    """
    parser = ArgumentParser(
        description="Setup Miru for a Vue project"
    )
    parser.add_argument(
        "--vue-dir",
        required=True,
        help="Path to the root folder of the Vue project"
    )
    args = parser.parse_args()

    package_dir = Path(__file__).resolve().parent
    src_js = package_dir / "web" / "miru.js"

    if not src_js.exists():
        print(f"Error: {src_js} not found", file=sys.stderr)
        sys.exit(1)

    target_assets = Path(args.vue_dir) / "src" / "assets" / "js"
    target_assets.mkdir(parents=True, exist_ok=True)

    dest_js = target_assets / "miru.js"
    copy2(src_js, dest_js)

    print(f"Copied {src_js} → {dest_js}")

    app_vue = Path(args.vue_dir) / "src" / "App.vue"

    if not app_vue.exists():
        print(f"Warning: {app_vue} not found — skipping injection")
        return

    app_code = app_vue.read_text(encoding="utf-8")

    inject_code = (
        "import { miru } from '@/assets/js/miru'\n"
        "window.miru = miru;\n"
        "window.miru.setup();\n"
    )

    open_tag_pattern = compile(r"(<script[^>]*>)", IGNORECASE)

    if inject_code.strip() in app_code:
        print("Miru setup code already injected — skipping")
    else:
        if open_tag_pattern.search(app_code):
            app_code = open_tag_pattern.sub(rf"\1\n{inject_code}", app_code, count=1)
        else:
            app_code = f"<script>\n{inject_code}</script>\n\n" + app_code

        app_vue.write_text(app_code, encoding="utf-8")
        print(f"Injected Miru setup code into {app_vue}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        sys.argv.pop(1)
        setup()
    else:
        print("Usage: python -m miru setup --vue-dir /path/to/vue")
