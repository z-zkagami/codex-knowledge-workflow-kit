
import sys
import json
import os
import subprocess

def run_test(pdf_path):
    """
    Runs a test of the PDF parser on a specific file.
    """
    print(f"🧪 Testing paper-summary parser with: {pdf_path}")
    
    script_path = os.path.join(os.path.dirname(__file__), "pdf_parser_pymupdf.py")
    
    try:
        # Run the parser as a subprocess to capture output
        result = subprocess.run(
            [sys.executable, script_path, pdf_path],
            capture_output=True,
            text=True
        )
        
        # Print stderr (logs)
        if result.stderr:
            print("\n📋 [Parser Logs]:")
            print(result.stderr)
            
        # Check success
        if result.returncode != 0:
            print("❌ Parser failed execution.")
            return
            
        # Parse output JSON
        try:
            output_data = json.loads(result.stdout)
            
            if "error" in output_data:
                print(f"❌ Parser returned error: {output_data['error']}")
            else:
                content_len = len(output_data.get("content", ""))
                print(f"✅ Success! Extracted {content_len} characters of Markdown.")
                
                # Preview first 500 chars
                print("\n📄 [Content Preview]:")
                print("-" * 40)
                print(output_data.get("content", "")[:500] + "...")
                print("-" * 40)
                
                # Save to debug file
                debug_file = "debug_output.md"
                with open(debug_file, "w", encoding="utf-8") as f:
                    f.write(output_data.get("content", ""))
                print(f"\n💾 Full content saved to: {debug_file}")
                
        except json.JSONDecodeError:
            print("❌ Failed to decode JSON output.")
            print("Raw output:", result.stdout)
            
    except Exception as e:
        print(f"❌ Test script error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_bench.py <path_to_pdf>")
    else:
        run_test(sys.argv[1])
