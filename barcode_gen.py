from pathlib import Path

from barcode import Code39
from barcode.writer import ImageWriter


def generate(serial: str, output_path: Path) -> Path:
    """Generate a Code 39 barcode PNG for the given serial number.

    Returns the path to the saved .png file.
    """
    writer = ImageWriter()
    code = Code39(serial.upper(), writer=writer, add_checksum=False)
    options = {
        "write_text": False,   # caption added separately in the label cell
        "module_height": 7.0,  # mm — compact bar height for 3/4" label
        "module_width": 0.45,  # mm per narrow bar
        "quiet_zone": 1.5,     # mm padding at each end
        "font_size": 0,
        "text_distance": 0,
        "dpi": 300,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    saved = code.save(str(output_path.with_suffix("")), options=options)
    return Path(saved)
