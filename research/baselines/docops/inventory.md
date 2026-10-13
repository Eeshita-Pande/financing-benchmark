# DocOps task inventory (210 tasks)

Generated from `tasks/*/task.toml` and `tests/task_metadata.json` of icip-cas/DocOps (commit ccf7a75). Level is `metadata.final_difficulty` or the prefix of `difficulty_level`. Format is `doc_type` from the task metadata. Outputs is the number of deliverable files the verifier checks.

## Counts by level and format

| level | format(s) | tasks |
|---|---|---|
| L1 | docx | 12 |
| L1 | pdf | 12 |
| L1 | pptx | 12 |
| L1 | xlsx | 14 |
| L2 | docx | 10 |
| L2 | pdf | 10 |
| L2 | pptx | 10 |
| L2 | xlsx | 10 |
| L3 | docx | 15 |
| L3 | pdf | 15 |
| L3 | pptx | 15 |
| L3 | xlsx | 15 |
| L4 | docx | 5 |
| L4 | docx+pdf | 2 |
| L4 | docx+pdf+xlsx | 1 |
| L4 | docx+pptx | 1 |
| L4 | docx+xlsx | 14 |
| L4 | pdf | 6 |
| L4 | pdf+docx | 2 |
| L4 | pdf+docx+xlsx | 2 |
| L4 | pdf+xlsx | 4 |
| L4 | pdf+xlsx+docx | 2 |
| L4 | pptx | 5 |
| L4 | pptx+docx | 1 |
| L4 | pptx+pdf | 1 |
| L4 | pptx+xlsx | 5 |
| L4 | xlsx | 6 |
| L4 | xlsx+pdf | 2 |
| L4 | xlsx+pptx | 1 |

## All tasks

| # | task | level | format(s) | outputs | summary |
|---|---|---|---|---|---|
| 1 | `atomic__excel_001_budget_bucket_totals_seed` | L1 | xlsx | 1 | This workbook tracks costs with a code in one column and needs totals split into Maintenance and Operations budgets. |
| 2 | `atomic__excel_002_last_nonblank_lookup_seed` | L1 | xlsx | 1 | This workbook stores monthly values by year and product, with many blanks. The user wants one result cell that returns the latest availab... |
| 3 | `atomic__excel_003_risk_highlighting_seed` | L1 | xlsx | 1 | This tracker sheet has risk scores, but urgent items do not stand out visually. |
| 4 | `atomic__excel_004_project_sheet_structure_seed` | L1 | xlsx | 1 | This workbook has multiple project sheets with the same task-table structure, but each one is missing a `Priority` column. |
| 5 | `atomic__excel_005_summary_conflict_reasoning_seed` | L1 | xlsx | 1 | This workbook contains a short summary sheet that may not match the actual regional performance data. |
| 6 | `atomic__excel_006_summary_generation_seed` | L1 | xlsx | 1 | This workbook has a raw incident log and a request for a concise executive summary sheet. |
| 7 | `atomic__excel_007_exception_credit_extraction_seed` | L1 | xlsx | 1 | This workbook contains an exception tracker plus an unstructured email trail with superseded values. |
| 8 | `atomic__excel_008_client_update_editing_seed` | L1 | xlsx | 1 | This workbook contains a draft client-facing status note that is too blunt for external communication. |
| 9 | `atomic__excel_009_body_style_consistency_seed` | L1 | xlsx | 1 | This workbook contains a candidate table where the body rows use inconsistent fonts, emphasis, and fills. |
| 10 | `atomic__excel_010_print_layout_control_seed` | L1 | xlsx | 1 | This workbook contains a weekly planning sheet that is readable on screen but poorly configured for print layout. |
| 11 | `atomic__excel_011_theme_transfer_seed` | L1 | xlsx | 1 | This workbook has three operational tabs with inconsistent accent colors and no shared visual theme. |
| 12 | `atomic__excel_012_archive_sheet_delete_seed` | L1 | xlsx | 1 | This workbook contains one obsolete sheet that should no longer be present in the deliverable. |
| 13 | `atomic__excel_013_workbook_reorder_seed` | L1 | xlsx | 1 | This workbook contains the right worksheets but they are arranged in an inconvenient order. |
| 14 | `atomic__excel_014_outline_hierarchy_seed` | L1 | xlsx | 1 | This workbook contains a flat program outline that has section rows and detail rows, but no usable hierarchy in Excel's outline structure. |
| 15 | `atomic__pdf_001_vendor_quote_extraction_seed` | L1 | pdf | 1 | This vendor quote PDF contains key commercial details in a messy, semi-structured layout. |
| 16 | `atomic__pdf_002_contract_conflict_reasoning_seed` | L1 | pdf | 1 | This contract excerpt contains payment clauses and schedule notes that may not agree with each other. |
| 17 | `atomic__pdf_003_budget_lines_highlighting_seed` | L1 | pdf | 1 | This approval sheet contains several spend lines, but only some should be visually emphasized for review. |
| 18 | `atomic__pdf_004_audit_pages_reorder_seed` | L1 | pdf | 1 | This audit PDF contains the right pages but in the wrong sequence. |
| 19 | `atomic__pdf_005_paragraph_editing_seed` | L1 | pdf | 1 | This PDF contains a client-facing draft where one paragraph is too blunt for external use. |
| 20 | `atomic__pdf_006_management_summary_generation_seed` | L1 | pdf | 1 | This PDF contains raw operational findings plus an empty management summary area. |
| 21 | `atomic__pdf_007_body_style_consistency_seed` | L1 | pdf | 1 | This PDF brief has consistent section labels but inconsistent body-paragraph styling. |
| 22 | `atomic__pdf_008_milestone_layout_control_seed` | L1 | pdf | 1 | This PDF contains three milestone callout boxes that are visually misaligned even though their content is correct. |
| 23 | `atomic__pdf_009_theme_transfer_seed` | L1 | pdf | 1 | This PDF proposal uses inconsistent accent colors across pages and callout elements. |
| 24 | `atomic__pdf_010_appendix_delete_seed` | L1 | pdf | 1 | This PDF packet contains one obsolete appendix page that should not be part of the final document. |
| 25 | `atomic__pdf_011_outline_hierarchy_seed` | L1 | pdf | 1 | This PDF already has bookmarks, but the bookmark hierarchy does not match the section structure of the document. |
| 26 | `atomic__pdf_012_table_structure_seed` | L1 | pdf | 1 | This PDF contains a structured table where one column incorrectly combines two logical fields. |
| 27 | `atomic__ppt_001_generate_risk_points_seed` | L1 | pptx | 1 | The second slide is only a placeholder, but the first slide already contains enough context to draft operational risk points. |
| 28 | `atomic__ppt_002_alignment_layout_seed` | L1 | pptx | 1 | This slide contains three content cards that are obviously misaligned and unevenly distributed. |
| 29 | `atomic__ppt_003_theme_transfer_seed` | L1 | pptx | 1 | This deck was assembled from mismatched slides and needs a consistent visual theme. |
| 30 | `atomic__ppt_004_slide_reorder_seed` | L1 | pptx | 1 | The deck's slides are out of logical order. |
| 31 | `atomic__ppt_005_table_structure_seed` | L1 | pptx | 1 | This slide contains a milestone table, but the table is missing an `Owner` column. |
| 32 | `atomic__ppt_006_delete_outdated_slide_seed` | L1 | pptx | 1 | This deck still contains one outdated appendix slide from a previous reporting cycle. |
| 33 | `atomic__ppt_007_cross_slide_extraction_seed` | L1 | pptx | 1 | This deck contains multiple mentions of dates and owners, but some values were later corrected. |
| 34 | `atomic__ppt_008_bullet_editing_seed` | L1 | pptx | 1 | This client-facing slide contains bullets that are too blunt and emotionally charged. |
| 35 | `atomic__ppt_009_metric_conflict_reasoning_seed` | L1 | pptx | 1 | This deck contains KPI commentary that may not be internally consistent. |
| 36 | `atomic__ppt_010_style_consistency_seed` | L1 | pptx | 1 | This deck feels visually inconsistent from slide to slide. |
| 37 | `atomic__ppt_011_highlight_key_item_seed` | L1 | pptx | 1 | This milestone slide contains one explicitly critical item that should stand out more clearly. |
| 38 | `atomic__ppt_012_outline_hierarchy_seed` | L1 | pptx | 1 | This slide outline has the wrong bullet hierarchy: some items that should be sub-points are currently at the top level. |
| 39 | `atomic__word_001_engineering_report_toc_hierarchy_seed` | L1 | docx | 1 | This engineering report draft has a broken heading hierarchy and a manually typed table of contents. |
| 40 | `atomic__word_002_resume_blank_first_page_seed` | L1 | docx | 1 | This resume document opens with an unwanted blank first page before the actual content begins. |
| 41 | `atomic__word_003_client_letter_editing_seed` | L1 | docx | 1 | This client communication draft contains rushed, overly blunt wording in the message body. |
| 42 | `atomic__word_004_transcript_style_consistency_seed` | L1 | docx | 1 | This transcript packet was assembled from multiple contributors and now has visibly inconsistent formatting. |
| 43 | `atomic__word_005_meeting_minutes_extraction_seed` | L1 | docx | 1 | This meeting-minutes draft contains several proposed dates and ownership notes, but some were superseded later in the document. |
| 44 | `atomic__word_006_section_reorder_seed` | L1 | docx | 1 | This report draft has major sections in the wrong order. |
| 45 | `atomic__word_007_summary_generation_seed` | L1 | docx | 1 | This briefing document has context notes but the executive summary section is still only a placeholder. |
| 46 | `atomic__word_008_policy_conflict_reasoning_seed` | L1 | docx | 1 | This memo draft contains procedural statements that may not all be compatible with one another. |
| 47 | `atomic__word_009_clause_highlighting_seed` | L1 | docx | 1 | This review note document contains several clauses, but only some are marked as critical. |
| 48 | `atomic__word_010_image_layout_seed` | L1 | docx | 1 | This document contains three site images, but they are not laid out cleanly. |
| 49 | `atomic__word_011_theme_transfer_seed` | L1 | docx | 1 | This document was assembled from mismatched source files and now looks visually inconsistent. |
| 50 | `atomic__word_012_table_structure_seed` | L1 | docx | 1 | This inspection table is missing a Status column. |
| 51 | `composite_same_type__excelc_001_ops_note_repair_and_evidence_highlight_seed` | L2 | xlsx | 1 | This workbook contains an inaccurate ops-summary note that should be corrected and visually supported with evidence. |
| 52 | `composite_same_type__excelc_002_priority_formula_and_theme_refresh_seed` | L2 | xlsx | 1 | This tracker workbook needs a computed priority column and a coherent navy-and-steel visual treatment. |
| 53 | `composite_same_type__excelc_003_workbook_reorder_then_exec_summary_seed` | L2 | xlsx | 1 | This workbook should follow an executive review order and include a tightly constrained summary sheet. |
| 54 | `composite_same_type__excelc_004_outline_and_print_ready_program_plan_seed` | L2 | xlsx | 1 | This program plan should become collapsible and print cleanly on a single landscape page. |
| 55 | `composite_same_type__excelc_005_extract_credit_amount_and_highlight_source_seed` | L2 | xlsx | 1 | This credit workbook needs the final approved amount surfaced and the source decision row highlighted. |
| 56 | `composite_same_type__excelc_006_formalize_update_and_match_body_style_seed` | L2 | xlsx | 1 | This client update sheet has one risky draft sentence and inconsistent nearby body formatting. |
| 57 | `composite_same_type__excelc_007_delete_archive_and_generate_cover_note_seed` | L2 | xlsx | 1 | This workbook still contains an obsolete archive sheet and needs a concise cover note for reviewers. |
| 58 | `composite_same_type__excelc_008_reorder_tabs_and_apply_review_theme_seed` | L2 | xlsx | 1 | This review pack should follow a clean tab order and use a cohesive blue theme. |
| 59 | `composite_same_type__excelc_009_insert_owner_column_from_lookup_seed` | L2 | xlsx | 1 | This milestone plan is missing owners that can be recovered from a lookup sheet. |
| 60 | `composite_same_type__excelc_010_compute_risk_flag_and_highlight_rows_seed` | L2 | xlsx | 1 | This tracker needs a computed risk flag and visible emphasis on the flagged items. |
| 61 | `composite_same_type__pdfc_001_payment_conflict_highlight_seed` | L2 | pdf | 1 | This contract excerpt contains a payment-timing conflict that should be highlighted for review. |
| 62 | `composite_same_type__pdfc_002_reorder_pages_and_rebuild_bookmarks_seed` | L2 | pdf | 1 | This report is out of order and the bookmark tree should match the corrected sequence. |
| 63 | `composite_same_type__pdfc_003_fill_summary_box_and_apply_theme_seed` | L2 | pdf | 1 | This report has an empty summary box and inconsistent accent colors. |
| 64 | `composite_same_type__pdfc_004_split_owner_team_and_flag_critical_rows_seed` | L2 | pdf | 1 | This action table needs separate owner/team columns and stronger emphasis on the critical rows. |
| 65 | `composite_same_type__pdfc_005_extract_vendor_fields_into_summary_panel_seed` | L2 | pdf | 1 | This vendor packet needs a concise extracted summary panel on the cover page. |
| 66 | `composite_same_type__pdfc_006_rewrite_paragraph_and_match_body_style_seed` | L2 | pdf | 1 | This status memo contains one informal paragraph and inconsistent body styling. |
| 67 | `composite_same_type__pdfc_007_delete_superseded_page_and_refresh_theme_seed` | L2 | pdf | 1 | This report still includes a superseded page and mixed accent colors. |
| 68 | `composite_same_type__pdfc_008_reorder_pages_and_add_cover_summary_seed` | L2 | pdf | 1 | This report should be reordered and open with a concise management summary box. |
| 69 | `composite_same_type__pdfc_009_reason_and_rewrite_conflict_note_seed` | L2 | pdf | 1 | This contract note misstates the real payment conflict and needs one corrected summary sentence. |
| 70 | `composite_same_type__pdfc_010_theme_and_align_callout_boxes_seed` | L2 | pdf | 1 | This one-page PDF has mismatched accent colors and uneven callout alignment. |
| 71 | `composite_same_type__pptc_001_retheme_restyle_and_realign_seed` | L2 | pptx | 1 | This deck needs a coherent theme, consistent typography, and aligned workstream cards. |
| 72 | `composite_same_type__pptc_002_reorder_storyline_and_add_exec_summary_seed` | L2 | pptx | 1 | This deck should follow an executive story order and open with a constrained summary slide. |
| 73 | `composite_same_type__pptc_003_delay_conflict_reason_and_emphasize_seed` | L2 | pptx | 1 | This deck contains one outdated delay statement that should be visually emphasized for review. |
| 74 | `composite_same_type__pptc_004_expand_table_and_polish_draft_slide_seed` | L2 | pptx | 1 | This milestone slide needs an extra status field and executive-ready supporting bullets. |
| 75 | `composite_same_type__pptc_005_extract_launch_fields_and_emphasize_source_seed` | L2 | pptx | 1 | This deck needs the final launch date and owner surfaced on the summary slide and the source line emphasized. |
| 76 | `composite_same_type__pptc_006_rewrite_bullets_and_standardize_text_style_seed` | L2 | pptx | 1 | This status deck has rough draft bullets and inconsistent text styling. |
| 77 | `composite_same_type__pptc_007_insert_summary_slide_and_generate_bullets_seed` | L2 | pptx | 1 | This deck needs a new executive summary slide at the front. |
| 78 | `composite_same_type__pptc_008_fix_outline_and_align_cards_seed` | L2 | pptx | 1 | This workstream slide has both incorrect bullet nesting and uneven card alignment. |
| 79 | `composite_same_type__pptc_009_reorder_and_theme_governance_deck_seed` | L2 | pptx | 1 | This governance deck should follow a cleaner story order and use one navy theme. |
| 80 | `composite_same_type__pptc_010_add_owner_column_from_notes_seed` | L2 | pptx | 1 | This milestone table is missing owner values that can be recovered from the notes panel. |
| 81 | `composite_same_type__wordc_001_repair_hierarchy_and_standardize_styles_seed` | L2 | docx | 1 | This engineering report draft has both a broken heading hierarchy and inconsistent formatting. |
| 82 | `composite_same_type__wordc_002_reorder_sections_then_generate_summary_seed` | L2 | docx | 1 | This report is out of order and needs a constrained executive summary at the front. |
| 83 | `composite_same_type__wordc_003_find_conflict_and_highlight_evidence_seed` | L2 | docx | 1 | This policy note contains an approval-logic conflict that should be highlighted for legal review. |
| 84 | `composite_same_type__wordc_004_insert_status_column_and_formalize_notes_seed` | L2 | docx | 1 | This action tracker section needs a richer table and more professional notes. |
| 85 | `composite_same_type__wordc_005_extract_fields_into_cover_table_and_highlight_seed` | L2 | docx | 1 | This shutdown memo needs the key fields surfaced at the top and the source evidence highlighted below. |
| 86 | `composite_same_type__wordc_006_rewrite_letter_and_match_body_style_seed` | L2 | docx | 1 | This client letter has two rough draft sections and inconsistent body formatting. |
| 87 | `composite_same_type__wordc_007_delete_blank_page_and_generate_profile_seed` | L2 | docx | 1 | This resume opens with a blank page and lacks a concise professional profile. |
| 88 | `composite_same_type__wordc_008_reorder_sections_and_apply_blue_heading_theme_seed` | L2 | docx | 1 | This report needs both a better section sequence and a consistent blue heading theme. |
| 89 | `composite_same_type__wordc_009_insert_status_column_from_notes_seed` | L2 | docx | 1 | This action table is missing status values that are stated in the notes below it. |
| 90 | `composite_same_type__wordc_010_reason_and_rewrite_summary_note_seed` | L2 | docx | 1 | This policy summary note misstates the true approval conflict and needs to be corrected. |
| 91 | `cross_doc_docops__excelxr_001_board_action_register_from_minutes_packet_and_aliases_seed` | L4 | xlsx | 1 | Populate only the blank rows of the `Decision Register` sheet with motion ID. |
| 92 | `cross_doc_docops__excelxr_002_submittal_log_revision_and_late_days_seed` | L4 | xlsx | 1 | Update only the returned submittal rows with the new revision status and resubmit date. |
| 93 | `cross_doc_docops__excelxr_003_rfp_traceability_matrix_from_rfp_and_outline_seed` | L4 | xlsx | 1 | Fill the blank traceability matrix with the exact requirement mappings. |
| 94 | `cross_doc_docops__excelxr_004_security_questionnaire_evidence_fill_from_policy_pack_seed` | L4 | xlsx | 1 | Fill only the unanswered required controls in the questionnaire. |
| 95 | `cross_doc_docops__excelxr_005_due_diligence_folder_import_numbering_and_owners_seed` | L4 | xlsx | 1 | Convert the sectioned request list into the folder-import workbook. |
| 96 | `cross_doc_docops__pdfxr_001_board_packet_cover_appendix_refresh_and_bookmarks_seed` | L4 | pdf | 1 | Replace only the stale finance-appendix pages in the seed packet. |
| 97 | `cross_doc_docops__pdfxr_002_resubmittal_package_selective_replace_preserve_approved_pages_seed` | L4 | pdf | 1 | Replace only the superseded Sheet B pages. |
| 98 | `cross_doc_docops__pdfxr_003_due_diligence_latest_uploads_packet_and_nested_bookmarks_seed` | L4 | pdf | 1 | Insert only the latest-upload exhibits. |
| 99 | `cross_doc_docops__pdfxr_004_security_response_packet_fill_cover_and_insert_evidence_seed` | L4 | pdf | 1 | Fill the cover placeholders from the answered questionnaire. |
| 100 | `cross_doc_docops__pdfxr_005_closeout_binder_reorder_status_summary_and_tabs_seed` | L4 | pdf | 1 | Reorder the binder into the requested closeout sequence. |
| 101 | `cross_doc_docops__pptxr_001_monthly_board_pack_refresh_locked_layout_seed` | L4 | pptx | 1 | Refresh the metric tiles and action table. |
| 102 | `cross_doc_docops__pptxr_002_qbr_storyline_reorder_and_risk_callout_seed` | L4 | pptx | 1 | Reorder the storyline slides into the requested sequence. |
| 103 | `cross_doc_docops__pptxr_003_security_readout_appendix_refresh_from_questionnaire_and_evidence_seed` | L4 | pptx | 1 | Update the customer answer grid. |
| 104 | `cross_doc_docops__pptxr_004_handover_owner_matrix_from_closeout_logs_seed` | L4 | pptx | 1 | Refresh the handover metrics. |
| 105 | `cross_doc_docops__pptxr_005_public_health_briefing_template_fill_from_message_map_seed` | L4 | pptx | 1 | Fill the title and subtitle placeholders. |
| 106 | `cross_doc_docops__wordxr_001_publish_minutes_from_agenda_attendance_and_motion_log_seed` | L4 | docx | 1 | Publish the minutes by replacing placeholders under existing headings. |
| 107 | `cross_doc_docops__wordxr_002_decision_memorandum_from_minutes_packet_and_vote_log_seed` | L4 | docx | 1 | Fill the metadata table and the bounded Decision. |
| 108 | `cross_doc_docops__wordxr_003_due_diligence_exhibit_index_sectioned_appendix_seed` | L4 | docx | 1 | Create the exhibit-index hierarchy from the request list. |
| 109 | `cross_doc_docops__wordxr_004_mou_template_scope_term_and_contacts_seed` | L4 | docx | 1 | Complete the Purpose. |
| 110 | `cross_doc_docops__wordxr_005_closeout_exception_memo_from_om_index_punchlist_and_warranty_log_seed` | L4 | docx | 1 | Replace the named body sections with the correct closeout exceptions. |
| 111 | `docops_v2_l3_001_docx_controlled_document_release_repair` | L3 | docx | 1 |  |
| 112 | `docops_v2_l3_002_docx_meeting_minutes_public_repair` | L3 | docx | 1 |  |
| 113 | `docops_v2_l3_003_docx_public_records_release_metadata_cleanup` | L3 | docx | 1 |  |
| 114 | `docops_v2_l3_004_docx_public_loan_agreement_copyedit_repair` | L3 | docx | 1 |  |
| 115 | `docops_v2_l3_005_docx_resilience_playbook_release` | L3 | docx | 1 | Prepare a complex community resilience operations playbook for public release from a messy working draft. |
| 116 | `docops_v2_l3_006_docx_grant_closeout_release` | L3 | docx | 1 | Prepare a complex public grant closeout packet from a messy single Word working draft. |
| 117 | `docops_v2_l3_007_docx_museum_installation_binder_release` | L3 | docx | 1 | Prepare a complex museum exhibition installation binder from a messy single Word working draft. |
| 118 | `docops_v2_l3_008_docx_mobility_board_packet_release` | L3 | docx | 1 | Prepare a complex public mobility pilot board packet from a messy single Word working draft. |
| 119 | `docops_v2_l3_009_docx_incident_manual_publication` | L3 | docx | 1 | A draft incident response Word manual must be converted into a public release manual through a long ordered workflow. |
| 120 | `docops_v2_l3_010_docx_policy_exception_cascade` | L3 | docx | 1 | A policy manual needs exceptions extracted into tables whose counts and blocking status affect the release header and control matrix. |
| 121 | `docops_v2_l3_011_xlsx_service_recovery_closeout` | L3 | xlsx | 1 | A field-service closeout workbook needs a long, ordered release workflow from raw tickets into a release-safe dashboard, exception regist... |
| 122 | `docops_v2_l3_012_xlsx_incident_action_plan_rebuild` | L3 | xlsx | 1 | Prepare a clean public Incident Action Plan workbook for a citywide heat emergency from a messy internal planning workbook. |
| 123 | `docops_v2_l3_013_xlsx_procurement_bid_evaluation_release` | L3 | xlsx | 1 | Prepare a clean public procurement bid evaluation workbook from a messy internal evaluation workbook. |
| 124 | `docops_v2_l3_014_xlsx_disaster_housing_grant_public_release` | L3 | xlsx | 1 |  |
| 125 | `docops_v2_l3_015_xlsx_reimbursement_workbook_formula_repair` | L3 | xlsx | 1 |  |
| 126 | `docops_v2_l3_016_xlsx_forecast_driver_cascade` | L3 | xlsx | 1 | A forecast workbook needs a scenario driver that cascades through model formulas, exception review, and dashboard totals. |
| 127 | `docops_v2_l3_017_xlsx_accreditation_evidence_pack_rebuild` | L3 | xlsx | 1 | Prepare a clean accreditation evidence package workbook from a messy internal review workbook. |
| 128 | `docops_v2_l3_018_xlsx_ai_governance_inventory_release` | L3 | xlsx | 1 | Prepare a clean public AI governance inventory workbook from a messy internal AI risk review workbook. |
| 129 | `docops_v2_l3_019_xlsx_vendor_compliance_exception_register_repair` | L3 | xlsx | 1 |  |
| 130 | `docops_v2_l3_020_xlsx_month_close_over10` | L3 | xlsx | 1 | A monthly close workbook needs a release-ready summary driven by cleaned transactions and exception logic. |
| 131 | `docops_v2_l3_021_pptx_shelter_accessibility_public_remediation` | L3 | pptx | 1 |  |
| 132 | `docops_v2_l3_022_pptx_port_cyber_ttx_public_deck` | L3 | pptx | 1 | Prepare a clean public after-action briefing deck from a messy internal port cyber tabletop exercise presentation. |
| 133 | `docops_v2_l3_023_pptx_transit_board_deck_style_cleanup` | L3 | pptx | 1 | Prepare a clean public board packet deck for the HarborLink fare pilot from a messy internal working presentation. |
| 134 | `docops_v2_l3_024_pptx_hospital_evacuation_public_briefing` | L3 | pptx | 1 | Prepare a clean public briefing deck from a messy internal hospital evacuation exercise presentation. |
| 135 | `docops_v2_l3_025_pptx_ai_incident_disclosure_packet` | L3 | pptx | 1 | Prepare a clean public AI incident disclosure briefing deck from a messy internal model-review presentation. |
| 136 | `docops_v2_l3_026_pptx_climate_disclosure_chart_rebuild` | L3 | pptx | 1 |  |
| 137 | `docops_v2_l3_027_pptx_food_recall_public_briefing_repair` | L3 | pptx | 1 |  |
| 138 | `docops_v2_l3_028_pptx_lab_safety_training_deck_remediation` | L3 | pptx | 1 |  |
| 139 | `docops_v2_l3_029_pptx_qbr_release_deck` | L3 | pptx | 1 | A QBR deck must be converted from draft staging state into a release-ready presentation through a long ordered workflow. |
| 140 | `docops_v2_l3_030_pptx_webinar_over10` | L3 | pptx | 1 | A webinar deck needs agenda, quiz, notes, numbering, and locked legal content synchronized after major cleanup. |
| 141 | `docops_v2_l3_031_pdf_public_hearing_packet_flatten_release` | L3 | pdf | 1 |  |
| 142 | `docops_v2_l3_032_pdf_hazmat_field_guide_rebuild` | L3 | pdf | 1 | Prepare a clean public hazardous-materials field guide from a messy internal working PDF. |
| 143 | `docops_v2_l3_033_pdf_ev_charging_reliability_public_report` | L3 | pdf | 1 | Prepare a clean public EV charging reliability report from a messy internal network operations PDF. |
| 144 | `docops_v2_l3_034_pdf_permit_notice_packet_errata_repair` | L3 | pdf | 1 |  |
| 145 | `docops_v2_l3_035_pdf_stormwater_compliance_public_report` | L3 | pdf | 1 | Prepare a clean public stormwater compliance report from a messy internal annual-review PDF. |
| 146 | `docops_v2_l3_036_pdf_school_meal_public_audit_report` | L3 | pdf | 1 | Prepare a clean public school meal program audit report from a messy internal review PDF. |
| 147 | `docops_v2_l3_037_pdf_bus_detour_notice_layout_repair` | L3 | pdf | 1 |  |
| 148 | `docops_v2_l3_038_pdf_benefits_notice_errata_repair` | L3 | pdf | 1 |  |
| 149 | `docops_v2_l3_039_pdf_night_work_variance_hearing_repair` | L3 | pdf | 1 |  |
| 150 | `docops_v2_l3_040_pdf_grant_reimbursement_closeout_packet_repair` | L3 | pdf | 1 |  |
| 151 | `docops_v2_l4_041_docx_pdf_xlsx_podcast_caption_delivery_packet` | L4 | docx+pdf+xlsx | 3 | Create a traditional document podcast caption delivery packet from transcript, timecode log, chapter outline, style guide, and private sp... |
| 152 | `docops_v2_l4_042_excel_pdf_month_close_exception_pack` | L4 | xlsx+pdf | 2 | A monthly close workbook and matching PDF exception packet must be prepared from transaction data, receipt manifest, invoice evidence, an... |
| 153 | `docops_v2_l4_043_xlsx_ppt_capa_audit_response_pack` | L4 | xlsx+pptx | 2 | A clinical quality CAPA audit response tracker and public audit response deck must be generated from a draft deck, deviation log, audit s... |
| 154 | `docops_v2_l4_044_excel_vendor_onboarding_tracker_from_policy_pack` | L4 | xlsx | 1 | A vendor onboarding tracker must be completed from a policy packet, owner directory, and evidence index while preserving formulas, valida... |
| 155 | `docops_v2_l4_045_pdf_word_cafe_allergen_menu_board_style` | L4 | pdf+docx | 2 | Create a public cafe allergen menu board PDF and an internal kitchen allergen print sheet from a draft menu PDF, menu source workbook, br... |
| 156 | `docops_v2_l4_046_pdf_word_campus_evacuation_signage_runbook` | L4 | pdf+docx | 2 | Create a public campus evacuation signage PDF and an internal floor marshal drill runbook from a draft sign PDF, zone roster, safety note... |
| 157 | `docops_v2_l4_047_pdf_docx_xlsx_prior_auth_denial_appeal_packet` | L4 | pdf+docx+xlsx | 2 | Create an external prior authorization appeal letter and evidence tracker workbook from nine source documents while mapping payer criteri... |
| 158 | `docops_v2_l4_048_pdf_docx_xlsx_payroll_garnishment_priority_packet` | L4 | pdf+docx+xlsx | 2 | Create a payroll garnishment setup memo and calculation tracker from multiple legal/payroll documents while calculating disposable earnin... |
| 159 | `docops_v2_l4_049_pdf_xlsx_docx_device_field_safety_recall_packet` | L4 | pdf+xlsx+docx | 3 | Prepare a public customer field safety notice PDF, an internal Excel reconciliation workbook, and a regulatory cover memo from a draft no... |
| 160 | `docops_v2_l4_050_pdf_xlsx_docx_litigation_exhibit_production_privilege_log` | L4 | pdf+xlsx+docx | 3 | Create a litigation exhibit production binder, production/privilege-log workbook, and production index memo from a draft memo, protocol, ... |
| 161 | `docops_v2_l4_051_pdf_xlsx_carton_artwork_locale_proof` | L4 | pdf+xlsx | 2 | Prepare a final carton artwork PDF proof and matching QA checklist from a draft PDF, SKU master, locale typography note, and style sheet ... |
| 162 | `docops_v2_l4_052_pdf_xlsx_closeout_binder_and_warranty_tracker` | L4 | pdf+xlsx | 2 | A closeout binder and warranty follow-up tracker must be prepared for owner release from punchlist, warranty, photo appendix, and superin... |
| 163 | `docops_v2_l4_053_pdf_xlsx_film_festival_screening_schedule` | L4 | pdf+xlsx | 2 | Create a public screening program PDF and schedule control workbook by resolving film runtime, venue, Q&A, turnaround, accessibility, and... |
| 164 | `docops_v2_l4_054_pdf_xlsx_workshop_certificate_badge_merge` | L4 | pdf+xlsx | 2 | Create a batch merged certificate/badge PDF packet and fulfillment manifest workbook from template, roster, corrections, brand guide, and... |
| 165 | `docops_v2_l4_055_pdf_invoice_packet_redaction_from_vendor_register` | L4 | pdf | 1 | A client invoice packet must be assembled from a register, redaction policy, and approved appendix while removing duplicate/internal page... |
| 166 | `docops_v2_l4_056_ppt_docx_incident_review_release_pack` | L4 | pptx+docx | 2 | An incident review deck and executive memo must be released from a draft deck, timeline/actions workbook, message map, and decision log w... |
| 167 | `docops_v2_l4_057_ppt_pdf_museum_wall_label_print_proof` | L4 | pptx+pdf | 2 | Create a final museum wall-label PPTX and PDF print proof from a draft deck, object checklist, rights note, and gallery style sheet while... |
| 168 | `docops_v2_l4_058_ppt_xlsx_qbr_readout_and_action_register` | L4 | pptx+xlsx | 2 | A QBR renewal deck and action register must be generated from a draft deck, risk workbook, account owner notes, and finance exception not... |
| 169 | `docops_v2_l4_059_ppt_xlsx_conference_poster_accessibility_style` | L4 | pptx+xlsx | 2 | Repair a conference poster deck and produce a print/accessibility specification workbook using a session schedule, accessibility note, an... |
| 170 | `docops_v2_l4_060_ppt_xlsx_conference_digital_signage_runofshow` | L4 | pptx+xlsx | 2 | Create a public conference digital-signage deck and internal run-of-show workbook from a draft deck, schedule source, operations note, an... |
| 171 | `docops_v2_l4_061_pptx_xlsx_utility_rebate_mv_packet` | L4 | pptx+xlsx | 2 | Create a utility rebate M&V deck and calculation tracker from an energy audit, rebate guide, vendor quote, baseline workbook, and interna... |
| 172 | `docops_v2_l4_062_pptx_xlsx_theater_foh_rebrand_accessibility` | L4 | pptx+xlsx | 2 | Create a rebranded public front-of-house signage deck and source trace workbook from a legacy deck, brand guide, run-of-show, accessibili... |
| 173 | `docops_v2_l4_063_word_pdf_contract_exhibit_style_repair` | L4 | docx+pdf | 2 | Repair a contract Word document and produce a final PDF exhibit packet using a style playbook, clause matrix, and draft exhibit source pa... |
| 174 | `docops_v2_l4_064_word_pdf_policy_exception_memo_public_appendix` | L4 | docx+pdf | 2 | A policy exception release memo and public appendix must be generated from an exception log, policy source, approval note, and evidence a... |
| 175 | `docops_v2_l4_065_word_ppt_shortlist_interview_package_style` | L4 | docx+pptx | 2 | Create a shortlist interview leave-behind and synchronized interview deck from a draft Word file, source matrix, agenda note, and style b... |
| 176 | `docops_v2_l4_066_word_xlsx_grant_narrative_budget_format` | L4 | docx+xlsx | 2 | Prepare a foundation grant narrative and budget workbook with strict upload formatting, public/internal budget line separation, and live ... |
| 177 | `docops_v2_l4_067_word_xlsx_site_inspection_response_and_commitment_tracker` | L4 | docx+xlsx | 2 | A site inspection response letter and internal commitment tracker must be prepared from a draft letter, observation log, sponsor comments... |
| 178 | `docops_v2_l4_068_word_xlsx_rfp_award_recommendation_scorebook` | L4 | docx+xlsx | 2 | Create a best-value RFP award recommendation memo and evaluation scorebook from a draft memo, raw scoring export, evaluation rules, vendo... |
| 179 | `docops_v2_l4_069_word_xlsx_accreditation_self_study_evidence_matrix` | L4 | docx+xlsx | 2 | Create a privacy-safe accreditation self-study response and evidence matrix workbook from draft response text, standards, raw assessment ... |
| 180 | `docops_v2_l4_070_word_xlsx_retail_lease_abstract_obligation_calendar` | L4 | docx+xlsx | 2 | Create a retail lease abstract memo and lease obligation calendar from a draft abstract, executed lease excerpt, amendment, landlord CAM ... |
| 181 | `docops_v2_l4_071_word_xlsx_security_incident_notification_clock` | L4 | docx+xlsx | 2 | Create a privacy-safe incident notification memo and breach notification tracker from a draft privileged incident note, timeline, contrac... |
| 182 | `docops_v2_l4_072_word_xlsx_construction_change_order_claim_package` | L4 | docx+xlsx | 2 | Create a substantiated construction change order request and cost/schedule workbook from ten input documents while excluding weather leve... |
| 183 | `docops_v2_l4_073_word_xlsx_disaster_grant_reimbursement_drawdown` | L4 | docx+xlsx | 2 | Create a grant reimbursement request and drawdown workbook from ten source documents while excluding ineligible and internal-only costs f... |
| 184 | `docops_v2_l4_074_word_xlsx_export_compliance_shipping_release` | L4 | docx+xlsx | 2 | Create an export shipping release memo and compliance workbook from ten source documents while holding controlled/internal lines, assembl... |
| 185 | `docops_v2_l4_075_word_xlsx_leave_accommodation_case_file` | L4 | docx+xlsx | 2 | Create a manager-safe leave accommodation determination memo and HR case tracker workbook from ten source documents while calculating eli... |
| 186 | `docops_v2_l4_076_word_xlsx_vendor_bnotice_backup_withholding_packet` | L4 | docx+xlsx | 2 | Create a vendor B-notice action memo and backup withholding tracker from IRS notice, corrected W-9s, vendor master, payment run, and priv... |
| 187 | `docops_v2_l4_077_word_xlsx_contract_redline_obligation_change` | L4 | docx+xlsx | 3 | Create a clean SLA amendment, an actual tracked-change redline amendment, and an obligation change log workbook from cross-document contr... |
| 188 | `docops_v2_l4_078_word_xlsx_manuscript_citation_crossref_cleanup` | L4 | docx+xlsx | 2 | Create a revised manuscript and citation/cross-reference audit workbook by converting author-date citations to numeric Vancouver style, r... |
| 189 | `docops_v2_l4_079_word_xlsx_board_minutes_and_action_register` | L4 | docx+xlsx | 2 | Publish board minutes and a matching action register from a draft minutes file, agenda packet, attendance/vote log, and chair reconciliat... |
| 190 | `docops_v2_l4_080_xlsx_pdf_budget_print_packet` | L4 | xlsx+pdf | 2 | Apply cross-document style and formatting rules to the budget print packet package while preserving native style controls. |
| 191 | `single_doc_workflow__excelwf_001_monthly_close_workbook_finalize_seed` | L3 | xlsx | 1 | Finalize a monthly close workbook. |
| 192 | `single_doc_workflow__excelwf_002_audit_tracker_publication_seed` | L3 | xlsx | 1 | Publish an audit tracker workbook. |
| 193 | `single_doc_workflow__excelwf_003_budget_review_pack_seed` | L3 | xlsx | 1 | Build a budget review workbook from internal sheets. |
| 194 | `single_doc_workflow__excelwf_004_capex_register_cleanup_seed` | L3 | xlsx | 1 | Clean up a capex register workbook. |
| 195 | `single_doc_workflow__excelwf_005_governance_workbook_release_seed` | L3 | xlsx | 1 | Release the governance workbook without renaming or deleting its live sheets. |
| 196 | `single_doc_workflow__pdfwf_001_closeout_packet_single_file_refresh_seed` | L3 | pdf | 1 | Clean the closeout packet PDF while preserving the live page text. |
| 197 | `single_doc_workflow__pdfwf_002_audit_brief_theme_and_summary_seed` | L3 | pdf | 1 | Clean the audit brief PDF while preserving the live page text. |
| 198 | `single_doc_workflow__pdfwf_003_policy_appendix_rebuild_seed` | L3 | pdf | 1 | Rebuild a policy appendix PDF in one file. |
| 199 | `single_doc_workflow__pdfwf_004_board_packet_cover_refresh_seed` | L3 | pdf | 1 | Clean the board packet PDF while preserving the live page text. |
| 200 | `single_doc_workflow__pdfwf_005_closeout_binder_page_labels_and_bookmarks_seed` | L3 | pdf | 1 | Rebuild a closeout binder PDF. |
| 201 | `single_doc_workflow__pptwf_001_board_deck_locked_layout_finalize_seed` | L3 | pptx | 1 | Finalize a board deck with a locked reference layout. |
| 202 | `single_doc_workflow__pptwf_002_qbr_deck_master_cleanup_seed` | L3 | pptx | 1 | Clean up a quarterly business review deck. |
| 203 | `single_doc_workflow__pptwf_003_training_deck_appendix_and_theme_seed` | L3 | pptx | 1 | Prepare a training deck with appendix and theme cleanup. |
| 204 | `single_doc_workflow__pptwf_004_program_review_publication_seed` | L3 | pptx | 1 | Publish a program review deck. |
| 205 | `single_doc_workflow__pptwf_005_team_sync_deck_caption_cleanup_seed` | L3 | pptx | 1 | Clean up a team sync deck with caption fixes. |
| 206 | `single_doc_workflow__wordwf_001_board_memo_publish_pipeline_seed` | L3 | docx | 1 | Clean the board memorandum draft without changing the live wording. |
| 207 | `single_doc_workflow__wordwf_002_policy_manual_resection_and_numbering_seed` | L3 | docx | 1 | Repair the policy manual draft while preserving the wording of the live sections. |
| 208 | `single_doc_workflow__wordwf_003_bilingual_report_publication_seed` | L3 | docx | 1 | Clean the bilingual report draft without paraphrasing the English or Chinese content. |
| 209 | `single_doc_workflow__wordwf_004_contract_schedule_cleanup_seed` | L3 | docx | 1 | Clean the contract schedule draft while preserving the listed clauses and schedule values. |
| 210 | `single_doc_workflow__wordwf_005_comprehensive_handbook_publication_seed` | L3 | docx | 1 | Clean the comprehensive handbook draft into a structured DOCX without rewriting its live content. |
