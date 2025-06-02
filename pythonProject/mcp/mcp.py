import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI
from mcp.server.fastmcp import fastMCP
import mcp

app = FastAPI()
mcp_app = fastMCP(app)


# Định nghĩa các kiểu dữ liệu
class Entity:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type

    def __str__(self):
        return f"{self.name} ({self.type})"


class Relationship:
    def __init__(self, source: str, target: str, type: str):
        self.source = source
        self.target = target
        self.type = type

    def __str__(self):
        return f"{self.source} --{self.type}--> {self.target}"


class Action:
    def __init__(self, name: str, params: Dict[str, Any] = None):
        self.name = name
        self.params = params or {}

    def __str__(self):
        params_str = ", ".join([f"{k}={v}" for k, v in self.params.items()])
        return f"{self.name}({params_str})"


class QueryState:
    def __init__(self,
                 question: str,
                 entities: List[Entity] = None,
                 relationships: List[Relationship] = None,
                 actions: List[Action] = None,
                 retrieved_info: str = "",
                 answer: str = "",
                 is_valid: bool = False,
                 comments: str = "",
                 iterations: int = 0):
        self.question = question
        self.entities = entities or []
        self.relationships = relationships or []
        self.actions = actions or []
        self.retrieved_info = retrieved_info
        self.answer = answer
        self.is_valid = is_valid
        self.comments = comments
        self.iterations = iterations

    def reset_for_iteration(self):
        """Reset the state for a new iteration while preserving the question and comments."""
        self.iterations += 1
        # Keep question, increment iterations, preserve comments
        # but reset other fields for new cycle
        self.entities = []
        self.relationships = []
        self.actions = []
        self.retrieved_info = ""
        self.answer = ""
        self.is_valid = False


# Định nghĩa knowledge bank mẫu
@mcp.resource()
def knowledge_bank():
    return {
        "product_info": {
            "smartphone": "Smartphone XYZ có màn hình 6.5 inch, chip A15, pin 5000mAh, giá 10 triệu đồng.",
            "laptop": "Laptop ABC có màn hình 15.6 inch, CPU Core i7, RAM 16GB, SSD 512GB, giá 25 triệu đồng.",
            "smartwatch": "Smartwatch DEF có màn hình 1.4 inch, đo nhịp tim, theo dõi giấc ngủ, giá 3 triệu đồng."
        },
        "pricing_info": {
            "smartphone": 10000000,
            "laptop": 25000000,
            "smartwatch": 3000000
        },
        "inventory_status": {
            "smartphone": "Còn hàng",
            "laptop": "Còn hàng",
            "smartwatch": "Hết hàng"
        },
        "shipping_policy": "Miễn phí vận chuyển cho đơn hàng trên 1 triệu đồng. Thời gian giao hàng 2-3 ngày."
    }


# 1. First Decision Agent - trích xuất entities, relationships và actions
@mcp.prompt()
def entity_extraction_prompt(question: str):
    return f"""
    Hãy phân tích câu hỏi sau và trích xuất các thực thể (entities), mối quan hệ (relationships) và hành động (actions) liên quan.

    Câu hỏi: {question}

    Entities: Liệt kê các thực thể chính trong câu hỏi (sản phẩm, dịch vụ, người dùng, v.v.) và loại của chúng.
    Ví dụ: smartphone (product), giá (attribute)

    Relationships: Xác định mối quan hệ giữa các thực thể.
    Ví dụ: smartphone --has_attribute--> giá

    Actions: Xác định các hành động cần thực hiện để trả lời câu hỏi.
    Các hành động có thể là: get_product_info, get_price, check_inventory, get_shipping_policy

    Trả về kết quả dưới dạng danh sách rõ ràng.
    """


@mcp.tool()
def first_decision(state: QueryState) -> QueryState:
    """Trích xuất entities, relationships và actions từ câu hỏi."""
    # Gọi LLM với prompt để trích xuất thông tin
    extraction_result = mcp.llm.complete(entity_extraction_prompt(state.question))

    # Phân tích kết quả từ LLM và cập nhật state
    # Đây là phần giả lập, trong thực tế cần phân tích văn bản từ LLM

    # Phân tích entities từ kết quả
    entities_section = extraction_result.split("Entities:")[1].split("Relationships:")[0]
    for line in entities_section.strip().split("\n"):
        if line.strip():
            parts = line.split("(")
            if len(parts) > 1:
                name = parts[0].strip()
                type = parts[1].replace(")", "").strip()
                state.entities.append(Entity(name, type))

    # Phân tích relationships từ kết quả
    if "Relationships:" in extraction_result and "Actions:" in extraction_result:
        relationships_section = extraction_result.split("Relationships:")[1].split("Actions:")[0]
        for line in relationships_section.strip().split("\n"):
            if "--" in line and "-->" in line:
                source = line.split("--")[0].strip()
                target = line.split("-->")[1].strip()
                rel_type = line.split("--")[1].split("-->")[0].strip()
                state.relationships.append(Relationship(source, target, rel_type))

    # Phân tích actions từ kết quả
    actions_section = extraction_result.split("Actions:")[1] if "Actions:" in extraction_result else ""
    for line in actions_section.strip().split("\n"):
        if line.strip():
            if "(" in line and ")" in line:
                name = line.split("(")[0].strip()
                params_str = line.split("(")[1].split(")")[0]
                params = {}
                if params_str:
                    for param in params_str.split(","):
                        if "=" in param:
                            k, v = param.split("=", 1)
                            params[k.strip()] = v.strip()
                state.actions.append(Action(name, params))
            else:
                state.actions.append(Action(line.strip()))

    return state


# 2. Retrieval Bank Agent - lựa chọn nguồn thông tin dựa trên action
@mcp.tool()
def retrieval_bank(state: QueryState) -> QueryState:
    """Truy xuất thông tin từ bank dựa trên actions."""
    bank = knowledge_bank()
    retrieved_info = []

    for action in state.actions:
        if action.name == "get_product_info":
            for entity in state.entities:
                if entity.type == "product" and entity.name in bank["product_info"]:
                    retrieved_info.append(bank["product_info"][entity.name])

        elif action.name == "get_price":
            for entity in state.entities:
                if entity.type == "product" and entity.name in bank["pricing_info"]:
                    price = bank["pricing_info"][entity.name]
                    retrieved_info.append(f"Giá của {entity.name} là {price:,} đồng.")

        elif action.name == "check_inventory":
            for entity in state.entities:
                if entity.type == "product" and entity.name in bank["inventory_status"]:
                    status = bank["inventory_status"][entity.name]
                    retrieved_info.append(f"Tình trạng kho hàng của {entity.name}: {status}.")

        elif action.name == "get_shipping_policy":
            retrieved_info.append(bank["shipping_policy"])

    state.retrieved_info = "\n".join(retrieved_info)
    return state


# 3. Generator Agent - tạo câu trả lời dựa trên thông tin đã truy xuất
@mcp.prompt()
def answer_generation_prompt(question: str, retrieved_info: str):
    return f"""
    Dựa trên câu hỏi và thông tin đã truy xuất được, hãy tạo câu trả lời đầy đủ và chính xác.

    Câu hỏi: {question}

    Thông tin truy xuất được:
    {retrieved_info}

    Hãy tạo câu trả lời ngắn gọn, đầy đủ và chính xác dựa trên thông tin trên.
    """


@mcp.tool()
def generator(state: QueryState) -> QueryState:
    """Tạo câu trả lời dựa trên thông tin truy xuất."""
    if not state.retrieved_info:
        state.answer = "Xin lỗi, tôi không có đủ thông tin để trả lời câu hỏi này."
        return state

    # Gọi LLM để tạo câu trả lời
    state.answer = mcp.llm.complete(answer_generation_prompt(state.question, state.retrieved_info))
    return state


# 4. Validator Agent - kiểm tra câu trả lời có phù hợp với câu hỏi không
@mcp.prompt()
def validation_prompt(question: str, answer: str):
    return f"""
    Hãy đánh giá xem câu trả lời có đáp ứng đầy đủ yêu cầu trong câu hỏi hay không.

    Câu hỏi: {question}
    Câu trả lời: {answer}

    Tiêu chí đánh giá:
    1. Câu trả lời có liên quan trực tiếp đến câu hỏi
    2. Câu trả lời cung cấp đầy đủ thông tin được yêu cầu
    3. Câu trả lời không chứa thông tin sai lệch

    Kết luận: (chỉ trả lời "yes" nếu đáp ứng tất cả tiêu chí, ngược lại trả lời "no")
    """


@mcp.tool()
def validator(state: QueryState) -> QueryState:
    """Kiểm tra câu trả lời có phù hợp với câu hỏi không."""
    validation_result = mcp.llm.complete(validation_prompt(state.question, state.answer))

    # Phân tích kết quả từ LLM
    if "yes" in validation_result.lower():
        state.is_valid = True
    else:
        state.is_valid = False

    return state


# 5. Commentor Agent - phản ánh câu trả lời để điều chỉnh hành động
@mcp.prompt()
def commentor_prompt(question: str, answer: str, entities: List[str], actions: List[str]):
    entities_str = ", ".join([str(e) for e in entities])
    actions_str = ", ".join([str(a) for a in actions])

    return f"""
    Hãy phân tích và đưa ra nhận xét về câu trả lời hiện tại, đồng thời đề xuất cách cải thiện.

    Câu hỏi: {question}
    Câu trả lời hiện tại: {answer}

    Các thực thể đã trích xuất: {entities_str}
    Các hành động đã thực hiện: {actions_str}

    Hãy cung cấp:
    1. Đánh giá về mức độ phù hợp của câu trả lời với câu hỏi
    2. Xác định thông tin còn thiếu hoặc không chính xác
    3. Đề xuất các thực thể hoặc hành động bổ sung cần thực hiện

    Nêu rõ các đề xuất để cải thiện câu trả lời trong lần lặp tiếp theo.
    """


@mcp.tool()
def commentor(state: QueryState) -> QueryState:
    """Phản ánh câu trả lời để điều chỉnh hành động."""
    entity_strs = [str(e) for e in state.entities]
    action_strs = [str(a) for a in state.actions]

    state.comments = mcp.llm.complete(
        commentor_prompt(state.question, state.answer, entity_strs, action_strs)
    )

    return state


# 6. Self Reflection Agent - nhận feedback để trích xuất lại
@mcp.prompt()
def self_reflection_prompt(question: str, comments: str):
    return f"""
    Dựa trên câu hỏi ban đầu và các nhận xét về câu trả lời hiện tại, hãy điều chỉnh quá trình trích xuất.

    Câu hỏi: {question}
    Nhận xét: {comments}

    Hãy trích xuất lại:

    Entities: Liệt kê các thực thể chính cần chú ý (có thể thêm thực thể mới hoặc loại bỏ thực thể không phù hợp)
    Ví dụ: smartphone (product), giá (attribute)

    Relationships: Xác định lại mối quan hệ giữa các thực thể
    Ví dụ: smartphone --has_attribute--> giá

    Actions: Xác định lại các hành động cần thực hiện để trả lời câu hỏi tốt hơn
    Các hành động có thể là: get_product_info, get_price, check_inventory, get_shipping_policy

    Trả về kết quả dưới dạng danh sách rõ ràng.
    """


@mcp.tool()
def self_reflection(state: QueryState) -> QueryState:
    """Nhận feedback để trích xuất lại entities, relationships và actions."""
    # Reset state cho vòng lặp mới
    state.reset_for_iteration()

    # Gọi LLM để trích xuất lại dựa trên nhận xét
    reflection_result = mcp.llm.complete(self_reflection_prompt(state.question, state.comments))

    # Phân tích kết quả từ LLM và cập nhật state
    # Tương tự như first_decision, nhưng sử dụng thông tin từ reflection

    # Phân tích entities từ kết quả
    if "Entities:" in reflection_result and "Relationships:" in reflection_result:
        entities_section = reflection_result.split("Entities:")[1].split("Relationships:")[0]
        for line in entities_section.strip().split("\n"):
            if line.strip():
                parts = line.split("(")
                if len(parts) > 1:
                    name = parts[0].strip()
                    type = parts[1].replace(")", "").strip()
                    state.entities.append(Entity(name, type))

    # Phân tích relationships từ kết quả
    if "Relationships:" in reflection_result and "Actions:" in reflection_result:
        relationships_section = reflection_result.split("Relationships:")[1].split("Actions:")[0]
        for line in relationships_section.strip().split("\n"):
            if "--" in line and "-->" in line:
                source = line.split("--")[0].strip()
                target = line.split("-->")[1].strip()
                rel_type = line.split("--")[1].split("-->")[0].strip()
                state.relationships.append(Relationship(source, target, rel_type))

    # Phân tích actions từ kết quả
    if "Actions:" in reflection_result:
        actions_section = reflection_result.split("Actions:")[1]
        for line in actions_section.strip().split("\n"):
            if line.strip():
                if "(" in line and ")" in line:
                    name = line.split("(")[0].strip()
                    params_str = line.split("(")[1].split(")")[0]
                    params = {}
                    if params_str:
                        for param in params_str.split(","):
                            if "=" in param:
                                k, v = param.split("=", 1)
                                params[k.strip()] = v.strip()
                    state.actions.append(Action(name, params))
                else:
                    state.actions.append(Action(line.strip()))

    return state


# Hàm chính để khởi động toàn bộ quy trình
@mcp.tool()
def process_question(question: str, max_iterations: int = 3) -> Dict:
    """Xử lý câu hỏi thông qua hệ thống Agent."""
    state = QueryState(question=question)

    # Vòng lặp chính của hệ thống
    for i in range(max_iterations):
        # 1. First decision / self reflection (từ lần lặp thứ 2)
        if i == 0:
            state = first_decision(state)
        else:
            state = self_reflection(state)

        # 2. Retrieval bank
        state = retrieval_bank(state)

        # 3. Generator
        state = generator(state)

        # 4. Validator
        state = validator(state)

        # Kiểm tra xem câu trả lời đã hợp lệ chưa
        if state.is_valid:
            break

        # 5. Commentor (nếu không hợp lệ)
        state = commentor(state)

    # Kết quả cuối cùng
    return {
        "question": state.question,
        "answer": state.answer,
        "is_valid": state.is_valid,
        "iterations": state.iterations
    }


# API endpoint để tiếp nhận và xử lý câu hỏi
@app.post("/query")
async def query_endpoint(question: str, max_iterations: int = 3):
    """API endpoint để tiếp nhận và xử lý câu hỏi."""
    result = process_question(question, max_iterations)
    return result


# Sử dụng ví dụ
if __name__ == "__main__":
    import uvicorn

    # Ví dụ về cách sử dụng
    print("Ví dụ sử dụng hệ thống:")
    result = process_question("Giá của laptop là bao nhiêu và có còn hàng không?")
    print(f"Câu hỏi: {result['question']}")
    print(f"Câu trả lời: {result['answer']}")
    print(f"Hợp lệ: {result['is_valid']}")
    print(f"Số lần lặp: {result['iterations']}")

    # Khởi động API server
    uvicorn.run(app, host="0.0.0.0", port=8000)