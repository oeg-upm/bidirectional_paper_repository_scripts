import os

def find_tex_with_includepdf(start_dir):
    valid_merged = []
    valid_merged_count = 0
    invalid_merge = []
    invalid_merge_count = 0
    valid_include_pdfs = []
    valid_include_pdfs_count = 0
    invalid_include_pdfs = []
    invalid_include_pdf_count = 0

    for root, dirs, files in os.walk(start_dir):
        if 'merged.tex' in files:
            file_path = os.path.join(root, 'merged.tex')
            with open(file_path, 'r') as file:
                content = file.read()
                if "\\title" in content or "\\abstract" in content:
                    valid_merged.append(file_path)
                    valid_merged_count += 1
                    if "\\includepdf" in content:
                        valid_include_pdfs.append(file_path)
                        valid_include_pdfs_count += 1
                else:
                    invalid_merge.append(file_path)
                    invalid_merge_count += 1
                    if '\\includepdf' in content:
                        invalid_include_pdfs.append(file_path)
                        invalid_include_pdf_count += 1

    with open('./valid_merge/valid_merge_results.txt', 'w') as f:
        f.write(f"Total number of valid merged.tex files: {valid_merged_count}\n")
        f.write("Valid merged.tex files:\n")
        for file in valid_merged:
            f.write(file + "\n")

    with open('./valid_merge/invalid_merge_results.txt', 'w') as f1:
        f1.write(f"Total number of Invalid merged.tex files: {invalid_merge_count}\n")
        f1.write("Invalid merged.tex files:\n")
        for file in invalid_merge:
            f1.write(file + "\n")

    with open('./valid_merge/merge_with_valid_include_pdfs.txt', 'w') as f2:
        f2.write(f"All valid merged.tex files that had \\includepdf: {valid_include_pdfs_count}\n")
        for file in valid_include_pdfs:
            f2.write(file + "\n")

    with open('./valid_merge/merge_with_invalid_include_pdfs.txt', 'w') as f3:
        f3.write(f"All invalid merged.tex files that had \\includepdf: {invalid_include_pdf_count}\n")
        for file in invalid_include_pdfs:
            f3.write(file + "\n")

    return {
        'valid_merged': valid_merged_count,
        'invalid_merge': invalid_merge_count,
        'valid_include_pdfs': valid_include_pdfs_count,
        'invalid_include_pdfs': invalid_include_pdf_count
    }

# Usage
matched_files = find_tex_with_includepdf('.')
print(matched_files)

