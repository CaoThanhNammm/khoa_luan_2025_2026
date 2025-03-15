<<<<<<< HEAD
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import configparser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import threading
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
import time
import concurrent.futures
import pytz


def config_chrome():
  options = webdriver.ChromeOptions()
  options.add_argument("--headless") # Chạy ở chế độ ẩn
  options.add_argument("--no-sandbox") # Tắt chế độ sandbox
  options.add_argument("--disable-dev-shm-usage") # Sử dụng bộ nhớ ảo
  return webdriver.Chrome(options=options)


def worker_task(hrefs_chunk):
    # Mỗi worker tự khởi tạo driver riêng
    driver = config_chrome()
    products = []
    hrefs_error = []

    for idx, href in enumerate(hrefs_chunk, start=1):
        # In thông báo sau mỗi 1000 lần lặp
        if idx % 1000 == 0:
            print(f"Worker {driver}: Đã xử lý {idx} mục")
        try:
            driver.get(href[0])
            name = driver.find_element(By.XPATH,
                                       '//*[@id="__next"]/div/div[4]/div[3]/div[1]/div[2]/div[1]/div[1]/h1').text
            price = driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/div/div[4]/div[3]/div[1]/div[2]/div[1]/div[3]/b').text
            price_sale = ''
            description_01 = driver.find_element(By.XPATH,
                                                 '//*[@id="__next"]/div/div[4]/div[3]/div[1]/div[2]/div[1]/div[2]').text
            description_02 = driver.find_element(By.XPATH,
                                                 '//*[@id="__next"]/div/div[4]/div[3]/div[2]/div/div[1]/div/p').text
            config_text = driver.find_element(By.XPATH,
                                              '//*[@id="__next"]/div/div[4]/div[3]/div[2]/div/div[2]/div').text
            short_des = ''
            category_id = href[1]
            products.append(
                [name, price, price_sale, description_01, description_02, config_text, short_des, category_id])
        except Exception as e:
            hrefs_error.append(href[0])
            print('Link bị lỗi:', href[0])
            continue

    driver.quit()
    return products, hrefs_error


def get_detail_product(hrefs, num_workers=5):
    # Chia danh sách hrefs thành các chunk gần bằng nhau cho mỗi worker
    chunk_size = (len(hrefs) + num_workers - 1) // num_workers  # Làm tròn lên
    chunks = [hrefs[i:i + chunk_size] for i in range(0, len(hrefs), chunk_size)]

    all_products = []
    all_errors = []

    # Sử dụng ThreadPoolExecutor với 5 worker
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(worker_task, chunk) for chunk in chunks]
        for future in concurrent.futures.as_completed(futures):
            products_chunk, errors_chunk = future.result()
            all_products.extend(products_chunk)
            all_errors.extend(errors_chunk)

    # Tạo DataFrame từ danh sách sản phẩm thu thập được
    columns = ['name', 'price', 'price_sale', 'des_01', 'des_02', 'config', 'short_des', 'category_id']
    df_products = pd.DataFrame(all_products, columns=columns)
    return df_products, all_errors

p_00 = pd.read_csv('C:/Users/Nam/Desktop/New folder/products_00.csv')
p_01 = pd.read_csv('C:/Users/Nam/Desktop/New folder/products_01.csv')
p_02 = pd.read_csv('C:/Users/Nam/Desktop/New folder/products_02.csv')
p_03 = pd.read_csv('C:/Users/Nam/Desktop/New folder/products_03.csv')
p_04 = pd.read_csv('C:/Users/Nam/Desktop/New folder/products_04.csv')
p_05 = pd.read_csv('C:/Users/Nam/Desktop/New folder/products_05.csv')
p_06 = pd.read_csv('C:/Users/Nam/Desktop/New folder/products_06.csv')
p_07 = pd.read_csv('C:/Users/Nam/Desktop/New folder/products_07.csv')
p_08 = pd.read_csv('C:/Users/Nam/Desktop/New folder/products_08.csv')
p_09 = pd.read_csv('C:/Users/Nam/Desktop/New folder/products_09.csv')

combined_df = pd.concat([p_00, p_01, p_02, p_03, p_04, p_05, p_06, p_07, p_08, p_09], ignore_index=True)
abc = np.array_split(combined_df, 40)
combined_df_02 = abc[2]
combined_df_03 = abc[3]

data_list_02 = combined_df_02.values.tolist()
data_list_03 = combined_df_03.values.tolist()


products_02, hrefs_error_02 = get_detail_product(data_list_02)
products_03, hrefs_error_03 = get_detail_product(data_list_03)


a = pd.DataFrame(products_02)
b = pd.DataFrame(hrefs_error_02)


a.to_csv('products_03.csv', index=False)
b.to_csv('urls_error_03.csv', index=False)

a = pd.DataFrame(products_03)
b = pd.DataFrame(hrefs_error_03)

a.to_csv('products_04.csv', index=False)
b.to_csv('urls_error_04.csv', index=False)









=======
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import math
import torch
import wikipedia
from newspaper import Article, ArticleException
from GoogleNews import GoogleNews
from pyvis.network import Network
import IPython

from KB import KB


def load_model():
    tokenizer = AutoTokenizer.from_pretrained("Babelscape/rebel-large")
    model = AutoModelForSeq2SeqLM.from_pretrained("Babelscape/rebel-large")
    return model, tokenizer

def extract_relations_from_model_output(text):
    relations = []
    relation, subject, relation, object_ = '', '', '', ''
    text = text.strip()
    current = 'x'
    text_replaced = text.replace("<s>", "").replace("<pad>", "").replace("</s>", "")
    for token in text_replaced.split():
        if token == "<triplet>":
            current = 't'
            if relation != '':
                relations.append({
                    'head': subject.strip(),
                    'type': relation.strip(),
                    'tail': object_.strip()
                })
                relation = ''
            subject = ''
        elif token == "<subj>":
            current = 's'
            if relation != '':
                relations.append({
                    'head': subject.strip(),
                    'type': relation.strip(),
                    'tail': object_.strip()
                })
            object_ = ''
        elif token == "<obj>":
            current = 'o'
            relation = ''
        else:
            if current == 't':
                subject += ' ' + token
            elif current == 's':
                object_ += ' ' + token
            elif current == 'o':
                relation += ' ' + token
    if subject != '' and relation != '' and object_ != '':
        relations.append({
            'head': subject.strip(),
            'type': relation.strip(),
            'tail': object_.strip()
        })
    return relations



# build a knowledge base from text
def from_small_text_to_kb(text, model, tokenizer, verbose=False):
    kb = KB()

    # Tokenizer text
    model_inputs = tokenizer(text, max_length=512, padding=True, truncation=True,
                            return_tensors='pt')
    if verbose:
        print(f"Num tokens: {len(model_inputs['input_ids'][0])}")

    # Generate
    gen_kwargs = {
        "max_length": 216,
        "length_penalty": 0,
        "num_beams": 3,
        "num_return_sequences": 3
    }
    generated_tokens = model.generate(
        **model_inputs,
        **gen_kwargs,
    )
    decoded_preds = tokenizer.batch_decode(generated_tokens, skip_special_tokens=False)

    # create kb
    for sentence_pred in decoded_preds:
        relations = extract_relations_from_model_output(sentence_pred)
        for r in relations:
            kb.add_relation(r)

    return kb

# test the `from_small_text_to_kb` function

text = "Napoleon Bonaparte (born Napoleone di Buonaparte; 15 August 1769 – 5 " \
"May 1821), and later known by his regnal name Napoleon I, was a French military " \
"and political leader who rose to prominence during the French Revolution and led " \
"several successful campaigns during the Revolutionary Wars. He was the de facto " \
"leader of the French Republic as First Consul from 1799 to 1804. As Napoleon I, " \
"he was Emperor of the French from 1804 until 1814 and again in 1815. Napoleon's " \
"political and cultural legacy has endured, and he has been one of the most " \
"celebrated and controversial leaders in world history."

model, tokenizer = load_model()
kb = from_small_text_to_kb(text, model, tokenizer, verbose=True)
kb.print()
>>>>>>> parent of 48b251f (xây dựng kg, viết phần mở đầu tài liệu)
