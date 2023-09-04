import io

import unicodedata
import zipfile
from xml.etree.ElementTree import XML

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

# ############################################################################
# Method that extract text from MS XML Word document (.docx).
# (Inspired by python-docx <https://github.com/mikemaccana/python-docx>)
# ############################################################################

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'


def extract_text_from_docx(content):
    """Take the path of a docx file or bytes object as argument,
    return the text in unicode."""
    document = zipfile.ZipFile(format_content(content))
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n\n'.join(paragraphs)

# ############################################################################
# Extract text from old word format: .doc
# ############################################################################


def extract_text_from_doc(content, encoding='utf-8'):
    if isinstance(content, bytes):
        return io.BytesIO(content).getvalue().decode(encoding)
    elif isinstance(content, str):
        return open(content, 'rb').read().decode(encoding)
    else:
        raise ValueError('Invalid argument type')

# ############################################################################
# Extract text from pfd files
# ############################################################################


def extract_text_from_pdf_by_page(content):
    content = format_content(content)
    for page in PDFPage.get_pages(content,
                                  caching=True,
                                  check_extractable=True):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()
        yield text

        # close open handles
        converter.close()
        fake_file_handle.close()


def extract_text_from_pdf(content):
    text = ''
    for page in extract_text_from_pdf_by_page(content):
        text += page
    return unicodedata.normalize("NFKD", text) \
        .replace('й', 'й') \
        .replace('Й', 'Й') \
        .replace('ё', 'ё') \
        .replace('Ё', 'Ё')


def format_content(content):
    if isinstance(content, bytes):
        return io.BytesIO(content)
    elif isinstance(content, str):
        return open(content, 'rb')
    else:
        raise ValueError('Invalid argument type')


if __name__ == '__main__':
    pass
