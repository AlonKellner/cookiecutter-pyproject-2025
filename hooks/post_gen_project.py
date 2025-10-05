#!/usr/bin/env python
import pathlib
import os
import subprocess

if __name__ == "__main__":

    # The current working directory is the newly generated project directory.
    project_dir = os.getcwd()

    # Initialize a Git repository
    try:
        subprocess.run(["git", "init"], cwd=project_dir, check=True)
        print("Git repository initialized.")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing Git repository: {e}")
        # Optional: Handle error, e.g., clean up the generated project if Git init fails.
    except FileNotFoundError:
        print("Git command not found. Please ensure Git is installed and in your PATH.")

    print("Your Python project has been created successfully!")