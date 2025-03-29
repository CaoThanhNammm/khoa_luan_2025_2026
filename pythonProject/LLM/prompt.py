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

def first_decision_stsv():
    return """Cho một câu hỏi về sổ tay sinh viên Nông Lâm năm 2024, nhiệm vụ của bạn là quyết định cách tiếp cận để tìm câu trả lời. Để làm điều này:
1. Xác định các từ khóa hoặc chủ đề chính trong câu hỏi liên quan đến sổ tay.
2. Xác định xem câu hỏi có thể được trả lời bằng cách tham khảo mục lục, cung cấp cái nhìn tổng quan về cấu trúc và các phần chính, hay cần đi sâu vào nội dung cụ thể trong các phần đó.
3. Nếu câu hỏi liên quan đến cấu trúc, các phần chính hoặc tổ chức chung của sổ tay, trả lời 'graph'.
4. Nếu câu hỏi yêu cầu thông tin cụ thể, quy định, hoặc chi tiết nằm trong các phần của sổ tay, trả lời 'text'.
5. Trả lời không quá 2 từ
Câu hỏi: {question}"""

def reflection_stsv():
    return """
        Thông tin lấy được không đúng. Trích xuất lại các thực thể chủ đề(topic entites) và quan hệ hữu ích(useful relationship) từ câu hỏi liên quan đến sổ tay Sinh viên Nông Lâm 2024.
        Sau đó, quyết định xem mục lục (graph) hay nội dung đầy đủ (text) hữu ích hơn để thu hẹp phạm vi tìm kiếm.
        Trả lời bằng 'graph' hoặc 'text'. Trả lời không quá 2 từ
        Câu hỏi: {question}
        Phản hồi: {feedback}
    """

def generator_stsv():
    return """
        Nhiệm vụ của bạn là dựa vào câu hỏi và các tài liệu khả thi mà tôi cung cấp, hãy trả lời câu hỏi:
        Câu hỏi: {question}
        Tài liệu khả thi: {references}
        Nếu tài liệu khả thi không có câu trả lời thì phản hồi "Tài liệu không có thông tin"
        Nếu tài liệu khả thi bị lặp lại thì hãy phản hồi "Câu trả lời không đổi"
    """

def valid_stsv():
    return """
        Điểm = 0
        Bạn là một bộ phận xác nhận cho các câu trả lời liên quan đến Sổ tay Sinh viên Nông Lâm 2024. Nhiệm vụ của bạn là đánh giá tính chính xác và đầy đủ của câu trả lời từ tác nhân dựa trên câu hỏi, câu trả lời và tài liệu khả thi.
        1. Kiểm tra xem câu trả lời có hợp ý nghĩa với câu hỏi không(Nếu có thì +2 điểm, nếu không thì -2 điểm).
        2. Xác minh rằng tất cả các nội dung trong câu trả lời đều được hỗ trợ bởi thông tin lấy được(Nếu có thì +2 điểm, nếu không thì -2 điểm).
        3. Đảm bảo không bỏ sót bất kỳ chi tiết quan trọng nào liên quan đến câu hỏi.(Nếu có thì +1 điểm, nếu không thì -1 điểm).
        4. Xác nhận rằng không có sai sót hay hiểu nhầm về thông tin lấy được.(Nếu có thì +3 điểm, nếu không thì -3 điểm).
        Nếu điểm > hoặc = 0 thì trả lời yes
        Nếu điểm  < 0 thì trả lời no
        Nếu câu trả lời bị lặp lại với các lần trước thì trả lời là yes
        Câu hỏi: {question}
        Câu trả lời: {answer}
        Tài liệu khả thi: {references}
        Trả lời không quá 2 từ
    """

def commentor_stsv():
    return """
    Câu hỏi: {question}
    Thực thể chủ đề: {action}
    Quan hệ: {action}
    Hãy chỉ ra thực thể chủ đề hoặc quan hệ nào được trích xuất sai từ câu hỏi liên quan đến Sổ tay Sinh viên Nông Lâm 2024, nếu có. Nếu không có sai sót, hãy xác nhận rằng các thực thể và quan hệ là chính xác dựa trên thông tin từ mục lục hoặc nội dung đầy đủ (text) của sổ tay.
    Đây là thông tin mục lục:
    "Phần 1: NLU - Định hướng trường đại học nghiên cứu:
    Quá trình hình thành và phát triển - Lịch sử và các giai đoạn phát triển của trường.
    Sứ mạng - Mục đích tồn tại và đóng góp của trường.
    Tầm nhìn - Định hướng phát triển tương lai của trường.
    Giá trị cốt lõi - Những nguyên tắc và niềm tin cơ bản của trường.
    Mục tiêu chiến lược - Các mục tiêu cụ thể trường hướng tới.
    Cơ sở vật chất - Giảng đường, thư viện, ký túc xá, trang thiết bị.
    Các đơn vị trong trường - Danh sách các phòng, ban, trung tâm, viện.
    Các khoa - ngành đào tạo - Danh sách các khoa và các ngành học.
    Tuần sinh hoạt công dân - sinh viên - Hoạt động định hướng đầu khóa cho tân sinh viên.
    Hoạt động phong trào sinh viên - Các hoạt động ngoại khóa, tình nguyện, văn nghệ, thể thao.
    Câu lạc bộ (CLB) - Đội, Nhóm - Danh sách các CLB, đội, nhóm sinh viên hoạt động.
    Cơ sở đào tạo - Địa chỉ các cơ sở chính và phân hiệu.
    
    Phần 2: HỌC TẬP VÀ RÈN LUYỆN:
    Quy chế sinh viên - Quyền lợi, nghĩa vụ và những điều sinh viên không được làm.
    Quy chế học vụ - Quy định về đăng ký, học tập, thi cử, đánh giá, tốt nghiệp.
    Quy định về việc đào tạo trực tuyến - Quy tắc và cách thức học tập online tại trường.
    Quy định khen thưởng, kỷ luật sinh viên - Các hình thức, tiêu chuẩn khen thưởng và xử lý vi phạm.
    Quy chế đánh giá kết quả rèn luyện - Tiêu chí và cách thức đánh giá điểm rèn luyện.
    Quy tắc ứng xử văn hóa của người học - Chuẩn mực giao tiếp, hành vi trong môi trường học đường.
    Cố vấn học tập - Vai trò và nhiệm vụ của người hỗ trợ sinh viên học tập.
    Danh hiệu sinh viên 5 tốt - Tiêu chí phấn đấu để đạt danh hiệu cao quý này.
    Danh hiệu sinh viên tiêu biểu - Tiêu chí xét chọn sinh viên xuất sắc hàng năm.
    
    Phần 3: HỖ TRỢ VÀ DỊCH VỤ:
    Quy định phân cấp giải quyết thắc mắc của sinh viên - Quy trình gửi và giải đáp các vấn đề của sinh viên.
    Thông tin học bổng - Các loại học bổng (khuyến khích, tài trợ) và cách xét duyệt.
    Vay vốn học tập từ ngân hàng chính sách xã hội - Hướng dẫn thủ tục vay vốn hỗ trợ học phí, sinh hoạt.
    Quy trình xác nhận hồ sơ sinh viên - Cách đăng ký và nhận các giấy xác nhận cần thiết.
    Hồ sơ yêu cầu bồi thường bảo hiểm tai nạn - Thủ tục cần chuẩn bị khi có tai nạn xảy ra.
    Thông tin về bảo hiểm y tế - Quy định bắt buộc và cách thức tham gia BHYT.
    Thông tin học bổng tài trợ - Học bổng tài trợ (>6 tỷ/năm) từ Quỹ Đồng hành hỗ trợ SV khó khăn/thành tích cao/năng động
    Hướng dẫn sử dụng các kênh thanh toán - Cách nộp học phí, BHYT qua ngân hàng, website.
    Tham vấn tâm lý học đường - Dịch vụ hỗ trợ tinh thần, giải tỏa căng thẳng cho sinh viên.
    Trung tâm Dịch vụ Sinh viên - Thông tin về ký túc xá, nhà ăn và các dịch vụ hỗ trợ khác."
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
    return f"""
    nhiệm vụ của bạn là dự đoán câu hỏi sau nằm trong phần nào dưới đây mà tôi cung cấp. Hãy trả lời ở phần nào, và ở mục nào của phần đó theo dạng json mà tôi cung cấp:
    "{{
    "episode": "",
    "part": ""
    }}"
    câu hỏi cần dự đoán: {question}
    Dưới đây là mục lục mà bạn cần dự đoán
    "Phần 1: NLU - Định hướng trường đại học nghiên cứu:
    Quá trình hình thành và phát triển - Lịch sử và các giai đoạn phát triển của trường.
    Sứ mạng - Mục đích tồn tại và đóng góp của trường.
    Tầm nhìn - Định hướng phát triển tương lai của trường.
    Giá trị cốt lõi - Những nguyên tắc và niềm tin cơ bản của trường.
    Mục tiêu chiến lược - Các mục tiêu cụ thể trường hướng tới.
    Cơ sở vật chất - Giảng đường, thư viện, ký túc xá, trang thiết bị.
    Các đơn vị trong trường - Danh sách các phòng, ban, trung tâm, viện.
    Các khoa - ngành đào tạo - Danh sách các khoa và các ngành học.
    Tuần sinh hoạt công dân - sinh viên - Hoạt động định hướng đầu khóa cho tân sinh viên.
    Hoạt động phong trào sinh viên - Các hoạt động ngoại khóa, tình nguyện, văn nghệ, thể thao.
    Câu lạc bộ (CLB) - Đội, Nhóm - Danh sách các CLB, đội, nhóm sinh viên hoạt động.
    Cơ sở đào tạo - Địa chỉ các cơ sở chính và phân hiệu.
    
    Phần 2: HỌC TẬP VÀ RÈN LUYỆN:
    Quy chế sinh viên - Quyền lợi, nghĩa vụ và những điều sinh viên không được làm.
    Quy chế học vụ - Quy định về đăng ký, học tập, thi cử, đánh giá, tốt nghiệp.
    Quy định về việc đào tạo trực tuyến - Quy tắc và cách thức học tập online tại trường.
    Quy định khen thưởng, kỷ luật sinh viên - Các hình thức, tiêu chuẩn khen thưởng và xử lý vi phạm.
    Quy chế đánh giá kết quả rèn luyện - Tiêu chí và cách thức đánh giá điểm rèn luyện.
    Quy tắc ứng xử văn hóa của người học - Chuẩn mực giao tiếp, hành vi trong môi trường học đường.
    Cố vấn học tập - Vai trò và nhiệm vụ của người hỗ trợ sinh viên học tập.
    Danh hiệu sinh viên 5 tốt - Tiêu chí phấn đấu để đạt danh hiệu cao quý này.
    Danh hiệu sinh viên tiêu biểu - Tiêu chí xét chọn sinh viên xuất sắc hàng năm.
    
    Phần 3: HỖ TRỢ VÀ DỊCH VỤ:
    Quy định phân cấp giải quyết thắc mắc của sinh viên - Quy trình gửi và giải đáp các vấn đề của sinh viên.
    Thông tin học bổng - Các loại học bổng (khuyến khích, tài trợ) và cách xét duyệt.
    Vay vốn học tập từ ngân hàng chính sách xã hội - Hướng dẫn thủ tục vay vốn hỗ trợ học phí, sinh hoạt.
    Quy trình xác nhận hồ sơ sinh viên - Cách đăng ký và nhận các giấy xác nhận cần thiết.
    Hồ sơ yêu cầu bồi thường bảo hiểm tai nạn - Thủ tục cần chuẩn bị khi có tai nạn xảy ra.
    Thông tin về bảo hiểm y tế - Quy định bắt buộc và cách thức tham gia BHYT.
        Thông tin học bổng tài trợ - Học bổng tài trợ (>6 tỷ/năm) từ Quỹ Đồng hành hỗ trợ SV khó khăn/thành tích cao/năng động
    Hướng dẫn sử dụng các kênh thanh toán - Cách nộp học phí, BHYT qua ngân hàng, website.
    Tham vấn tâm lý học đường - Dịch vụ hỗ trợ tinh thần, giải tỏa căng thẳng cho sinh viên.
    Trung tâm Dịch vụ Sinh viên - Thông tin về ký túc xá, nhà ăn và các dịch vụ hỗ trợ khác."
"""

# dùng để tạo mã cypher cho câu hỏi
def create_cypher_from_question(question):
    return f"""
    Nhiệm vụ của bạn là tạo mã cypher từ câu hỏi mà tôi đưa vào. Chỉ tạo ra mã cypher và không thêm bất cứ thông tin gì. Tất cả source đều ghi bằng chữ thường. Target chỉ có chữ e, không chỉ định gì thêm. 
Dưới đây tôi sẽ cung cấp cho bạn tất cả các type và relation mà bạn sẽ tạo ra, chỉ tạo ra type và relation mà tôi đã đề cập, không được thêm bất cứ từ nào: 
Đây là các type đã có sẵn: episode, part, organization, quantity, department, phone_number, website, center, institute, faculty, training_program, person, email, location, facility, activity, type_of_organization, concept, document, year, strategy, time, award, group_of_people, group, title, event, position, disciplinary_action, movement, abbreviation, percentage, beverage, item, network, frequency, action, material, code, device, system, status, clause, chapter, document_type, software, sequence, media, variable, natural_phenomenon, service, crime, grade, data, course_type, degree, assignment, criteria, subject, money, field, right, teaching_method, platform, account, image, feature
Đây là các relation đã có sẵn: website, có, là, tôn_trọng, theo, hủy, in, dưới, bị, mời, đối_với, của, gửi, không, gồm, trong, từ, email, công_bố, BAO_GỒM, sở_hữu, số_điện_thoại, thuộc_khoa, chương_trình_tiên_tiến_tại, chương_trình_nâng_cao_tại, chương_trình_đào_tạo_tại, quản_lý_bởi, chủ_nhiệm, trưởng_ban_điều_hành, đội_trưởng, số_lượng_sách, sử_dụng, số_lượng_phòng, sức_chứa, bao_gồm, về, sánh_vai, trên, đổi_mới, thúc_đẩy, phát_huy, xây_dựng, trở_thành, hàng_đầu, đáp_ứng, tầm_nhìn, tên_khác, trực_thuộc, tọa_lạc_tại, thuộc, thời_gian_hoạt_động, nhận_giải_thưởng, thành_lập, phục_vụ, đào_tạo, và, mục_tiêu_đến, sẽ_trở_thành, với, tổ_chức_bởi, được_đăng_tại, gìn_giữ_và_phát_huy, phát_hiện, nâng_đỡ, cho, đề_cao, hoạt_động_của, dành_cho, hỗ_trợ, tư_vấn, phù_hợp, hướng_dẫn, đăng_ký, ở, điều_chỉnh, xác_nhận, theo_dõi, cập_nhật_trên, không_dưới, ít_nhất, xem_xét, cấp, tham_gia, trường, tổ_chức, vào_cuối, tuyên_dương, khen_thưởng, căn_cứ, đánh_giá, phòng_chống, đạt, thang_điểm, chấp_hành, đến, không_vượt_quá, đánh_giá_qua, đoạt_giải, có_thành_tích, đóng_góp, hoạt_động_tại, thực_hiện, bảo_đảm_an_ninh, ít_hơn_hoặc_bằng, chọn, cao_nhất, cao_thứ_hai, bằng_nhau, công_nhận, xét, áp_dụng_bởi, thông_báo, gửi_thông_báo, làm, tham_dự, sau, chấm_dứt, trừ, vô_lễ, lần_1, giao_cho, hạ_điểm, tài_sản_trong, làm_hư_hỏng, lần_2, lần_3, trái, xâm_phạm, chống_phá, thu_hồi, lắng_nghe, hoàn_thành, nghiêm_túc, phát_động, hỏi, trả_lời, làm_phiền, quan_hệ, không_gây_ồn_ào, giữ_gìn, cung_cấp, nhận, dấu_và_chữ_ký, truy_cập, nhập, thanh_toán, hiển_thị, lưu, tại, tương_ứng, phản_hồi, đăng_nhập, chụp_ảnh, quét, đọc, lấy_ảnh, kiểm_tra, trạng_thái, chuyển_tới, viết, trực_tuyến, không_chấp_nhận, nộp, trao_đổi, thắc_mắc, đề_nghị, mang, được_hỗ_trợ, đi_học, chưa_được_sửa, mất, giúp_đỡ, nêu, hoặc, ghi, chuyển, ký, đã, kèm, giải_quyết, loại, bổ_sung, cập_nhật, trình_ký, đóng_dấu, hoạt_động, liên_hệ, như, cùng, xếp, so_sánh, không_cần, bằng, bố_trí, trọng_số, không_bị, quyết_định, cao_hơn, hơn, lập, trình, làm_tròn, trích_từ, do, phối_hợp, trị_giá, một_lần, qua, mỗi, đóng_mộc, sửa_đổi, mã, nhân, tra_cứu, quản_lý, điện_thoại, thành_lập_từ, vay, để, giúp, thủ_tục, gặp_khó_khăn, cư_trú, sinh_sống, đủ_tiêu_chuẩn, tối_đa, lãi_suất, thông_qua, trả_nợ, đóng_trụ_sở, tuân_thủ_quy_định_của, học_tập_tại, được_tôn_trọng_bởi, được_cung_cấp, được_sử_dụng, hoạt_động_trong, kiến_nghị_với, đề_đạt_nguyện_vọng_lên, được_ở, được_nhận, tuân_thủ_chủ_trương_của, tuân_thủ_pháp_luật_của, tuân_thủ_quy_chế_của, đóng, không_được_xúc_phạm, không_được_tham_gia, không_được, không_được_tổ_chức_hoạt_động_mà_chưa_được_cho_phép, cung_cấp_ctđt_cho, tư_vấn_xây_dựng_khht_cho, thông_báo_học_phần_cho, hướng_dẫn_đăng_ký_cho, thực_hiện_theo, đăng_ký_học_lại, cải_thiện_điểm, cho_phép_đăng_ký_ít_hơn_14_tín_chỉ, rút, không_đi_học, không_dự_thi, nhận_điểm_r, nhận_điểm_f, rút_học_phần_trên, đề_xuất_hủy_hoặc_mở_thêm, đăng_ký_trực_tuyến, công_bố_kết_quả_đăng_ký_cho, cải_thiện_kết_quả, đề_xuất, duy_trì, phê_duyệt_duy_trì, đề_xuất_mở_thêm, chấp_thuận_mở_thêm, mở_thêm, dự_thi, đề_xuất_cấm_thi, duyệt_danh_sách_cấm_thi, tối_thiểu, chuẩn, được_quy_định_trong, thông_báo_cho, thông_báo_lịch_thi, hưởng, chấp_thuận, duyệt_đơn, tổ_chức_thi_cho, xét_tương_đương, quy_định, rà_soát, phê_duyệt, xác_định, đồng_ý, không_đạt, tính_vào, xử_lý, xem_kết_quả, được_đánh_giá, tính, không_tính, dựa_vào, trung_bình_cộng, kỷ_luật, không_tham_gia, xếp_loại, lưu_trong, ghi_vào, đình_chỉ, tiêu_chí, cho_phép, chuyển_sang, cấp_bằng, chấm, thỏa_mản, phân_công, tổ_chức_bảo_vệ, thảo_luận, gia_hạn, quyết_định_gia_hạn, không_hoàn_thành, tích_lũy, ra_quyết_định, được_cấp, báo, bảo_lưu, được_điều_động, cần, theo_quy_định, học_xong, nghỉ, được_công_nhận, học, vượt_quá, nghiên_cứu, bổ_sung_vào, tăng_cường, áp_dụng, chỉ_đạo, phát_triển_trên, không_tổ_chức, giữ_bí_mật, bảo_vệ, chịu_trách_nhiệm, trước, nhấn, mở, tắt, bấm, chia_sẻ
Câu hỏi: {question}
Ví dụ về cypher mà bạn cần tạo:
1.MATCH (o:organization {{name: "trường đại học nông lâm thành phố hồ chí minh"}})-[r:trực_thuộc]->(e) RETURN o AS source, r AS relationship, e AS target 
2.MATCH (o:organization {{name: "trường đại học nông lâm thành phố hồ chí minh"}})-[r:tọa_lạc_tại]->(e) RETURN o AS source, r AS relationship, e AS target 
3.MATCH (o:organization {{name: "trường đại học nông lâm thành phố hồ chí minh"}})-[r:thời_gian_hoạt_động]->(e) RETURN o AS source, r AS relationship, e AS target 
4.MATCH (o:organization {{name: "trường đại học nông lâm thành phố hồ chí minh"}})-[r:nhận_giải_thưởng]->(e) RETURN o AS source, r AS relationship, e AS target 
5.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:là]->(e) RETURN o AS source, r AS relationship, e AS target 
6.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:đào_tạo]->(e) RETURN o AS source, r AS relationship, e AS target 
7.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:sẽ_trở_thành]->(e) RETURN o AS source, r AS relationship, e AS target 
8.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target 
9.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:trở_thành]->(e) RETURN o AS source, r AS relationship, e AS target 
10.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:phát_huy]->(e) RETURN o AS source, r AS relationship, e AS target 
11.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:xây_dựng]->(e) RETURN o AS source, r AS relationship, e AS target 
12.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:sánh_vai]->(e) RETURN o AS source, r AS relationship, e AS target 
13.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:đổi_mới]->(e) RETURN o AS source, r AS relationship, e AS target 
14.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:thúc_đẩy]->(e) RETURN o AS source, r AS relationship, e AS target 
15.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:sử_dụng]->(e) RETURN o AS source, r AS relationship, e AS target 
16.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
17.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
18.MATCH (o:organization {{name: "trường đại học nông lâm tp.hcm"}})-[r:email]->(e) RETURN o AS source, r AS relationship, e AS target 
19.MATCH (o:department {{name: "phòng công tác sinh viên"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
20.MATCH (o:department {{name: "phòng công tác sinh viên"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
21.MATCH (o:department {{name: "phòng đào tạo"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
22.MATCH (o:department {{name: "phòng đào tạo"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
23.MATCH (o:department {{name: "phòng đào tạo sau đại học"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
24.MATCH (o:department {{name: "phòng đào tạo sau đại học"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
25.MATCH (o:department {{name: "phòng hành chính"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
26.MATCH (o:department {{name: "phòng hành chính"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
27.MATCH (o:department {{name: "phòng hợp tác quốc tế"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
28.MATCH (o:department {{name: "phòng hợp tác quốc tế"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
29.MATCH (o:department {{name: "phòng kế hoạch tài chính"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
30.MATCH (o:department {{name: "phòng kế hoạch tài chính"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
31.MATCH (o:department {{name: "phòng quản lý chất lượng"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
32.MATCH (o:department {{name: "phòng quản lý chất lượng"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
33.MATCH (o:department {{name: "phòng quản trị vật tư"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
34.MATCH (o:department {{name: "phòng quản trị vật tư"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
35.MATCH (o:department {{name: "phòng tổ chức cán bộ"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
36.MATCH (o:department {{name: "phòng tổ chức cán bộ"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
37.MATCH (o:department {{name: "phòng thanh tra giáo dục"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
38.MATCH (o:department {{name: "phòng thanh tra giáo dục"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
39.MATCH (o:department {{name: "phòng thông tin và truyền thông"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
40.MATCH (o:department {{name: "phòng thông tin và truyền thông"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
41.MATCH (o:facility {{name: "thư viện"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
42.MATCH (o:facility {{name: "thư viện"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
43.MATCH (o:center {{name: "trung tâm dịch vụ sinh viên"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
44.MATCH (o:center {{name: "trung tâm dịch vụ sinh viên"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
45.MATCH (o:center {{name: "trung tâm nghiên cứu biến đổi khí hậu"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
46.MATCH (o:center {{name: "trung tâm nghiên cứu biến đổi khí hậu"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
47.MATCH (o:center {{name: "trung tâm nghiên cứu và ứng dụng công nghệ địa chính"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
48.MATCH (o:center {{name: "trung tâm nghiên cứu và ứng dụng công nghệ địa chính"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
49.MATCH (o:institute {{name: "viện nghiên cứu công nghệ sinh học và môi trường"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
50.MATCH (o:institute {{name: "viện nghiên cứu công nghệ sinh học và môi trường"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
51.MATCH (o:faculty {{name: "khoa công nghệ hóa học và thực phẩm"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
52.MATCH (o:faculty {{name: "khoa công nghệ hóa học và thực phẩm"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
53.MATCH (o:faculty {{name: "khoa công nghệ thông tin"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
54.MATCH (o:faculty {{name: "khoa công nghệ thông tin"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
55.MATCH (o:faculty {{name: "khoa cơ khí công nghệ"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
56.MATCH (o:faculty {{name: "khoa cơ khí công nghệ"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
57.MATCH (o:faculty {{name: "khoa chăn nuôi thú y"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
58.MATCH (o:faculty {{name: "khoa chăn nuôi thú y"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
59.MATCH (o:faculty {{name: "khoa kinh tế"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
60.MATCH (o:faculty {{name: "khoa kinh tế"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
61.MATCH (o:faculty {{name: "khoa khoa học"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
62.MATCH (o:faculty {{name: "khoa khoa học"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
63.MATCH (o:faculty {{name: "khoa khoa học sinh học"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
64.MATCH (o:faculty {{name: "khoa khoa học sinh học"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
65.MATCH (o:faculty {{name: "khoa lâm nghiệp"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
66.MATCH (o:faculty {{name: "khoa lâm nghiệp"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
67.MATCH (o:faculty {{name: "khoa môi trường và tài nguyên"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
68.MATCH (o:faculty {{name: "khoa môi trường và tài nguyên"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
69.MATCH (o:faculty {{name: "khoa nông học"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
70.MATCH (o:faculty {{name: "khoa nông học"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
71.MATCH (o:faculty {{name: "khoa ngoại ngữ - sư phạm"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
72.MATCH (o:faculty {{name: "khoa ngoại ngữ - sư phạm"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
73.MATCH (o:faculty {{name: "khoa quản lý đất đai và bất động sản"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
74.MATCH (o:faculty {{name: "khoa quản lý đất đai và bất động sản"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
75.MATCH (o:faculty {{name: "khoa thủy sản"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
76.MATCH (o:faculty {{name: "khoa thủy sản"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
77.MATCH (o:department_subject {{name: "bộ môn lý luận chính trị"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
78.MATCH (o:department_subject {{name: "bộ môn lý luận chính trị"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
79.MATCH (o:training_program {{name: "bất động sản"}})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target 
80.MATCH (o:training_program {{name: "công nghệ chế biến thủy sản"}})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target 
81.MATCH (o:training_program {{name: "lâm học"}})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target 
82.MATCH (o:training_program {{name: "quản lý tài nguyên rừng"}})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target 
83.MATCH (o:training_program {{name: "công nghệ thực phẩm"}})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target 
84.MATCH (o:training_program {{name: "thú y"}})-[r:thuộc_khoa]->(e) RETURN o AS source, r AS relationship, e AS target 
85.MATCH (o:person {{name: "sinh viên"}})-[r:có]->(e) RETURN o AS source, r AS relationship, e AS target 
86.MATCH (o:organization {{name: "clb cán bộ đoàn ngôi sao xanh"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
87.MATCH (o:organization {{name: "clb cán bộ đoàn ngôi sao xanh"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
88.MATCH (o:organization {{name: "bec english club"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
89.MATCH (o:organization {{name: "bec english club"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
90.MATCH (o:organization {{name: "clb bóng rổ đại học nông lâm"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
91.MATCH (o:organization {{name: "clb bóng rổ đại học nông lâm"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
92.MATCH (o:organization {{name: "clb du lịch sinh thái"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
93.MATCH (o:organization {{name: "clb du lịch sinh thái"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
94.MATCH (o:organization {{name: "clb dược thú y"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
95.MATCH (o:organization {{name: "clb dược thú y"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
96.MATCH (o:organization {{name: "fire english club"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
97.MATCH (o:organization {{name: "fire english club"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
98.MATCH (o:organization {{name: "clb karate-do"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
99.MATCH (o:organization {{name: "clb karate-do"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
100.MATCH (o:organization {{name: "clb kết nối thành công"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
101.MATCH (o:organization {{name: "clb kết nối thành công"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
102.MATCH (o:organization {{name: "clb khởi nghiệp (nlu startup club) nsc"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
103.MATCH (o:organization {{name: "clb khởi nghiệp (nlu startup club) nsc"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
104.MATCH (o:organization {{name: "clb một sức khỏe tp.hcm (hcmc one health club)"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
105.MATCH (o:organization {{name: "clb sách và hành động nông lâm tp.hcm"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
106.MATCH (o:organization {{name: "clb sách và hành động nông lâm tp.hcm"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
107.MATCH (o:organization {{name: "clb tiếng anh khoa công nghệ hóa học và thực phẩm (seeds for future) sff"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
108.MATCH (o:organization {{name: "clb tiếng anh khoa công nghệ hóa học và thực phẩm (seeds for future) sff"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
109.MATCH (o:organization {{name: "clb tiếng anh khoa kinh tế efb (english for business club) efb"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
110.MATCH (o:organization {{name: "clb tiếng anh khoa kinh tế efb (english for business club) efb"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
111.MATCH (o:organization {{name: "clb thú y engscope"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
112.MATCH (o:organization {{name: "clb truyền thông nông lâm radio"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
113.MATCH (o:organization {{name: "clb truyền thông nông lâm radio"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
114.MATCH (o:organization {{name: "wildlife vet student club"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
115.MATCH (o:organization {{name: "clb yêu môi trường"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
116.MATCH (o:organization {{name: "tổ tu dưỡng rèn luyện hạt giống đỏ"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
117.MATCH (o:organization {{name: "tổ tu dưỡng rèn luyện hạt giống đỏ"}})-[r:trưởng_ban_điều_hành]->(e) RETURN o AS source, r AS relationship, e AS target 
118.MATCH (o:organization {{name: "đội công tác xã hội"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
119.MATCH (o:organization {{name: "đội công tác xã hội"}})-[r:đội_trưởng]->(e) RETURN o AS source, r AS relationship, e AS target 
120.MATCH (o:organization {{name: "đội khát vọng tuổi trẻ khoa chăn nuôi thú y"}})-[r:đội_trưởng]->(e) RETURN o AS source, r AS relationship, e AS target 
121.MATCH (o:organization {{name: "đội nhiệt huyết rừng xanh"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
122.MATCH (o:organization {{name: "đội nhiệt huyết rừng xanh"}})-[r:đội_trưởng]->(e) RETURN o AS source, r AS relationship, e AS target 
123.MATCH (o:organization {{name: "đội văn nghệ rạng đông"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
124.MATCH (o:organization {{name: "đội văn nghệ rạng đông"}})-[r:đội_trưởng]->(e) RETURN o AS source, r AS relationship, e AS target 
125.MATCH (o:organization {{name: "đội văn nghệ xung kích nhịp điệu xanh"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
126.MATCH (o:organization {{name: "đội văn nghệ xung kích nhịp điệu xanh"}})-[r:đội_trưởng]->(e) RETURN o AS source, r AS relationship, e AS target 
127.MATCH (o:organization {{name: "đội xung kích khoa khoa học sinh học"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
128.MATCH (o:organization {{name: "đội xung kích khoa khoa học sinh học"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
129.MATCH (o:organization {{name: "hội cổ động viên (nong lam buffaloes) nlb"}})-[r:quản_lý_bởi]->(e) RETURN o AS source, r AS relationship, e AS target 
130.MATCH (o:organization {{name: "hội cổ động viên (nong lam buffaloes) nlb"}})-[r:chủ_nhiệm]->(e) RETURN o AS source, r AS relationship, e AS target 
131.MATCH (o:organization {{name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"}})-[r:tọa_lạc_tại]->(e) RETURN o AS source, r AS relationship, e AS target 
132.MATCH (o:organization {{name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
133.MATCH (o:organization {{name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
134.MATCH (o:organization {{name: "phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận"}})-[r:email]->(e) RETURN o AS source, r AS relationship, e AS target 
135.MATCH (o:organization {{name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"}})-[r:tọa_lạc_tại]->(e) RETURN o AS source, r AS relationship, e AS target 
136.MATCH (o:organization {{name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"}})-[r:số_điện_thoại]->(e) RETURN o AS source, r AS relationship, e AS target 
137.MATCH (o:organization {{name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"}})-[r:website]->(e) RETURN o AS source, r AS relationship, e AS target 
138.MATCH (o:organization {{name: "phân hiệu trường đại học nông lâm tp.hcm tại gia lai"}})-[r:email]->(e) RETURN o AS source, r AS relationship, e AS target



"""

# dùng để trích xuất entities và relationship cho câu hỏi
def extract_entities_relationship_from_question():
    return """Bạn là một hệ thống trích xuất thông tin từ văn bản. Nhiệm vụ của bạn là:
1. Trích xuất tất cả các thực thể có trong đoạn văn bản.
   - Mỗi thực thể cần có tên(name) và loại(type).  
   - Loại(type) hãy sử dụng các từ mà tôi cung cấp dưới đây: 
   "episode, part, organization, quantity, department, phone_number, website, center, institute, faculty, training_program, person, email, location, facility, activity, type_of_organization, concept, document, year, strategy, time, award, group_of_people, group, title, event, position, disciplinary_action, movement, abbreviation, percentage, beverage, item, network, frequency, action, material, code, device, system, status, clause, chapter, document_type, software, sequence, media, variable, natural_phenomenon, service, crime, grade, data, course_type, degree, assignment, criteria, subject, money, field, right, teaching_method, platform, account, image, feature"
2. Xác định các mối quan hệ(relaion) giữa các thực thể.  
    - Mỗi mối quan hệ phải có nguồn(source), tên mối quan hệ(relation) và loại của nguồn(type_source)(lấy từ entities). 
    - PHẢI sử dụng các mối quan hệ có sẵn dưới đây, nếu câu hỏi không có sẵn quan hệ bên dưới hãy tìm từ đồng nghĩa, KHÔNG ĐƯỢC LẤY LẠI MỐI QUAN HỆ Ở CÂU HỎI:
    "website, có, là, tôn_trọng, theo, hủy, in, dưới, bị, mời, đối_với, của, gửi, không, gồm, trong, từ, email, công_bố, BAO_GỒM, sở_hữu, số_điện_thoại, thuộc_khoa, chương_trình_tiên_tiến_tại, chương_trình_nâng_cao_tại, chương_trình_đào_tạo_tại, quản_lý_bởi, chủ_nhiệm, trưởng_ban_điều_hành, đội_trưởng, số_lượng_sách, sử_dụng, số_lượng_phòng, sức_chứa, bao_gồm, về, sánh_vai, trên, đổi_mới, thúc_đẩy, phát_huy, xây_dựng, trở_thành, hàng_đầu, đáp_ứng, tầm_nhìn, tên_khác, trực_thuộc, tọa_lạc_tại, thuộc, thời_gian_hoạt_động, nhận_giải_thưởng, thành_lập, phục_vụ, đào_tạo, và, mục_tiêu_đến, sẽ_trở_thành, với, tổ_chức_bởi, được_đăng_tại, gìn_giữ_và_phát_huy, phát_hiện, nâng_đỡ, cho, đề_cao, hoạt_động_của, dành_cho, hỗ_trợ, tư_vấn, phù_hợp, hướng_dẫn, đăng_ký, ở, điều_chỉnh, xác_nhận, theo_dõi, cập_nhật_trên, không_dưới, ít_nhất, xem_xét, cấp, tham_gia, trường, tổ_chức, vào_cuối, tuyên_dương, khen_thưởng, căn_cứ, đánh_giá, phòng_chống, đạt, thang_điểm, chấp_hành, đến, không_vượt_quá, đánh_giá_qua, đoạt_giải, có_thành_tích, đóng_góp, hoạt_động_tại, thực_hiện, bảo_đảm_an_ninh, ít_hơn_hoặc_bằng, chọn, cao_nhất, cao_thứ_hai, bằng_nhau, công_nhận, xét, áp_dụng_bởi, thông_báo, gửi_thông_báo, làm, tham_dự, sau, chấm_dứt, trừ, vô_lễ, lần_1, giao_cho, hạ_điểm, tài_sản_trong, làm_hư_hỏng, lần_2, lần_3, trái, xâm_phạm, chống_phá, thu_hồi, lắng_nghe, hoàn_thành, nghiêm_túc, phát_động, hỏi, trả_lời, làm_phiền, quan_hệ, không_gây_ồn_ào, giữ_gìn, cung_cấp, nhận, dấu_và_chữ_ký, truy_cập, nhập, thanh_toán, hiển_thị, lưu, tại, tương_ứng, phản_hồi, đăng_nhập, chụp_ảnh, quét, đọc, lấy_ảnh, kiểm_tra, trạng_thái, chuyển_tới, viết, trực_tuyến, không_chấp_nhận, nộp, trao_đổi, thắc_mắc, đề_nghị, mang, được_hỗ_trợ, đi_học, chưa_được_sửa, mất, giúp_đỡ, nêu, hoặc, ghi, chuyển, ký, đã, kèm, giải_quyết, loại, bổ_sung, cập_nhật, trình_ký, đóng_dấu, hoạt_động, liên_hệ, như, cùng, xếp, so_sánh, không_cần, bằng, bố_trí, trọng_số, không_bị, quyết_định, cao_hơn, hơn, lập, trình, làm_tròn, trích_từ, do, phối_hợp, trị_giá, một_lần, qua, mỗi, đóng_mộc, sửa_đổi, mã, nhân, tra_cứu, quản_lý, điện_thoại, thành_lập_từ, vay, để, giúp, thủ_tục, gặp_khó_khăn, cư_trú, sinh_sống, đủ_tiêu_chuẩn, tối_đa, lãi_suất, thông_qua, trả_nợ, đóng_trụ_sở, tuân_thủ_quy_định_của, học_tập_tại, được_tôn_trọng_bởi, được_cung_cấp, được_sử_dụng, hoạt_động_trong, kiến_nghị_với, đề_đạt_nguyện_vọng_lên, được_ở, được_nhận, tuân_thủ_chủ_trương_của, tuân_thủ_pháp_luật_của, tuân_thủ_quy_chế_của, đóng, không_được_xúc_phạm, không_được_tham_gia, không_được, không_được_tổ_chức_hoạt_động_mà_chưa_được_cho_phép, cung_cấp_ctđt_cho, tư_vấn_xây_dựng_khht_cho, thông_báo_học_phần_cho, hướng_dẫn_đăng_ký_cho, thực_hiện_theo, đăng_ký_học_lại, cải_thiện_điểm, cho_phép_đăng_ký_ít_hơn_14_tín_chỉ, rút, không_đi_học, không_dự_thi, nhận_điểm_r, nhận_điểm_f, rút_học_phần_trên, đề_xuất_hủy_hoặc_mở_thêm, đăng_ký_trực_tuyến, công_bố_kết_quả_đăng_ký_cho, cải_thiện_kết_quả, đề_xuất, duy_trì, phê_duyệt_duy_trì, đề_xuất_mở_thêm, chấp_thuận_mở_thêm, mở_thêm, dự_thi, đề_xuất_cấm_thi, duyệt_danh_sách_cấm_thi, tối_thiểu, chuẩn, được_quy_định_trong, thông_báo_cho, thông_báo_lịch_thi, hưởng, chấp_thuận, duyệt_đơn, tổ_chức_thi_cho, xét_tương_đương, quy_định, rà_soát, phê_duyệt, xác_định, đồng_ý, không_đạt, tính_vào, xử_lý, xem_kết_quả, được_đánh_giá, tính, không_tính, dựa_vào, trung_bình_cộng, kỷ_luật, không_tham_gia, xếp_loại, lưu_trong, ghi_vào, đình_chỉ, tiêu_chí, cho_phép, chuyển_sang, cấp_bằng, chấm, thỏa_mản, phân_công, tổ_chức_bảo_vệ, thảo_luận, gia_hạn, quyết_định_gia_hạn, không_hoàn_thành, tích_lũy, ra_quyết_định, được_cấp, báo, bảo_lưu, được_điều_động, cần, theo_quy_định, học_xong, nghỉ, được_công_nhận, học, vượt_quá, nghiên_cứu, bổ_sung_vào, tăng_cường, áp_dụng, chỉ_đạo, phát_triển_trên, không_tổ_chức, giữ_bí_mật, bảo_vệ, chịu_trách_nhiệm, trước, nhấn, mở, tắt, bấm, chia_sẻ"
    - Tên mối quan hệ phải được ghi thường. Nếu tên mối quan hệ gồm từ hai từ trở lên, các từ phải được nối với nhau bằng dấu gạch dưới (ví dụ: "không_tính", "thông_báo_lịch_thi"). 

3. Trả về kết quả dưới dạng JSON với các trường:
   - "entities": Danh sách các thực thể. Mỗi thực thể có các thuộc tính "name" và "type".
   - "relationships": Danh sách các mối quan hệ: . Mỗi mối quan hệ có các thuộc tính "source", "relation" và "type_source"(lấy từ entities).

Đoạn văn bản cần trích xuất:
{question}

Yêu cầu:
- Trả về kết quả dưới dạng JSON với các trường: entities, relationships.
- Mỗi entity cần có name và type.
- Mỗi relationship cần có source, relation và "type_source"(lấy từ entities).

---
### Giải thích:
1. **Entity**:
   - Là các đối tượng được nhắc đến trong văn bản, ví dụ: tên người, địa điểm, tổ chức, ngày tháng, v.v.
   - Mỗi entity cần được gán một loại phù hợp, ví dụ: NGƯỜI, ĐỊA ĐIỂM, TỔ CHỨC, NGÀY, v.v.

2. **Relationship**:
   - Là mối quan hệ giữa các entity, nhưng không trích xuất target

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

def extract_text_from_paragraph(paragraph):
    return f"""
    Bạn là một trợ lý AI chuyên xử lý văn bản tự nhiên. Tôi có một văn bản lớn và muốn bạn giúp tôi trích xuất các đoạn văn nhỏ từ văn bản đó để lưu vào vectordatabase. Hãy thực hiện theo các yêu cầu sau:

1. Chia văn bản thành các đoạn nhỏ, mỗi đoạn có độ dài từ 100 đến 200 từ (hoặc khoảng 2-4 câu, tùy vào ngữ cảnh), nhưng không được cắt giữa chừng làm mất nghĩa của câu hoặc ý chính.

2. Đảm bảo mỗi đoạn nhỏ giữ được ý nghĩa độc lập hoặc liên quan chặt chẽ đến ngữ cảnh của văn bản gốc, không bị rời rạc.

3. Các đoạn văn nhỏ phải liền mạch với nhau, nghĩa là nội dung của đoạn sau phải có sự kết nối tự nhiên với đoạn trước, giống như trong văn bản gốc.

4. Trả về kết quả dưới dạng json có thuộc tính text lưu trữ từng đoạn văn.

5. Nếu có câu hoặc ý nào quá dài, hãy điều chỉnh để đoạn văn vẫn nằm trong khoảng độ dài mong muốn mà không làm mất ý nghĩa.

6. BẮT BUỘC TRÍCH XUẤT ĐÀY ĐỦ NỘI DUNG CỦA VĂN BẢN, KHÔNG ĐƯỢC CHỈNH SỬA NỘI DUNG NHƯ THÊM HOẶC BỚT, KHÔNG ĐƯỢC ĐÍNH KÈM CÁC TỪ CHUNG CHUNG NHƯ "các liên kết dưới đây" hoặc "các thông tin sau"nếu như từ đó không có trong văn bản.
7. có thể thêm các từ để bổ sung ý nghĩa cho 1 câu như "khu vực A có email kva@gmai..com", "Khư vực B có số điện thoại 0901231212"
Dưới đây là văn bản lớn mà tôi cung cấp:
{paragraph}"""

def chunking(paragraph):
    return f"""
    Bạn là một trợ lý AI chuyên xử lý văn bản tự nhiên. Nhiệm vụ của bạn là giúp tôi trích xuất các đoạn văn nhỏ từ văn bản lớn. Tôi sẽ đưa vào một văn bản lớn. Hãy thực hiện theo các yêu cầu sau:

1. Chia văn bản thành các đoạn nhỏ, mỗi đoạn có độ dài từ 100 đến 200 từ (hoặc khoảng 2-4 câu, tùy vào ngữ cảnh), nhưng không được cắt giữa chừng làm mất nghĩa của câu hoặc ý chính.
2. Đảm bảo mỗi đoạn nhỏ giữ được ý nghĩa độc lập và liên quan chặt chẽ đến ngữ cảnh của văn bản gốc, không bị rời rạc.
3. Các đoạn văn nhỏ phải liền mạch với nhau, nghĩa là nội dung của đoạn sau phải có sự kết nối tự nhiên với đoạn trước, giống như trong văn bản gốc.
4. Trả về kết quả dưới dạng json như sau:
{{
'đoạn 1': '',
'đoạn 2': '',
'đoạn 3': '',
'đoạn 4': '',
....
}}
5. Phải trích xuất từ đầu đến cuối, một cách liên tục và liền mạch mà không bỏ lỡ bất kỳ từ gì

Dưới đây là văn bản lớn mà tôi cung cấp:
{paragraph}
Hãy trích xuất các đoạn văn nhỏ theo yêu cầu trên và trả lời bằng tiếng Việt."""

def rewrite_question(question):
    return f"""
        Nhiệm vụ của bạn là ghi lại câu hỏi một cách đầy đủ chủ ngữ, vị ngữ để bổ sung đầy đủ ý nghĩa cho câu. 
        Hãy dựa vào các relationship dưới đây mà bạn có thể thay thế từ ghép nào có thể đồng nghĩa với câu hỏi ban đầu
        "website, có, là, tôn_trọng, theo, hủy, in, dưới, bị, mời, đối_với, của, gửi, không, gồm, trong, từ, email, công_bố, BAO_GỒM, sở_hữu, số_điện_thoại, thuộc_khoa, chương_trình_tiên_tiến_tại, chương_trình_nâng_cao_tại, chương_trình_đào_tạo_tại, quản_lý_bởi, chủ_nhiệm, trưởng_ban_điều_hành, đội_trưởng, số_lượng_sách, sử_dụng, số_lượng_phòng, sức_chứa, bao_gồm, về, sánh_vai, trên, đổi_mới, thúc_đẩy, phát_huy, xây_dựng, trở_thành, hàng_đầu, đáp_ứng, tầm_nhìn, tên_khác, trực_thuộc, tọa_lạc_tại, thuộc, thời_gian_hoạt_động, nhận_giải_thưởng, thành_lập, phục_vụ, đào_tạo, và, mục_tiêu_đến, sẽ_trở_thành, với, tổ_chức_bởi, được_đăng_tại, gìn_giữ_và_phát_huy, phát_hiện, nâng_đỡ, cho, đề_cao, hoạt_động_của, dành_cho, hỗ_trợ, tư_vấn, phù_hợp, hướng_dẫn, đăng_ký, ở, điều_chỉnh, xác_nhận, theo_dõi, cập_nhật_trên, không_dưới, ít_nhất, xem_xét, cấp, tham_gia, trường, tổ_chức, vào_cuối, tuyên_dương, khen_thưởng, căn_cứ, đánh_giá, phòng_chống, đạt, thang_điểm, chấp_hành, đến, không_vượt_quá, đánh_giá_qua, đoạt_giải, có_thành_tích, đóng_góp, hoạt_động_tại, thực_hiện, bảo_đảm_an_ninh, ít_hơn_hoặc_bằng, chọn, cao_nhất, cao_thứ_hai, bằng_nhau, công_nhận, xét, áp_dụng_bởi, thông_báo, gửi_thông_báo, làm, tham_dự, sau, chấm_dứt, trừ, vô_lễ, lần_1, giao_cho, hạ_điểm, tài_sản_trong, làm_hư_hỏng, lần_2, lần_3, trái, xâm_phạm, chống_phá, thu_hồi, lắng_nghe, hoàn_thành, nghiêm_túc, phát_động, hỏi, trả_lời, làm_phiền, quan_hệ, không_gây_ồn_ào, giữ_gìn, cung_cấp, nhận, dấu_và_chữ_ký, truy_cập, nhập, thanh_toán, hiển_thị, lưu, tại, tương_ứng, phản_hồi, đăng_nhập, chụp_ảnh, quét, đọc, lấy_ảnh, kiểm_tra, trạng_thái, chuyển_tới, viết, trực_tuyến, không_chấp_nhận, nộp, trao_đổi, thắc_mắc, đề_nghị, mang, được_hỗ_trợ, đi_học, chưa_được_sửa, mất, giúp_đỡ, nêu, hoặc, ghi, chuyển, ký, đã, kèm, giải_quyết, loại, bổ_sung, cập_nhật, trình_ký, đóng_dấu, hoạt_động, liên_hệ, như, cùng, xếp, so_sánh, không_cần, bằng, bố_trí, trọng_số, không_bị, quyết_định, cao_hơn, hơn, lập, trình, làm_tròn, trích_từ, do, phối_hợp, trị_giá, một_lần, qua, mỗi, đóng_mộc, sửa_đổi, mã, nhân, tra_cứu, quản_lý, điện_thoại, thành_lập_từ, vay, để, giúp, thủ_tục, gặp_khó_khăn, cư_trú, sinh_sống, đủ_tiêu_chuẩn, tối_đa, lãi_suất, thông_qua, trả_nợ, đóng_trụ_sở, tuân_thủ_quy_định_của, học_tập_tại, được_tôn_trọng_bởi, được_cung_cấp, được_sử_dụng, hoạt_động_trong, kiến_nghị_với, đề_đạt_nguyện_vọng_lên, được_ở, được_nhận, tuân_thủ_chủ_trương_của, tuân_thủ_pháp_luật_của, tuân_thủ_quy_chế_của, đóng, không_được_xúc_phạm, không_được_tham_gia, không_được, không_được_tổ_chức_hoạt_động_mà_chưa_được_cho_phép, cung_cấp_ctđt_cho, tư_vấn_xây_dựng_khht_cho, thông_báo_học_phần_cho, hướng_dẫn_đăng_ký_cho, thực_hiện_theo, đăng_ký_học_lại, cải_thiện_điểm, cho_phép_đăng_ký_ít_hơn_14_tín_chỉ, rút, không_đi_học, không_dự_thi, nhận_điểm_r, nhận_điểm_f, rút_học_phần_trên, đề_xuất_hủy_hoặc_mở_thêm, đăng_ký_trực_tuyến, công_bố_kết_quả_đăng_ký_cho, cải_thiện_kết_quả, đề_xuất, duy_trì, phê_duyệt_duy_trì, đề_xuất_mở_thêm, chấp_thuận_mở_thêm, mở_thêm, dự_thi, đề_xuất_cấm_thi, duyệt_danh_sách_cấm_thi, tối_thiểu, chuẩn, được_quy_định_trong, thông_báo_cho, thông_báo_lịch_thi, hưởng, chấp_thuận, duyệt_đơn, tổ_chức_thi_cho, xét_tương_đương, quy_định, rà_soát, phê_duyệt, xác_định, đồng_ý, không_đạt, tính_vào, xử_lý, xem_kết_quả, được_đánh_giá, tính, không_tính, dựa_vào, trung_bình_cộng, kỷ_luật, không_tham_gia, xếp_loại, lưu_trong, ghi_vào, đình_chỉ, tiêu_chí, cho_phép, chuyển_sang, cấp_bằng, chấm, thỏa_mản, phân_công, tổ_chức_bảo_vệ, thảo_luận, gia_hạn, quyết_định_gia_hạn, không_hoàn_thành, tích_lũy, ra_quyết_định, được_cấp, báo, bảo_lưu, được_điều_động, cần, theo_quy_định, học_xong, nghỉ, được_công_nhận, học, vượt_quá, nghiên_cứu, bổ_sung_vào, tăng_cường, áp_dụng, chỉ_đạo, phát_triển_trên, không_tổ_chức, giữ_bí_mật, bảo_vệ, chịu_trách_nhiệm, trước, nhấn, mở, tắt, bấm, chia_sẻ"
        Hãy trả về 1 câu hỏi đã được ghi lại, không trả lời quá 1 câu
        Câu hỏi: {question}
    """






























