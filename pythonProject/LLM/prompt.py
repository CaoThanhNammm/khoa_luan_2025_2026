""""
1. nhận câu hỏi
2. llm xác dịnh xem nên chọn CSDL nào(agent)
3. vào CSDL đó để truy xuất thông tin(retriever bank)
4. llm sẽ trả lời câu hỏi bằng cách kết hợp câu hỏi và thông tin truy xuất ở 3(generator)
5. llm sẽ valid xem câu trả lời ở 4 nên chấp nhận hay không. Nếu có thì phản hồi và kết thúc quá trình.
nếu không thì tới 6(validator)
6. llm sẽ tiếp tục điều chỉnh hành vi bằng cách tiêp tục chọn CSDL để truy xuất thông tin(commentor)
7. lặp lại cho đến khi rơi vào "có" ở 6(agent)
"""

def agent():
    return """
You are a helpful, pattern-following assistant. Given the following question, extract the information from the question as requested. 
Rules: 
    1. The Relational information must come from the given relational types. 
    2. Each entity must exactly have one category in the parentheses.

Examples for entity and relation extraction:
1. Question: "Where does Alice work?"  
   - Entity: Alice (Person)  
   - Relation: works_for  
2. Question: "Which company is located in California?"  
   - Entity: California (Location)  
   - Relation: located_in  
3. Question: "Who founded Microsoft?"  
   - Entity: Microsoft (Organization)  
   - Relation: founded_by  
4. Question: "Does Bob work for Google?"  
   - Entity: Bob (Person), Google (Organization)  
   - Relation: works_for  
5. Question: "Is Tesla located in Texas?"  
   - Entity: Tesla (Organization), Texas (Location)  
   - Relation: located_in  
6. Question: "Who founded Apple?"  
   - Entity: Apple (Organization)  
   - Relation: founded_by  
7. Question: "Does Charlie work for Amazon?"  
   - Entity: Charlie (Person), Amazon (Organization)  
   - Relation: works_for  
8. Question: "Which organization is located in New York?"  
   - Entity: New York (Location)  
   - Relation: located_in  
9. Question: "Who founded SpaceX?"  
   - Entity: SpaceX (Organization)  
   - Relation: founded_by  
10. Question: "Does Diana work for IBM?"  
    - Entity: Diana (Person), IBM (Organization)  
    - Relation: works_for  

Given the following question, based on the entity type and the relation type, extract the topic entities and useful relations from the question.  
Entity Type: <<<{entity types}>>>
Relation Type: <<<{relation types}>>>
Question: <<<{question}>>>

Documents are required to answer the given question, and the goal is to search the useful documents. Each entity in the knowledge graph is associated with a document. Based on the extracted entities and relations, is knowledge graph or text documents helpful to narrow down the search space? 
YOU MUST ANSWER WITH EITHER OF THEM WITH NO MORE THAN TWO WORDS.
    """

def reflection():
    return """
        The retrieved document is incorrect.
        Feedback: "Error - Entity 'Tesla' was categorized as 'Company' instead of 'Organization'; Relation 'works_for' was incorrectly applied to a location context."
        Question: "Does Elon Musk work for Tesla?"
        The retrieved document is incorrect. Answer again based on newly extracted topic entities and useful relations. Is knowledge graph or text documents helpful to narrow down the 
        search space? You must answer with either of them with no more than two words.
    """

def valid():
    return """
        You are a helpful, pattern-following assistant.
        
        Examples for retrieval validation, 2 for each type of entity:
        1. Entity Type: Person
           - Question: "Does John work for Microsoft?"
           - Document: "John is an employee of Microsoft. Reasoning: The document states John's employment status with Microsoft, which matches the question."
           - Task: Is the document aligned with the requirements of the question? Reply with only yes or no.
           - Answer: Yes
           - Question: "Where does Mary live?"
           - Document: "Mary lives in London. Reasoning: The document provides Mary's location, which aligns with the question."
           - Task: Is the document aligned with the requirements of the question? Reply with only yes or no.
           - Answer: Yes
        2. Entity Type: Organization
           - Question: "Is Tesla located in California?"
           - Document: "Tesla's headquarters are in California. Reasoning: The document confirms Tesla's location, matching the question."
           - Task: Is the document aligned with the requirements of the question? Reply with only yes or no.
           - Answer: Yes
           - Question: "Who founded Apple?"
           - Document: "Apple was founded by Steve Jobs. Reasoning: The document provides the founder of Apple, which is relevant to the question."
           - Task: Is the document aligned with the requirements of the question? Reply with only yes or no.
           - Answer: Yes
        3. Entity Type: Location
           - Question: "Which company is located in New York?"
           - Document: "Google has an office in New York. Reasoning: The document links a company to New York, aligning with the question."
           - Task: Is the document aligned with the requirements of the question? Reply with only yes or no.
           - Answer: Yes
           - Question: "Is Paris a capital city?"
           - Document: "Paris is the capital of France. Reasoning: The document confirms Paris's status as a capital, matching the question."
           - Task: Is the document aligned with the requirements of the question? Reply with only yes or no.
           - Answer: Yes
        
        ### Question: "Does Elon Musk work for Tesla?"
        ### Document: "Elon Musk is the CEO of Tesla. Reasoning: The document indicates Elon Musk's role at Tesla, which implies he works for Tesla, aligning with the question."
        ### Task: Is the document aligned with the requirements of the question? Reply with only yes or no.
    """

def commentor():
    return """
        You are a helpful, pattern-following assistant.
        
        Examples of action and feedback pair:
        1. Question: "Does Alice work for Google?"
           - Topic Entities: Alice (Person), Google (Organization)
           - Useful Relations: works_for
           - Feedback: No errors
        2. Question: "Is Tesla located in California?"
           - Topic Entities: Tesla (Organization), California (Location)
           - Useful Relations: located_in
           - Feedback: No errors
        3. Question: "Who founded Microsoft?"
           - Topic Entities: Microsoft (Organization)
           - Useful Relations: founded_by
           - Feedback: No errors
        4. Question: "Does Bob live in New York?"
           - Topic Entities: Bob (Person), New York (City)
           - Useful Relations: lives_in
           - Feedback: Error - 'lives_in' is not a valid relation; should be 'located_in'
        5. Question: "Where does Charlie work?"
           - Topic Entities: Charlie (Person), Amazon (Company)
           - Useful Relations: works_for
           - Feedback: Error - 'Company' is not a valid entity category; should be 'Organization'
        6. Question: "Is Paris a capital?"
           - Topic Entities: Paris (City)
           - Useful Relations: is_capital_of
           - Feedback: Error - 'is_capital_of' is not a valid relation; should be 'located_in' with additional context
        7. Question: "Does Diana work for IBM?"
           - Topic Entities: Diana (Person), IBM (Organization)
           - Useful Relations: works_for
           - Feedback: No errors
        8. Question: "Which company is in Texas?"
           - Topic Entities: Texas (Location), Apple (Company)
           - Useful Relations: located_in
           - Feedback: Error - 'Company' is not a valid entity category; should be 'Organization'
        9. Question: "Who founded SpaceX?"
           - Topic Entities: SpaceX (Organization)
           - Useful Relations: founded_by
           - Feedback: No errors
        10. Question: "Is London located in France?"
            - Topic Entities: London (City), France (Country)
            - Useful Relations: located_in
            - Feedback: Error - London is not located in France; should be 'United Kingdom'
        
        Question: "Does Elon Musk work for Tesla?"
        Topic Entities: Elon Musk (Person), Tesla (Company)
        Useful Relations: works_for
        Please point out the wrong entity or relation extracted from the question, if there is any
    """

def extract_entities_relationship_from_text():
    return """
    Bạn là một hệ thống trích xuất thông tin từ văn bản. Nhiệm vụ của bạn là:

1. Trích xuất tất cả các thực thể có trong đoạn văn bản.
   - Mỗi thực thể cần có tên và loại.  
   - Loại của thực thể (ví dụ: người, tổ chức, địa điểm, ngày tháng, sản phẩm, v.v.) phải được ghi bằng tiếng Việt, ghi thường, có dấu.

2. Xác định các mối quan hệ giữa các thực thể.  
   - Mỗi mối quan hệ phải có nguồn, đích và tên mối quan hệ.  
   - Tên mối quan hệ phải được ghi IN HOA. Nếu tên mối quan hệ gồm từ hai từ trở lên, các từ phải được nối với nhau bằng dấu gạch dưới (ví dụ: "THỦ_ĐÔ_CỦA", "TẠO_RA").  
   - Nếu một mối quan hệ giống nhau ở nhiều trường hợp, hãy thống nhất sử dụng một tên mối quan hệ duy nhất và không thêm từ gì khác. Ví dụ: nếu "tphcm ở việt nam" được quy định là mối quan hệ "Ở", thì với mọi trường hợp tương tự, mối quan hệ phải là "Ở".

3. Trả về kết quả dưới dạng JSON với các trường:
   - "entities": Danh sách các thực thể. Mỗi thực thể có các thuộc tính "name" và "type".
   - "relationships": Danh sách các mối quan hệ. Mỗi mối quan hệ có các thuộc tính "source", "target" và "relation".

Đoạn văn bản cần trích xuất:
{question}

Yêu cầu:
- Trả về kết quả dưới dạng JSON với các trường: entities, relationships.
- Mỗi entity cần có name và type.
- Mỗi relationship cần có source, target, và relation.

---
### Giải thích:
1. **Entity**:
   - Là các đối tượng được nhắc đến trong văn bản, ví dụ: tên người, địa điểm, tổ chức, ngày tháng, v.v.
   - Mỗi entity cần được gán một loại phù hợp, ví dụ: NGƯỜI, ĐỊA ĐIỂM, TỔ CHỨC, NGÀY, v.v.

2. **Relationship**:
   - Là mối quan hệ giữa các entity, ví dụ: "Alice knows Bob" → quan hệ Biết giữa Alice và Bob.

3. **Định dạng đầu ra**:
   - Sử dụng JSON để trả về kết quả một cách có cấu trúc, dễ dàng xử lý tiếp theo.
---
### Ví dụ 1:
Câu hỏi: "steve jobs là người sáng lập apple, một công ty công nghệ có trụ sở tại cupertino."
{
  "entities": [
    {"name": "steve jobs", "type": "người"},
    {"name": "apple", "type": "tổ chức"},
    {"name": "cupertino", "type": "địa điểm"}
  ],
  "relationships": [
    {"source": "steve jobs", "target": "apple", "relation": "SÁNG_LẬP"},
    {"source": "apple", "target": "cupertino", "relation": "Ở"}
  ]
}
### Ví dụ 2:
Câu hỏi: "paris là thủ đô của nước pháp, nằm ở châu âu."
{
  "entities": [
    {"name": "paris", "type": "địa điểm"},
    {"name": "pháp", "type": "địa điểm"},
    {"name": "châu âu", "type": "địa điểm"}
  ],
  "relationships": [
    {"source": "paris", "target": "pháp", "relation": "THỦ_ĐÔ_CỦA"},
    {"source": "pháp", "target": "châu âu", "relation": "Ở"}
  ]
}
### Ví dụ 3:
Câu hỏi: "elon musk là ceo của tesla và spacex, hai công ty công nghệ hàng đầu thế giới."
{
  "entities": [
    {"name": "elon musk", "type": "người"},
    {"name": "tesla", "type": "tổ chức"},
    {"name": "spacex", "type": "tổ chức"}
  ],
  "relationships": [
    {"source": "elon musk", "target": "tesla", "relation": "CEO_CỦA"},
    {"source": "elon musk", "target": "spacex", "relation": "CEO_CỦA"}
  ]
}
### Ví dụ 4:
Câu hỏi: "harry potter là nhân vật chính trong bộ truyện cùng tên, được viết bởi j.k. rowling."
{
  "entities": [
    {"name": "harry potter", "type": "người"},
    {"name": "j.k. rowling", "type": "người"}
  ],
  "relationships": [
    {"source": "harry potter", "target": "j.k. rowling", "relation": "TẠO_RA"}
  ]
}
### Ví dụ 5:
Câu hỏi: "sông amazon chảy qua brazil và peru, là một trong những con sông dài nhất thế giới."
{
  "entities": [
    {"name": "sông amazon", "type": "địa điểm"},
    {"name": "brazil", "type": "địa điểm"},
    {"name": "peru", "type": "địa điểm"}
  ],
  "relationships": [
    {"source": "sông amazon", "target": "brazil", "relation": "CHẢY_QUA"},
    {"source": "sông amazon", "target": "peru", "relation": "CHẢY_QUA"}
  ]
}
### Ví dụ 6:
Câu hỏi: "mark zuckerberg kết hôn với priscilla chan vào năm 2012."
{
  "entities": [
    {"name": "mark zuckerberg", "type": "người"},
    {"name": "priscilla chan", "type": "người"},
    {"name": "2012", "type": "ngày tháng"}
  ],
  "relationships": [
    {"source": "mark zuckerberg", "target": "priscilla chan", "relation": "KẾT_HÔN_VỚI"},
    {"source": "mark zuckerberg", "target": "2012", "relation": "KẾT_HÔN_VÀO"}
  ]
}
### Ví dụ 7:
Câu hỏi: "iphone là sản phẩm của apple, được phát hành lần đầu vào năm 2007."
{
  "entities": [
    {"name": "iphone", "type": "sản phẩm"},
    {"name": "apple", "type": "tổ chức"},
    {"name": "2007", "type": "ngày tháng"}
  ],
  "relationships": [
    {"source": "iphone", "target": "apple", "relation": "SẢN_XUẤT_BỞI"},
    {"source": "iphone", "target": "2007", "relation": "PHÁT_HÀNH_VÀO"}
  ]
}
### Ví dụ 8:
Câu hỏi: "albert einstein đoạt giải nobel vật lý vào năm 1921."
{
  "entities": [
    {"name": "albert einstein", "type": "người"},
    {"name": "nobel vật lý", "type": "giải thưởng"},
    {"name": "1921", "type": "ngày tháng"}
  ],
  "relationships": [
    {"source": "albert einstein", "target": "nobel vật lý", "relation": "ĐOẠT"},
    {"source": "albert einstein", "target": "1921", "relation": "ĐOẠT_VÀO"}
  ]
}
### Ví dụ 9:
Câu hỏi: "facebook mua lại instagram vào năm 2012 với giá 1 tỷ usd."
{
  "entities": [
    {"name": "facebook", "type": "tổ chức"},
    {"name": "instagram", "type": "tổ chức"},
    {"name": "2012", "type": "ngày tháng"},
    {"name": "1 tỷ usd", "type": "tiền"}
  ],
  "relationships": [
    {"source": "facebook", "target": "instagram", "relation": "MUA_LẠI"},
    {"source": "facebook", "target": "2012", "relation": "MUA_VÀO"},
    {"source": "facebook", "target": "1 tỷ usd", "relation": "MUA_VỚI_GIÁ"}
  ]
}
### Ví dụ 10:
Câu hỏi: "leonardo da vinci là một họa sĩ nổi tiếng người ý, tác giả của bức tranh mona lisa."
{
  "entities": [
    {"name": "leonardo da vinci", "type": "người"},
    {"name": "mona lisa", "type": "tác phẩm nghệ thuật"},
    {"name": "ý", "type": "địa điểm"}
  ],
  "relationships": [
    {"source": "leonardo da vinci", "target": "mona lisa", "relation": "TẠO_RA"},
    {"source": "leonardo da vinci", "target": "ý", "relation": "QUỐC_TỊCH"}
  ]
}
    """

def extract_question_from_text():
    return """nhiệm vụ của bạn là sẽ tạo ra TẤT CẢ các câu hỏi từ văn bản từ đầu đến cuối mà không bỏ xót 1 chi tiết nào, các câu hỏi viết chữ thường, chỉ tạo ra danh sách câu hỏi và không thêm bất cứ thông tin gì"""

# yêu cầu llm dự đoán câu hỏi sẽ thuộc về phần nào trong sổ tay sinh viên
def predict_question_belong_to(question):
    return f"""nhiệm vụ của bạn là dự đoán câu hỏi sau nằm trong phần nào dưới đây mà tôi cung cấp. Hãy trả lời ở phần nào, và ở mục nào của phần đó theo dạng json mà tôi cung cấp:
"{
"episode": "",
"part": ""
}"
câu hỏi cần dự đoán: {question}
Dưới đây là mục lục mà bạn cần dự đoán
"Phần 1: NLU - Định hướng trường đại học nghiên cứu
Quá trình hình thành và phát triển
Sứ mạng
Tầm nhìn
Giá trị cốt lõi
Mục tiêu chiến lược
Cơ sở vật chất
Các đơn vị trong trường
Các khoa - ngành đào tạo
Tuần sinh hoạt công dân - sinh viên
Hoạt động phong trào sinh viên
Câu lạc bộ (CLB) - Đội, Nhóm
Cơ sở đào tạo
Phần 2: HỌC TẬP VÀ RÈN LUYỆN
Quy chế sinh viên
Quy chế học vụ
Quy định về việc đào tạo trực tuyến
Quy định khen thưởng, kỷ luật sinh viên
Quy chế đánh giá kết quả rèn luyện
Quy tắc ứng xử văn hóa của người học
Cố vấn học tập
Danh hiệu sinh viên 5 tốt
Danh hiệu sinh viên tiêu biểu
Phần 3: HỖ TRỢ VÀ DỊCH VỤ
Quy định phân cấp giải quyết thắc mắc của sinh viên
Thông tin học bổng
Vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên
Quy trình xác nhận hồ sơ sinh viên
Hồ sơ yêu cầu bồi thường bảo hiểm tai nạn sinh viên
Thông tin về bảo hiểm y tế
Hướng dẫn sử dụng các kênh thanh toán học phí, BHYT, lệ phí xét tốt nghiệp
Tham vấn tâm lý học đường
thông tin học bổng khuyến khích học tập
Trung tâm Dịch vụ Sinh viên"
"""

# dùng để tạo mã cypher cho câu hỏi
def create_cypher_from_question():
    return """
    Nhiệm vụ của bạn là tạo mã cypher từ câu hỏi mà tôi đưa vào. Chỉ tạo ra mã cypher và không thêm bất cứ thông tin gì. Tất cả source đều ghi bằng chữ thường. Target chỉ có chữ e, không chỉ định gì thêm. 
Dưới đây tôi sẽ cung cấp cho bạn tất cả các type và relation mà bạn sẽ tạo ra, chỉ tạo ra type và relation mà tôi đã đề cập, không được thêm bất cứ từ nào: 
Đây là các type đã có sẵn: episode, part, organization, quantity, department, phone_number, website, facility, center, institute, faculty, department_subject, training_program, program_type, person, email, location, concept, group, activity, type_of_organization, time, strategy, award, group_of_people, document, title, event, phase, position, disciplinary_action, movement, abbreviation, percentage, beverage, item, product, network, frequency, action, material, code, application, device, system, amount, status, clause, chapter, document_type, software, sequence, method, media, variable, natural_phenomenon, year, service, crime, online_platform, grade, data, course_type, degree, date, assignment, criteria, subject, money, field, right, teaching_method, platform, account, image, link, task, email_address, feature 
Đây là các relation đã có sẵn: BAO_GỒM, sở_hữu, website, số_điện_thoại, thuộc_khoa, chương_trình_đào_tạo_tại, chương_trình_tiên_tiến_tại, chương_trình_nâng_cao_tại, có, là, trong, email, địa_chỉ, sử_dụng, về, sánh_vai, đổi_mới, thúc_đẩy, phát_huy, xây_dựng, trở_thành, phục_vụ, đào_tạo, mục_tiêu_đến, sẽ_trở_thành, với, cho, xác_nhận, tăng_cường, áp_dụng, quản_lý_bởi, chủ_nhiệm, trưởng_ban_điều_hành, đội_trưởng, số_lượng_sách, số_lượng_phòng, sức_chứa, gìn_giữ_và_phát_huy, của, phát_hiện, nâng_đỡ, tôn_trọng, tham_gia, đánh_giá, phòng_chống, đạt, chấp_hành, đến, thực_hiện, lắng_nghe, hoàn_thành, nghiêm_túc, hỏi, trả_lời, làm_phiền, không_gây_ồn_ào, giữ_gìn, đề_cao, hoạt_động_của, theo, xem_xét, tổ_chức, gửi_thông_báo, không_chấp_nhận, không_cần, đóng_trụ_sở, và, bao_gồm, đáp_ứng, trên, hàng_đầu, tầm_nhìn, gồm, công_bố, tên_khác, trực_thuộc, tọa_lạc_tại, thời_gian_hoạt_động, nhận_giải_thưởng, tại, xét_tương_đương, thuộc, thành_lập, tổ_chức_bởi, được_đăng_tại, dành_cho, trường, gửi, xét, nhận, bố_trí, quản_lý, cung_cấp_ctđt_cho, đề_xuất_hủy_hoặc_mở_thêm, đề_xuất, duy_trì, đề_xuất_mở_thêm, xử_lý, phân_công, hỗ_trợ, tư_vấn, hướng_dẫn, theo_dõi, bị, mời, không, từ, điều_chỉnh, không_dưới, ít_nhất, khen_thưởng, không_vượt_quá, đánh_giá_qua, đoạt_giải, có_thành_tích, đóng_góp, hoạt_động_tại, bảo_đảm_an_ninh, bằng_nhau, công_nhận, áp_dụng_bởi, thông_báo, làm, tham_dự, sau, chấm_dứt, truy_cập, nhập, đăng_nhập, chụp_ảnh, quét, đọc, lấy_ảnh, kiểm_tra, chuyển_tới, viết, trực_tuyến, nộp, mang, được_hỗ_trợ, đi_học, chưa_được_sửa, mất, chuyển, đã, bổ_sung, cập_nhật, liên_hệ, như, cùng, xếp, so_sánh, bằng, không_bị, do, vay, để, thủ_tục, sinh_sống, đủ_tiêu_chuẩn, tối_đa, lãi_suất, thông_qua, tuân_thủ_quy_định_của, học_tập_tại, được_tôn_trọng_bởi, được_cung_cấp, được_sử_dụng, hoạt_động_trong, kiến_nghị_với, đề_đạt_nguyện_vọng_lên, được_ở, được_nhận, tuân_thủ_chủ_trương_của, tuân_thủ_pháp_luật_của, tuân_thủ_quy_chế_của, đóng, không_được_xúc_phạm, không_được_tham_gia, không_được, không_được_tổ_chức_hoạt_động_mà_chưa_được_cho_phép, thực_hiện_theo, đăng_ký_học_lại, cải_thiện_điểm, rút, không_đi_học, không_dự_thi, nhận_điểm_r, nhận_điểm_f, rút_học_phần_trên, đăng_ký_trực_tuyến, cải_thiện_kết_quả, dự_thi, hưởng, xác_định, xem_kết_quả, được_đánh_giá, không_tham_gia, xếp_loại, đình_chỉ, chuyển_sang, thỏa_mãn, thảo_luận, gia_hạn, không_hoàn_thành, tích_lũy, được_cấp, báo, bảo_lưu, được_điều_động, cần, theo_quy_định, học_xong, nghỉ, được_công_nhận, học, vượt_quá, nghiên_cứu, bổ_sung_vào, giữ_bí_mật, bảo_vệ, chịu_trách_nhiệm, trước, nhấn, mở, tắt, bấm, chia_sẻ, trao_đổi, thắc_mắc, đăng_ký, chọn, phù_hợp, ở, cập_nhật_trên, lập, trình, qua, hủy, cho_phép_đăng_ký_ít_hơn_14_tín_chỉ, mở_thêm, kỷ_luật, thang_điểm, ít_hơn_hoặc_bằng, cấp, vào_cuối, tuyên_dương, căn_cứ, dưới, trừ, vô_lễ, lần_1, giao_cho, hạ_điểm, tài_sản_trong, làm_hư_hỏng, lần_2, lần_3, trái, xâm_phạm, chống_phá, thu_hồi, cao_nhất, cao_thứ_hai, quyết_định, phê_duyệt_duy_trì, chấp_thuận_mở_thêm, quy_định, phê_duyệt, đồng_ý, cho_phép, ra_quyết_định, duyệt_danh_sách_cấm_thi, chấp_thuận, duyệt_đơn, rà_soát, quyết_định_gia_hạn, phát_động, đề_nghị, chấm, quan_hệ, phản_hồi, cung_cấp, thanh_toán, lưu, dấu_và_chữ_ký, hiển_thị, tương_ứng, in, trạng_thái, kèm, giải_quyết, thông_báo_học_phần_cho, hướng_dẫn_đăng_ký_cho, công_bố_kết_quả_đăng_ký_cho, giúp_đỡ, ghi, đề_xuất_cấm_thi, nêu, hoặc, ký, tổ_chức_bảo_vệ, loại, trình_ký, đóng_dấu, hoạt_động, trị_giá, cao_hơn, hơn, trọng_số, làm_tròn, trích_từ, phối_hợp, một_lần, mỗi, đối_với, đóng_mộc, sửa_đổi, mã, nhân, tra_cứu, điện_thoại, thành_lập_từ, giúp, trả_nợ, cư_trú, gặp_khó_khăn, tư_vấn_xây_dựng_khht_cho, tối_thiểu, được_quy_định_trong, thông_báo_cho, thông_báo_lịch_thi, không_đạt, tính_vào, chuẩn, tổ_chức_thi_cho, cấp_bằng, dựa_vào, tính, không_tính, trung_bình_cộng, lưu_trong, ghi_vào, tiêu_chí, chỉ_đạo, phát_triển_trên, không_tổ_chức 
Câu hỏi: {question}
Ví dụ về cypher mà bạn cần tạo:
1.	MATCH (o:organization {name: "trường đại học nông lâm thành phố hồ chí minh"})-[r:trực_thuộc]->(e) RETURN o AS source, r AS relationship, e AS target
2.	MATCH (o:organization {name: "trường đại học nông lâm thành phố hồ chí minh"})-[r:tọa_lạc_tại]->(e) RETURN o AS source, r AS relationship, e AS target
3.	MATCH (o:organization {name: "trường đại học nông lâm thành phố hồ chí minh"})-[r:thời_gian_hoạt_động]->(e) RETURN o AS source, r AS relationship, e AS target
4.	MATCH (o:organization {name: "trường đại học nông lâm thành phố hồ chí minh"})-[r:nhận_giải_thưởng]->(e) RETURN o AS source, r AS relationship, e AS target
5.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:là]->(e) RETURN o AS source, r AS relationship, e AS target
6.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:đào_tạo]->(e) RETURN o AS source, r AS relationship, e AS target
7.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:sẽ_trở_thành]->(e) RETURN o AS source, r AS relationship, e AS target
8.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
9.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:trở_thành]->(e) RETURN o AS source, r AS relationship, e AS target
10.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:phát_huy]->(e) RETURN o AS source, r AS relationship, e AS target
11.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
12.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:đào_tạo]->(e) RETURN o AS source, r AS relationship, e AS target
13.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:đào_tạo]->(e) RETURN o AS source, r AS relationship, e AS target
14.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:xây_dựng]->(e) RETURN o AS source, r AS relationship, e AS target
15.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:xây_dựng]->(e) RETURN o AS source, r AS relationship, e AS target
16.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
17.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
18.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
19.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
20.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:sánh_vai]->(e) RETURN o AS source, r AS relationship, e AS target
21.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:sánh_vai]->(e) RETURN o AS source, r AS relationship, e AS target
22.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:đổi_mới]->(e) RETURN o AS source, r AS relationship, e AS target
23.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:đổi_mới]->(e) RETURN o AS source, r AS relationship, e AS target
24.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:đổi_mới]->(e) RETURN o AS source, r AS relationship, e AS target
25.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:thúc_đẩy]->(e) RETURN o AS source, r AS relationship, e AS target
26.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:thúc_đẩy]->(e) RETURN o AS source, r AS relationship, e AS target
27.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:phát_huy]->(e) RETURN o AS source, r AS relationship, e AS target
28.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:phát_huy]->(e) RETURN o AS source, r AS relationship, e AS target
29.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:xây_dựng]->(e) RETURN o AS source, r AS relationship, e AS target
30.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:xây_dựng]->(e) RETURN o AS source, r AS relationship, e AS target
31.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:xây_dựng]->(e) RETURN o AS source, r AS relationship, e AS target
32.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:trở_thành]->(e) RETURN o AS source, r AS relationship, e AS target
33.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:xây_dựng]->(e) RETURN o AS source, r AS relationship, e AS target
34.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:xây_dựng]->(e) RETURN o AS source, r AS relationship, e AS target
35.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
36.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
37.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
38.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
39.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
40.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
41.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
42.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
43.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
44.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
45.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
46.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
47.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
48.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
49.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
50.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
51.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
52.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
53.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
54.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
55.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
56.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
57.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
58.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
59.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
60.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:sử_dụng]->(e) RETURN o AS source, r AS relationship, e AS target
61.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
62.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
63.	MATCH (o:department {name: "phòng công tác sinh viên"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
64.	MATCH (o:department {name: "phòng công tác sinh viên"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
65.	MATCH (o:department {name: "phòng đào tạo"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
66.	MATCH (o:department {name: "phòng đào tạo"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
67.	MATCH (o:department {name: "phòng đào tạo sau đại học"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
68.	MATCH (o:department {name: "phòng đào tạo sau đại học"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
69.	MATCH (o:department {name: "phòng hành chính"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
70.	MATCH (o:department {name: "phòng hành chính"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
71.	MATCH (o:department {name: "phòng hợp tác quốc tế"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
72.	MATCH (o:department {name: "phòng hợp tác quốc tế"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
73.	MATCH (o:department {name: "phòng kế hoạch tài chính"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
74.	MATCH (o:department {name: "phòng kế hoạch tài chính"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
75.	MATCH (o:department {name: "phòng quản lý chất lượng"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
76.	MATCH (o:department {name: "phòng quản lý chất lượng"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
77.	MATCH (o:department {name: "phòng quản trị vật tư"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
78.	MATCH (o:department {name: "phòng quản trị vật tư"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
79.	MATCH (o:department {name: "phòng tổ chức cán bộ"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
80.	MATCH (o:department {name: "phòng tổ chức cán bộ"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
81.	MATCH (o:department {name: "phòng thanh tra giáo dục"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
82.	MATCH (o:department {name: "phòng thanh tra giáo dục"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
83.	MATCH (o:department {name: "phòng thông tin và truyền thông"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
84.	MATCH (o:department {name: "phòng thông tin và truyền thông"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
85.	MATCH (o:facility {name: "thư viện"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
86.	MATCH (o:facility {name: "thư viện"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
87.	MATCH (o:center {name: "trung tâm dịch vụ sinh viên"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
88.	MATCH (o:center {name: "trung tâm dịch vụ sinh viên"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
89.	MATCH (o:center {name: "trung tâm nghiên cứu biến đổi khí hậu"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
90.	MATCH (o:center {name: "trung tâm nghiên cứu biến đổi khí hậu"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
91.	MATCH (o:center {name: "trung tâm nghiên cứu và ứng dụng công nghệ địa chính"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
92.	MATCH (o:center {name: "trung tâm nghiên cứu và ứng dụng công nghệ địa chính"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
93.	MATCH (o:institute {name: "viện nghiên cứu công nghệ sinh học và môi trường"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
94.	MATCH (o:institute {name: "viện nghiên cứu công nghệ sinh học và môi trường"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
95.	MATCH (o:faculty {name: "khoa công nghệ hóa học và thực phẩm"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
96.	MATCH (o:faculty {name: "khoa công nghệ hóa học và thực phẩm"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
97.	MATCH (o:faculty {name: "khoa công nghệ thông tin"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
98.	MATCH (o:faculty {name: "khoa công nghệ thông tin"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
99.	MATCH (o:faculty {name: "khoa cơ khí công nghệ"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
100.	MATCH (o:faculty {name: "khoa cơ khí công nghệ"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
101.	MATCH (o:faculty {name: "khoa chăn nuôi thú y"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
102.	MATCH (o:faculty {name: "khoa chăn nuôi thú y"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
103.	MATCH (o:faculty {name: "khoa kinh tế"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
104.	MATCH (o:faculty {name: "khoa kinh tế"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
105.	MATCH (o:faculty {name: "khoa khoa học"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
106.	MATCH (o:faculty {name: "khoa khoa học"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
107.	MATCH (o:faculty {name: "khoa khoa học sinh học"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
108.	MATCH (o:faculty {name: "khoa khoa học sinh học"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
109.	MATCH (o:faculty {name: "khoa lâm nghiệp"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
110.	MATCH (o:faculty {name: "khoa lâm nghiệp"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
111.	MATCH (o:faculty {name: "khoa môi trường và tài nguyên"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
112.	MATCH (o:faculty {name: "khoa môi trường và tài nguyên"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
113.	MATCH (o:faculty {name: "khoa nông học"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
114.	MATCH (o:faculty {name: "khoa nông học"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
115.	MATCH (o:faculty {name: "khoa ngoại ngữ - sư phạm"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
116.	MATCH (o:faculty {name: "khoa ngoại ngữ - sư phạm"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
117.	MATCH (o:faculty {name: "khoa quản lý đất đai và bất động sản"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
118.	MATCH (o:faculty {name: "khoa quản lý đất đai và bất động sản"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
119.	MATCH (o:faculty {name: "khoa thủy sản"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
120.	MATCH (o:faculty {name: "khoa thủy sản"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
121.	MATCH (o:department_subject {name: "bộ môn lý luận chính trị"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
122.	MATCH (o:department_subject {name: "bộ môn lý luận chính trị"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
123.	MATCH (o:training_program {name: "bất động sản"})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target
124.	MATCH (o:training_program {name: "công nghệ chế biến thủy sản"})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target
125.	MATCH (o:training_program {name: "lâm học"})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target
126.	MATCH (o:training_program {name: "quản lý tài nguyên rừng"})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target
127.	MATCH (o:training_program {name: "công nghệ thực phẩm"})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target
128.	MATCH (o:training_program {name: "thú y"})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target
129.	MATCH (o:person {name: "sinh viên"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
130.	MATCH (o:person {name: "sinh viên"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
131.	MATCH (o:person {name: "sinh viên"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
132.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
133.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target
134.	MATCH (o:organization {name: "clb cán bộ đoàn ngôi sao xanh"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
135.	MATCH (o:organization {name: "clb cán bộ đoàn ngôi sao xanh"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
136.	MATCH (o:organization {name: "bec english club"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
137.	MATCH (o:organization {name: "bec english club"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
138.	MATCH (o:organization {name: "clb bóng rổ đại học nông lâm"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
139.	MATCH (o:organization {name: "clb bóng rổ đại học nông lâm"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
140.	MATCH (o:organization {name: "clb du lịch sinh thái"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
141.	MATCH (o:organization {name: "clb du lịch sinh thái"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
142.	MATCH (o:organization {name: "clb dược thú y"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
143.	MATCH (o:organization {name: "clb dược thú y"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
144.	MATCH (o:organization {name: "fire english club"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
145.	MATCH (o:organization {name: "fire english club"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
146.	MATCH (o:organization {name: "clb karate-do"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
147.	MATCH (o:organization {name: "clb karate-do"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
148.	MATCH (o:organization {name: "clb kết nối thành công"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
149.	MATCH (o:organization {name: "clb kết nối thành công"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
150.	MATCH (o:organization {name: "clb khởi nghiệp (nlu startup club) nsc"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
151.	MATCH (o:organization {name: "clb khởi nghiệp (nlu startup club) nsc"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
152.	MATCH (o:organization {name: "clb một sức khỏe tp.hcm (hcmc one health club)"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
153.	MATCH (o:organization {name: "clb sách và hành động nông lâm tp.hcm"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
154.	MATCH (o:organization {name: "clb sách và hành động nông lâm tp.hcm"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
155.	MATCH (o:organization {name: "clb tiếng anh khoa công nghệ hóa học và thực phẩm (seeds for future) sff"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
156.	MATCH (o:organization {name: "clb tiếng anh khoa công nghệ hóa học và thực phẩm (seeds for future) sff"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
157.	MATCH (o:organization {name: "clb tiếng anh khoa kinh tế efb (english for business club) efb"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
158.	MATCH (o:organization {name: "clb tiếng anh khoa kinh tế efb (english for business club) efb"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
159.	MATCH (o:organization {name: "clb thú y engscope"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
160.	MATCH (o:organization {name: "clb truyền thông nông lâm radio"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
161.	MATCH (o:organization {name: "clb truyền thông nông lâm radio"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
162.	MATCH (o:organization {name: "wildlife vet student club"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
163.	MATCH (o:organization {name: "clb yêu môi trường"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
164.	MATCH (o:organization {name: "tổ tu dưỡng rèn luyện hạt giống đỏ"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
165.	MATCH (o:organization {name: "tổ tu dưỡng rèn luyện hạt giống đỏ"})-[r:trưởng_ban_điều_hành]->(e) RETURN o AS source, r AS relationship, e AS target
166.	MATCH (o:organization {name: "đội công tác xã hội"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
167.	MATCH (o:organization {name: "đội công tác xã hội"})-[r:đội_trưởng]->(e) RETURN o AS source, r AS relationship, e AS target
168.	MATCH (o:organization {name: "đội khát vọng tuổi trẻ khoa chăn nuôi thú y"})-[r:đội_trưởng]->(e) RETURN o AS source, r AS relationship, e AS target
169.	MATCH (o:organization {name: "đội nhiệt huyết rừng xanh"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
170.	MATCH (o:organization {name: "đội nhiệt huyết rừng xanh"})-[r:đội_trưởng]->(e) RETURN o AS source, r AS relationship, e AS target
171.	MATCH (o:organization {name: "đội văn nghệ rạng đông"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
172.	MATCH (o:organization {name: "đội văn nghệ rạng đông"})-[r:đội_trưởng]->(e) RETURN o AS source, r AS relationship, e AS target
173.	MATCH (o:organization {name: "đội văn nghệ xung kích nhịp điệu xanh"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
174.	MATCH (o:organization {name: "đội văn nghệ xung kích nhịp điệu xanh"})-[r:đội_trưởng]->(e) RETURN o AS source, r AS relationship, e AS target
175.	MATCH (o:organization {name: "đội xung kích khoa khoa học sinh học"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
176.	MATCH (o:organization {name: "đội xung kích khoa khoa học sinh học"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
177.	MATCH (o:organization {name: "hội cổ động viên (nong lam buffaloes) nlb"})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target
178.	MATCH (o:organization {name: "hội cổ động viên (nong lam buffaloes) nlb"})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target
179.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:địa_chỉ]->(e) RETURN o AS source, r AS relationship, e AS target
180.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
181.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
182.	MATCH (o:organization {name: "trường đại học nông lâm tp.hcm"})-[r:email]->(e) RETURN o AS source, r AS relationship, e AS target
183.	MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:địa_chỉ]->(e) RETURN o AS source, r AS relationship, e AS target
184.	MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:địa_chỉ]->(e) RETURN o AS source, r AS relationship, e AS target
185.	MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
186.	MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
187.	MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"})-[r:email]->(e) RETURN o AS source, r AS relationship, e AS target
188.	MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:địa_chỉ]->(e) RETURN o AS source, r AS relationship, e AS target
189.	MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target
190.	MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target
191.	MATCH (o:organization {name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"})-[r:email]->(e) RETURN o AS source, r AS relationship, e AS target"""

# dùng để trích xuất entities và relationship cho câu hỏi
def extract_entities_relationship_from_question(question):
    return f"""Bạn là một hệ thống trích xuất thông tin từ văn bản. Nhiệm vụ của bạn là:

1. Trích xuất tất cả các thực thể có trong đoạn văn bản.
   - Mỗi thực thể cần có tên và loại.  
   - Loại của thực thể hãy sử dụng các từ mà tôi cung cấp không được dùng từ khác: 'episode', 'part', 'organization', 'quantity', 'department', 'phone_number', 'website', 'facility', 'center', 'institute', 'faculty', 'department_subject', 'training_program', 'program_type', 'person', 'email', 'location', 'concept', 'group', 'activity', 'type_of_organization', 'time', 'strategy', 'award', 'group_of_people', 'document', 'title', 'event', 'phase', 'position', 'disciplinary_action', 'movement', 'abbreviation', 'percentage', 'beverage', 'item', 'product', 'network', 'frequency', 'action', 'material', 'code', 'application', 'device', 'system', 'amount', 'status', 'clause', 'chapter', 'document_type', 'software', 'sequence', 'method', 'media', 'variable', 'natural_phenomenon', 'year', 'service', 'crime', 'online_platform', 'grade', 'data', 'course_type', 'degree', 'date', 'assignment', 'criteria', 'subject', 'money', 'field', 'right', 'teaching_method', 'platform', 'account', 'image', 'link', 'task', 'email_address', 'feature'.

2. Xác định các mối quan hệ giữa các thực thể.  
   - Mỗi mối quan hệ phải có nguồn, đích và tên mối quan hệ. 
sử dụng các mối quan hệ có sẵn:
'BAO_GỒM', 'sở_hữu', 'website', 'số_điện_thoại', 'thuộc_khoa', 'chương_trình_đào_tạo_tại', 'chương_trình_tiên_tiến_tại', 'chương_trình_nâng_cao_tại', 'có', 'là', 'trong', 'email', 'địa_chỉ', 'sử_dụng', 'về', 'sánh_vai', 'đổi_mới', 'thúc_đẩy', 'phát_huy', 'xây_dựng', 'trở_thành', 'phục_vụ', 'đào_tạo', 'mục_tiêu_đến', 'sẽ_trở_thành', 'với', 'cho', 'xác_nhận', 'tăng_cường', 'áp_dụng', 'quản_lý_bởi', 'chủ_nhiệm', 'trưởng_ban_điều_hành', 'đội_trưởng', 'số_lượng_sách', 'số_lượng_phòng', 'sức_chứa', 'gìn_giữ_và_phát_huy', 'của', 'phát_hiện', 'nâng_đỡ', 'tôn_trọng', 'tham_gia', 'đánh_giá', 'phòng_chống', 'đạt', 'chấp_hành', 'đến', 'thực_hiện', 'lắng_nghe', 'hoàn_thành', 'nghiêm_túc', 'hỏi', 'trả_lời', 'làm_phiền', 'không_gây_ồn_ào', 'giữ_gìn', 'đề_cao', 'hoạt_động_của', 'theo', 'xem_xét', 'tổ_chức', 'gửi_thông_báo', 'không_chấp_nhận', 'không_cần', 'đóng_trụ_sở', 'và', 'bao_gồm', 'đáp_ứng', 'trên', 'hàng_đầu', 'tầm_nhìn', 'gồm', 'công_bố', 'tên_khác', 'trực_thuộc', 'tọa_lạc_tại', 'thời_gian_hoạt_động', 'nhận_giải_thưởng', 'tại', 'xét_tương_đương', 'thuộc', 'thành_lập', 'tổ_chức_bởi', 'được_đăng_tại', 'dành_cho', 'trường', 'gửi', 'xét', 'nhận', 'bố_trí', 'quản_lý', 'cung_cấp_ctđt_cho', 'đề_xuất_hủy_hoặc_mở_thêm', 'đề_xuất', 'duy_trì', 'đề_xuất_mở_thêm', 'xử_lý', 'phân_công', 'hỗ_trợ', 'tư_vấn', 'hướng_dẫn', 'theo_dõi', 'bị', 'mời', 'không', 'từ', 'điều_chỉnh', 'không_dưới', 'ít_nhất', 'khen_thưởng', 'không_vượt_quá', 'đánh_giá_qua', 'đoạt_giải', 'có_thành_tích', 'đóng_góp', 'hoạt_động_tại', 'bảo_đảm_an_ninh', 'bằng_nhau', 'công_nhận', 'áp_dụng_bởi', 'thông_báo', 'làm', 'tham_dự', 'sau', 'chấm_dứt', 'truy_cập', 'nhập', 'đăng_nhập', 'chụp_ảnh', 'quét', 'đọc', 'lấy_ảnh', 'kiểm_tra', 'chuyển_tới', 'viết', 'trực_tuyến', 'nộp', 'mang', 'được_hỗ_trợ', 'đi_học', 'chưa_được_sửa', 'mất', 'chuyển', 'đã', 'bổ_sung', 'cập_nhật', 'liên_hệ', 'như', 'cùng', 'xếp', 'so_sánh', 'bằng', 'không_bị', 'do', 'vay', 'để', 'thủ_tục', 'sinh_sống', 'đủ_tiêu_chuẩn', 'tối_đa', 'lãi_suất', 'thông_qua', 'tuân_thủ_quy_định_của', 'học_tập_tại', 'được_tôn_trọng_bởi', 'được_cung_cấp', 'được_sử_dụng', 'hoạt_động_trong', 'kiến_nghị_với', 'đề_đạt_nguyện_vọng_lên', 'được_ở', 'được_nhận', 'tuân_thủ_chủ_trương_của', 'tuân_thủ_pháp_luật_của', 'tuân_thủ_quy_chế_của', 'đóng', 'không_được_xúc_phạm', 'không_được_tham_gia', 'không_được', 'không_được_tổ_chức_hoạt_động_mà_chưa_được_cho_phép', 'thực_hiện_theo', 'đăng_ký_học_lại', 'cải_thiện_điểm', 'rút', 'không_đi_học', 'không_dự_thi', 'nhận_điểm_r', 'nhận_điểm_f', 'rút_học_phần_trên', 'đăng_ký_trực_tuyến', 'cải_thiện_kết_quả', 'dự_thi', 'hưởng', 'xác_định', 'xem_kết_quả', 'được_đánh_giá', 'không_tham_gia', 'xếp_loại', 'đình_chỉ', 'chuyển_sang', 'thỏa_mản', 'thảo_luận', 'gia_hạn', 'không_hoàn_thành', 'tích_lũy', 'được_cấp', 'báo', 'bảo_lưu', 'được_điều_động', 'cần', 'theo_quy_định', 'học_xong', 'nghỉ', 'được_công_nhận', 'học', 'vượt_quá', 'nghiên_cứu', 'bổ_sung_vào', 'giữ_bí_mật', 'bảo_vệ', 'chịu_trách_nhiệm', 'trước', 'nhấn', 'mở', 'tắt', 'bấm', 'chia_sẻ', 'trao_đổi', 'thắc_mắc', 'đăng_ký', 'chọn', 'phù_hợp', 'ở', 'cập_nhật_trên', 'lập', 'trình', 'qua', 'hủy', 'cho_phép_đăng_ký_ít_hơn_14_tín_chỉ', 'mở_thêm', 'kỷ_luật', 'thang_điểm', 'ít_hơn_hoặc_bằng', 'cấp', 'vào_cuối', 'tuyên_dương', 'căn_cứ', 'dưới', 'trừ', 'vô_lễ', 'lần_1', 'giao_cho', 'hạ_điểm', 'tài_sản_trong', 'làm_hư_hỏng', 'lần_2', 'lần_3', 'trái', 'xâm_phạm', 'chống_phá', 'thu_hồi', 'cao_nhất', 'cao_thứ_hai', 'quyết_định', 'phê_duyệt_duy_trì', 'chấp_thuận_mở_thêm', 'quy_định', 'phê_duyệt', 'đồng_ý', 'cho_phép', 'ra_quyết_định', 'duyệt_danh_sách_cấm_thi', 'chấp_thuận', 'duyệt_đơn', 'rà_soát', 'quyết_định_gia_hạn', 'phát_động', 'đề_nghị', 'chấm', 'quan_hệ', 'phản_hồi', 'cung_cấp', 'thanh_toán', 'lưu', 'dấu_và_chữ_ký', 'hiển_thị', 'tương_ứng', 'in', 'trạng_thái', 'kèm', 'giải_quyết', 'thông_báo_học_phần_cho', 'hướng_dẫn_đăng_ký_cho', 'công_bố_kết_quả_đăng_ký_cho', 'giúp_đỡ', 'ghi', 'đề_xuất_cấm_thi', 'nêu', 'hoặc', 'ký', 'tổ_chức_bảo_vệ', 'loại', 'trình_ký', 'đóng_dấu', 'hoạt_động', 'trị_giá', 'cao_hơn', 'hơn', 'trọng_số', 'làm_tròn', 'trích_từ', 'phối_hợp', 'một_lần', 'mỗi', 'đối_với', 'đóng_mộc', 'sửa_đổi', 'mã', 'nhân', 'tra_cứu', 'điện_thoại', 'thành_lập_từ', 'giúp', 'trả_nợ', 'cư_trú', 'gặp_khó_khăn', 'tư_vấn_xây_dựng_khht_cho', 'tối_thiểu', 'được_quy_định_trong', 'thông_báo_cho', 'thông_báo_lịch_thi', 'không_đạt', 'tính_vào', 'chuẩn', 'tổ_chức_thi_cho', 'cấp_bằng', 'dựa_vào', 'tính', 'không_tính', 'trung_bình_cộng', 'lưu_trong', 'ghi_vào', 'tiêu_chí', 'chỉ_đạo', 'phát_triển_trên', 'không_tổ_chức' 
   - Tên mối quan hệ phải được ghi thường. Nếu tên mối quan hệ gồm từ hai từ trở lên, các từ phải được nối với nhau bằng dấu gạch dưới (ví dụ: "không_tính", "thông_báo_lịch_thi"). 

3. Trả về kết quả dưới dạng JSON với các trường:
   - "entities": Danh sách các thực thể. Mỗi thực thể có các thuộc tính "name" và "type".
   - "relationships": Danh sách các mối quan hệ: . Mỗi mối quan hệ có các thuộc tính "source", "target", "relation", "type_source" và "type_target"(lấy từ entities).

Đoạn văn bản cần trích xuất:
{question}

Yêu cầu:
- Trả về kết quả dưới dạng JSON với các trường: entities, relationships.
- Mỗi entity cần có name và type.
- Mỗi relationship cần có source, target, relation, "type_source" và "type_target"(lấy từ entities).

---
### Giải thích:
1. **Entity**:
   - Là các đối tượng được nhắc đến trong văn bản, ví dụ: tên người, địa điểm, tổ chức, ngày tháng, v.v.
   - Mỗi entity cần được gán một loại phù hợp, ví dụ: NGƯỜI, ĐỊA ĐIỂM, TỔ CHỨC, NGÀY, v.v.

2. **Relationship**:
   - Là mối quan hệ giữa các entity, ví dụ: "Alice knows Bob" → quan hệ Biết giữa Alice và Bob.

3. **Định dạng đầu ra**:
   - Sử dụng JSON để trả về kết quả một cách có cấu trúc, dễ dàng xử lý tiếp theo."""


def rewrite_query():
    return """
    ("system", "Bạn là một trợ lý hữu ích, tạo ra nhiều truy vấn tìm kiếm dựa trên một truy vấn đầu vào duy nhất.
    Thực hiện mở rộng truy vấn. Nếu có nhiều cách phổ biến để diễn đạt một câu hỏi của người dùng hoặc 
    có các từ đồng nghĩa phổ biến cho các từ khóa trong câu hỏi, hãy đảm bảo trả về nhiều phiên bản của truy vấn với các cách diễn đạt khác nhau.
    Nếu có các từ viết tắt hoặc từ bạn không quen thuộc, đừng cố gắng diễn đạt lại chúng.
    Trả về 3 phiên bản khác nhau của câu hỏi.")

    ("human", {question})
    """




































