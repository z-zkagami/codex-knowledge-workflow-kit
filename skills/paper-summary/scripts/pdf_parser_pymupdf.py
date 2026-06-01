import sys
import pymupdf4llm
import json
import os

def extract_markdown_from_pdf(pdf_path):
    """
    Extracts text from a PDF file as Markdown using pymupdf4llm.
    This preserves headers, tables, and reading order much better than raw text extraction.
    
    Args:
        pdf_path (str): Path to the PDF file.
        
    Returns:
        dict: A dictionary containing the full markdown text and metadata.
    """
    try:
        if not os.path.exists(pdf_path):
            error_msg = f"File not found: {pdf_path}"
            print(f"❌ {error_msg}", file=sys.stderr)
            return {"error": error_msg}
            
        print(f"🚀 Starting PDF extraction for: {pdf_path}", file=sys.stderr)
        
        # Convert PDF to Markdown
        # This function handles multi-column layouts and tables automatically
        print(f"⏳ Parsing PDF content (this may take a moment)...", file=sys.stderr)
        md_text = pymupdf4llm.to_markdown(pdf_path)
        
        print(f"✅ Extraction complete! Length: {len(md_text)} characters", file=sys.stderr)
        
        return {
            "content": md_text,
            "source": pdf_path
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python pdf_parser.py <path_to_pdf>"}))
        sys.exit(1)
        
    pdf_path = sys.argv[1]
    data = extract_markdown_from_pdf(pdf_path)
    # Output JSON with Ensure ASCII=False to support Chinese characters properly
    print(json.dumps(data, indent=2, ensure_ascii=False))
