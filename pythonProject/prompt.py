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

def prompt_agent():
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

def prompt_reflection():
    return """
        The retrieved document is incorrect.
        Feedback: "Error - Entity 'Tesla' was categorized as 'Company' instead of 'Organization'; Relation 'works_for' was incorrectly applied to a location context."
        Question: "Does Elon Musk work for Tesla?"
        The retrieved document is incorrect. Answer again based on newly extracted topic entities and useful relations. Is knowledge graph or text documents helpful to narrow down the 
        search space? You must answer with either of them with no more than two words.
    """

def prompt_valid():
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

def prompt_commentor():
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

def prompt_extract_entities_relationship():
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