import time

import pandas as pd

import general
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import spearmanr
import os
from dotenv import load_dotenv
load_dotenv()

def generate_answer(model, question):
    resp = model.generate_content(question)
    return resp.text

# Hit@K
def hit_at_k(y_true, y_pred, k):
    return int(y_true in y_pred[:k])

# Recall@K
def recall_at_k(y_true, y_pred, k):
    return int(y_true in y_pred[:k]) / min(k, len(y_pred))

# MRR - Mean Reciprocal Rank
def mrr(y_true, y_pred):
    try:
        rank = y_pred.index(y_true) + 1
        return 1 / rank
    except ValueError:
        return 0

# Tính cosine similarity
def cosine_similarity_score(v1, v2):
    print(v1)
    print(v2)
    return cosine_similarity([v1], [v2])[0][0]

# Tính Spearman cosine similarity
def spearman_cosine(vecs1, vecs2):
    cosines = [cosine_similarity_score(v1, v2) for v1, v2 in zip(vecs1, vecs2)]
    return spearmanr(cosines)

# Hàm đánh giá mô hình trên các câu hỏi
def evaluate_model(model, data, top_k=20):
    hit_1, hit_5, recall_20, total_mrr = 0, 0, 0, 0
    cosines, spearman_cosines = [], []
    call = 0
    for i, row in data.iterrows():
        question, true_answer = row['query'], row['answers']
        print(question,': ', true_answer)
        predicted_answers = generate_answer(model, question)  # Mô hình trả về danh sách dự đoán
        print('predicted_answers: ', predicted_answers)
        hit_1 += hit_at_k(true_answer, predicted_answers, 1)
        hit_5 += hit_at_k(true_answer, predicted_answers, 5)
        recall_20 += recall_at_k(true_answer, predicted_answers, top_k)
        total_mrr += mrr(true_answer, predicted_answers)
        call += 1
        print('call: ', call)
        if call == 10:
            time.sleep(120)
            call = 0

        # Giả sử vector embedding của các câu trả lời được tính từ mô hình
        # true_vec = general.encode(true_answer)
        # pred_vecs = [general.encode(ans) for ans in predicted_answers[:top_k]]  # Vector của các câu trả lời dự đoán
        #
        # for pred_vec in pred_vecs:
        #     cosines.append(cosine_similarity_score(true_vec, pred_vec))
        #
        # spearman_cosines.append(spearman_cosine([true_vec], pred_vecs)[0])

    num_samples = len(data)
    return {
        "Hit@1": hit_1 / num_samples,
        "Hit@5": hit_5 / num_samples,
        "Recall@20": recall_20 / num_samples,
        "MRR": total_mrr / num_samples,
        # "Person Cosine": np.mean(cosines),
        # "Spearman Cosine": np.mean(spearman_cosines)
    }

# Đánh giá chỉ sử dụng LLM
model_name = os.getenv("model")
prompt = """
Hãy sử dụng những dữ liệu đã được huấn luyện của bạn để trả lời các câu hỏi. 
Trả lời ngắn gọn, súc tích. Nếu không biết hoặc không thể truy cập thì hãy trở lời tôi không biết hoặc không thể truy cập
Nếu biết thì hãy trả lời theo dạng sau:
name: Tên của bệnh/dị tật
type: Loại, được xác định là một "disease" (bệnh).
    + disease
    + gene/protein
    + molecular_function
    + drug
    + pathway
    + anatomy
    + effect/phenotype
    + biological_process
    + cellular_component
    + exposure
source: Nguồn thông tin đến từ cơ sở dữ liệu, một cơ sở dữ liệu về các bệnh hiếm gặp.
details: Nói về chi tiết hơn bệnh/dị tật
"""
model = general.load_model(model_name, prompt)
dataset = pd.read_csv('dataset/prime/prime_auto_qa.csv')

evaluation_results = evaluate_model(model, dataset)
for metric, score in evaluation_results.items():
    print(f"{metric}: {score:.4f}")





