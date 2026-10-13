#!/usr/bin/env python3
"""Build the artifact-rule task materials: frozen workbook, base decks, briefs, expected specs.

Usage: python3 generate.py [--out DIR]   (default: ./instances next to this file)

Everything is deterministic. Figures are fictional illustrative outputs; nothing is calculated
from a workbook, so no grading step depends on any spreadsheet engine.
"""
import argparse
import copy
import json
import os
import shutil

import openpyxl
from openpyxl.styles import Font
from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.parts.slide import SlideLayoutPart
from pptx.util import Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------------------
# Fictional model outputs (self-consistent across tabs)
# --------------------------------------------------------------------------------------
CASES = [
    # id, name, min_op_dscr, min_cure_dscr, support_k, irr_pct, receipts_m, debt_service_m, closing_cash_m,
    # months_below_after_cure, peak_monthly_draw_k, equity_k, distribution_k
    dict(id=1, name="Base", op=1.31, cure=1.31, support=0, irr=12.1, receipts=59.4, ds=16.4, cash=9.7,
         below=0, peak=0, equity=7560, dist=11920),
    dict(id=2, name="Delayed usage receipt", op=0.62, cure=1.25, support=320, irr=11.0, receipts=59.4, ds=16.4,
         cash=9.4, below=0, peak=250, equity=7880, dist=11960),
    dict(id=3, name="Major operating incident", op=-33.6, cure=-33.1, support=1000, irr="n/a", receipts=59.4,
         ds=16.4, cash=-8.5, below=1, peak=250, equity=8560, dist="n/a"),
    dict(id=4, name="Renewal without credit transfer", op=1.18, cure=1.25, support=410, irr=10.4, receipts=58.2,
         ds=16.4, cash=8.1, below=0, peak=250, equity=7970, dist=11850),
]
SENSITIVITY = dict(name="DSCR with support cap minus 20% (Case 2 basis)", op=0.62, cure=1.14, support=270,
                   irr=11.1, receipts=59.4, ds=16.4, cash=9.3)

TILE_LABELS = ["Min operating DSCR", "Min post-cure DSCR", "Sponsor support used", "Sponsor IRR"]
TABLE_LABELS = ["Total service receipts", "Total debt service", "Closing cash, 31 Dec 2031"]

CASE_SUMMARY_HEADER = ["Case ID", "Case", "Min operating DSCR (x)", "Min post-cure DSCR (x)",
                       "Sponsor support used (USD k)", "Sponsor IRR (%)", "Total service receipts (USD m)",
                       "Total debt service (USD m)", "Closing cash 31 Dec 2031 (USD m)"]
DSCR_HEADER = ["Case", "Min operating DSCR (x)", "Min post-cure DSCR (x)", "Months below 1.25x after cure"]
SUPPORT_HEADER = ["Case", "Peak monthly draw (USD k)", "Lifetime support used (USD k)",
                  "Lifetime cap utilisation (%)"]
RETURN_HEADER = ["Case", "Equity invested (USD k)", "Distribution 31 Dec 2031 (USD k)", "Sponsor IRR (%)"]
SENS_HEADER = ["Sensitivity"] + CASE_SUMMARY_HEADER[2:]

LIFETIME_CAP_K = 1000


def fmt_x(v):
    return "n/a" if isinstance(v, str) else f"{v:.2f}x"


def fmt_k(v):
    return "n/a" if isinstance(v, str) else f"USD {v:,.0f}k"


def fmt_pct(v):
    return "n/a (unfunded)" if isinstance(v, str) else f"{v:.1f}%"


def fmt_m(v):
    return "n/a" if isinstance(v, str) else f"USD {v:.1f}m"


def fmt_int(v):
    return "n/a" if isinstance(v, str) else f"{v:,.0f}"


def card_values(c):
    """(tile texts, table value texts) for a case-card from a case/sensitivity dict."""
    tiles = [fmt_x(c["op"]), fmt_x(c["cure"]), fmt_k(c["support"]), fmt_pct(c["irr"])]
    rows = [fmt_m(c["receipts"]), fmt_m(c["ds"]), fmt_m(c["cash"])]
    return tiles, rows


def support_rows(cases=None):
    out = []
    for c in (cases or CASES):
        util = round(100.0 * c["support"] / LIFETIME_CAP_K, 1)
        out.append([c["name"], c["peak"], c["support"], util])
    return out


def dscr_rows(cases=None):
    return [[c["name"], c["op"], c["cure"], c["below"]] for c in (cases or CASES)]


def return_rows(cases=None):
    return [[c["name"], c["equity"], c["dist"], c["irr"]] for c in (cases or CASES)]


# --------------------------------------------------------------------------------------
# Workbook
# --------------------------------------------------------------------------------------
def build_workbook(path, scale=False):
    cases = CASES6 if scale else CASES
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Read me"
    lines = [
        ("Northstar Compute - model outputs (frozen)", True),
        ("Fictional illustrative outputs of the Northstar Compute operating and financing model. "
         "All names and amounts are invented.", False),
        ("This workbook is read-only reference data for the investment committee deck. "
         "Nothing is recalculated; every value is a stored number.", False),
        ("", False),
        ("Tabs, in order:", True),
        ("Case summary - headline metrics per case (feeds the case cards)", False),
        ("DSCR summary - covenant results per case (appendix schedule)", False),
        ("Support cap - sponsor support utilisation per case (appendix schedule)", False),
        ("Sponsor return - equity, distribution and IRR per case (appendix schedule)", False),
    ] + ([
        ("Debt service - interest, principal and fees per case (appendix schedule)", False),
        ("Closing cash - minimum and closing cash per case (appendix schedule)", False),
        ("Receipts - fixed and usage receipts per case (appendix schedule)", False),
        ("Covenant tests - months tested and months below covenant per case (appendix schedule)", False),
        ("Equity cure - cure months and amounts per case (appendix schedule)", False),
    ] if scale else []) + [
        ("Sensitivity - headline metrics for the DSCR sensitivity", False),
        ("", False),
        ("Units: DSCR in multiples (x); support, equity and distributions in USD thousands (k); "
         "receipts, debt service and cash in USD millions (m); IRR in percent.", False),
    ]
    for i, (t, bold) in enumerate(lines, 1):
        ws.cell(row=i, column=1, value=t).font = Font(bold=bold)
    ws.column_dimensions["A"].width = 110

    def sheet(title, header, rows, widths=None):
        s = wb.create_sheet(title)
        for j, h in enumerate(header, 1):
            s.cell(row=1, column=j, value=h).font = Font(bold=True)
        for i, r in enumerate(rows, 2):
            for j, v in enumerate(r, 1):
                s.cell(row=i, column=j, value=v)
        for j in range(1, len(header) + 1):
            s.column_dimensions[openpyxl.utils.get_column_letter(j)].width = (widths or {}).get(j, 30)
        s.freeze_panes = "A2"
        return s

    sheet("Case summary", CASE_SUMMARY_HEADER,
          [[c["id"], c["name"], c["op"], c["cure"], c["support"], c["irr"], c["receipts"], c["ds"], c["cash"]]
           for c in cases], {1: 10, 2: 34})
    sheet("DSCR summary", DSCR_HEADER, dscr_rows(cases), {1: 34})
    sheet("Support cap", SUPPORT_HEADER, support_rows(cases), {1: 34})
    sheet("Sponsor return", RETURN_HEADER, return_rows(cases), {1: 34})
    if scale:
        for name, header, rows_fn, _ in SCALE_SCHEDULES[3:]:
            sheet(name, header, rows_fn(cases), {1: 34})
    sheet("Sensitivity", SENS_HEADER,
          [[SENSITIVITY["name"], SENSITIVITY["op"], SENSITIVITY["cure"], SENSITIVITY["support"],
            SENSITIVITY["irr"], SENSITIVITY["receipts"], SENSITIVITY["ds"], SENSITIVITY["cash"]]], {1: 48})
    wb.save(path)


# --------------------------------------------------------------------------------------
# Deck helpers
# --------------------------------------------------------------------------------------
NAVY = RGBColor(0x1F, 0x3A, 0x5F)
GREY = RGBColor(0x59, 0x59, 0x59)
TILE_FILL = RGBColor(0xE8, 0xEE, 0xF5)


def clone_layout(prs, src, name):
    master = prs.slide_master
    pkg = prs.part.package
    partname = pkg.next_partname("/ppt/slideLayouts/slideLayout%d.xml")
    el = copy.deepcopy(src._element)
    el.cSld.set("name", name)
    part = SlideLayoutPart(partname, src.part.content_type, pkg, el)
    part.relate_to(master.part, RT.SLIDE_MASTER)
    rId = master.part.relate_to(part, RT.SLIDE_LAYOUT)
    lst = master._element.find(qn("p:sldLayoutIdLst"))
    ids = [int(x.get("id")) for x in lst]
    new = etree.SubElement(lst, qn("p:sldLayoutId"))
    new.set("id", str(max(ids) + 1))
    new.set(qn("r:id"), rId)
    return part.slide_layout


def set_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def add_textbox(slide, left, top, width, height, text, size=11, color=GREY, bold=False, align=None):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.font.bold = bold
    if align is not None:
        p.alignment = align
    return tb


def fill_body(slide, paragraphs, sizes=(18, 16)):
    """paragraphs: list of (text, level)."""
    body = [ph for ph in slide.placeholders if ph.placeholder_format.idx != 0][0]
    tf = body.text_frame
    tf.clear()
    first = True
    for text, level in paragraphs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.text = text
        p.level = level
        for r in p.runs:
            r.font.size = Pt(sizes[0] if level == 0 else sizes[1])


def add_tile(slide, left, top, width, height, label, value):
    from pptx.enum.shapes import MSO_SHAPE
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shp.fill.solid()
    shp.fill.fore_color.rgb = TILE_FILL
    shp.line.color.rgb = NAVY
    shp.name = "Tile " + label
    tf = shp.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.size = Pt(12)
    r.font.color.rgb = GREY
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = value
    r2.font.size = Pt(22)
    r2.font.bold = True
    r2.font.color.rgb = NAVY
    return shp


def add_table(slide, left, top, width, height, rows, col_widths=None, font_size=12):
    nrows, ncols = len(rows), len(rows[0])
    gf = slide.shapes.add_table(nrows, ncols, left, top, width, height)
    gf.name = "Metrics table"
    tbl = gf.table
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(font_size)
                    r.font.bold = (i == 0)
    if col_widths:
        for j, w in enumerate(col_widths):
            tbl.columns[j].width = w
    return gf


def case_card(prs, layout, title, tiles, table_vals, footer, notes):
    s = prs.slides.add_slide(layout)
    s.shapes.title.text = title
    left0, top, w, h, gap = Inches(0.5), Inches(1.6), Inches(2.05), Inches(1.3), Inches(0.2)
    for i, (lab, val) in enumerate(zip(TILE_LABELS, tiles)):
        add_tile(s, left0 + i * (w + gap), top, w, h, lab, val)
    rows = [["Metric", "Value"]] + [[lab, val] for lab, val in zip(TABLE_LABELS, table_vals)]
    add_table(s, Inches(0.5), Inches(3.3), Inches(9.0), Inches(1.6), rows, [Inches(5.5), Inches(3.5)])
    fb = add_textbox(s, Inches(0.5), Inches(6.6), Inches(9.0), Inches(0.5), footer, size=10)
    fb.name = "Source note"
    set_notes(s, notes)
    return s


def schedule_slide(prs, layout, title, header, rows, footer, notes, fmts):
    s = prs.slides.add_slide(layout)
    s.shapes.title.text = title
    body = [header] + [[rows[i][0]] + [fmts[j](rows[i][j]) for j in range(1, len(header))] for i in range(len(rows))]
    add_table(s, Inches(0.5), Inches(1.6), Inches(9.0), Inches(2.6), body,
              [Inches(3.0), Inches(2.0), Inches(2.0), Inches(2.0)])
    fb = add_textbox(s, Inches(0.5), Inches(6.6), Inches(9.0), Inches(0.5), footer, size=10)
    fb.name = "Source note"
    set_notes(s, notes)
    return s


def section_slide(prs, layout, title, body, notes):
    s = prs.slides.add_slide(layout)
    s.shapes.title.text = title
    fill_body(s, [(body, 0)])
    set_notes(s, notes)
    return s


def content_slide(prs, layout, title, bullets, notes, sizes=(18, 16)):
    s = prs.slides.add_slide(layout)
    s.shapes.title.text = title
    fill_body(s, [(b, 0) for b in bullets], sizes)
    set_notes(s, notes)
    return s


# --------------------------------------------------------------------------------------
# Rules and neutral fillers
# --------------------------------------------------------------------------------------
RULES = {
    "i1_case4": {
        "location": "body text of the 'Cases' section divider slide",
        "text": ("Case slides are grouped by scenario family rather than by case number: a renewal variant "
                 "is presented immediately after its base case, before the delayed-receipt and "
                 "operating-incident cases."),
    },
    "i2_schedule": {
        "location": "speaker notes of the 'Appendix' section divider slide",
        "text": ("Supporting schedules appear in the order of the workbook tabs they are drawn from; a new "
                 "schedule is inserted at that position, never appended at the end."),
    },
    "i3_sensitivity": {
        "location": "footnote text box on the 'Agenda' slide",
        "text": ("Deck conventions: Recommendation always immediately precedes Closing; a sensitivity slide "
                 "is placed directly after the slide it sensitises."),
    },
    # ---- v2 instances ----
    "i2b_schedule_first": {
        "location": "speaker notes of the 'Appendix' section divider slide",
        "text": ("Appendix convention: a newly added schedule is inserted directly after this Appendix divider, "
                 "ahead of the existing schedules, so that the committee sees new material first. Schedules are "
                 "never appended at the end of the appendix and are not ordered by workbook tab."),
    },
    "i4_sensitivity_anchor": {
        "location": "footnote text box on the 'Agenda' slide",
        "text": ("Deck conventions: a sensitivity slide is placed directly after the slide it sensitises; "
                 "Recommendation always immediately precedes Closing."),
    },
    "i5_sensitivity_notes_anchor": {
        "location": "speaker notes of the 'Financing and covenant' section divider slide",
        "text": ("Section convention: a sensitivity slide is placed directly after the slide it sensitises, "
                 "never at the end of the section."),
    },
    "i6_sensitivity_scale": {
        "location": "footnote text box on the 'Agenda' slide",
        "text": ("Deck conventions: a sensitivity slide is placed directly after the slide it sensitises; "
                 "Recommendation always immediately precedes Closing."),
    },
}
V1_INSTANCES = ["i1_case4", "i2_schedule", "i3_sensitivity"]
AGENDA_RULE_INSTANCES = {"i3_sensitivity", "i4_sensitivity_anchor", "i6_sensitivity_scale"}
APPENDIX_NOTES_RULE_INSTANCES = {"i2_schedule", "i2b_schedule_first"}
FINANCING_NOTES_RULE_INSTANCES = {"i5_sensitivity_notes_anchor"}
SCALE_INSTANCES = {"i6_sensitivity_scale"}
NEUTRAL = {
    "cases_body": ("Each case changes only the fields shown in the Cases tab of the source workbook; prices, "
                   "service obligations and the financing commitments are fixed."),
    "appendix_notes": "Schedules are drawn directly from the frozen workbook; no figures are recalculated in this deck.",
    "agenda_footnote": "All figures are fictional illustrative outputs of the Northstar Compute model (model_outputs.xlsx).",
    "financing_notes": "Financing section: covenant first, then sources and uses.",
}

# ---- extended data for the scale instance (i6): eight cases and eight appendix schedules ----
EXTRA_CASES = [
    dict(id=5, name="Early renewal at reduced rate", op=1.27, cure=1.27, support=0, irr=11.4, receipts=57.1,
         ds=16.4, cash=8.9, below=0, peak=0, equity=7560, dist=11640),
    dict(id=6, name="Hardware refresh deferred", op=1.29, cure=1.29, support=0, irr=11.8, receipts=59.4,
         ds=16.4, cash=9.2, below=0, peak=0, equity=7560, dist=11790),
    dict(id=7, name="Interest rate plus 200bp", op=1.22, cure=1.25, support=90, irr=11.3, receipts=59.4,
         ds=17.1, cash=8.6, below=0, peak=90, equity=7650, dist=11700),
    dict(id=8, name="Customer payment term extension", op=0.84, cure=1.25, support=180, irr=11.6, receipts=59.4,
         ds=16.4, cash=9.5, below=0, peak=180, equity=7740, dist=11880),
]
CASES6 = CASES + EXTRA_CASES
DEBT_HEADER = ["Case", "Total interest (USD m)", "Total principal (USD m)", "Agent fees (USD k)"]
CASH_HEADER = ["Case", "Minimum cash balance (USD m)", "Month of minimum", "Closing cash 31 Dec 2031 (USD m)"]
RECEIPTS_HEADER = ["Case", "Fixed consideration (USD m)", "Usage receipts (USD m)", "Total service receipts (USD m)"]
TESTS_HEADER = ["Case", "Months tested", "Months below 1.25x before cure", "Months below 1.25x after cure"]
CURE_HEADER = ["Case", "Cure months", "Cure amount (USD k)", "Remaining lifetime cap (USD k)"]


def debt_rows(cases):
    return [[c["name"], round(c["ds"] - 14.0 - 0.18, 1), 14.0, 180] for c in cases]


def cash_rows(cases):
    return [[c["name"], round(min(c["cash"], 2.4 - 0.1 * c["id"]), 1), 3 + c["id"], c["cash"]] for c in cases]


def receipts_rows(cases):
    return [[c["name"], 36.0, round(c["receipts"] - 36.0, 1), c["receipts"]] for c in cases]


def tests_rows(cases):
    before = {1: 0, 2: 1, 3: 6, 4: 2, 5: 0, 6: 0, 7: 1, 8: 1}
    return [[c["name"], 34, before[c["id"]], c["below"]] for c in cases]


def cure_rows(cases):
    months = {1: 0, 2: 2, 3: 4, 4: 2, 5: 0, 6: 0, 7: 1, 8: 1}
    return [[c["name"], months[c["id"]], c["support"], LIFETIME_CAP_K - c["support"]] for c in cases]


SCALE_SCHEDULES = [
    # (tab/slide name, header, rows fn, formats)
    ("DSCR summary", DSCR_HEADER, lambda cs: [[c["name"], c["op"], c["cure"], c["below"]] for c in cs], None),
    ("Support cap", SUPPORT_HEADER, None, None),
    ("Sponsor return", RETURN_HEADER, lambda cs: [[c["name"], c["equity"], c["dist"], c["irr"]] for c in cs], None),
    ("Debt service", DEBT_HEADER, debt_rows, None),
    ("Closing cash", CASH_HEADER, cash_rows, None),
    ("Receipts", RECEIPTS_HEADER, receipts_rows, None),
    ("Covenant tests", TESTS_HEADER, tests_rows, None),
    ("Equity cure", CURE_HEADER, cure_rows, None),
]

REFERENCE_TITLE = "Layout reference: Case card"
REFERENCE_FOOTER = "Reference slide. Duplicate this layout for new case slides. Do not edit this slide."
CASE_FOOTER = "Source: model_outputs.xlsx, tab 'Case summary'"


def build_deck(path, instance):
    scale = instance in SCALE_INSTANCES
    cases = CASES6 if scale else CASES
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    L = {l.name: l for l in prs.slide_layouts}
    case_layout = clone_layout(prs, L["Title Only"], "Case card")
    sched_layout = clone_layout(prs, L["Title Only"], "Schedule")

    # 1 Title
    s = prs.slides.add_slide(L["Title Slide"])
    s.shapes.title.text = "Northstar Compute: hardware financing and customer arrangements"
    s.placeholders[1].text = "Investment committee pack. Fictional illustrative figures."
    set_notes(s, "Investment committee pack for the Northstar Compute GPU infrastructure financing.")

    # 2 Agenda
    s = prs.slides.add_slide(L["Title and Content"])
    s.shapes.title.text = "Agenda"
    if scale:
        fill_body(s, [
            ("1. Executive summary", 0),
            ("2. Key assumptions and risks", 0),
            ("3. Transaction timeline", 0),
            ("4. Cases", 0),
        ] + [(f"Case {c['id']} — {c['name']}", 1) for c in cases] + [
            ("5. Financing and covenant", 0),
            ("6. Recommendation", 0),
            ("7. Closing", 0),
            ("Appendix: supporting schedules", 0),
        ], sizes=(14, 12))
    else:
        fill_body(s, [
            ("1. Executive summary", 0),
            ("2. Cases", 0),
            ("Case 1 — Base", 1),
            ("Case 2 — Delayed usage receipt", 1),
            ("Case 3 — Major operating incident", 1),
            ("3. Financing and covenant", 0),
            ("4. Recommendation", 0),
            ("5. Closing", 0),
            ("Appendix: supporting schedules", 0),
        ])
    foot = RULES[instance]["text"] if instance in AGENDA_RULE_INSTANCES else NEUTRAL["agenda_footnote"]
    fb = add_textbox(s, Inches(0.5), Inches(6.6), Inches(9.0), Inches(0.6), foot, size=10)
    fb.name = "Agenda footnote"
    set_notes(s, "Walk through the agenda briefly. The case list mirrors the order of the case slides in the deck.")

    # 3 Executive summary
    content_slide(prs, L["Title and Content"], "Executive summary", [
        "Helix Research anchor contract and USD 20.0m hardware financing commence 1 January 2028.",
        "Base case meets the 1.25x monthly DSCR covenant in every tested month without sponsor support.",
        "Delayed usage receipt needs USD 320k of sponsor support over two months; the cure restores the covenant.",
        "Major operating incident exhausts the USD 1.0m support cap and leaves an unresolved breach.",
        "Sponsor IRR ranges from 10.4% to 12.1% across the funded cases.",
    ], "Headline messages. Figures are fictional illustrative model outputs.")

    if scale:
        content_slide(prs, L["Title and Content"], "Key assumptions", [
            "Anchor contract: Helix Research, 36 months from 1 January 2028, fixed consideration USD 36.0m.",
            "Usage receipts: metered monthly, invoiced in arrears, 30-day terms.",
            "Hardware: USD 20.0m purchased on signing; refresh assumed at month 30 unless deferred.",
            "Financing: USD 14.0m lender advance at 10% cash interest, 36 equal principal instalments from month 3.",
            "Sponsor support: USD 250k monthly cap and USD 1.0m lifetime cap, counted as an equity cure.",
        ], "Assumptions common to every case.")
        content_slide(prs, L["Title and Content"], "Key risks", [
            "Usage shortfall or late usage receipts tighten the monthly DSCR in the affected months.",
            "An operating incident exceeding the support cap leaves an unresolved covenant breach.",
            "Renewal without credit transfer lowers receipts from month 37 onward.",
            "A 200bp rise in the interest rate raises debt service by about USD 0.7m over the term.",
        ], "Risks ranked by covenant impact.")
        content_slide(prs, L["Title and Content"], "Transaction timeline", [
            "Signing and funding: 1 January 2028.",
            "First covenant test: forecast month 3 (March 2028).",
            "Hardware refresh decision: month 30 (June 2030).",
            "Renewal decision with Helix Research: month 34 (October 2030).",
            "Final principal instalment and model horizon: 31 December 2031.",
        ], "Key dates for the committee.")

    # Section: Cases
    body = RULES["i1_case4"]["text"] if instance == "i1_case4" else NEUTRAL["cases_body"]
    section_slide(prs, L["Section Header"], "Cases", body,
                  ("All eight modelled cases are presented in this version of the deck." if scale else
                   "Three of the four modelled cases are presented in this version of the deck."))

    # Case cards
    for c in (cases if scale else cases[:3]):
        tiles, rows = card_values(c)
        case_card(prs, case_layout, f"Case {c['id']} — {c['name']}", tiles, rows, CASE_FOOTER,
                  f"Case {c['id']} headline metrics from the Case summary tab.")

    # Section: Financing and covenant
    fin_notes = RULES[instance]["text"] if instance in FINANCING_NOTES_RULE_INSTANCES else NEUTRAL["financing_notes"]
    section_slide(prs, L["Section Header"], "Financing and covenant",
                  "Facility terms, covenant performance and sponsor support across the presented cases.", fin_notes)

    # Covenant
    content_slide(prs, L["Title and Content"], "Covenant: monthly DSCR and sponsor support", [
        "Minimum monthly cash DSCR of 1.25x, tested from forecast month 3 in each month with debt service.",
        "Sponsor support: USD 250k monthly cap and USD 1.0m lifetime cap; the covenant portion counts as a "
        "current-month equity cure.",
        "Base case minimum operating DSCR 1.31x. Delayed receipt falls to 0.62x in the delayed month and is "
        "cured to 1.25x.",
        "Operating incident: the covenant breach is unresolved once the lifetime cap is exhausted.",
    ], "Covenant mechanics and results. Operating ratio and post-cure ratio are shown separately on the case cards.")

    # Funding
    content_slide(prs, L["Title and Content"], "Funding: sources and uses", [
        "Uses: new hardware USD 20.0m, paid on signing on 1 January 2028.",
        "Sources: lender advance USD 14.0m (70%) and sponsor hardware equity USD 6.0m (30%), both on 1 January 2028.",
        "Customer advance of USD 10.8m (30% of initial fixed consideration) is unrestricted operating cash and "
        "is excluded from the covenant numerator at receipt.",
        "Debt: 10% annual cash interest, 36 equal principal instalments from month 3, USD 15k quarter-end agent fee.",
    ], "Sources and uses on the funding date.")

    # Recommendation
    content_slide(prs, L["Title and Content"], "Recommendation", [
        "Proceed with the hardware financing under the signed terms and the base-case credit designation.",
        "Retain the committed sponsor support of USD 1.0m for the delayed-receipt case.",
        "Do not present the operating-incident case as an achievable sponsor return; its shortfall is unfunded.",
        "Confirm the renewal credit-transfer position with Helix Research before the renewal is signed.",
    ], "Recommendation to the committee.")

    # Closing
    content_slide(prs, L["Title and Content"], "Closing", [
        "Decisions requested: approve the financing; approve the support commitment; note the incident-case exposure.",
        "Next steps: lender confirmation of the covenant definitions; renewal clause confirmation with Helix Research.",
    ], "Close with the decisions requested and next steps.")

    # Section: Appendix
    notes = RULES[instance]["text"] if instance in APPENDIX_NOTES_RULE_INSTANCES else NEUTRAL["appendix_notes"]
    section_slide(prs, L["Section Header"], "Appendix", "Supporting schedules drawn from model_outputs.xlsx.", notes)

    # Schedules
    if scale:
        fmts = {
            "DSCR summary": [None, fmt_x, fmt_x, fmt_int],
            "Support cap": [None, fmt_int, fmt_int, fmt_pct],
            "Sponsor return": [None, fmt_int, fmt_int, fmt_pct],
            "Debt service": [None, fmt_m, fmt_m, fmt_int],
            "Closing cash": [None, fmt_m, fmt_int, fmt_m],
            "Receipts": [None, fmt_m, fmt_m, fmt_m],
            "Covenant tests": [None, fmt_int, fmt_int, fmt_int],
            "Equity cure": [None, fmt_int, fmt_int, fmt_int],
        }
        for name, header, rows_fn, _ in SCALE_SCHEDULES:
            rows = support_rows(cases) if name == "Support cap" else rows_fn(cases)
            schedule_slide(prs, sched_layout, f"Appendix: {name}", header, rows,
                           f"Source: model_outputs.xlsx, tab '{name}'", f"{name} schedule per case.", fmts[name])
    else:
        schedule_slide(prs, sched_layout, "Appendix: DSCR summary", DSCR_HEADER, dscr_rows(),
                       "Source: model_outputs.xlsx, tab 'DSCR summary'", "DSCR schedule per case.",
                       [None, fmt_x, fmt_x, fmt_int])
        schedule_slide(prs, sched_layout, "Appendix: Sponsor return", RETURN_HEADER, return_rows(),
                       "Source: model_outputs.xlsx, tab 'Sponsor return'", "Sponsor return schedule per case.",
                       [None, fmt_int, fmt_int, fmt_pct])

    # Reference slide (last)
    case_card(prs, case_layout, REFERENCE_TITLE, ["[Fill]"] * 4, ["[Fill]"] * 3, REFERENCE_FOOTER,
              "Locked reference slide. Keep it as the last slide of the deck.")

    prs.save(path)


# --------------------------------------------------------------------------------------
# Briefs and expected specs
# --------------------------------------------------------------------------------------
BASE_TITLES = [
    "Northstar Compute: hardware financing and customer arrangements",
    "Agenda",
    "Executive summary",
    "Cases",
    "Case 1 — Base",
    "Case 2 — Delayed usage receipt",
    "Case 3 — Major operating incident",
    "Financing and covenant",
    "Covenant: monthly DSCR and sponsor support",
    "Funding: sources and uses",
    "Recommendation",
    "Closing",
    "Appendix",
    "Appendix: DSCR summary",
    "Appendix: Sponsor return",
    REFERENCE_TITLE,
]
SCALE_TITLES = [
    "Northstar Compute: hardware financing and customer arrangements",
    "Agenda",
    "Executive summary",
    "Key assumptions",
    "Key risks",
    "Transaction timeline",
    "Cases",
] + [f"Case {c['id']} — {c['name']}" for c in CASES6] + [
    "Financing and covenant",
    "Covenant: monthly DSCR and sponsor support",
    "Funding: sources and uses",
    "Recommendation",
    "Closing",
    "Appendix",
] + [f"Appendix: {name}" for name, _, _, _ in SCALE_SCHEDULES] + [REFERENCE_TITLE]


def base_titles(instance):
    return list(SCALE_TITLES if instance in SCALE_INSTANCES else BASE_TITLES)


ANCHORS = {
    "i1_case4": "Place it with the other case slides, before the \"Financing and covenant\" divider.",
    "i2_schedule": "Place it in the appendix, before the \"Layout reference: Case card\" slide.",
    "i3_sensitivity": "Place it in the financing section, before the Recommendation slide.",
}
PLACEMENT_LINES = {
    "i1_case4": "4. Place it with the other case slides.",
    "i2_schedule": "4. Place it in the appendix.",
    "i3_sensitivity": "4. Place it in the financing section.",
}
# v2 anchor: strong, literal, true under the correct answer, and not readable as "immediately before".
ANCHOR_V2 = ("Place it in the financing section, ahead of the Recommendation slide (that is, anywhere between the "
             "\"Financing and covenant\" divider and the Recommendation slide).")

COMMON_TAIL = ("\n\nSave the result in place as `inputs/ic_deck_base.pptx` (same filename). "
               "Work only with the files in this directory.\n")

CASE4_BRIEF = """# Brief: add the Case 4 slide

The investment committee deck `inputs/ic_deck_base.pptx` presents three of the four Northstar Compute cases.
The frozen model outputs for all four cases are in `inputs/model_outputs.xlsx` (read-only reference data;
do not recalculate anything).

Add a slide for Case 4, "Renewal without credit transfer":

1. Build it by duplicating the Case card layout (see the last slide, "Layout reference: Case card").
   The new slide must have the same structure as the existing case slides.
2. Title it exactly: `Case 4 — Renewal without credit transfer`.
3. Fill the four metric tiles and the three table rows from the `Case summary` tab of the workbook,
   using the same labels, units and number formats as the existing case slides. Replace the reference
   note at the bottom with the same source line the other case slides use.
4. Place it with the other case slides.
5. Update the agenda so that it lists Case 4 with the other cases.
6. Leave the "Layout reference: Case card" slide unchanged, and do not change any other slide."""

SCHEDULE_BRIEF = """# Brief: add the support-cap schedule

The investment committee deck `inputs/ic_deck_base.pptx` has an appendix of supporting schedules drawn from
the frozen workbook `inputs/model_outputs.xlsx` (read-only reference data; do not recalculate anything).

Add an appendix schedule for sponsor support-cap utilisation:

1. Build it by duplicating the schedule layout used by the existing appendix schedule slides
   (slide layout "Schedule": a title, one 5-row by 4-column table and a source line). The new slide must
   have the same structure as the existing schedule slides.
2. Title it exactly: `Appendix: Support-cap utilisation`.
3. Fill the table from the `Support cap` tab of the workbook: the workbook column headings as the header row,
   one row per case in workbook order, using the same number formats as the existing schedules
   (USD k values as whole numbers, percentages with one decimal and a % sign). Use a source line in the same
   style as the other schedules, naming the `Support cap` tab.
4. Place it in the appendix.
5. Leave the "Layout reference: Case card" slide unchanged, and do not change any other slide."""

SENSITIVITY_BRIEF = """# Brief: add the DSCR sensitivity slide

The investment committee deck `inputs/ic_deck_base.pptx` presents the Northstar Compute cases and the
covenant analysis. The frozen workbook `inputs/model_outputs.xlsx` (read-only reference data; do not
recalculate anything) contains a sensitivity of the covenant DSCR with the sponsor support cap reduced by 20%.

Add a sensitivity slide for the covenant DSCR with the support cap minus 20%:

1. Build it by duplicating the Case card layout (see the last slide, "Layout reference: Case card").
   The new slide must have the same structure as the existing case slides.
2. Title it exactly: `Sensitivity: DSCR with support cap minus 20%`.
3. Fill the four metric tiles and the three table rows from the `Sensitivity` tab of the workbook,
   using the same labels, units and number formats as the existing case slides. Replace the reference
   note at the bottom with a source line in the same style naming the `Sensitivity` tab.
4. Place it in the financing section.
5. Leave the "Layout reference: Case card" slide unchanged, and do not change any other slide."""

SENSITIVITY_ANCHOR_BRIEF = SENSITIVITY_BRIEF.replace(PLACEMENT_LINES["i3_sensitivity"], "4. " + ANCHOR_V2)
assert SENSITIVITY_ANCHOR_BRIEF != SENSITIVITY_BRIEF

SENS_SPEC = dict(title="Sensitivity: DSCR with support cap minus 20%",
                 insert_after="Covenant: monthly DSCR and sponsor support",
                 literal_after="Funding: sources and uses",
                 template=REFERENCE_TITLE, allowed_to_change=[])

BRIEFS = {
    "i1_case4": {
        "title": "Case 4 — Renewal without credit transfer",
        "insert_after": "Case 1 — Base",
        "literal_after": "Case 3 — Major operating incident",
        "template": REFERENCE_TITLE,
        "allowed_to_change": ["Agenda"],
        "brief": CASE4_BRIEF,
    },
    "i2_schedule": {
        "title": "Appendix: Support-cap utilisation",
        "insert_after": "Appendix: DSCR summary",
        "literal_after": "Appendix: Sponsor return",
        "template": "Appendix: DSCR summary",
        "allowed_to_change": [],
        "brief": SCHEDULE_BRIEF,
    },
    "i3_sensitivity": dict(SENS_SPEC, brief=SENSITIVITY_BRIEF),
    # ---- v2 ----
    "i2b_schedule_first": {
        "title": "Appendix: Support-cap utilisation",
        "insert_after": "Appendix",                       # directly after the divider, ahead of DSCR summary
        "literal_after": "Appendix: Sponsor return",      # append at the end of the appendix
        "decoy_after": "Appendix: DSCR summary",          # workbook tab order (the v1 I2 answer): now wrong
        "template": "Appendix: DSCR summary",
        "allowed_to_change": [],
        "brief": SCHEDULE_BRIEF,
    },
    "i4_sensitivity_anchor": dict(SENS_SPEC, brief=SENSITIVITY_ANCHOR_BRIEF),
    "i5_sensitivity_notes_anchor": dict(SENS_SPEC, brief=SENSITIVITY_ANCHOR_BRIEF),
    "i6_sensitivity_scale": dict(SENS_SPEC, brief=SENSITIVITY_ANCHOR_BRIEF),
}


def order_with(instance, after_key):
    spec = BRIEFS[instance]
    order = base_titles(instance)
    order.insert(order.index(spec[after_key]) + 1, spec["title"])
    return order


def expected_order(instance):
    return order_with(instance, "insert_after")


def literal_order(instance):
    return order_with(instance, "literal_after")


def expected_values(instance):
    if instance == "i1_case4":
        c = CASES[3]
        return {"kind": "card",
                "tiles": [{"label": l, "value": v} for l, v in zip(TILE_LABELS, [c["op"], c["cure"], c["support"], c["irr"]])],
                "table_rows": [{"label": l, "value": v} for l, v in zip(TABLE_LABELS, [c["receipts"], c["ds"], c["cash"]])],
                "table_dims": [4, 2]}
    if instance in ("i3_sensitivity", "i4_sensitivity_anchor", "i5_sensitivity_notes_anchor", "i6_sensitivity_scale"):
        c = SENSITIVITY
        return {"kind": "card",
                "tiles": [{"label": l, "value": v} for l, v in zip(TILE_LABELS, [c["op"], c["cure"], c["support"], c["irr"]])],
                "table_rows": [{"label": l, "value": v} for l, v in zip(TABLE_LABELS, [c["receipts"], c["ds"], c["cash"]])],
                "table_dims": [4, 2]}
    if instance in ("i2_schedule", "i2b_schedule_first"):
        return {"kind": "schedule", "header": SUPPORT_HEADER, "rows": support_rows(), "table_dims": [5, 4]}
    raise ValueError(instance)


def control_sentence(instance):
    rule = RULES[instance]
    if instance in V1_INSTANCES:
        return "\n\nDeck convention (stated in the " + rule["location"] + "): " + rule["text"]
    return ("\n\nNote the convention stated in the " + rule["location"] + " of the deck: \"" + rule["text"] +
            "\" Apply it when placing the new slide.")


def write_instance(root, instance):
    inst_dir = os.path.join(root, instance)
    if os.path.exists(inst_dir):
        shutil.rmtree(inst_dir)
    os.makedirs(os.path.join(inst_dir, "inputs"))
    os.makedirs(os.path.join(inst_dir, "expected"))
    build_workbook(os.path.join(inst_dir, "inputs", "model_outputs.xlsx"), scale=instance in SCALE_INSTANCES)
    build_deck(os.path.join(inst_dir, "inputs", "ic_deck_base.pptx"), instance)

    spec = BRIEFS[instance]
    rule = RULES[instance]
    with open(os.path.join(inst_dir, "brief.md"), "w") as f:
        f.write(spec["brief"] + COMMON_TAIL)
    with open(os.path.join(inst_dir, "brief_control.md"), "w") as f:
        f.write(spec["brief"] + control_sentence(instance) + COMMON_TAIL)
    if instance in V1_INSTANCES:
        # anchor variant: same brief, placement sentence carries a stronger (still true) literal anchor
        assert PLACEMENT_LINES[instance] in spec["brief"]
        with open(os.path.join(inst_dir, "brief_anchor.md"), "w") as f:
            f.write(spec["brief"].replace(PLACEMENT_LINES[instance], "4. " + ANCHORS[instance]) + COMMON_TAIL)
    agenda = None
    if instance == "i1_case4":
        agenda = {"case_labels_order": ["Case 1", "Case 4", "Case 2", "Case 3"],
                  "must_contain": ["Renewal without credit transfer"]}
    expected = {
        "instance": instance,
        "new_slide_title": spec["title"],
        "expected_title_order": expected_order(instance),
        "expected_new_slide_index": expected_order(instance).index(spec["title"]),
        "literal_placement_title_order": literal_order(instance),
        "structure_template_title": spec["template"],
        "reference_title": REFERENCE_TITLE,
        "slides_allowed_to_change": spec["allowed_to_change"],
        "agenda_check": agenda,
        "values": expected_values(instance),
        "forbidden_text_on_new_slide": ["[Fill]", "Do not edit this slide", "Reference slide"],
        "rule_location": rule["location"],
        "rule_text": rule["text"],
    }
    if "decoy_after" in spec:
        expected["decoy_placement_title_order"] = order_with(instance, "decoy_after")
        expected["decoy_placement_description"] = "workbook tab order (between DSCR summary and Sponsor return)"
    with open(os.path.join(inst_dir, "expected", "spec.json"), "w") as f:
        json.dump(expected, f, indent=2, ensure_ascii=False)
    with open(os.path.join(inst_dir, "expected", "expected_order.txt"), "w") as f:
        f.write("\n".join(f"{i + 1:2d}. {t}" for i, t in enumerate(expected_order(instance))) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "instances"))
    ap.add_argument("--instances", default=",".join(BRIEFS), help="comma-separated subset to (re)build")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    for inst in args.instances.split(","):
        write_instance(args.out, inst)
        print("built", inst)


if __name__ == "__main__":
    main()
