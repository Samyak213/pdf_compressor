import subprocess
import os
from pathlib import Path

def batch_compress_pdfs(folder_path, compression_level=3):
    """Compresses all PDFs in a given folder using Ghostscript."""
    
    # 1. Setup paths
    source_dir = Path(folder_path)
    output_dir = source_dir / "Compressed_SOPs"
    
    # Create the output folder if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Ghostscript quality settings
    quality = {
        0: '/default',
        1: '/prepress',
        2: '/printer',
        3: '/ebook',  # 150 dpi - Best balance of size and readability
        4: '/screen'
    }

    # Ghostscript command for Windows
    gs_cmd = r'C:\Program Files\gs\gs10.07.1\bin\gswin64c.exe' 

    # 2. Find all PDF files in the folder
    pdf_files = list(source_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {source_dir}")
        return

    print(f"Found {len(pdf_files)} PDF files. Starting compression...\n")

    # 3. Loop through and compress each file
    for pdf_path in pdf_files:
        input_file = str(pdf_path)
        output_file = str(output_dir / pdf_path.name)
        
        command = [
            gs_cmd,
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            f'-dPDFSETTINGS={quality[compression_level]}',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            f'-sOutputFile={output_file}',
            input_file
        ]

        print(f"Compressing: {pdf_path.name}")
        try:
            initial_size = os.path.getsize(input_file) / (1024 * 1024)
            
            # Run Ghostscript
            subprocess.run(command, check=True)
            
            final_size = os.path.getsize(output_file) / (1024 * 1024)
            reduction = ((initial_size - final_size) / initial_size) * 100
            
            print(f"  -> Reduced from {initial_size:.2f} MB to {final_size:.2f} MB ({reduction:.1f}% smaller)\n")
            
        except subprocess.CalledProcessError:
            print(f"  -> Error: Ghostscript failed on {pdf_path.name}.\n")
        except FileNotFoundError:
            print("\nError: Ghostscript is not installed or not in your system PATH.")
            print("Please install Ghostscript from https://ghostscript.com/releases/gsdnld.html")
            return

    print(f"All done! You can find your compressed files here: {output_dir}")

# Your specific folder path
my_folder = r"Your PDF Directory"

# Run the batch process
batch_compress_pdfs(my_folder, compression_level=3)
