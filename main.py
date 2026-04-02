import subprocess
import sys


def run_script(script_name):
    print(f"\nRunning {script_name} ...")
    result = subprocess.run([sys.executable, script_name])

    if result.returncode != 0:
        print(f"{script_name} failed.")
        raise SystemExit(1)


def main():
    run_script("preprocess.py")
    run_script("run_all_clips.py")
    run_script("merge_results.py")
    run_script("report.py")
    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()