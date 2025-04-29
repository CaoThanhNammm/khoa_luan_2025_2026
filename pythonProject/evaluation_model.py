import json
import time
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import spearmanr
from scipy.stats import rankdata
import os
import numpy as np
from dotenv import load_dotenv
from LLM.Gemini import Gemini
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
def cosine_similarity(vector1, vector2):
    # Tính tích vô hướng
    dot_product = np.dot(vector1, vector2)
    # Tính độ dài (norm) của từng vector
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    # Tính cosine similarity
    if norm1 == 0 or norm2 == 0:
        return 0.0  # Tránh chia cho 0
    return dot_product / (norm1 * norm2)

# Tính Spearman cosine similarity
def spearman_cosine(vector1, vector2):
    # Chuyển vector thành thứ hạng (rank)
    rank1 = rankdata(vector1, method='average')
    rank2 = rankdata(vector2, method='average')
    # Tính cosine similarity trên vector thứ hạng
    return cosine_similarity(rank1, rank2)

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
# prompt = """
# Hãy sử dụng những dữ liệu đã được huấn luyện của bạn để trả lời các câu hỏi.
# Trả lời ngắn gọn, súc tích. Nếu không biết hoặc không thể truy cập thì hãy trở lời tôi không biết hoặc không thể truy cập
# Nếu biết thì hãy trả lời theo dạng sau:
# name: Tên của bệnh/dị tật
# type: # Loại, được xác định là một "disease" (bệnh).
#     + disease
#     + gene/protein
#     + molecular_function
#     + drug
#     + pathway
#     + anatomy
#     + effect/phenotype
#     + biological_process
#     + cellular_component
#     + exposure
# source: Nguồn thông tin đến từ cơ sở dữ liệu, một cơ sở dữ liệu về các bệnh hiếm gặp.
# details: Nói về chi tiết hơn bệnh/dị tật
# """
#
api_key = os.getenv("API_KEY")
model_name = os.getenv("MODEL")
gemini = Gemini(model_name, api_key)
#
# # dataset = pd.read_csv('dataset/prime/prime_auto_qa.csv')
# #
# # evaluation_results = evaluate_model(model, dataset)
# # for metric, score in evaluation_results.items():
# #     print(f"{metric}: {score:.4f}")
#
#
# qa_truth = pd.read_csv('qa_human.csv')
# my_qa = pd.read_csv('D:\PycharmProjects\pythonProject\my_qa_human.csv')
#
# answer_truth = qa_truth.answer
# answer_predict = my_qa.answer
#
# question_truth = qa_truth.question
# question_predict = my_qa.question
#
# similarity_score = 0
# spearman_score = 0
# df = pd.DataFrame()
# file_name = 'evaluation_1.csv'
#
# for i in range(0, len(question_truth)):
#     embed_truth = gemini.encode(json.loads(answer_truth[i]))
#     embed_predict = gemini.encode(answer_predict[i])
#
#     similarity_score += cosine_similarity(embed_truth, embed_predict)
#     spearman_score += spearman_cosine(embed_truth, embed_predict)
#     new_row = pd.DataFrame({
#         'embed_truth': [embed_truth],
#         'embed_predict': [embed_predict]
#     })
#     df = pd.concat([df, new_row], ignore_index=True)
#     if len(df) % 10 == 0:
#         print(df)
#         print("save")
#         df.to_csv(fr"C:\Users\Nam\Desktop\{file_name}", encoding='utf-8-sig')
#
#     print(f'{i}: {cosine_similarity(embed_truth, embed_predict)} and {spearman_cosine(embed_truth, embed_predict)}')
#
# print(f'similarity_score: {similarity_score/len(answer_truth)}')
# print(f'spearman_score: {spearman_score/len(answer_truth)}')

# ----------------------------------------------------------------------------------------
truth = pd.read_csv('qa_human_hybrid.csv')
predict = pd.read_csv('my_qa_hybrid_grag.csv')

embeds_truth = truth.answer
embeds_predict = predict.answer
similarity_score = 0
spearman_score = 0

for i in range(len(embeds_truth)):
    print(i)
    encode_truth = gemini.encode(embeds_truth[i])
    encode_predict = gemini.encode(embeds_predict[i])

    similarity_score += cosine_similarity(encode_truth, encode_predict)
    spearman_score += spearman_cosine(encode_truth, encode_predict)

print(f'similarity_score: {similarity_score/len(embeds_truth)}')
print(f'spearman_score: {spearman_score/len(embeds_truth)}')



# benchmark data my_qa.csv embedding 004 (RAG + GRAG + LLM)
# similarity_score: 0.8015445589374844
# spearman_score: 0.9464503249841755

# benchmark data my_qa_human.csv embedding 004 (RAG + GRAG + LLM)
# similarity_score: 0.7749737597910906
# spearman_score: 0.9395749651892696

# benchmark data my_qa_human.csv intfloat/multilingual-e5-large (RAG + GRAG + LLM)
# similarity_score: 0.8570323586463928
# spearman_score: 0.9635358473051144

# benchmark data my_qa_human_hybrid.csv intfloat/multilingual-e5-large (RAG + GRAG + LLM)
# similarity_score: 0.892623782157898
# spearman_score: 0.9722299487490241

# benchmark data my_qa_human_hybrid.csv intfloat/multilingual-e5-large (RAG + LLM)
# similarity_score: 0.8894450664520264
# spearman_score: 0.9713068594485564

# benchmark data my_qa_human_hybrid.csv intfloat/multilingual-e5-large (GRAG + LLM)
# similarity_score: 0.8492812514305115
# spearman_score: 0.9616331415421461

# -----------------------------------------------------------------------------------------------
#
# a = 'Trường được thành lập vào năm 1955 với tên gọi Trường Đại học Nông Lâm và hiện nay nằm ở Thành phố Thủ Đức, Thành phố Hồ Chí Minh và Thành phố Dĩ An - Tỉnh Bình Dương.'
# b = 'Trường được thành lập vào năm 1234 với tên gọi Trường Đại học Nông Lâm và hiện nay nằm ở Mỹ'
# a_encode = gemini.encode(a)
# b_encode = gemini.encode(b)
#
# similarity_score = cosine_similarity(a_encode, b_encode)
# print(similarity_score)




