# Brief: add the support-cap schedule

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
5. Leave the "Layout reference: Case card" slide unchanged, and do not change any other slide.

Save the result in place as `inputs/ic_deck_base.pptx` (same filename). Work only with the files in this directory.
