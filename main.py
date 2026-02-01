import subprocess
import sys


def main() -> None:
    """
    Point d'entrée du projet.
    Ce script démarre automatiquement le dashboard Streamlit.
    """
    print("🚲 Lancement du dashboard Vélib (Streamlit)...")

    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/dashboard.py"])


if __name__ == "__main__":
    main()
