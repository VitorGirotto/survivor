import shutil
import subprocess
import zipfile
from pathlib import Path


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
