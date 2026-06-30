import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import entity


REQUIRED_ASSETS = {
    "assets/adriano-bugnotto-background.jpg",
    "assets/play_button.png",
    "assets/exit_button.png",
    "assets/game_logo.png",
    "assets/bg_game.png",
    "assets/PLAYER_PLACEHOLDER.png",
    "assets/char_base_sheet.png",
    "assets/Slime1_Walk_body.png",
}

REQUIRED_MODULES = {
    "animation.py",
    "button.py",
    "constants.py",
    "enemy.py",
    "enemySpawn.py",
    "entity.py",
    "game.py",
    "main.py",
    "menu.py",
    "player.py",
    "shot.py",
    "sprite_frames.py",
    "sprite_sheet.py",
}


def test_frozen_pyinstaller_asset_lookup_uses_meipass(monkeypatch, tmp_path):
    temp_dir = tmp_path / "Temp"
    frozen_dir = temp_dir / "_MEI12345"
    packaged_assets_dir = frozen_dir / "assets"
    packaged_assets_dir.mkdir(parents=True)
    (temp_dir / "assets").mkdir()

    monkeypatch.setattr(entity, "__file__", str(frozen_dir / "entity.py"))
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(frozen_dir), raising=False)

    assert entity._resolve_assets_dir() == packaged_assets_dir


def test_wheel_includes_runtime_assets_and_modules(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    shutil.rmtree(project_root / "build", ignore_errors=True)
    shutil.rmtree(project_root / "survivor.egg-info", ignore_errors=True)
    shutil.rmtree(project_root / "src" / "survivor.egg-info", ignore_errors=True)

    subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", str(tmp_path)],
        check=True,
        cwd=project_root,
    )
    wheel = next(tmp_path.glob("*.whl"))

    with zipfile.ZipFile(wheel) as archive:
        packaged_files = set(archive.namelist())

    assert REQUIRED_ASSETS <= packaged_files
    assert REQUIRED_MODULES <= packaged_files
