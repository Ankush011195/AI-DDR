import fitz
import os

def extract_from_pdf(pdf_path, output_image_folder):
    os.makedirs(output_image_folder, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    full_text = ""
    image_paths = []
    
    total_pages = len(doc)
    
    # Pehle 2 pages skip karo (form/cover pages hote hain)
    start_page = 2
    
    for page_num in range(start_page, total_pages):
        page = doc[page_num]
        
        # Text extract karo
        full_text += f"\n--- Page {page_num + 1} ---\n"
        full_text += page.get_text()
        
        # Poora page screenshot ki tarah save karo
        mat = fitz.Matrix(1.5, 1.5)
        pix = page.get_pixmap(matrix=mat)
        
        image_filename = f"page{page_num+1}.png"
        image_full_path = os.path.join(output_image_folder, image_filename)
        pix.save(image_full_path)
        
        image_paths.append({
            "path": image_full_path,
            "page": page_num + 1,
            "filename": image_filename
        })
    
    doc.close()
    return full_text, image_paths