import re
import time

from langchain_core.prompts import PromptTemplate
from Chat import Chat
from LLM import prompt
from LLM.Gemini import Gemini
import os
from dotenv import load_dotenv
load_dotenv()
from PreProcessing.PreProcessing import PreProcessing
import pandas as pd

if __name__ == "__main__":
    qa = pd.read_csv(r'D:/PycharmProjects/pythonProject/qa_human_hybrid.csv')
    # 1. khởi tạo gemini và chat
    model_name_15_flash = os.getenv('MODEL_15_FLASH')
    model_name_20_flash = os.getenv('MODEL_20_FLASH')

    api_key_agent = os.getenv('API_KEY_AGENT')
    api_key_generator = os.getenv('API_KEY_GENERATOR')
    api_key_valid = os.getenv('API_KEY_VALID')
    api_key_commentor = os.getenv('API_KEY_COMMENTOR')
    pre_processing = PreProcessing()

    t = 6

    gemini_agent = Gemini(model_name_15_flash, api_key_agent)
    gemini_generator = Gemini(model_name_20_flash, api_key_generator)
    gemini_valid = Gemini(model_name_15_flash, api_key_valid)
    gemini_commentor = Gemini(model_name_15_flash, api_key_commentor)
    chat = Chat(t, gemini_agent, gemini_generator, gemini_valid, gemini_commentor, pre_processing)
    question = [
        "Trường yêu cầu điểm thi kết thúc học phần tối thiểu chiếm bao nhiêu?",
        "Bao nhiêu phần trăm điểm học phần phải là từ thi kết thúc học phần?",
        "Khi nào sinh viên được nhận điểm I?",
        "Sinh viên vắng mặt trong buổi thi vì ốm có thể nhận điểm gì?",
        "Điểm nào được ghi nếu sinh viên không thể thi vì tai nạn?",
        "Ai là người rà soát và đề xuất danh sách học phần công nhận tương đương?",
        "Ai là người xem xét và lập danh sách học phần tương đương?",
        "Ai thực hiện việc kiểm tra và đề xuất các học phần tương đương?",
        "Ai đảm nhiệm việc rà soát học phần được công nhận?",
        "Ai phê duyệt danh sách học phần được công nhận từ cơ sở đào tạo khác?",
        "Ai có quyền phê duyệt học phần tương đương?",
        "Tối đa bao nhiêu phần trăm khối lượng học tập được phép chuyển đổi?",
        "Tối đa bao nhiêu % khối lượng chương trình được công nhận từ nơi khác?",
        "Tối đa bao nhiêu phần chương trình được xét công nhận tương đương?",
        "Tối đa có thể công nhận bao nhiêu phần trăm học phần từ nơi khác?",
        "Có thể chuyển đổi tối đa bao nhiêu phần trăm học phần?",
        "Sinh viên nhận điểm gì khi học phần được công nhận tương đương?",
        "Sinh viên cần làm gì trước khi học tại cơ sở đào tạo khác?",
        "Sinh viên phải thực hiện bước nào khi muốn học nơi khác?",
        "Để được học ở cơ sở khác, sinh viên cần làm gì trước?",
        "Sinh viên phải làm gì trước khi được phép học tại nơi khác?",
        "Để được công nhận học phần từ nơi khác, sinh viên cần gì?",
        "Sinh viên cần nộp gì để công nhận kết quả từ nơi khác?",
        "Cách chuyển đổi điểm chữ sang điểm số như thế nào?",
        "Học lực sinh viên được phân loại như thế nào?",
        "Sinh viên được xếp trình độ năm học dựa trên yếu tố nào?",
        "Việc xác định năm học của sinh viên phụ thuộc vào yếu tố nào?",
        "Học phần nào được xem là đã tích lũy trong kết quả học tập?",
        "Thời hạn nộp điểm học phần về Phòng Đào tạo là bao lâu kể từ ngày thi?",
        "Điểm học phần phải được nộp về Phòng Đào tạo trong thời gian bao lâu sau ngày thi?",
        "Sau ngày thi, giảng viên có bao lâu để nộp điểm học phần về Phòng Đào tạo?",
        "Kể từ ngày thi, thời gian tối đa để gửi điểm học phần về Phòng Đào tạo là bao lâu?",
        "Trong bao lâu sau ngày thi, điểm học phần cần được nộp về Phòng Đào tạo theo quy định?",
        "Sinh viên có thể xem kết quả học tập của mình ở đâu vào cuối mỗi học kỳ?",
        "Sinh viên có thể kiểm tra kết quả học tập cuối học kỳ ở nơi nào?",
        "Đâu là nơi sinh viên xem được kết quả học tập của mình sau mỗi học kỳ?",
        "Cuối mỗi học kỳ, kết quả học tập của sinh viên được đăng tải ở đâu?",
        "Hậu quả của việc sinh viên bị xếp loại rèn luyện kém trong cả năm học là gì?",
        "Sinh viên có điểm rèn luyện kém cả năm sẽ bị xử lý ra sao?",
        "Nếu sinh viên bị xếp loại rèn luyện kém cả năm, điều gì sẽ xảy ra?",
        "Nếu không được Hiệu trưởng cho phép, sinh viên cần đăng ký ít nhất bao nhiêu tín chỉ trong học kỳ chính để tránh bị cảnh báo học tập?",
        "Không được Hiệu trưởng chấp thuận, sinh viên phải đăng ký bao nhiêu tín chỉ trong học kỳ chính để không bị cảnh báo?",
        "Số tín chỉ tối thiểu sinh viên cần đăng ký trong học kỳ chính để tránh cảnh báo học tập, nếu không có phép của Hiệu trưởng, là bao nhiêu?",
        "Sinh viên bị buộc thôi học nếu tổng số tín chỉ nợ đọng từ đầu khóa học vượt quá bao nhiêu?",
        "Bao nhiêu tín chỉ nợ đọng từ đầu khóa học sẽ khiến sinh viên bị buộc thôi học?",
        "Điểm trung bình chung tích lũy tối thiểu để sinh viên được nhận đề tài khóa luận là bao nhiêu?",
        "Để được nhận đề tài khóa luận, điểm trung bình chung tích lũy tối thiểu của sinh viên là bao nhiêu?",
        "Điểm trung bình tích lũy tối thiểu để sinh viên đủ điều kiện làm khóa luận là bao nhiêu?",
        "Sinh viên phải có điểm trung bình chung tích lũy bao nhiêu để được làm khóa luận?",
        "Thời điểm phân công đề tài khóa luận thường diễn ra khi nào?",
        "Đề tài khóa luận thường được phân công vào thời điểm nào trong chương trình đào tạo?",
        "Khi nào đề tài khóa luận được phân công cho sinh viên?",
        "Phân công đề tài khóa luận diễn ra vào thời gian nào trong khóa học?",
        "Sinh viên được phân công đề tài khóa luận vào lúc nào?",
        "Sinh viên phải nộp bao nhiêu cuốn báo cáo khóa luận có xác nhận của giảng viên hướng dẫn?",
        "Số lượng báo cáo khóa luận mà sinh viên cần nộp với xác nhận của giảng viên hướng dẫn là bao nhiêu?",
        "Để báo cáo khóa luận, sinh viên phải nộp bao nhiêu cuốn có xác nhận từ giảng viên hướng dẫn?",
        "Bao nhiêu cuốn báo cáo khóa luận có xác nhận của giảng viên hướng dẫn mà sinh viên phải nộp?",
        "Thời gian tối đa để sinh viên trình bày tóm tắt kết quả khóa luận trước hội đồng là bao lâu?",
        "Sinh viên được phép trình bày tóm tắt khóa luận trong bao nhiêu phút trước hội đồng?",
        "Thời gian giới hạn để sinh viên trình bày kết quả khóa luận trước hội đồng là bao lâu?",
        "Sinh viên có tối đa bao nhiêu phút để trình bày tóm tắt khóa luận trước hội đồng đánh giá?",
        "Bao nhiêu phút là thời gian tối đa cho sinh viên trình bày khóa luận trước hội đồng?",
        "Sinh viên được gia hạn thời gian thực hiện đề tài khóa luận tối đa bao nhiêu lần?",
        "Số lần tối đa sinh viên có thể xin gia hạn làm khóa luận là bao nhiêu?",
        "Sinh viên có thể gia hạn thực hiện khóa luận bao nhiêu lần theo quy định?",
        "Số đề tài khóa luận tối đa mà một giảng viên hướng dẫn độc lập có thể nhận mỗi lớp mỗi đợt là bao nhiêu?",
        "Sinh viên được xét và công nhận tốt nghiệp vào những tháng nào trong năm?",
        "Thời điểm nào trong năm trường xét và công nhận tốt nghiệp cho sinh viên?",
        "Điểm trung bình tích lũy tối thiểu để sinh viên được xét tốt nghiệp là bao nhiêu?",
        "Thời hạn tối đa để Hiệu trưởng cấp bằng tốt nghiệp sau khi sinh viên đủ điều kiện là bao lâu?",
        "Thời gian tối đa để cấp bằng tốt nghiệp sau khi sinh viên hoàn thành điều kiện là bao lâu?",
        "Nếu không tốt nghiệp, sinh viên nhận được chứng nhận gì?",
        "Sinh viên không đủ điều kiện tốt nghiệp được cấp chứng nhận gì?",
        "Loại chứng nhận nào được cấp cho sinh viên không tốt nghiệp?",
        "Hội đồng xét tốt nghiệp Khoa phải chuyển biên bản xét tốt nghiệp về trường trước ngày nào?",
        "Biên bản xét tốt nghiệp của Khoa phải được gửi về trường trước ngày nào trong các tháng 3, 6, 9, 12?",
        "Trước ngày nào, Hội đồng xét tốt nghiệp Khoa cần nộp biên bản xét tốt nghiệp cho trường?",
        "Sinh viên phải báo sai sót trong danh sách tốt nghiệp trong bao lâu kể từ ngày công bố?",
        "Thời gian tối đa để sinh viên báo lỗi trong danh sách tốt nghiệp sau khi công bố là bao lâu?",
        "Sinh viên có bao lâu để thông báo sai sót trong danh sách công nhận tốt nghiệp?",
        "Trong bao lâu sau khi danh sách tốt nghiệp được công bố, sinh viên phải báo cáo sai sót?",
        "Sinh viên cần báo sai sót trong danh sách tốt nghiệp trong thời gian bao lâu kể từ ngày công bố?",
        "Để được khen thưởng khi tốt nghiệp, sinh viên không được vi phạm kỷ luật ở mức nào?",
        "Điểm trung bình học tập tích lũy tối thiểu để xét khen thưởng tốt nghiệp là gì?",
        "Sinh viên tốt nghiệp Thủ khoa toàn khóa cần đạt xếp loại rèn luyện tối thiểu là gì?",
        "Để xét Thủ khoa tốt nghiệp, xếp loại rèn luyện của sinh viên phải đạt mức nào?",
        "Sinh viên hệ vừa làm vừa học được xét Thủ khoa tốt nghiệp khi nào?",
        "Thủ khoa tốt nghiệp hệ vừa làm vừa học được xét ở thời điểm nào?",
        "Để xin nghỉ học tạm thời vì lý do cá nhân, điểm trung bình chung tích lũy tối thiểu là bao nhiêu?",
        "Sinh viên muốn quay lại học sau khi thôi học phải làm gì?",
        "Quy trình để sinh viên thôi học quay lại trường là gì?",
        "Sinh viên sau khi thôi học muốn tiếp tục học cần thực hiện bước nào?",
        "Sinh viên cần chuẩn bị gì khi xin nghỉ học tạm thời hoặc thôi học?",
        "Khi nào sinh viên muốn học lại sau thời gian nghỉ tạm thời phải nộp đơn?",
        "Sinh viên sau nghỉ tạm thời muốn học tiếp cần nộp đơn trước học kỳ mới bao lâu?",
        "Điểm trung bình tích lũy tối thiểu để đăng ký chương trình thứ hai nếu xếp loại khá là bao nhiêu?",
        "Sinh viên xếp loại khá cần điểm trung bình tích lũy như thế nào để học chương trình thứ hai?",
        "Sinh viên sẽ bị xóa khỏi danh sách chương trình thứ hai nếu dừng học liên tục bao nhiêu học kỳ?",
        "Bao nhiêu học kỳ liên tiếp dừng học chương trình thứ hai khiến sinh viên bị loại khỏi danh sách?",
        "Để được công nhận sang chương trình thứ hai, học phần từ chương trình thứ nhất cần điểm tối thiểu bao nhiêu?",
        "Học phần từ chương trình thứ nhất cần đạt bao nhiêu điểm để được công nhận cho chương trình thứ hai?",
        "Sinh viên cần đạt điểm học phần tối thiểu bao nhiêu để được công nhận từ chương trình thứ nhất sang chương trình thứ hai?",
        "Sinh viên phải đăng ký chương trình thứ hai muộn nhất bao lâu trước khi xét tốt nghiệp chương trình thứ hai?",
        "Thời gian muộn nhất để đăng ký chương trình thứ hai trước khi xét tốt nghiệp là bao lâu?",
        "Sinh viên cần đăng ký chương trình thứ hai bao lâu trước thời điểm xét tốt nghiệp chương trình này?",
        "Sinh viên muốn học chương trình thứ hai phải làm gì trước mỗi học kỳ chính?",
        "Sinh viên học chương trình thứ hai sau khi tốt nghiệp chương trình thứ nhất được chuyển về đâu quản lý?",
        "Sinh viên học chương trình thứ hai sau tốt nghiệp chương trình thứ nhất thuộc quản lý của đơn vị nào?",
        "Tỷ lệ dạy trực tuyến tại Trường Đại học Nông Lâm TP.HCM không được vượt quá bao nhiêu phần trăm số giờ tín chỉ?",
        "Số giờ dạy trực tuyến tại Trường Đại học Nông Lâm TP.HCM được giới hạn tối đa bao nhiêu phần trăm tín chỉ?",
        "Trường Đại học Nông Lâm TP.HCM quy định tỷ lệ dạy online không vượt quá bao nhiêu phần trăm số giờ tín chỉ?",
        "Tỷ lệ tối đa của giảng dạy trực tuyến so với tổng số giờ tín chỉ tại Trường Đại học Nông Lâm TP.HCM là bao nhiêu?",
        "Giới hạn phần trăm số giờ tín chỉ dành cho dạy trực tuyến tại Trường Đại học Nông Lâm TP.HCM là bao nhiêu?",
        "Điểm đánh giá quá trình học trực tuyến đóng góp tối đa bao nhiêu phần trăm vào điểm học phần?",
        "Quyết định tổ chức thi cuối kỳ trực tuyến hay trực tiếp thuộc về ai?",
        "Người nào có quyền quyết định thi cuối kỳ bằng hình thức trực tuyến hay trực tiếp?",
        "Học phần thực hành đánh giá kỹ năng có được tổ chức thi cuối kỳ trực tuyến không?",
        "Các học phần thực hành kỹ năng có được phép thi cuối kỳ bằng hình thức trực tuyến không?",
        "Học phần thực hành kỹ năng có được thi cuối kỳ trực tuyến theo quy định không?",
        "Việc bảo vệ đồ án trực tuyến cần sự đồng thuận của ai?",
        "Giảng viên phải làm gì trước khi tổ chức lớp học trực tuyến?",
        "Giảng viên cần chuẩn bị gì trước khi bắt đầu lớp học trực tuyến?",
        "Hồ sơ cá nhân của sinh viên có thể bổ sung những gì?",
        "Sinh viên được phép thêm thông tin gì vào hồ sơ cá nhân của mình trên hệ thống?",
        "Sinh viên phải đăng nhập lớp học trực tuyến trước bao lâu so với giờ bắt đầu?",
        "Trước giờ học trực tuyến, sinh viên cần đăng nhập sớm bao lâu?",
        "Sinh viên phải vào lớp học trực tuyến sớm hơn giờ bắt đầu bao nhiêu phút?",
        "Thao tác nào sinh viên cần làm để được phát biểu trong lớp trực tuyến?",
        "Sinh viên được yêu cầu gì về trang phục khi đến trường?",
        "Sinh viên cần ăn mặc thế nào khi đến trường?",
        "Sinh viên cần làm gì để giữ trật tự tại trường?",
        "Thái độ của sinh viên với tài sản công của trường là gì?",
        "Sinh viên cần hành động thế nào để bảo vệ cơ sở vật chất trường?",
        "Quy định về môi trường trường học yêu cầu sinh viên gì?",
        "Sinh viên được yêu cầu ra sao để giữ môi trường trường học?",
        "Sinh viên cần làm gì để bảo vệ môi trường sống tại trường?",
        "Khi nào sinh viên thủ khoa kỳ thi đầu vào được nhận khen thưởng?",
        "Thời điểm khen thưởng thủ khoa kỳ thi tuyển sinh đầu vào là khi nào?",
        "Khoa có dưới 500 sinh viên được chọn bao nhiêu sinh viên tiêu biểu?",
        "Số lượng sinh viên tiêu biểu được chọn ở khoa có dưới 500 sinh viên là bao nhiêu?",
        "Khoa dưới 500 sinh viên được xét bao nhiêu sinh viên tiêu biểu?",
        "Bao nhiêu sinh viên tiêu biểu được chọn ở khoa có quy mô dưới 500 sinh viên?",
        "Khối lượng học phần bắt buộc học lại vượt bao nhiêu phần trăm tổng số tín chỉ làm giảm hạng tốt nghiệp?",
        "Nếu học lại học phần bắt buộc vượt bao nhiêu phần trăm tín chỉ, hạng tốt nghiệp sẽ bị giảm?",
        "Hạng tốt nghiệp bị giảm khi khối lượng học phần bắt buộc học lại vượt quá bao nhiêu phần trăm tín chỉ?",
        "Bao nhiêu phần trăm tín chỉ học lại của học phần bắt buộc làm giảm hạng tốt nghiệp?",
        "Khối lượng học lại học phần bắt buộc vượt mức bao nhiêu phần trăm tổng tín chỉ gây giảm hạng tốt nghiệp?",
        "Từ mức kỷ luật nào trở lên, sinh viên sẽ bị giảm hạng tốt nghiệp?",
        "Sau bao lâu kể từ ngày bị kỷ luật khiển trách, sinh viên được chấm dứt hiệu lực quyết định nếu không tái phạm?",
        "Quyết định kỷ luật khiển trách hết hiệu lực sau bao lâu nếu sinh viên không vi phạm thêm?",
        "Thời gian để chấm dứt hiệu lực kỷ luật khiển trách khi không có vi phạm mới là bao lâu?",
        "Nếu không tái phạm, sinh viên bị khiển trách được khôi phục quyền lợi sau bao lâu?",
        "Quyết định kỷ luật cảnh cáo hết hiệu lực sau bao lâu nếu sinh viên không vi phạm thêm?",
        "Sinh viên bị cảnh cáo được xóa kỷ luật sau bao lâu nếu không có vi phạm mới?",
        "Thời gian để chấm dứt hiệu lực kỷ luật cảnh cáo khi không tái phạm là bao lâu?",
        "Nếu không vi phạm thêm, sinh viên bị cảnh cáo được khôi phục quyền lợi sau bao lâu?",
        "Sinh viên bị đình chỉ học tập cần xuất trình gì khi hết thời hạn để được học tiếp?",
        "Để được học lại sau khi hết thời hạn đình chỉ, sinh viên phải nộp gì?",
        "Đi học muộn hoặc nghỉ học không phép bị xử lý như thế nào?",
        "Hình thức xử lý khi sinh viên đi học muộn hoặc nghỉ học quá số buổi cho phép là gì?",
        "Sinh viên nghỉ học không phép bị trừ bao nhiêu điểm rèn luyện?",
        "Sinh viên gây mất trật tự trong giờ học bị trừ bao nhiêu điểm rèn luyện?",
        "Học thay cho người khác bị xử lý ở mức độ nào?",
        "Sinh viên nhờ người học thay bị kỷ luật ra sao?",
        "Hình thức xử lý khi sinh viên học thay hoặc nhờ học thay là gì?",
        "Sinh viên gian lận thi lần đầu tiên chịu hình thức kỷ luật nào?",
        "Hậu quả khi sinh viên vi phạm gian lận thi lần đầu là gì?",
        "Lần đầu gian lận trong thi, sinh viên bị kỷ luật ra sao?",
        "Vi phạm gian lận thi lần thứ hai dẫn đến hình thức xử lý nào?",
        "Tổ chức gian lận thi lần đầu bị xử lý như thế nào?",
        "Sinh viên tổ chức gian lận thi lần đầu tiên bị kỷ luật ra sao?",
        "Hình thức xử lý khi sinh viên tổ chức gian lận thi lần đầu là gì?",
        "Vi phạm tổ chức gian lận thi lần đầu dẫn đến hậu quả nào?",
        "Lần đầu tổ chức gian lận thi, sinh viên bị xử lý như thế nào?",
        "Vi phạm mang tài liệu trái phép vào phòng thi dẫn đến hậu quả nào?",
        "Chậm nộp học phí không lý do bị xử lý ở mức độ nào?",
        "Hình thức xử lý khi sinh viên không nộp học phí đúng hạn là gì?",
        "Làm hư hỏng tài sản trường bị xử lý như thế nào?",
        "Hình thức xử lý khi sinh viên tàng trữ văn hóa đồi trụy là gì?",
        "Sinh viên tàng trữ sản phẩm đồi trụy có thể bị xử lý như thế nào?",
        "Sử dụng ma túy bị xử lý như thế nào?",
        "Sinh viên sử dụng ma túy chịu hình thức kỷ luật nào?",
        "Vi phạm chứa chấp mại dâm lần đầu bị xử lý ra sao?",
        "Sinh viên chứa chấp mại dâm lần đầu bị xử lý như thế nào?",
        "Vi phạm về đánh nhau bị xử lý ra sao?",
        "Sử dụng văn bằng giả mạo để trúng tuyển bị xử lý như thế nào?",
        "Hình thức xử lý cho các vi phạm không được nêu rõ là gì?",
        "Tiêu chí “Đạo đức tốt” yêu cầu sinh viên có điểm rèn luyện tối thiểu bao nhiêu?",
        "Điểm rèn luyện tối thiểu để đạt tiêu chí “Đạo đức tốt” là bao nhiêu?",
        "Sinh viên cần bao nhiêu điểm rèn luyện để đáp ứng tiêu chí “Đạo đức tốt”?",
        "Tiêu chí “Đạo đức tốt” quy định điểm rèn luyện ở mức nào?",
        "Để đạt “Đạo đức tốt”, sinh viên cần đạt điểm rèn luyện ra sao?",
        "Sinh viên cần đạt điểm trung bình bao nhiêu để đáp ứng “Học tập tốt”?",
        "Sinh viên năm nhất cần điểm đầu vào bao nhiêu để đạt tiêu chí “Học tập tốt”?",
        "Điểm đầu vào tối thiểu cho sinh viên năm nhất đạt “Học tập tốt” là bao nhiêu?",
        "Sinh viên năm nhất cần bao nhiêu điểm đầu vào để đáp ứng “Học tập tốt”?",
        "Điểm đầu vào để sinh viên năm nhất đạt “Học tập tốt” là bao nhiêu?",
        "Sinh viên cần đáp ứng gì để đạt tiêu chí “Thể lực tốt”?",
        "Sinh viên cần sinh hoạt bao lâu trong CLB ngoại ngữ để đáp ứng “Hội nhập tốt”?",
        "Sinh viên hiến máu bao nhiêu lần để được ưu tiên trong “Sinh viên 5 tốt”?",
        "Sinh viên có hành động dũng cảm được khen thưởng từ cấp nào để được ưu tiên xét “Sinh viên 5 tốt”?",
        "Hành động dũng cảm cần được khen thưởng từ cấp nào để ưu tiên xét “Sinh viên 5 tốt”?",
        "Sinh viên có hành động dũng cảm được khen thưởng ở cấp nào để ưu tiên “Sinh viên 5 tốt”?",
        "Sinh viên bị khiển trách được xếp loại rèn luyện tối đa là gì?",
        "Khi bị khiển trách, kết quả rèn luyện của sinh viên bị giới hạn ở mức nào?",
        "Sinh viên chịu kỷ luật khiển trách được xếp loại rèn luyện cao nhất là gì?",
        "Sinh viên bị khiển trách không được xếp loại rèn luyện vượt quá mức nào?",
        "Sinh viên bị cảnh cáo được xếp loại rèn luyện tối đa là gì?",
        "Sinh viên bị cảnh cáo không được xếp loại rèn luyện vượt quá mức nào?",
        "Trong thời gian bị đình chỉ, sinh viên có được chấm điểm rèn luyện không?",
        "Sinh viên bị đình chỉ học tập được xét kết quả rèn luyện hay không?",
        "Sinh viên trong thời gian đình chỉ có được đánh giá rèn luyện không?",
        "Sinh viên bị buộc thôi học có được đánh giá rèn luyện không?",
        "Sinh viên chịu kỷ luật buộc thôi học có được xét rèn luyện không?",
        "Sinh viên bị buộc thôi học được đánh giá kết quả rèn luyện hay không?",
        "Sinh viên có thể thắc mắc qua điện thoại tại Đại học Nông Lâm không?",
        "Thắc mắc bằng cách gọi điện thoại có được phép tại Đại học Nông Lâm không?",
        "Sinh viên gửi đơn kiến nghị cần thực hiện bước nào?",
        "Sinh viên thắc mắc gì với giáo viên giảng dạy?",
        "Sinh viên cần gặp giáo viên giảng dạy để giải quyết vấn đề gì?",
        "Các vấn đề trao đổi với Khoa chuyên môn là gì?",
        "Sinh viên cần gặp Khoa chuyên môn để giải quyết vấn đề gì?",
        "Sinh viên cần làm gì khi gặp vướng mắc đăng ký trực tuyến?",
        "Khi đăng ký trực tuyến có vấn đề, sinh viên cần mang gì đến Phòng Đào tạo?",
        "Vướng mắc đăng ký trực tuyến yêu cầu sinh viên làm gì?",
        "Quy trình xử lý vướng mắc đăng ký trực tuyến là gì?",
        "Sinh viên cần làm gì khi dữ liệu cá nhân trên website trường có thay đổi sau 3 tuần học?",
        "Sinh viên xử lý thay đổi dữ liệu cá nhân trên website sau 3 tuần học ra sao?",
        "Quy trình thông báo thay đổi dữ liệu trên website sau 3 tuần là gì?",
        "Sinh viên cần làm gì nếu mất tài khoản cá nhân hoặc email đăng nhập website trường?",
        "Sinh viên xử lý mất email đăng nhập website trường ra sao?",
        "Quy trình lấy lại tài khoản cá nhân website trường là gì?",
        "Sinh viên cần mang gì đến Phòng Công tác sinh viên khi mất tài khoản?",
        "Phòng Đào tạo xử lý sai sót điểm học phần trong thời gian bao lâu?",
        "Thời gian điều chỉnh điểm học phần sai sót của Phòng Đào tạo là bao lâu?",
        "Sinh viên được sửa điểm học phần sai trong bao lâu?",
        "Phòng Đào tạo cần bao lâu để sửa lỗi điểm học phần?",
        "Sinh viên nhận kết quả phúc khảo điểm thi sau bao lâu?",
        "Ai đủ điều kiện xét học bổng khuyến khích học tập?",
        "Sinh viên nào được nhận học bổng khuyến khích học tập?",
        "Điều kiện để sinh viên được xét học bổng khuyến khích học tập là gì?",
        "Sinh viên học nhiều chương trình được nhận học bổng như thế nào?",
        "Quy định về học bổng cho sinh viên học nhiều chương trình là gì?",
        "Sinh viên học cùng lúc nhiều chương trình được xét học bổng ra sao?",
        "Sinh viên thuộc diện chính sách được xét học bổng ra sao?",
        "Sinh viên diện chính sách có được xét học bổng khuyến khích học tập không?",
        "Sinh viên hưởng trợ cấp xã hội có được nhận học bổng khuyến khích không?",
        "Sinh viên diện ưu đãi có được xét học bổng khuyến khích học tập không?",
        "Quỹ học bổng khối được tính theo công thức nào?",
        "Quy định tính điểm trung bình chung học bổng là gì?",
        "Điều kiện chung để nhận học bổng khuyến khích học tập là gì?",
        "Quy định tín chỉ học kỳ cuối để nhận học bổng là bao nhiêu?",
        "Số tín chỉ tối thiểu để xét học bổng trong học kỳ cuối là bao nhiêu?",
        "Học kỳ cuối cần hoàn thành bao nhiêu tín chỉ để xét học bổng?",
        "Sinh viên học kỳ cuối cần bao nhiêu tín chỉ để đủ điều kiện học bổng?",
        "Tiêu chí tín chỉ cho học kỳ cuối để xét học bổng là gì?",
        "Sinh viên cần gì để đạt học bổng loại Khá?",
        "Quy định mức học bổng loại Khá chương trình đại trà ra sao?",
        "Giá trị học bổng loại Giỏi so với loại Khá chương trình đại trà là gì?",
        "Quy định mức học bổng Giỏi chương trình đại trà là gì?",
        "Mức học bổng Giỏi chương trình đại trà được xác định ra sao?",
        "Quy định mức học bổng Xuất sắc chương trình đại trà là gì?",
        "Học bổng Khá chương trình đại trà có giá trị bao nhiêu?",
        "Mỗi năm học bổng tài trợ có tổng trị giá thế nào?",
        "Học bổng “Đồng hành” có giá trị bao nhiêu mỗi năm?",
        "Hình thức nhận học bổng “Đồng hành” là gì?",
        "Học bổng tài trợ được cấp bao nhiêu lần trong một năm học?",
        "Phòng nào lập danh sách sinh viên xét học bổng sau mỗi học kỳ?",
        "Đơn vị nào phụ trách danh sách xét học bổng khuyến khích?",
        "Ai lập danh sách sinh viên đủ điều kiện học bổng sau học kỳ?",
        "Phòng Công tác sinh viên có vai trò gì trong xét học bổng?",
        "Thứ tự xét học bổng khi nhiều sinh viên cùng loại được quy định thế nào?",
        "Cách xếp ưu tiên sinh viên cùng loại học bổng là gì?",
        "Sinh viên cùng loại học bổng được xét ưu tiên ra sao?",
        "Học bổng được xét thế nào khi dựa vào quỹ khối học bổng?",
        "Hội đồng phân bổ học bổng dựa trên nguyên tắc nào?",
        "Số sinh viên được trường xác nhận vay vốn mỗi năm là bao nhiêu?",
        "Số lượng sinh viên được xác nhận hồ sơ vay vốn mỗi năm là bao nhiêu?",
        "Đại học Nông Lâm hỗ trợ bao nhiêu sinh viên vay vốn hàng năm?",
        "Giấy tờ cần nộp cho bồi thường tai nạn giao thông là gì?",
        "Sinh viên nộp gì để yêu cầu bồi thường tai nạn giao thông?",
        "Giấy tờ cần nộp cho bồi thường tai nạn sinh hoạt là gì?",
        "Sinh viên nộp gì để yêu cầu bồi thường tai nạn sinh hoạt?",
        "Giấy tờ cần nộp cho bồi thường tiêm ngừa bệnh dại là gì?",
        "Sinh viên nộp hồ sơ bảo hiểm tai nạn vào thời gian nào?",
        "Lịch nộp hồ sơ bồi thường bảo hiểm tai nạn ra sao?",
        "Hồ sơ bảo hiểm tai nạn được nộp khi nào?",
        "Sinh viên cần làm gì đối với các trường hợp tai nạn khác?",
        "Sinh viên xử lý hồ sơ tai nạn khác ra sao?",
        "Quy trình bồi thường các tai nạn đặc biệt là gì?",
        "Hậu quả nếu sinh viên không tham gia BHYT là gì?",
        "Sinh viên không tham gia BHYT bị phạt thế nào?",
        "Sinh viên đóng BHYT theo công thức nào?",
        "Quy định tính tiền BHYT cho sinh viên là gì?",
        "Mức BHYT sinh viên phải đóng được xác định ra sao?",
        "Bước thứ hai trong quy trình làm BHYT là gì?",
        "Bước 3 trong quy trình làm BHYT là gì?",
        "Sau khi kê khai thông tin, sinh viên làm gì để làm BHYT?",
        "Sinh viên làm gì sau khi điền thông tin BHYT?",
        "Quy trình làm BHYT ở bước thứ ba là gì?",
        "SV có BHYT do Nhà nước cấp phải cập nhật thông tin ở đâu?",
        "Sinh viên tra cứu thời hạn thẻ BHYT ở đâu?",
        "Website để kiểm tra thời hạn thẻ BHYT là gì?",
        "Sinh viên xem thời hạn sử dụng BHYT tại đâu?",
        "Thời hạn thẻ BHYT được tra cứu ở đâu?",
        "Bước thứ hai khi thanh toán học phí qua BIDV Online là gì?",
        "Sinh viên chọn gì sau khi login BIDV Online?",
        "Quy trình thanh toán học phí qua BIDV Online ở bước 2 là gì?",
        "Quy trình thanh toán học phí qua BIDV Online ở bước 3 là gì?",
        "Quy trình thanh toán học phí qua BIDV Online ở bước 4 là gì?",
        "Sau khi chọn hóa đơn, SV làm gì trên BIDV Online?",
        "Quy trình thanh toán học phí qua BIDV Online ở bước 5 là gì?",
        "Bước thứ hai khi thanh toán học phí qua ATM BIDV là gì?",
        "Sinh viên chọn gì sau khi login ATM BIDV?",
        "Quy trình thanh toán học phí qua ATM BIDV ở bước 2 là gì?",
        "Quy trình thanh toán học phí qua ATM BIDV ở bước 3 là gì?",
        "Quy trình thanh toán học phí qua ATM BIDV ở bước 4 là gì?",
        "Quy định nhà cung cấp thanh toán học phí qua ATM BIDV là gì?",
        "Sinh viên có được đóng học phí bằng chuyển khoản không?",
        "Sau khi điền thông tin, SV làm gì trên website sinh viên?",
        "Bước 5 trong thanh toán qua website sinh viên là gì?",
        "Sau khi xem số tiền, SV làm gì để kết thúc thanh toán website?",
        "Quy trình thanh toán học phí qua website sinh viên ở bước cuối là gì?",
        "Tài khoản đăng nhập bhytsv.hcmuaf.edu.vn là gì?",
        "Quy định đăng nhập website BHYT cho sinh viên là gì?",
        "Những hồ sơ nào được phòng Công tác sinh viên xác nhận?",
        "Giấy tờ sinh viên được xác nhận bao gồm những gì?",
        "Sinh viên đăng ký xác nhận giấy tờ qua kênh nào?",
        "Sinh viên làm thủ tục xác nhận giấy tờ ở đâu?",
        "Địa chỉ đăng ký xác nhận hồ sơ sinh viên là gì?",
        "Website để đăng ký xác nhận giấy tờ cho sinh viên là gì?",
        "Sinh viên sử dụng thiết bị gì để đăng ký xác nhận giấy tờ?",
        "Thiết bị nào dùng để đăng ký xác nhận hồ sơ sinh viên?",
        "Sinh viên cần gì để đăng ký xác nhận giấy tờ trực tuyến?",
        "Đăng ký xác nhận giấy tờ cần thiết bị nào?",
        "Sau khi truy cập website, sinh viên làm gì tiếp theo?",
        "Bước 2 để xác nhận hồ sơ sinh viên là gì?",
        "Bước 3 trong quy trình xác nhận hồ sơ là gì?",
        "Sinh viên làm gì sau khi cập nhật thông tin cá nhân?",
        "Bước 4 để xác nhận hồ sơ sinh viên là gì?",
        "Sau khi kiểm tra thông tin, sinh viên thực hiện gì?",
        "Quy trình xác nhận giấy tờ ở bước thứ tư là gì?",
        "Sau khi sinh viên đăng ký, giấy xác nhận được xử lý ra sao?",
        "Bước 6 trong quy trình xác nhận hồ sơ là gì?",
        "Sau khi giấy được ký, sinh viên làm gì?",
        "Kết quả cài đặt sinh trắc học BIDV Smart Banking là gì?"
    ]

    my_qa = pd.DataFrame(columns=['question', 'answer'])
    file_name = 'my_qa_human_updated_02.csv'
    for q in question:
        print(f'question: {q}')
        time.sleep(60)

        try:
            answer = chat.answer(q)
            new_row = pd.DataFrame({
                'question': [q],
                'answer': [answer]
            })
            my_qa = pd.concat([my_qa, new_row], ignore_index=True)
            if len(my_qa) % 2 == 0:
                my_qa.to_csv(fr"C:\Users\Nam\Desktop\{file_name}", encoding='utf-8-sig')
                print(my_qa)
        except:
            gemini_agent = Gemini(model_name_15_flash, api_key_agent)
            gemini_generator = Gemini(model_name_20_flash, api_key_generator)
            gemini_valid = Gemini(model_name_15_flash, api_key_valid)
            gemini_commentor = Gemini(model_name_15_flash, api_key_commentor)
            chat = Chat(t, gemini_agent, gemini_generator, gemini_valid, gemini_commentor, pre_processing)
            time.sleep(60)

            answer = chat.answer(q)
            new_row = pd.DataFrame({
                'question': [q],
                'answer': [answer]
            })
            my_qa = pd.concat([my_qa, new_row], ignore_index=True)
            if len(my_qa) % 2 == 0:
                my_qa.to_csv(fr"C:\Users\Nam\Desktop\{file_name}", encoding='utf-8-sig')
                print(my_qa)


    my_qa.to_csv(fr"C:\Users\Nam\Desktop\my_qa_human_updated_final", encoding='utf-8-sig')

    # 2. câu hỏi
    # rows = list(qa.itertuples())[:]
    # file_name = f'my_qa_hybrid_grag_1.csv'
    #
    # for row in rows:
    #     question = row.question
    #     if question == 'nan':
    #         continue
    #
    #     prompt_template = PromptTemplate(
    #         input_variables=["question"],
    #         template=prompt.separate_question()
    #     )
    #     formatted_prompt = prompt_template.format(question=question)
    #     answer = gemini_agent.generator(formatted_prompt)
    #     separate_question = pre_processing.string_to_json(answer)
    #     print(f'question: {question}')
    #     answer_child = ""
    #     for attr in separate_question:
    #         time.sleep(60)
    #         question_child = separate_question[attr]
    #
    #         try:
    #             answer_child += chat.answer(question_child)
    #         except:
    #             time.sleep(60)
    #             gemini = Gemini(model_name, api_key)
    #             chat = Chat(t, gemini, pre_processing)
    #             answer_child += chat.answer(question_child)
    #
    #
    #         prompt_template = PromptTemplate(
    #             input_variables=["question", 'answer'],
    #             template=prompt.summary_answer()
    #         )
    #         formatted_prompt = prompt_template.format(question=question, answer=answer_child)
    #         answer_child = gemini_agent.generator(formatted_prompt)
    #
    #     new_row = pd.DataFrame({
    #         'question': [question],
    #         'answer': [answer_child]
    #     })
    #
    #     my_qa = pd.concat([my_qa, new_row], ignore_index=True)
    #     if len(my_qa) % 2 == 0:
    #         print(my_qa)
    #         print("save")
    #         my_qa.to_csv(fr"C:\Users\Nam\Desktop\{file_name}", encoding='utf-8-sig')
    #
    # my_qa.to_csv(r"C:\Users\Nam\Desktop\my_qa_final.csv", encoding='utf-8-sig')


    # 3. trả lời
    # prompt_template = PromptTemplate(
    #     input_variables=["question"],
    #     template=prompt.criteria_complete_question()
    # )
    # formatted_prompt = prompt_template.format(question=question)
    # criteria = gemini.generator(formatted_prompt)
    # criteria = pre_processing.string_to_json(criteria)
    # result = ""
    # for c in criteria['criteria']:
    #     result += f'{c}: {chat.answer(c)} \n'
    # result = re.sub(r'\s+', ' ', result).strip()
    # prompt_template = PromptTemplate(
    #     input_variables=["question", "answer"],
    #     template=prompt.summary_answer()
    # )
    # formatted_prompt = prompt_template.format(question=question, answer=result)
    # answer = gemini.generator(formatted_prompt)




    # print(chat.retrieval_graph(question))
    # print('---------------------------------------')
    # print(chat.retrieval_text(question))
    # """
    #     1. nhận 1 câu hỏi q, khởi tạo f0
    #     2. đưa vào llm với prompt first decision => return vector or graph at
    #     3. if(vector):
    #             truy xuat vao vector
    #         if(graph):
    #             truy xuat vao graph
    #         return ve 1 cau tra loi Xt
    #     4. đưa câu hỏi q và cau tra loi Xt vào llm với prompt generator => return về câu trả lời y^
    #     5. đưa câu hỏi q, câu trả lời y^, Xt vào llm với prompt validator nếu True => return câu trả lời y^
    #     Nếu không tới B6
    #     6. đưa câu hỏi q và hành động at vào llm với prompt commentor => return về ft, gán f0 thành ft
    # """


    # # câu hỏi q, csdl D, số lần lặp T
    # # khởi tạo phản hồi ban đầu
    # f0 = ""
    # # số lần lặp
    # t = 10
    # for i in t:
    #     # xác định hành dộng dựa trên câu hỏi và hành động trước đó
    #     at = Agent(q, f(t-1))
    #     Xt = retrievalbank(q, at, D)
    #     y mu t = generator(q, Xt)
    #     if Cval(q, y mu t, Xt):
    #         return y mu t
    #     else:
    #         f0 = Ccom(q, at)

    first_decision_stsv_function = {
        'name': "first_decision_stsv",
        'description': "Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu. Với câu hỏi sau, hãy trích xuất thông tin từ câu hỏi theo yêu cầu. Quy tắc: 1. Thông tin quan hệ phải đến từ các loại quan hệ đã cho. 2. Mỗi thực thể phải có chính xác một danh mục trong ngoặc đơn. Với câu hỏi sau, dựa trên loại thực thể và loại quan hệ, hãy trích xuất các thực thể chủ đề và các quan hệ hữu ích từ câu hỏi. Loại thực thể: [phần 1: nlu - định hướng, trường đại học nghiên cứu, quá trình hình thành và phát triển, sứ mạng, tầm nhìn, giá trị cốt lõi, mục tiêu chiến lược, cơ sở vật chất, các đơn vị trong trường, các khoa - ngành đào tạo, tuần sinh hoạt công dân - sinh viên, hoạt động phong trào sinh viên, câu lạc bộ (clb) - đội, nhóm, cơ sở đào tạo], [phần 2: học tập và rèn luyện, quy chế sinh viên, quy chế học vụ, quy định về việc đào tạo trực tuyến, quy định khen thưởng, kỷ luật sinh viên, quy chế đánh giá kết quả rèn luyện, quy tắc ứng xử văn hóa của người học, cố vấn học tập, danh hiệu sinh viên 5 tốt, danh hiệu sinh viên tiêu biểu], [phần 3: hỗ trợ và dịch vụ, quy định phân cấp giải quyết thắc mắc của sinh viên, thông tin học bổng, vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên, quy trình xác nhận hồ sơ sinh viên, hồ sơ yêu cầu bồi thường bảo hiểm tai nạn sinh viên, thông tin về bảo hiểm y tế, hướng dẫn sử dụng các kênh thanh toán học phí, bhyt, lệ phí xét tốt nghiệp, tham vấn tâm lý học đường, trung tâm dịch vụ sinh viên, trường đại học nông lâm tp.hồ chí minh, 12 phòng ban, 07 trung tâm, 01 viện nghiên cứu, 12 khoa đào tạo chuyên môn, 01 khoa cơ bản, phòng công tác sinh viên, ...]. Loại quan hệ: [website, có, là, tôn_trọng, theo, hủy, in, dưới, bị, mời, đối_với, của, gửi, không, gồm, trong, từ, email, công_bố, BAO_GỒM, sở_hữu, số_điện_thoại, thuộc_khoa, chương_trình_tiên_tiến_tại, chương_trình_nâng_cao_tại, chương_trình_đào_tạo_tại, quản_lý_bởi, chủ_nhiệm, trưởng_ban_điều_hành, đội_trưởng, số_lượng_sách, sử_dụng, số_lượng_phòng, sức_chứa, bao_gồm, về, sánh_vai, trên, đổi_mới, thúc_đẩy, phát_huy, xây_dựng, trở_thành, hàng_đầu, đáp_ứng, tầm_nhìn, tên_khác, trực_thuộc, tọa_lạc_tại, thuộc, thời_gian_hoạt_động, nhận_giải_thưởng, thành_lập, phục_vụ, đào_tạo, và, mục_tiêu_đến, sẽ_trở_thành, với, tổ_chức_bởi, được_đăng_tại, gìn_giữ_và_phát_huy, phát_hiện, nâng_đỡ, cho, đề_cao, hoạt_động_của, dành_cho, hỗ_trợ, tư_vấn, phù_hợp, hướng_dẫn, đăng_ký, ở, điều_chỉnh, xác_nhận, theo_dõi, cập_nhật_trên, không_dưới, ít_nhất, xem_xét, cấp, tham_gia, trường, tổ_chức, vào_cuối, tuyên_dương, khen_thưởng, căn_cứ, đánh_giá, phòng_chống, đạt, thang_điểm, chấp_hành, đến, không_vượt_quá, đánh_giá_qua, đoạt_giải, có_thành_tích, đóng_góp, hoạt_động_tại, thực_hiện, bảo_đảm_an_ninh, ít_hơn_hoặc_bằng, chọn, cao_nhất, cao_thứ_hai, bằng_nhau, công_nhận, xét, áp_dụng_bởi, thông_báo, gửi_thông_báo, làm, tham_dự, sau, chấm_dứt, trừ, vô_lễ, lần_1, giao_cho, hạ_điểm, tài_sản_trong, làm_hư_hỏng, lần_2, lần_3, trái, xâm_phạm, chống_phá, thu_hồi, lắng_nghe, hoàn_thành, nghiêm_túc, phát_động, hỏi, trả_lời, làm_phiền, quan_hệ, không_gây_ồn_ào, giữ_gìn, cung_cấp, nhận, dấu_và_chữ_ký, truy_cập, nhập, thanh_toán, hiển_thị, lưu, tại, tương_ứng, phản_hồi, đăng_nhập, chụp_ảnh, quét, đọc, lấy_ảnh, kiểm_tra, trạng_thái, chuyển_tới, viết, trực_tuyến, không_chấp_nhận, nộp, trao_đổi, thắc_mắc, đề_nghị, mang, được_hỗ_trợ, đi_học, chưa_được_sửa, mất, giúp_đỡ, nêu, hoặc, ghi, chuyển, ký, đã, kèm, giải_quyết, loại, bổ_sung, cập_nhật, trình_ký, đóng_dấu, hoạt_động, liên_hệ, như, cùng, xếp, so_sánh, không_cần, bằng, bố_trí, trọng_số, không_bị, quyết_định, cao_hơn, hơn, lập, trình, làm_tròn, trích_từ, do, phối_hợp, trị_giá, một_lần, qua, mỗi, đóng_mộc, sửa_đổi, mã, nhân, tra_cứu, quản_lý, điện_thoại, thành_lập_từ, vay, để, giúp, thủ_tục, gặp_khó_khăn, cư_trú, sinh_sống, đủ_tiêu_chuẩn, tối_đa, lãi_suất, thông_qua, trả_nợ, đóng_trụ_sở, tuân_thủ_quy_định_của, học_tập_tại, được_tôn_trọng_bởi, được_cung_cấp, được_sử_dụng, hoạt_động_trong, kiến_nghị_với, đề_đạt_nguyện_vọng_lên, được_ở, được_nhận, tuân_thủ_chủ_trương_của, tuân_thủ_pháp_luật_của, tuân_thủ_quy_chế_của, đóng, không_được_xúc_phạm, không_được_tham_gia, không_được, không_được_tổ_chức_hoạt_động_mà_chưa_được_cho_phép, cung_cấp_ctđt_cho, tư_vấn_xây_dựng_khht_cho, thông_báo_học_phần_cho, hướng_dẫn_đăng_ký_cho, thực_hiện_theo, đăng_ký_học_lại, cải_thiện_điểm, cho_phép_đăng_ký_ít_hơn_14_tín_chỉ, rút, không_đi_học, không_dự_thi, nhận_điểm_r, nhận_điểm_f, rút_học_phần_trên, đề_xuất_hủy_hoặc_mở_thêm, đăng_ký_trực_tuyến, công_bố_kết_quả_đăng_ký_cho, cải_thiện_kết_quả, đề_xuất, duy_trì, phê_duyệt_duy_trì, đề_xuất_mở_thêm, chấp_thuận_mở_thêm, mở_thêm, dự_thi, đề_xuất_cấm_thi, duyệt_danh_sách_cấm_thi, tối_thiểu, chuẩn, được_quy_định_trong, thông_báo_cho, thông_báo_lịch_thi, hưởng, chấp_thuận, duyệt_đơn, tổ_chức_thi_cho, xét_tương_đương, quy_định, rà_soát, phê_duyệt, xác_định, đồng_ý, không_đạt, tính_vào, xử_lý, xem_kết_quả, được_đánh_giá, tính, không_tính, dựa_vào, trung_bình_cộng, kỷ_luật, không_tham_gia, xếp_loại, lưu_trong, ghi_vào, đình_chỉ, tiêu_chí, cho_phép, chuyển_sang, cấp_bằng, chấm, thỏa_mản, phân_công, tổ_chức_bảo_vệ, thảo_luận, gia_hạn, quyết_định_gia_hạn, không_hoàn_thành, tích_lũy, ra_quyết_định, được_cấp, báo, bảo_lưu, được_điều_động, cần, theo_quy_định, học_xong, nghỉ, được_công_nhận, học, vượt_quá, nghiên_cứu, bổ_sung_vào, tăng_cường, áp_dụng, chỉ_đạo, phát_triển_trên, không_tổ_chức, giữ_bí_mật, bảo_vệ, chịu_trách_nhiệm, trước, nhấn, mở, tắt, bấm, chia_sẻ]. Câu hỏi: {question} Các có tài liệu để trả lời câu hỏi đã cho và mục tiêu là tìm kiếm các tài liệu hữu ích. Mỗi thực thể trong biểu đồ tri thức được liên kết với một tài liệu. Dựa trên các thực thể và quan hệ đã trích xuất, 'graph' hay 'text' hữu ích hơn để thu hẹp không gian tìm kiếm? Bạn phải trả lời bằng một trong hai từ, không quá hai từ.",
        'parameters': {
            "type": "object",
            'required': ["Câu hỏi"],
            'properties': {
                "Câu hỏi": {
                    "type": "string",
                },
            },
        },
    }
    reflection_stsv_function = {
        'name': "reflection_stsv",
        'description': "Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu. Hãy phản hồi dựa trên yêu cầu sau: 1. Nếu feedback là 'Tài liệu đã truy xuất không đúng. Mô-đun truy xuất hiện tại có thể không hữu ích để thu hẹp không gian tìm kiếm.' thì hãy sử dụng nguồn truy xuất khác với bước trước đó. Nếu trước đó dùng 'graph' thì chuyển sang 'text' và ngược lại. Bạn phải trả lời bằng một trong hai từ. Trả lời không quá hai từ. Câu hỏi: {question} feedback: {feedback}",
        'parameters': {
            "type": "object",
            'required': ["Câu hỏi"],
            'properties': {
                "Câu hỏi": {
                    "type": "string",
                },
                "Feedback": {
                    "type": "string",
                },
            },
        },
    }
    generator_stsv_function = {
        'name': "generator_stsv",
        'description': """Nhiệm vụ của bạn là dựa vào câu hỏi và các tài liệu khả thi mà tôi cung cấp, hãy trả lời câu hỏi: Câu hỏi: {question} Tài liệu khả thi: {references} Trả lời ngắn gọn theo tài liệu được cung cấp. Nếu không có thông tin thì trả lời 'Không có thông tin'""",
        'parameters': {
            "type": "object",
            'required': ["Câu hỏi"],
            'properties': {
                "Câu hỏi": {
                    "type": "string",
                },
                "Tài liệu khả thi": {
                    "type": "string",
                },
            },
        },
    }
    valid_stsv_function = {
        'name': "valid_stsv",
        'description': "Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu. Câu hỏi: {question} Câu trả lời: {answer} Tài liệu khả thi: {references} Điểm = 0 Nhiệm vụ của bạn là hãy xem xét: 1. Câu trả lời có đầy đủ ý nghĩa với câu hỏi không? Nếu có +3 điểm, nếu không -3 điểm. 2. Nếu tài liệu không có thông tin để trả lời câu hỏi thì -3 điểm. Nếu có +3 điểm. 3. Nếu câu trả lời có ý nghĩa tương tự như tài liệu không có thông tin chính xác thì -2 điểm. Ngược lại +2 điểm. Nếu: 1. điểm > 0 thì 'yes'. 2. điểm < 0 thì 'no'. Trả lời không quá 2 từ",
        'parameters': {
            "type": "object",
            'required': ["Câu hỏi"],
            'properties': {
                "Câu hỏi": {
                    "type": "string",
                },
                "Câu trả lời": {
                    "type": "string",
                },
                "Tài liệu khả thi": {
                    "type": "string",
                },
            },
        },
    }
    commentor_stsv_function = {
        'name': "commentor_stsv",
        'description': "Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu. Câu hỏi: {question} Tài liệu khả thi: {references} Nếu 'sai tài liệu khả thi': phản hồi 'Tài liệu đã truy xuất không đúng. Mô-đun truy xuất hiện tại có thể không hữu ích để thu hẹp không gian tìm kiếm.'",
        'parameters': {
            "type": "object",
            'required': ["Câu hỏi"],
            'properties': {
                "Câu hỏi": {
                    "type": "string",
                },
                "Tài liệu khả thi": {
                    "type": "string",
                },
            },
        },
    }




