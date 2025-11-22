#!/usr/bin/env python3
"""Script de vérification pré-commit pour s'assurer que le code est prêt."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def run_command(cmd: list[str], description: str) -> bool:
    """Exécute une commande et retourne True si succès."""
    print(f"\n[VERIFICATION] {description}...")
    try:
        result = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] {e.stderr}")
        return False


def check_imports() -> bool:
    """Vérifie que tous les imports fonctionnent."""
    print("\n[VERIFICATION] Vérification des imports...")
    import sys
    sys.path.insert(0, str(BASE_DIR))
    try:
        import app_core  # noqa: F401
        import app_core.config  # noqa: F401
        import app_core.data  # noqa: F401
        import app_core.metrics  # noqa: F401
        import app_core.plots  # noqa: F401
        import app_core.sections  # noqa: F401
        print("[OK] Tous les imports sont valides")
        return True
    except ImportError as e:
        print(f"[ERREUR] Erreur d'import: {e}")
        return False


def check_data_files() -> bool:
    """Vérifie que les fichiers de données requis existent."""
    print("\n[VERIFICATION] Vérification des fichiers de données...")
    required = [
        BASE_DIR / "Data" / "sample_clients.csv",
        BASE_DIR / "Data" / "reponses_free.csv",
    ]
    all_ok = True
    for path in required:
        if path.exists():
            print(f"[OK] {path.name} existe")
        else:
            print(f"[AVERTISSEMENT] {path.name} manquant (non bloquant pour le commit)")
    return all_ok


def main() -> int:
    """Point d'entrée principal."""
    print("Verification pre-commit du dashboard Free SAV")
    print("=" * 60)

    checks = [
        (check_imports, "Imports"),
        (check_data_files, "Fichiers de données"),
        (
            lambda: run_command(
                ["python", "-m", "pytest", "-v", "--tb=short"],
                "Exécution des tests",
            ),
            "Tests",
        ),
    ]

    results = []
    for check_func, name in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"[ERREUR] Erreur lors de la verification {name}: {e}")
            results.append((name, False))

    print("\n" + "=" * 60)
    print("Resume des verifications:")
    all_passed = True
    for name, passed in results:
        status = "[OK]" if passed else "[ERREUR]"
        print(f"  {status} {name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n[SUCCES] Toutes les verifications ont reussi.")
        return 0
    else:
        print("\n[AVERTISSEMENT] Certaines verifications ont echoue. Verifiez les erreurs ci-dessus.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

