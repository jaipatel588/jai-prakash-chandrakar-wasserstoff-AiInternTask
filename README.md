# Theme Identifier Chatbot

## Features
- Upload PDFs/images
- OCR support via Tesseract
- FastAPI backend
- OpenAI-powered semantic search
- Theme synthesis and citation
- Deployable via Render or Replit

## How to Run
1. Clone repo
2. Install requirements
3. Run: `uvicorn backend.app.main:app --reload`

## Sample Query
> "What penalties were imposed?"

### Output:
- **Theme 1: Regulatory Action** - Found in `DOC001`, `DOC002`
- **Theme 2: Penalty Explanation** - Found in `DOC003`
