import pcbnew
import zipfile
import tempfile
import pathlib
import logging
import subprocess
from pprint import pprint

def export_gerbers(pcb_file, output_folder):
    layers = [
        "F.Cu",
        "F.Mask",
        "F.Silkscreen",
        "In1.Cu",
        "In2.Cu",
        "B.Cu",
        "B.Mask",
        "B.Silkscreen",
        "Edge.Cuts"]

    # Gerber files
    cmd = ["kicad-cli", "pcb", "export", "gerbers",
           "--layers", ",".join(layers),
           "--output", output_folder, pcb_file]
    logging.info(f"{cmd=}")
    with subprocess.Popen(cmd) as pid:
        pid.communicate(timeout=10)

    # Drill files
    cmd = ["kicad-cli", "pcb", "export", "drill",
           "--output", output_folder, pcb_file]
    logging.info(f"{cmd=}")
    with subprocess.Popen(cmd) as pid:
        pid.communicate(timeout=10)

def main():
    logging.basicConfig(level=logging.INFO)

    pcb_file = pathlib.Path("pcb_segger_edu.kicad_pcb")
    if not pcb_file.exists():
        raise FileNotFoundError(f"Cannot find {pcb_file=}")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create gerber folder
        gerber_folder = pathlib.Path(temp_dir) / "gerbers"
        gerber_folder.mkdir()
        gerber_folder_str = str(gerber_folder) + "/"

        # Export gerbers
        logging.info(gerber_folder)
        export_gerbers(pcb_file, gerber_folder_str)

        # Delete gbrjob
        for file in gerber_folder.glob("*.gbrjob"):
            file.unlink()

        # Create zip
        gerber_zip = pcb_file.parent / "gerbers.zip"
        with zipfile.ZipFile(gerber_zip, "w") as zfid:
            for file in gerber_folder.glob("*"):
                zfid.write(file, file.name)
                logging.info("Zipping %s", file)

if __name__ == "__main__":
    main()
