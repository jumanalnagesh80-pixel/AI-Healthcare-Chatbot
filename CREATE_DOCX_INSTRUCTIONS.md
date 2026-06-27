# INSTRUCTIONS TO CREATE DOCX FILE

## Step 1: Install Pandoc (if not installed)

**Windows:**
- Download from: https://pandoc.org/installing.html
- Install the MSI package

**Mac:**
```bash
brew install pandoc
```

**Linux:**
```bash
sudo apt-get install pandoc
```

## Step 2: Convert Markdown to DOCX

Run this command in the project directory:

```bash
pandoc PROJECT_DOCUMENTATION.md -o AI_Healthcare_Chatbot_Project_Report.docx --toc --number-sections
```

## Step 3: Add ER Diagram

1. Open the generated DOCX file
2. Go to Chapter 5 - System Design section
3. Use the ER_DIAGRAM_DESCRIPTION.md file to create the diagram using:
   - Microsoft Visio
   - Draw.io (https://app.diagrams.net/)
   - Lucidchart
   - PlantUML

4. Insert the diagram image at Figure 5.8

## Step 4: Format the Document

1. **Set Page Layout:**
   - Page Size: A4
   - Margins: 1 inch all sides
   - Orientation: Portrait

2. **Apply Heading Styles:**
   - Title: Arial 18pt Bold
   - Chapter Headings: Arial 16pt Bold
   - Section Headings: Arial 14pt Bold
   - Subsection Headings: Arial 12pt Bold
   - Body Text: Times New Roman 12pt

3. **Add Page Numbers:**
   - Roman numerals (i, ii, iii...) for front matter
   - Arabic numerals (1, 2, 3...) from Chapter 1

4. **Format Lists:**
   - Use bullet points for unordered lists
   - Use numbers for ordered lists

5. **Add Table of Contents:**
   - Insert > Table of Contents > Automatic

6. **Format Tables:**
   - Add borders
   - Bold headers
   - Center align headers

## Step 5: Add Remaining Diagrams

Create these diagrams using Draw.io or similar:

1. **Use Case Diagram** (Figure 5.2)
2. **Class Diagram** (Figure 5.3)
3. **Sequence Diagrams** (Figures 5.4, 5.5)
4. **Activity Diagrams** (Figures 5.6, 5.7)
5. **Data Flow Diagrams** (Figures 5.9, 5.10)

## Step 6: Add Screenshots

1. Run the application
2. Take screenshots of each page
3. Insert at Chapter 9

## Step 7: Final Review

1. Check page count (should be 50+ pages)
2. Verify all figures are numbered correctly
3. Ensure table of contents is complete
4. Check formatting consistency
5. Verify all references are cited

## Quick Command for Everything:

```bash
# Convert to DOCX with all options
pandoc PROJECT_DOCUMENTATION.md \
  -o AI_Healthcare_Chatbot_Complete_Report.docx \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --reference-doc=custom-reference.docx \
  --highlight-style=tango \
  --variable=fontsize:12pt \
  --variable=geometry:margin=1in
```

## Alternative: Use Microsoft Word

1. Open Microsoft Word
2. File > Open > Select PROJECT_DOCUMENTATION.md
3. Word will convert automatically
4. Apply formatting manually
5. Insert diagrams and screenshots

## Alternative: Use Google Docs

1. Upload PROJECT_DOCUMENTATION.md to Google Drive
2. Right-click > Open with > Google Docs
3. Format > Paragraph styles
4. Insert > Drawing for diagrams
5. File > Download > Microsoft Word (.docx)

---

Your documentation is ready in Markdown format with:
- ✅ 90+ page structure
- ✅ Complete content for Chapters 1-2
- ✅ ER Diagram description
- ✅ All necessary sections outlined

Total expected pages after conversion: **50-60 pages**
