import tempfile
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

import config
from barcode_gen import generate as gen_barcode


def _build_col_layout():
    widths, indices = [], []
    for i in range(config.LABELS_PER_ROW):
        indices.append(i * 2)
        widths.append(config.LABEL_WIDTH_IN)
        if i < config.LABELS_PER_ROW - 1:
            widths.append(config.COL_GAP_IN)
    return widths, indices


_COL_WIDTHS_IN, _LABEL_COL_INDICES = _build_col_layout()


def build(records: list[dict], output_path: str | Path) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        barcode_paths = _generate_barcodes(records, tmp)
        doc = _make_document(list(records), barcode_paths)
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        doc.save(str(out))


def _generate_barcodes(records: list[dict], tmp: Path) -> dict[str, Path]:
    seen: dict[str, Path] = {}
    for r in records:
        serial = r["serial_number"]
        if serial not in seen:
            seen[serial] = gen_barcode(serial, tmp / f"bc_{serial}")
    return seen


def _make_document(records: list[dict], barcode_paths: dict[str, Path]) -> Document:
    doc = Document()
    _setup_page(doc)

    # Remove the default empty paragraph Word adds
    for para in doc.paragraphs:
        para._element.getparent().remove(para._element)

    # Pad to a full number of pages
    while len(records) % config.LABELS_PER_PAGE != 0:
        records.append(None)

    total_rows = len(records) // config.LABELS_PER_ROW
    table = doc.add_table(rows=total_rows, cols=len(_COL_WIDTHS_IN))
    _configure_table(table)

    for row_idx in range(total_rows):
        _configure_row(table.rows[row_idx])
        for label_pos, col_idx in enumerate(_LABEL_COL_INDICES):
            record_idx = row_idx * config.LABELS_PER_ROW + label_pos
            record = records[record_idx]
            cell = table.cell(row_idx, col_idx)
            _set_cell_margins(cell)
            if record:
                _fill_cell(cell, record, barcode_paths.get(record["serial_number"]))

    return doc


def _setup_page(doc: Document) -> None:
    section = doc.sections[0]
    section.page_width = Inches(config.PAGE_WIDTH_IN)
    section.page_height = Inches(config.PAGE_HEIGHT_IN)
    section.top_margin = Inches(config.MARGIN_TOP_IN)
    section.bottom_margin = Inches(config.MARGIN_BOTTOM_IN)
    section.left_margin = Inches(config.MARGIN_LEFT_IN)
    section.right_margin = Inches(config.MARGIN_RIGHT_IN)

    # Remove Normal style paragraph spacing so cells start clean
    normal = doc.styles["Normal"]
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(0)


def _configure_table(table) -> None:
    tbl = table._tbl
    tblPr = tbl.tblPr

    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)

    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "none")
        el.set(qn("w:sz"), "0")
        borders.append(el)
    tblPr.append(borders)

    spacing = OxmlElement("w:tblCellSpacing")
    spacing.set(qn("w:w"), "0")
    spacing.set(qn("w:type"), "dxa")
    tblPr.append(spacing)

    tblGrid = OxmlElement("w:tblGrid")
    for w_in in _COL_WIDTHS_IN:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(_twips(w_in)))
        tblGrid.append(gc)
    tblPr.addnext(tblGrid)

    for row in table.rows:
        for col_idx, cell in enumerate(row.cells):
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            existing = tcPr.find(qn("w:tcW"))
            if existing is not None:
                tcPr.remove(existing)
            tcW = OxmlElement("w:tcW")
            tcW.set(qn("w:w"), str(_twips(_COL_WIDTHS_IN[col_idx])))
            tcW.set(qn("w:type"), "dxa")
            tcPr.append(tcW)


def _configure_row(row) -> None:
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    trHeight = OxmlElement("w:trHeight")
    trHeight.set(qn("w:val"), str(_twips(config.LABEL_HEIGHT_IN)))
    trHeight.set(qn("w:hRule"), "exact")
    trPr.append(trHeight)


def _set_cell_margins(cell, margin_in: float = 0.03) -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(_twips(margin_in)))
        el.set(qn("w:type"), "dxa")
        tcMar.append(el)
    tcPr.append(tcMar)


def _fill_cell(cell, record: dict, barcode_path: Path | None) -> None:
    label_text = record.get("label", config.DEFAULT_LABEL_TEXT)
    serial = record["serial_number"]

    p0 = cell.paragraphs[0]
    _style_para(p0, label_text, config.FONT_HEADER_PT, bold=True)

    _style_para(cell.add_paragraph(), f"{config.SERIAL_LINE_PREFIX}: {serial}", config.FONT_SERIAL_PT)

    if barcode_path and barcode_path.exists():
        p_bc = cell.add_paragraph()
        # Use auto line spacing for the image paragraph — exact spacing causes the
        # image to anchor at the text baseline and overflow above the line boundary,
        # overlapping the serial number text. Auto lets Word expand the line to fit.
        _set_para_spacing_auto(p_bc)
        p_bc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_bc.add_run().add_picture(
            str(barcode_path),
            width=Inches(config.BARCODE_WIDTH_IN),
            height=Inches(config.BARCODE_HEIGHT_IN),
        )

    _style_para(cell.add_paragraph(), f"*{serial}*", config.FONT_CAPTION_PT)


def _style_para(para, text: str, font_pt: float, bold: bool = False) -> None:
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _set_para_spacing(para, line_pt=font_pt + 1)
    run = para.add_run(text)
    run.bold = bold
    run.font.size = Pt(font_pt)
    run.font.name = "Arial"


def _set_para_spacing(para, line_pt: float) -> None:
    """Exact line spacing + zero before/after via direct XML (overrides style defaults)."""
    pPr = para._p.get_or_add_pPr()
    spacing = pPr.find(qn("w:spacing"))
    if spacing is None:
        spacing = OxmlElement("w:spacing")
        pPr.append(spacing)
    spacing.set(qn("w:before"), "0")
    spacing.set(qn("w:after"), "0")
    spacing.set(qn("w:line"), str(int(line_pt * 20)))  # twips (1pt = 20 twips)
    spacing.set(qn("w:lineRule"), "exact")


def _set_para_spacing_auto(para) -> None:
    """Zero before/after; let Word auto-size the line height to fit inline content."""
    pPr = para._p.get_or_add_pPr()
    spacing = pPr.find(qn("w:spacing"))
    if spacing is None:
        spacing = OxmlElement("w:spacing")
        pPr.append(spacing)
    spacing.set(qn("w:before"), "0")
    spacing.set(qn("w:after"), "0")


def _twips(inches: float) -> int:
    return int(inches * 1440)
