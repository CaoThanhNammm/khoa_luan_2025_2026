import time
from Chat import Chat
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
    model_name_25_flash = os.getenv('MODEL_25_FLASH')

    api_key_agent = os.getenv('API_KEY_AGENT')
    api_key_generator = os.getenv('API_KEY_GENERATOR')
    api_key_valid = os.getenv('API_KEY_VALID')
    api_key_commentor = os.getenv('API_KEY_COMMENTOR')
    pre_processing = PreProcessing()

    t = 5

    gemini_agent = Gemini(model_name_15_flash, api_key_agent)
    gemini_generator = Gemini(model_name_25_flash, api_key_generator)
    gemini_valid = Gemini(model_name_15_flash, api_key_valid)
    gemini_commentor = Gemini(model_name_15_flash, api_key_commentor)
    chat = Chat(t, gemini_agent, gemini_generator, gemini_valid, gemini_commentor, pre_processing)
    question = [
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
    file_name = 'my_qa_human_updated_13.csv'
    for q in question:
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




