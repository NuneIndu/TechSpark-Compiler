import os
import shutil
import subprocess
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "..", "temp")


def execute_code(language, code, user_input):

    folder = str(uuid.uuid4())
    work_dir = os.path.join(TEMP_DIR, folder)

    os.makedirs(work_dir, exist_ok=True)

    try:

        # ---------------- JAVA ----------------

        if language == "java":

            filename = "Main.java"

            with open(os.path.join(work_dir, filename), "w", encoding="utf-8") as f:
                f.write(code)

            volume = f"{os.path.abspath(work_dir)}:/app"

            compile_cmd = [
                "docker",
                "run",
                "--rm",
                "-v",
                volume,
                "-w",
                "/app",
                "eclipse-temurin:21-jdk",
                "javac",
                "Main.java"
            ]

            compile = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True
            )

            if compile.returncode != 0:

                return {
                    "success": False,
                    "error": compile.stderr
                }

            run_cmd = [
                "docker",
                "run",
                "--rm",
                "-i",
                "-v",
                volume,
                "-w",
                "/app",
                "eclipse-temurin:21-jdk",
                "java",
                "Main"
            ]

        # ---------------- PYTHON ----------------

        elif language == "python":

            filename = "program.py"

            with open(os.path.join(work_dir, filename), "w", encoding="utf-8") as f:
                f.write(code)

            volume = f"{os.path.abspath(work_dir)}:/code"

            run_cmd = [
                "docker",
                "run",
                "--rm",
                "-i",
                "-v",
                volume,
                "-w",
                "/code",
                "python:3.13",
                "python",
                "program.py"
            ]

        # ---------------- C ----------------

        elif language == "c":

            filename = "main.c"

            with open(os.path.join(work_dir, filename), "w", encoding="utf-8") as f:
                f.write(code)

            volume = f"{os.path.abspath(work_dir)}:/app"

            compile_cmd = [
                "docker",
                "run",
                "--rm",
                "-v",
                volume,
                "-w",
                "/app",
                "gcc:14",
                "gcc",
                "main.c",
                "-o",
                "main"
            ]

            compile = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True
            )

            if compile.returncode != 0:

                return {
                    "success": False,
                    "error": compile.stderr
                }

            run_cmd = [
                "docker",
                "run",
                "--rm",
                "-i",
                "-v",
                volume,
                "-w",
                "/app",
                "gcc:14",
                "./main"
            ]

        # ---------------- C++ ----------------

        elif language == "cpp":

            filename = "main.cpp"

            with open(os.path.join(work_dir, filename), "w", encoding="utf-8") as f:
                f.write(code)

            volume = f"{os.path.abspath(work_dir)}:/app"

            compile_cmd = [
                "docker",
                "run",
                "--rm",
                "-v",
                volume,
                "-w",
                "/app",
                "gcc:14",
                "g++",
                "main.cpp",
                "-o",
                "main"
            ]

            compile = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True
            )

            if compile.returncode != 0:

                return {
                    "success": False,
                    "error": compile.stderr
                }

            run_cmd = [
                "docker",
                "run",
                "--rm",
                "-i",
                "-v",
                volume,
                "-w",
                "/app",
                "gcc:14",
                "./main"
            ]

        else:

            return {
                "success": False,
                "error": "Unsupported Language"
            }

        # ---------- RUN PROGRAM ----------

        result = subprocess.run(
            run_cmd,
            input=user_input,
            capture_output=True,
            text=True,
            timeout=20
        )

        if result.returncode != 0:

            return {
                "success": False,
                "error": result.stderr if result.stderr else result.stdout
            }

        return {
            "success": True,
            "output": result.stdout
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "error": "Execution Timed Out (20 Seconds)"
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }

    finally:

        shutil.rmtree(work_dir, ignore_errors=True)