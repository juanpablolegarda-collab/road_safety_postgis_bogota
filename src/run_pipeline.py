from pathlib import Path
import subprocess
import sys


PROJECT_DIR = Path(__file__).resolve().parents[1]

PIPELINE_STEPS = [
    {
        "name": "Build clean dataset",
        "script": PROJECT_DIR / "src" / "build_clean_dataset.py",
    },
    {
        "name": "Load clean data to PostGIS",
        "script": PROJECT_DIR / "src" / "load_to_postgis.py",
    },
    {
        "name": "Create SQL analysis views",
        "script": PROJECT_DIR / "src" / "run_sql_views.py",
    },
]


def run_step(step_name, script_path):
    print("=" * 80)
    print(f"RUNNING STEP: {step_name}")
    print("=" * 80)

    if not script_path.exists():
        raise FileNotFoundError(f"Script not found: {script_path}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_DIR,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Pipeline failed at step: {step_name}")

    print(f"COMPLETED STEP: {step_name}")


def main():
    print("=" * 80)
    print("ROAD SAFETY GEOSPATIAL PIPELINE - BOGOTÁ")
    print("=" * 80)

    for step in PIPELINE_STEPS:
        run_step(step["name"], step["script"])

    print("=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    main()