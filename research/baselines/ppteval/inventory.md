# PPT-Eval task inventory (120 tasks)

Generated from `task_registry/tasks.json` and `task_registry/rubrics/*.json` at microsoft/ppteval commit 1b8b55a.
Kind is a keyword heuristic over the goal text (create = adds new content; edit = modifies existing content). Rubric leaves counts scoring nodes; VLM nodes are the leaves whose scorer calls `vlm_call`.

| Task ID | File | Tier | Kind | Rubric leaves (critical) | VLM nodes | Goal |
|---|---|---|---|---|---|---|
| 3-002 | 3.pptx | Easy | edit | 2 (1) | 0 | Change the lecture number from 'Lecture 3' to 'Lecture 1' in the presentation title. |
| 3-003 | 3.pptx | Easy | create | 4 (2) | 0 | Add a new bullet point after 'Dual Mode' that says 'File System' on slide 2. |
| 3-006 | 3.pptx | Medium | edit | 5 (2) | 3 | Change the vCPU1 color from magenta to green on slide 3 |
| 3-007 | 3.pptx | Hard | create | 6 (4) | 4 | On slide 3, Add a fourth vCPU circle (vCPU4) next to the existing three circles using a different color and also add vCPU4 to the time-sharing diagram |
| 3-009 | 3.pptx | Hard | edit | 3 (1) | 1 | Change the color tone of the figure on slide 4 to blue by adding a shape on top of the figure and increasing it's transparency |
| 3-017 | 3.pptx | Easy | create | 5 (3) | 1 | On slide 14, add a text box below the processor image with the caption 'Intel Skylake Die Layout' |
| 3-020 | 3.pptx | Easy | edit | 3 (1) | 2 | On slide 8, change the red border around the OS box to blue |
| 3-021 | 3.pptx | Medium | create | 5 (2) | 2 | On slide 8, add a new process box 'Proc 3' in purple color next to the existing processes. |
| 3-030 | 3.pptx | Hard | create | 4 (2) | 3 | On slide 33, add a code example showing a simple fork() call below the bullet points |
| 3-042 | 3.pptx | Easy | edit | 5 (2) | 2 | Change the circular bullets on the final slide to numbered list items. |
| 4._Pre-Colonial_Filipino_Culture-001 | 4._Pre-Colonial_Filipino_Culture.pptx | Easy | edit | 3 (1) | 0 | Change the presentation title font size to 48pt |
| 4._Pre-Colonial_Filipino_Culture-002 | 4._Pre-Colonial_Filipino_Culture.pptx | Easy | edit | 6 (2) | 0 | Edit the subtitle text box below the main title so that it says: "Philippine History: An Educational Overview" |
| 4._Pre-Colonial_Filipino_Culture-004 | 4._Pre-Colonial_Filipino_Culture.pptx | Medium | edit | 5 (2) | 2 | Replace the background image of the slide 2 to with a lighter one |
| 4._Pre-Colonial_Filipino_Culture-005 | 4._Pre-Colonial_Filipino_Culture.pptx | Hard | edit | 7 (5) | 2 | Combine slides 2 and 3 into a single slide with table for male and female clothing. Include the images from both slides. Don't delete the original slides yet; just insert this as a new slide after slide 3. |
| 4._Pre-Colonial_Filipino_Culture-010 | 4._Pre-Colonial_Filipino_Culture.pptx | Medium | create | 8 (5) | 0 | Add a new slide after slide 4 with the title 'Traditional Weapons'. |
| 4._Pre-Colonial_Filipino_Culture-014 | 4._Pre-Colonial_Filipino_Culture.pptx | Easy | edit | 4 (1) | 2 | On slide 8, change the numbered list to use Roman numerals (I, II, III, IV) |
| 4._Pre-Colonial_Filipino_Culture-015 | 4._Pre-Colonial_Filipino_Culture.pptx | Medium | create | 5 (3) | 3 | Add appropriate emojis icons next to each social class type on slide 8 |
| 4._Pre-Colonial_Filipino_Culture-017 | 4._Pre-Colonial_Filipino_Culture.pptx | Easy | edit | 2 (1) | 2 | On slide 11, change the yellow font color text to add blue highlighting |
| 4._Pre-Colonial_Filipino_Culture-020 | 4._Pre-Colonial_Filipino_Culture.pptx | Hard | edit | 4 (1) | 2 | On slide 12, make the fourth and fifth items in the numbered list look consistent with the first three. |
| 4._Pre-Colonial_Filipino_Culture-022 | 4._Pre-Colonial_Filipino_Culture.pptx | Medium | edit | 3 (1) | 1 | On slide 9, resize the text in the diagram so that 'Nobles' fits in the pyramid. |
| Accounting Equation-001 | Accounting Equation.pptx | Easy | edit | 3 (1) | 0 | Change the title color of 'Accounting Equation' from blue to red on slide 1 |
| Accounting Equation-003 | Accounting Equation.pptx | Easy | create | 5 (2) | 0 | Add a new bullet point 'Capital' after 'Expenses' on slide 5 |
| Accounting Equation-004 | Accounting Equation.pptx | Medium | edit | 3 (1) | 0 | Replace the word 'Liability' with 'Debt' throughout the slides |
| Accounting Equation-008 | Accounting Equation.pptx | Hard | edit | 3 (2) | 0 | On slide 6. Change the slide layout to 'Two Content' and split the Assets and Liabilities sections into two separate content areas |
| Accounting Equation-012 | Accounting Equation.pptx | Hard | create | 4 (3) | 0 | Add a footer to every slide with the text 'Fundamental Accounting Concepts', and ensure that the footer is center-aligned |
| Accounting Equation-014 | Accounting Equation.pptx | Easy | create | 4 (3) | 0 | Add a new slide after slide 6 with the title 'Summary of Accounting Terms' |
| Accounting Equation-015 | Accounting Equation.pptx | Hard | create | 5 (2) | 1 | Insert a SmartArt graphic on slide 3 to represent the accounting equation (Assets = Capital + Liabilities) using a SmartArt suitable for an equation |
| Accounting Equation-025 | Accounting Equation.pptx | Medium | create | 3 (2) | 0 | Add slide numbering at the bottom right corner of all slides |
| Accounting Equation-042 | Accounting Equation.pptx | Medium | create | 4 (2) | 4 | Insert a black calculator icon next to the equation on slide 3 |
| Accounting Equation-045 | Accounting Equation.pptx | Hard | create | 5 (3) | 0 | On slide 3, Create a flowchart showing the logic: Left Hand Side → Right Hand Side → Balance using rounder rectangles and line arrows |
| Aircraft_surface-001 | Aircraft_surface.pptx | Easy | edit | 4 (1) | 0 | On slide 1, Change the title 'AIRCRAFT SURFACE' to 'AIRCRAFT FUNDAMENTALS' |
| Aircraft_surface-002 | Aircraft_surface.pptx | Easy | create | 4 (3) | 0 | On slide 1, Add a new text box below the author name that says 'An Introduction to Flight Dynamics' |
| Aircraft_surface-003 | Aircraft_surface.pptx | Easy | edit | 3 (1) | 0 | On slide 2, Change the bullet point 'Lateral Axis' to 'Lateral (Side-to-Side) Axis'. |
| Aircraft_surface-004 | Aircraft_surface.pptx | Hard | edit | 6 (3) | 1 | On slide 2, Add a new bullet point at the end of the list that says 'All three axes intersect at the aircraft's center of gravity'. Resize the image to avoid overlap. |
| Aircraft_surface-006 | Aircraft_surface.pptx | Easy | edit | 2 (1) | 0 | On slide 4, Change the title from 'Longitudinal Axis (2 of 3)' to 'Longitudinal Axis - Roll Movement (2 of 3)' |
| Aircraft_surface-007 | Aircraft_surface.pptx | Easy | create | 3 (2) | 0 | On slide 3, Add a new text box below the image that says 'Ailerons control the roll movement of the aircraft' |
| Aircraft_surface-009 | Aircraft_surface.pptx | Easy | create | 4 (2) | 0 | On slide 5, Add the text box 'Roll Movement Demonstration' below the main title |
| Aircraft_surface-011 | Aircraft_surface.pptx | Medium | edit | 4 (3) | 0 | On slide 7, Add a new text box that says 'Elevators control the pitch attitude of the aircraft' positioned below the aircraft diagram. Resize the image to avoid overlap. |
| Aircraft_surface-013 | Aircraft_surface.pptx | Easy | edit | 3 (1) | 0 | On slide 8, Replace the 'Click to add text' placeholder with 'Elevator movement controls aircraft pitch attitude' |
| Aircraft_surface-016 | Aircraft_surface.pptx | Easy | edit | 3 (1) | 0 | On slide 11, Replace the 'Click to add text' placeholder with 'Left rudder causes left yaw, right rudder causes right yaw' |
| Drummond_Troilo-Unseen Aspects of Sea Level Rise (final)-002 | Drummond_Troilo-Unseen Aspects of Sea Level Rise (final).pptx | Easy | create | 4 (3) | 0 | Add a text box with the text 'Updated Presentation' in the top-right corner of the title slide |
| Drummond_Troilo-Unseen Aspects of Sea Level Rise (final)-008 | Drummond_Troilo-Unseen Aspects of Sea Level Rise (final).pptx | Medium | edit | 5 (3) | 4 | On slide 2, Move the chart/image and caption to the left side of the slide and resize the text content to fit the right side |
| Drummond_Troilo-Unseen Aspects of Sea Level Rise (final)-011 | Drummond_Troilo-Unseen Aspects of Sea Level Rise (final).pptx | Easy | create | 4 (2) | 2 | On slide 3, Add a text box with the text 'Data shows increasing trend since 1980' below the chart |
| Drummond_Troilo-Unseen Aspects of Sea Level Rise (final)-019 | Drummond_Troilo-Unseen Aspects of Sea Level Rise (final).pptx | Easy | edit | 3 (1) | 2 | On slide 5, Remove the '43 year horizon' red annotation from the chart |
| Drummond_Troilo-Unseen Aspects of Sea Level Rise (final)-020 | Drummond_Troilo-Unseen Aspects of Sea Level Rise (final).pptx | Medium | edit | 4 (2) | 3 | On slide 5, Move the Miami-Dade report document image to the left side of the slide and move the chart image to the right side |
| Drummond_Troilo-Unseen Aspects of Sea Level Rise (final)-022 | Drummond_Troilo-Unseen Aspects of Sea Level Rise (final).pptx | Medium | edit | 3 (1) | 2 | Resize the images on slide 5 to make the main chart larger and more prominent on the slide |
| Drummond_Troilo-Unseen Aspects of Sea Level Rise (final)-024 | Drummond_Troilo-Unseen Aspects of Sea Level Rise (final).pptx | Medium | create | 4 (2) | 1 | Add a bullet point 'Aquifer contamination' under the Groundwater section on slide 7 |
| Drummond_Troilo-Unseen Aspects of Sea Level Rise (final)-039 | Drummond_Troilo-Unseen Aspects of Sea Level Rise (final).pptx | Easy | create | 4 (2) | 1 | Add a title 'Storm Event Analysis' above the objective text on slide 11 |
| Drummond_Troilo-Unseen Aspects of Sea Level Rise (final)-040 | Drummond_Troilo-Unseen Aspects of Sea Level Rise (final).pptx | Medium | create | 5 (2) | 1 | Add a text box on slide 11 explaining that this chart shows cumulative rainfall over the storm period |
| Drummond_Troilo-Unseen Aspects of Sea Level Rise (final)-042 | Drummond_Troilo-Unseen Aspects of Sea Level Rise (final).pptx | Easy | edit | 3 (1) | 0 | Make the objective text italic on slide 11 |
| HSC Careers and Expo FINAL COM MOD-001 | HSC Careers and Expo FINAL COM MOD.pptx | Easy | edit | 4 (1) | 0 | Change the title of the presentation from 'Texts and Human Experiences The Common Modules' to 'Literature and Human Experiences The Common Modules' |
| HSC Careers and Expo FINAL COM MOD-003 | HSC Careers and Expo FINAL COM MOD.pptx | Easy | edit | 4 (1) | 0 | Change the font size of the main title 'Texts and Human Experiences' on the first slide to make it larger |
| HSC Careers and Expo FINAL COM MOD-004 | HSC Careers and Expo FINAL COM MOD.pptx | Medium | edit | 3 (1) | 1 | Change the background color of the slide 1 to light blue |
| HSC Careers and Expo FINAL COM MOD-008 | HSC Careers and Expo FINAL COM MOD.pptx | Medium | create | 4 (3) | 0 | Create a text box on slide 2 with the phrase 'Important Note' and position it in the bottom right corner of the slide |
| HSC Careers and Expo FINAL COM MOD-022 | HSC Careers and Expo FINAL COM MOD.pptx | Hard | create | 4 (3) | 1 | Create a callout box with no fill around the entire second checkbox item on slide 5 |
| HSC Careers and Expo FINAL COM MOD-038 | HSC Careers and Expo FINAL COM MOD.pptx | Hard | edit | 5 (1) | 1 | Convert the entire checklist on slide 8 into a two-column layout to save space |
| HSC Careers and Expo FINAL COM MOD-045 | HSC Careers and Expo FINAL COM MOD.pptx | Medium | create | 2 (1) | 0 | On slide 38, Add the word 'mysterious' to the negative section of the word bank |
| HSC Careers and Expo FINAL COM MOD-051 | HSC Careers and Expo FINAL COM MOD.pptx | Easy | edit | 3 (1) | 0 | Convert all the bullet points into a numbered list format on slide 19 |
| HSC Careers and Expo FINAL COM MOD-064 | HSC Careers and Expo FINAL COM MOD.pptx | Hard | create | 3 (2) | 0 | Add a hyperlink on the word 'HSC' on slide 19 that links to slide 1 |
| HSC Careers and Expo FINAL COM MOD-072 | HSC Careers and Expo FINAL COM MOD.pptx | Hard | create | 4 (2) | 0 | Create a table with two columns and convert the checklist into table format on slide 8 |
| Jean-Nicolas-Louis Durand-001 | Jean-Nicolas-Louis Durand.pptx | Easy | edit | 3 (1) | 0 | Change the title text to 'French Architect: Jean-Nicolas-Louis Durand' on the first slide |
| Jean-Nicolas-Louis Durand-008 | Jean-Nicolas-Louis Durand.pptx | Hard | edit | 4 (2) | 0 | Resize the historical document image on slide 4 to be 20% smaller while maintaining aspect ratio |
| Jean-Nicolas-Louis Durand-009 | Jean-Nicolas-Louis Durand.pptx | Easy | edit | 5 (1) | 1 | Change all bullet points on slide 5 to numbered list format |
| Jean-Nicolas-Louis Durand-012 | Jean-Nicolas-Louis Durand.pptx | Medium | create | 4 (1) | 1 | Add a border around the architectural diagram image on sllide 6 |
| Jean-Nicolas-Louis Durand-015 | Jean-Nicolas-Louis Durand.pptx | Hard | edit | 4 (1) | 1 | Crop the architectural diagram image on slide 8 to show only the top two rows of buildings |
| Jean-Nicolas-Louis Durand-020 | Jean-Nicolas-Louis Durand.pptx | Easy | edit | 5 (1) | 2 | Change the font color of 'Conclusion:' on slide 23 from white to yellow |
| Jean-Nicolas-Louis Durand-025 | Jean-Nicolas-Louis Durand.pptx | Hard | edit | 4 (1) | 0 | Rotate the architectural diagram image 45 degrees clockwise on slide 6 |
| Jean-Nicolas-Louis Durand-026 | Jean-Nicolas-Louis Durand.pptx | Easy | create | 4 (2) | 0 | Add a text box explaining 'These drawings show standardized proportional relationships' on slide 7 |
| Jean-Nicolas-Louis Durand-028 | Jean-Nicolas-Louis Durand.pptx | Easy | create | 5 (3) | 0 | Create a new slide after slide 8 with the title 'Building Analysis Methods' |
| Jean-Nicolas-Louis Durand-029 | Jean-Nicolas-Louis Durand.pptx | Easy | edit | 3 (1) | 2 | Change the French title text color from white to gold on slide 4 |
| Obesity-002 | Obesity.pptx | Medium | edit | 5 (3) | 2 | Change the background color of the title slide to light blue by creating a rectangular shape with transparency, overlaying it on the slide and sending it to the back. |
| Obesity-004 | Obesity.pptx | Medium | create | 8 (6) | 0 | Add a bullet point list with three items: 'Obesity definition', 'Global statistics', and 'Impact on health' as a new slide between 1 and 2, titled "Agenda" |
| Obesity-009 | Obesity.pptx | Medium | edit | 3 (2) | 2 | On slide 2, break the paragraph into two bullet points: 'Obesity is defined as excess body fat' and 'Because body fat is difficult to measure directly, obesity is often measured by body mass index (BMI)', and indent the second bullet point |
| Obesity-010 | Obesity.pptx | Medium | create | 4 (3) | 3 | Add a text box with BMI calculation formula 'BMI = (Weight in kg)/(Height in m)^2​' positioned at the bottom right of slide 2 |
| Obesity-011 | Obesity.pptx | Medium | edit | 2 (2) | 2 | Convert the first bullet in the content placeholder for Slide 9 into three: *. The association may be stronger for obese adolescents than younger children *. Obese children are also more likely to have increased risk of heart disease *. Obese children are also more likely to develop asthma, then change only the first bullet point to a numbered list item '1' on slide 9. |
| Obesity-013 | Obesity.pptx | Medium | create | 4 (3) | 0 | Add a second bullet point to slide 6: 'Determining healthy weight for children requires precise measurement tools' and underline it |
| Obesity-014 | Obesity.pptx | Easy | edit | 2 (1) | 2 | Bold the text '85th and 94th percentiles' and '95th percentile' |
| Obesity-015 | Obesity.pptx | Hard | create | 4 (2) | 1 | Insert a small table on slide 3 showing BMI ranges categorized by male and female and for ages (2-5, 6-11, 12-19, 20+) using <,> and – to denote ranges on slide 3 |
| Obesity-017 | Obesity.pptx | Easy | edit | 2 (1) | 1 | Convert the paragraph on slide 5 into two bullet points: 'Early Life: A child's risk of becoming obese may begin before birth' and 'Pregnant women who use tobacco, gain excessive weight, or have diabetes increase their children's obesity risk' |
| Obesity-020 | Obesity.pptx | Hard | edit | 6 (4) | 4 | Change slide 8 to a two-column comparison layout with 'Adults' on the left and 'Children' on the right, moving appropriate bullet points to each column |
| Revisiting Classical  Social Experiments [Autosaved]-001 | Revisiting Classical  Social Experiments [Autosaved].pptx | Easy | edit | 3 (1) | 0 | Change the title text from 'REVISITING CLASSICAL SOCIAL EXPERIMENTS' to 'EXPLORING CLASSICAL SOCIAL EXPERIMENTS' |
| Revisiting Classical  Social Experiments [Autosaved]-008 | Revisiting Classical  Social Experiments [Autosaved].pptx | Easy | create | 4 (2) | 1 | Add a subtitle below the main title on slide 1 that says 'A Comprehensive Review' |
| Revisiting Classical  Social Experiments [Autosaved]-011 | Revisiting Classical  Social Experiments [Autosaved].pptx | Easy | create | 3 (2) | 0 | In slide 5, add a new bullet point at the end which says: 'Published findings in 1898' |
| Revisiting Classical  Social Experiments [Autosaved]-016 | Revisiting Classical  Social Experiments [Autosaved].pptx | Hard | create | 5 (3) | 0 | Create slide after slide 3 with a table listing each experiment from slide 3 with columns for Researcher, Year, and Key Finding |
| Revisiting Classical  Social Experiments [Autosaved]-018 | Revisiting Classical  Social Experiments [Autosaved].pptx | Hard | create | 3 (2) | 1 | Add icons or symbols inside each of the three circles in slide 2 which illustrate the respective text |
| Revisiting Classical  Social Experiments [Autosaved]-020 | Revisiting Classical  Social Experiments [Autosaved].pptx | Easy | edit | 2 (1) | 0 | Center align the title text on slide 4 |
| Revisiting Classical  Social Experiments [Autosaved]-021 | Revisiting Classical  Social Experiments [Autosaved].pptx | Easy | create | 4 (1) | 0 | Add a slide transition effect of 'Fade' to slide 2 |
| Revisiting Classical  Social Experiments [Autosaved]-023 | Revisiting Classical  Social Experiments [Autosaved].pptx | Medium | create | 3 (3) | 0 | Insert a new slide after slide 4 with the title 'Milgram's Obedience Study' |
| Revisiting Classical  Social Experiments [Autosaved]-027 | Revisiting Classical  Social Experiments [Autosaved].pptx | Medium | create | 3 (2) | 0 | Add a text box with 'These are the key elements' positioned below the circles and text in slide 2 |
| Revisiting Classical  Social Experiments [Autosaved]-033 | Revisiting Classical  Social Experiments [Autosaved].pptx | Hard | create | 3 (2) | 0 | Create hyperlinks from each experiment name in slide 3 to corresponding Wikipedia pages about either the experiment or the researcher(s) |
| Worms-002 | Worms.pptx | Easy | create | 5 (2) | 0 | In the title slide, add a subtitle 'A Comprehensive Study' below the main title |
| Worms-003 | Worms.pptx | Medium | edit | 3 (1) | 1 | In slide 2, format the last three bullets which detail the types of worms as a numbered list |
| Worms-004 | Worms.pptx | Easy | edit | 2 (1) | 0 | Change the font size of the title in the second slide to 36pt |
| Worms-007 | Worms.pptx | Hard | create | 4 (3) | 1 | Add a text box in Slide 4 explaining what 'prostomium' means and position it above the word  'prostomium' on the diagram |
| Worms-008 | Worms.pptx | Easy | edit | 6 (1) | 1 | Change the background color of Slide 4 to light blue |
| Worms-019 | Worms.pptx | Medium | create | 5 (2) | 0 | Add a bullet point with a fact about worm reproduction in slide 5 |
| Worms-024 | Worms.pptx | Medium | edit | 4 (1) | 0 | Vertically center-align both images on slide 3 |
| Worms-042 | Worms.pptx | Medium | create | 5 (1) | 0 | Add slide numbers to all slides except the title slide |
| Worms-050 | Worms.pptx | Medium | edit | 5 (1) | 1 | Rotate the diagram on slide 4 clockwise 90 degrees |
| Worms-060 | Worms.pptx | Hard | create | 8 (5) | 1 | Add a slide after slide 2 with a table comparing characteristics of all three worm types |
| application+layer+slide-001 | application+layer+slide.pptx | Easy | edit | 4 (2) | 0 | Slide 1: Change the title text 'Application Layer' to 'Network Application Layer' and make it bold |
| application+layer+slide-007 | application+layer+slide.pptx | Easy | edit | 4 (1) | 1 | Change the font size of the question 'Q: does IP address of host suffice for identifying the process?' on slide 7 to be smaller (less than 18pt) |
| application+layer+slide-010 | application+layer+slide.pptx | Medium | create | 5 (1) | 1 | Add a bullet point explaining 'Objects include CSS files, JavaScript files, images, videos' at an appropriate place on slide 10 |
| application+layer+slide-011 | application+layer+slide.pptx | Hard | edit | 6 (2) | 3 | On slide 11, replace the existing diagram with a simpler flowchart showing 'Browser → HTTP Request → Web Server → HTTP Response → Browser' |
| application+layer+slide-014 | application+layer+slide.pptx | Easy | edit | 3 (1) | 0 | Change the background color of slide 3 to light blue |
| application+layer+slide-015 | application+layer+slide.pptx | Medium | create | 8 (5) | 0 | On slide 4, create a simple table with two columns: 'Application' and 'Architecture Type' and insert Skype and Instant messaging |
| application+layer+slide-018 | application+layer+slide.pptx | Easy | create | 4 (2) | 1 | Add a subtitle 'Port Numbers and Process Identification' below the main title in slide 7 |
| application+layer+slide-019 | application+layer+slide.pptx | Hard | edit | 5 (2) | 2 | On slide 8, replace the IP address and Port number bullet points with a simple diagram showing IP address (128.119.245.12) connected to Port 80 |
| application+layer+slide-021 | application+layer+slide.pptx | Hard | edit | 5 (1) | 2 | Replace the URL example with 'https://university.edu/courses/networking.html' and update the URL labels breakdown accordingly |
| application+layer+slide-024 | application+layer+slide.pptx | Medium | edit | 5 (3) | 3 | Remove the blue box on the right side along with its contents and replace it with a simple bullet point 'Stateless protocols are simpler to implement' on slide 12 |
| pediatic glasses when to prescribe1-005 | pediatic glasses when to prescribe1.pptx | Easy | create | 5 (2) | 1 | Add a new team member to the first slide with the name 'Dr. Sarah Johnson' and role 'Pediatric Ophthalmologist' |
| pediatic glasses when to prescribe1-006 | pediatic glasses when to prescribe1.pptx | Easy | edit | 3 (1) | 0 | Change the section heading from 'Myopia' to 'Nearsightedness (Myopia)' on slide 18 |
| pediatic glasses when to prescribe1-019 | pediatic glasses when to prescribe1.pptx | Hard | edit | 2 (2) | 1 | Apply a different design theme to the entire presentation while maintaining the current color scheme of greenish backgrounds |
| pediatic glasses when to prescribe1-024 | pediatic glasses when to prescribe1.pptx | Medium | edit | 5 (2) | 0 | Change all text on slide 27 to be center-aligned, including the page number. |
| pediatic glasses when to prescribe1-031 | pediatic glasses when to prescribe1.pptx | Medium | edit | 3 (1) | 0 | Sort the table data on slide 10 in alphabetically by isometropia type |
| pediatic glasses when to prescribe1-032 | pediatic glasses when to prescribe1.pptx | Hard | create | 3 (2) | 1 | Add a chart based on the table data showing age distribution on slide 13 |
| pediatic glasses when to prescribe1-033 | pediatic glasses when to prescribe1.pptx | Easy | edit | 3 (2) | 1 | Delete the current images on slide 5 and replace it with a text box containing 'Image Placeholder - Eye Examination 1' and 'Image Placeholder - Eye Examination 2' |
| pediatic glasses when to prescribe1-034 | pediatic glasses when to prescribe1.pptx | Medium | edit | 2 (1) | 0 | Apply animation effects: make the text content appear with 'Fly In' animation from the left on the references slide |
| pediatic glasses when to prescribe1-035 | pediatic glasses when to prescribe1.pptx | Hard | edit | 3 (3) | 2 | Change the slide layout to "Three Content" and apply it to slide 14, rearranging content into a three-column comparison format, adding a new column that calls out the difference between unilateral and bilateral |
| pediatic glasses when to prescribe1-037 | pediatic glasses when to prescribe1.pptx | Medium | create | 3 (2) | 0 | Add a text box to slide 1 with the text "More Information", and then add a hyperlink on the text 'More Information' that links to slide 34 |
