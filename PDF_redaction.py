import PyPDF2
import os

def redact_pdf(input_pdf, output_pdf, redactions):
    """
    Redacts the specified text in the input PDF and saves the result to the output PDF.

    Args:
        input_pdf: The path to the input PDF file.
        output_pdf: The path to the output PDF file.
        redactions: A list of tuples, where each tuple contains the page number, start position, and end position of the text to redact.
    """

    if not os.path.exists(input_pdf):
        print(f"Error: File not found - {input_pdf}")
        return

    with open(input_pdf, 'rb') as input_file:
        reader = PyPDF2.PdfReader(input_file)

        writer = PyPDF2.PdfWriter()
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            for start_pos, end_pos in redactions.get(page_num, []):
                page.add_text(start_pos, end_pos, '')
            writer.add_page(page)

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_pdf)

# Example usage
input_pdf = 'src\input.pdf'
output_pdf = 'output.pdf'
redactions = {
    0: [(100, 200), (300, 400)],
    1: [(50, 100)]
}

redact_pdf(input_pdf, output_pdf, redactions)