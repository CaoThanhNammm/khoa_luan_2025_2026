from dotenv import load_dotenv
load_dotenv()
import os
import pdfplumber

def read_chunks(data_path, footer_height=40):
    all_pages_text = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, data_path)

    pdf_files = [f for f in os.listdir(data_path) if f.lower().endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(data_path, pdf_file)

        try:
            with pdfplumber.open(pdf_path) as pdf:
                num_pages = len(pdf.pages)
                start_page = 9
                end_page = num_pages - 2

                # Duyệt qua các trang theo nhóm 3
                for i in range(start_page, end_page + 1, 3):
                    group_text = []
                    group_pages = []

                    # Lấy tối đa 3 trang liên tiếp
                    for j in range(i, min(i + 3, end_page + 1)):
                        page = pdf.pages[j]
                        page_height = page.height

                        # Chỉ cắt bỏ footer
                        cropped_page = page.within_bbox(
                            (0, 0, page.width, page_height - footer_height)
                        )
                        text = cropped_page.extract_text()
                        if text:
                            group_text.append(text)
                            group_pages.append(j + 1)  # Số trang người dùng thấy (bắt đầu từ 1)

                    if group_text:  # Chỉ thêm nếu có text
                        all_pages_text.append('\n'.join(group_text))
        except Exception as e:
            print(f"Lỗi khi xử lý file {pdf_file}: {str(e)}")

    return all_pages_text

a = read_chunks('data')
print(a)