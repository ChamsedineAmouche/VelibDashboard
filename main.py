import subprocess
import sys


def main() -> None:
    """
    Point d'entrée du projet.
    Ce script démarre automatiquement le dashboard Streamlit.
    """
    print("🚲 Lancement du dashboard Vélib (Streamlit)...")

    try: 
        subprocess.run([sys.executable, "-m", "streamlit", "run", "src/dashboard.py"],
                    check=False,
                    )
    except KeyboardInterrupt:
        print("\n Dashboard arrêté !")


if __name__ == "__main__":
    main()
