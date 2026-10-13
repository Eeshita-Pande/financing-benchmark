# Brief: add the DSCR sensitivity slide

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
5. Leave the "Layout reference: Case card" slide unchanged, and do not change any other slide.

Deck convention (stated in the footnote text box on the 'Agenda' slide): Deck conventions: Recommendation always immediately precedes Closing; a sensitivity slide is placed directly after the slide it sensitises.

Save the result in place as `inputs/ic_deck_base.pptx` (same filename). Work only with the files in this directory.
