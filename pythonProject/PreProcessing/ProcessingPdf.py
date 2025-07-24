from dotenv import load_dotenv
load_dotenv()
import pdfplumber
import os

class PDF:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    # đọc tất cả file pdf trong thư mục {data_path}. Mỗi lần đọc 3 trang
    # trả về danh sách các nội dung bao gồm của 3 trang được ghép thành 1
    def read_chunks_stsv(self, footer_height=40):
        all_pages_text = []
        script_dir = os.path.dirname(os.path.abspath(__file__))

        data_path = os.path.join(script_dir, self.folder)
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

    def read_chunks(self):
        all_pages_text = []

        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                num_pages = len(pdf.pages)

                # Duyệt qua các trang, mỗi nhóm 2 trang
                for i in range(0, num_pages, 2):
                    group_text = []

                    for j in range(i, min(i + 2, num_pages)):
                        page = pdf.pages[j]
                        text = page.extract_text()
                        if text:
                            group_text.append(text)

                    if group_text:
                        all_pages_text.append('\n'.join(group_text))
        except Exception as e:
            print(f"Lỗi khi xử lý file {self.pdf_path}: {str(e)}")

        return all_pages_text


