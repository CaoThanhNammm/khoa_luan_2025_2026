import ast

llm_output = """
{
'đoạn 1': 'Bốn là, các Bộ, ngành, địa phương thực hiện quyết liệt các nhiệm vụ, giải pháp thúc đẩy giải ngân vốn đầu tư công những tháng cuối năm 2024 theo chỉ đạo của Thủ tướng Chính phủ quy định tại Chỉ thị số 26/CT-TTg ngày 08/8/2024, thu hút đầu tư nước ngoài chất lượng cao.',
'đoạn 2': 'Tập trung thúc đẩy tiến độ thi công các dự án quan trọng quốc gia, các công trình trọng điểm, nhất là các công trình hạ tầng giao thông quan trọng; phát huy nguồn lực đầu tư của các tập đoàn, doanh nghiệp Nhà nước; thu hút, sử dụng hiệu quả nguồn lực khu vực tư nhân, khu vực nước ngoài.',
'đoạn 3': 'Tích cực, chủ động thu hút FDI có chọn lọc, bảo đảm chất lượng; chú trọng chuyển giao công nghệ, liên kết với doanh nghiệp trong nước và tham gia vào chuỗi cung ứng khu vực, toàn cầu.',
'đoạn 4': 'Năm là, tháo gỡ khó khăn, vướng mắc trong thủ tục hành chính, quy định pháp lý nhằm cải thiện môi trường đầu tư kinh doanh; hỗ trợ giảm chi phí cho doanh nghiệp.',
'đoạn 5': 'Tiếp tục thực hiện các chính sách miễn, giảm, gia hạn thuế, phí như thuế giá trị gia tăng, thuế thu nhập doanh nghiệp, thuế tiêu thụ đặc biệt, thuế bảo vệ môi trường và tiền thuê đất…',
'đoạn 6': 'Sáu là, đẩy mạnh triển khai các chương trình, giải pháp hỗ trợ doanh nghiệp đổi mới sáng tạo, thúc đẩy chuyển đổi số, đặc biệt là chuyển đổi số bao trùm, “chuyển đổi kép”',
'đoạn 7': 'Chương trình hỗ trợ doanh nghiệp khu vực tư nhân kinh doanh bền vững giai đoạn 2022-2025 nhằm thúc đẩy phát triển các mô hình kinh doanh bền vững, kinh doanh bao trùm, hướng tới dịch chuyển cơ cấu nền kinh tế theo hướng tăng cường kinh tế số và xanh, bao trùm.'
}
"""
all_paragraphs = []
parsed_dict = ast.literal_eval(llm_output)
print(parsed_dict.items())
