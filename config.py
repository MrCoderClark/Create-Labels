# Avery 61528 — PermaTrack Metallic Silver Asset Tags, 1-1/4" x 2-3/4", 14/sheet

LABELS_PER_ROW = 2
ROWS_PER_PAGE = 7
LABELS_PER_PAGE = LABELS_PER_ROW * ROWS_PER_PAGE  # 14

# Physical label dimensions (inches)
LABEL_WIDTH_IN = 2.75
LABEL_HEIGHT_IN = 1.25
COL_GAP_IN = 0.5  # horizontal gap between columns

# Page layout — verify with test print on plain paper
# Math: left(1.25) + label(2.75) + gap(0.5) + label(2.75) + right(1.25) = 8.5" ✓
# Math: top(0.5) + 7*label(8.75) + bottom(1.75) = 11.0" ✓
PAGE_WIDTH_IN = 8.5
PAGE_HEIGHT_IN = 11.0
MARGIN_TOP_IN = 0.5
MARGIN_LEFT_IN = 1.25
MARGIN_RIGHT_IN = 1.25
MARGIN_BOTTOM_IN = 1.75

# Label text defaults
DEFAULT_LABEL_TEXT = "Property of HRA"
SERIAL_LINE_PREFIX = "Serial Number"

# Font sizes (points) — sized for 1.25" tall label
FONT_HEADER_PT = 9
FONT_SERIAL_PT = 8
FONT_CAPTION_PT = 7

# Barcode image dimensions in inches
BARCODE_WIDTH_IN = 2.4
BARCODE_HEIGHT_IN = 0.5
