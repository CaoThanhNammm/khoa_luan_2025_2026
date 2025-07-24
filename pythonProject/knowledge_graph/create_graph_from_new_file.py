import os

from LLM import prompt
from LLM.Llama import Llama
from PreProcessing.PreProcessing import PreProcessing
from PreProcessing.ProcessingPdf import PDF
from knowledge_graph.KnowledgeGraphDatabase import Neo4j
import json
from dotenv import load_dotenv
load_dotenv()
import ast
import uuid

if __name__ == "__main__":
    # Thay đổi thông tin kết nối theo cấu hình Neo4j của bạn
    # folder_pdf = r"D:\PycharmProjects\dataset\vmlu\vi_squad.pdf"
    uri = os.getenv("URI_NEO")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    model_llama_405b = os.getenv("MODEL_LLAMA_405B")
    model_llama_70b = os.getenv("MODEL_LLAMA_70B")
    # pre_processing = PreProcessing()
    api_key_01 =  os.getenv("API_KEY_NVIDIA_01")
    api_key_02 =  os.getenv("API_KEY_NVIDIA_02")

    # Tạo instance của class Neo4j, llama, pdf
    neo = Neo4j(uri, user, password)
    llama_title = Llama(api_key_01, model_llama_70b)
    llama_content = Llama(api_key_02, model_llama_405b)

    llama_content.set_prompt(prompt.extract_entities_relationship_from_text())
    llama_content.set_text("""Thành lập xã Ia Khai (Ia Grai) trên cơ sở một phần xã Ia Krái. Xã Ia Khai có 16.518,5 ha diện tích tự
nhiên và 2.475 nhân khẩu. Thành lập xã Ia Nhin (Chư Păh) trên cơ sở một phần xã Ia Ka. Xã Ia Nhin
có 3.205 ha diện tích tự nhiên và 3.758 nhân khẩu. Điều chỉnh địa giới hành chính 2 xã Ia Mơ Nông
và xã Ia Phí (Chư Păh). Thành lập xã Ia Ly (Chư Păh) trên cơ sở một phần xã Ia Mơ Nông. Xã Ia Ly có
4.844 ha diện tích tự nhiên và 4.570 nhân khẩu. Xã Ia Mơ Nông có 16.951 ha diện tích tự nhiên và
4.071 nhân khẩu. Xã Ia Phí có 6.995 ha diện tích tự nhiên và 5.172 nhân khẩu.Các phiên bảnNhiều
phiên bản của UDF đã được phát hành: Bản sửa đổi 1,00 (ngày 24 tháng 10 năm 1995). Bản phát
hành gốc. Bản sửa đổi 1.01 (ngày 3 tháng 11 năm 1995). Thêm Phụ lục DVD và thực hiện một vài
thay đổi nhỏ. Phiên bản 1.02 (ngày 30 tháng 8 năm 1996). Định dạng này được đĩa DVD-Video sử
dụng. Bản sửa đổi 1.50 (ngày 4 tháng 2 năm 1997). Đã thêm hỗ trợ ghi lại (ảo) trên phương tiện CDR/DVD-R bằng cách giới thiệu cấu trúc VAT. Đã thêm các bảng trống dự phòng để quản lý lỗi trên các
phương tiện ghi lại được như CD-RW và DVD-RW và DVD+RW.Cách tính điểmThang điểm của IELTS
là từ 1 – 9. Trên bảng kết quả của thí sinh sẽ thể hiện điểm của từng kỹ năng thi. Phần điểm tổng sẽ
được tính dựa trên điểm trung bình cộng của 4 kỹ năng.Điểm tổng của 4 kỹ năng sẽ được làm tròn số
theo quy ước chung như sau: Nếu điểm trung bình cộng của 4 kỹ năng có số lẻ là.25, thì sẽ được làm
tròn lên thành.5, còn nếu là.75 sẽ được làm tròn thành 1.0.Ví dụ: một thí sinh có số điểm như sau:
6.5 (Nghe), 6.5 (Đọc), 5.0 (Viết) và 7.0 (Nói). Điểm trung bình của thí sinh này là 6.5 (25 ÷ 4 = 6.25 =
6.5)Mycobacterium elephantis's đã được nghiên cứu để cung cấp một số hiểu biết về bản chất di
truyền của sinh vật này. Một chủng M. elephantis, Lipa, chứa hàm lượng GC 67,8% và kích thước bộ
gen là 5,19 Mb. 250 pseudogenes cũng được tìm thấy trong chủng này.<ref name=":4">Chuỗi gen
484 t (giống như DSM 44368) 16S rRNA so với các mycobacterium phát triển nhanh khác cho thấy độ
tương đồng trung bình 96,7+ 0,5%. Nó cũng cho thấy một sự tương đồng 96,2+ 0,4% với
mycobacteria phát triển chậm. Những nước láng giềng gần nhất thể hiện sự tương đồng nhất với M.
voi là M. confluentis ở 97,8% và M. phlei ở 97,7%. Mặc dù liên quan chặt chẽ, chủng 484 t cho thấy
29 và 30 nucleotide khác biệt trong các loài quen thuộc.Drupal 6 được phát hành vào ngày
13/02/2008. Vào ngày 5/3/2009, Buytaert thông báo đóng-băng-mã kể từ ngày 1/9/2009 để chuẩn
bị cho Drupal 7. Drupal 7 được phát hành vào ngày 5/1/2011, với các đối tác phát hành ở nhiều quốc
gia. Sau đó, việc bảo trì Drupal 5 bị chấm dứt, chỉ còn Drupal 6 và Drupal 7 được bảo trì. Cập nhật
cho các phiên bản Drupal 7 được phát hành thường xuyên. Việc chấm dứt bảo trì cho Drupal 7 theo
kế hoạch là vào tháng 11 năm 2021, nhưng vì ảnh hưởng của dịch COVID-19, đã được dời sang tháng
11 năm 2022. Drupal 8 sẽ vẫn bị ngừng bảo trì vào ngày 2 tháng 11 năm 2021.Nó có 3 hành tinh quá
cảnh được quan sát bởi tàu vũ trụ Kepler trong cuộc khảo sát K2 của họ. Kể từ tháng 10 năm 2017,
đây là ngôi sao gần nhất được phát hiện có các ngoại hành tinh quá cảnh được tìm thấy bởi các
nhiệm vụ Kepler hoặc K2. Các hành tinh (b, c, d) có bán kính bằng 1,62, 1,27 và 2,09 lần so với Trái
Đất và các khoảng thời gian 1,209, 3.648 và 6.201 ngày (tỷ lệ 1: 3: 5). Do khoảng cách gần, hệ thống
được coi là mục tiêu tuyệt vời để nghiên cứu khí quyển của các ngoại hành tinh.Cầu thủ ghi bàn
nhiều nhất trong 1 mùa giải: 12 – Clive Allen (Tottenham Hotspur, mùa giải 1986–87)Cầu thủ ghi bàn
nhiều nhất trong 1 trận đấu: 6 – Frankie Bunn (Oldham Athletic vs Scarborough, ngày 25 tháng 10
năm 1989)Chiến thắng với tỷ số lớn nhất:Liverpool 10–0 Fulham ở vòng 2 lượt đi ngày 23 tháng 9
năm 1986West Ham United 10–0 Bury ở vòng 2 lượt về ngày 25 tháng 10 năm 1983Chiến thắng với
tổng tỷ số lớn nhất sau 2 lượt trận ở vòng bán kết: Manchester City 10–0 Burton Albion (9–0 sân
nhà, 1–0 sân khách), ngày 23 tháng 1 năm 2019.Năm đĩa đơn được ra mắt cho việc quảng bá album
— "Thinkin Bout You" vào 17 tháng 4, "Pyramids" vào 8 tháng 6, "Sweet Life" vào 6 tháng 7,, "Lost"
vào 17 tháng 12, và "Super Rich Kids" vào 17 tháng 3 năm 2013. "Thinkin Bout You" là đĩa đơn đạt
được thứ hạng cao nhất của Ocean tại Hoa Kỳ, đứng thứ 32 trên bảng xếp hạng Billboard Hot 100.
Ocean đã biểu diễn ca khúc tại giải thưởng MTV Video Music Awards 2012 vào 6 tháng 9. Vào 15
tháng 9, anh là khách mời và biểu diễn "Thinkin Bout You" và "Pyramids" trên Saturday Night Live,
được đệm đàn ghita bởi John Mayer.Thân cây thanh mảnh, cao tới 3 m, ánh xám, có lông tơ dọc
theo 2 hàng. Cuống lá 4-15 mm; phiến lá hình trứng tới hình trứng-mũi mác, kích thước 1,5-5 × 0,6-4
cm, mỏng bóng như da, không lông, đáy thuôn tròn, hiếm khi gần giống hình tim, đỉnh có mấu nhọn;
4 hoặc 5 đôi gân bên, gần trục phẳng, xa trục hơi nâng lên. Các xim hoa hơi ngắn hơn lá, 8-10 hoa;
cuống hoa 2-5(-17) mm, có lông măng. Lá đài hình trứng, không cân đối, hơi khô xác, tới 0,8 mm, có
lông rung, đỉnh thuôn tròn. Tràng hoa lục tới vàng, 3-4 mm; các thùy thẳng đứng, hình trứng-thuôn
dài, khoảng 1,5 × 1 mm. Các thùy vành bao hoa hình lưỡi liềm. Các phần phụ của bao phấn nhọn, cụp
vào trong. Bầu nhụy không lông. Quả đại thẳng-mũi mác, khảng 8 cm × 5 mm, không lông. Hạt hình
trứng-thuôn dài, khoảng 6 × 2 mm, có mép; mào lông đầu hạt khoảng 3,5 cm. Ra hoa tháng 3-9, kết
quả tháng 5-12.Cây thân thảo nhỏ, yếu. Thân lá cao tới 0,5 m, đáy mập ~7 mm, đỉnh ~2 mm, hơi có
lông lụa, màu xanh vàng ô liu sẫm. Thân rễ mỏng, gồm các nhánh hình trứng ngược, ruột màu vàng
nhạt. Lá hình mác, đỉnh gần nhọn thon tới rất nhọn, đáy trên cuống lá ngắn (4-5 mm), mép men
xuống, lá to 19-23 × 5,7-5 cm, lá nhỏ 11,5 × 3-4,2 cm, mặt dưới gần trụ rải rác lông áp ép; lưỡi bẹ
thuôn tròn-hình trứng, thường rộng đầu, dài 5-10 mm, màu trắng. Cán hoa thanh mảnh, 15 × 0,5 cm;
vảy che phủ 4, dài 3-4 cm, màu đỏ ánh nâu, phía dưới màu ánh trắng. Vảy tổng thể nhỏ, dài 2,5 cm,
mọc ở hướng đối diện với lá bắc của cành hoa bông thóc, màu xanh vàng ô liu. Cán hoa và vảy có
lông tơ. Cành hoa bông thóc hình elip thon nhỏ dần hoặc hình thoi ngắn, đáy và đỉnh thon nhỏ dần,
nhọn, 3,5-6 × 1,7-2 cm, hầu như không phồng. Lá bắc thuôn tròn-hình trứng ngược, mép hẹp (0,25-
0,5 mm) màu trắng, khi khô nổi rõ, cong vào trong nhiều hay ít, mấu nhọn nhỏ gần như không thấy,
có lông tơ, phần còn lại ngoại trừ đáy nhẵn nhụi, nhẹ, mỏng, có sọc, khi tươi màu xanh lục, các lá bắc
ở phía trên màu tía nhạt ở phần gần đỉnh, các lá bắc ngoài tạo thành khoang rỗng, có lông, phồng
mạnh. Lá bắc con rộng, 2,5 × 1,5 cm, nhẵn nhụi. Hoa lớn, màu trắng kem, cánh môi giữa màu vành
chanh nhạt, dài 4,5-5,4 cm (ống tràng 3,4 cm). Thùy tràng lưng hình trứng, nhọn, 2,4 × 0,9 cm; các
thùy tràng bên hẹp, nhọn, 2 × 0,3 cm, hợp sinh với thùy tràng giữa. Cánh môi hình gần tròn, đáy có
vuốt, thon nhỏ dần, đỉnh ở hoa trưởng thành có khe chẻ sâu tới giữa, 1,6 × 1,4 mm, các thùy hình
nửa trứng, hơi rẽ ra. Nhị lép bên hình elip hoặc hình phỏng thoi nhọn, có vuốt, rời với cánh môi, 1,2
× 0,6 cm.Y tế ở Hoa Kỳ trong bối cảnh toàn cầuNăm 2019, tỷ suất tử vong ở trẻ em dưới 5 tuổi là 6,5
trẻ em trên 1000 trẻ còn sống khi sinh, xếp Hoa Kỳ vào vị trí thứ 33 trong số 37 quốc gia thuộc OECD.
Trong năm 2010-2012, hơn 57.000 trẻ sơ sinh (52%) và trẻ em dưới 18 tuổi tử vong ở Hoa Kỳ.Mặc dù
không cao bằng năm 2015 (14) như năm 2013 (18,5), tử vong mẹ liên quan đến sinh đẻ đã tăng gần
đây; năm 1987, tỷ lệ tử vong là 7,2 trên 100.000. Tính đến năm 2015, tỷ lệ tử vong ở Mỹ cao gấp đôi
tỷ lệ tử vong mẹ ở Bỉ hoặc Canada, và cao hơn gấp ba lần tỷ lệ này ở Phần Lan cũng như một số quốc
gia Tây Âu khác.Ca nhiễm và tử vong do nCoV ở Anh lần lượt là 233.151 và 33.614 sau khi báo cáo
thêm lần lượt 3.446 và 428 ca.Italy ghi nhận thêm 992 ca nhiễm và 262 ca tử vong, nâng tổng số lên
lần lượt 223.096 và 31.368.Pháp xác nhận 178.870 ca nhiễm và 27.425 ca tử vong, tăng lần lượt 810
và 351 ca so với một ngày trước đó. Đức ghi nhận thêm 877 ca nhiễm, nâng tổng số lên 174.975,
trong đó 7.928 người chết, tăng 67 ca. (vnexpress)Quy định cách ly được ban hành do nguy cơ
nhiễm Coronavirus cho những người trở về và tới Đức từ các nước EU và Schengen sẽ được bãi bỏ.
(FAZ)Thiết giáp: 3 quân đoàn, 44 lữ đoàn và 7 tiểu đoàn xe tăng, 1 lữ đoàn và 1 trung đoàn pháo tự
hành, 2 lữ đoàn và 7 trung đoàn cơ giới.Không quân: 11 sư đoàn, 15 trung đoàn và 1 Cụm không
quân chiến lượcCông binh: 4 lữ đoàn và 58 tiểu đoànTháng 1 năm 1943:Biên chế cơ bản: Các tập
đoàn quân bộ binh 5, 10, 16, 20, 29, 30, 31, 33, 49, 50, 61; Tập đoàn quân không quân 1.Bộ binh: 3
quân đoàn, 65 sư đoàn và 7 lữ đoàn bộ binh, 2 sư đoàn bộ binh cơ giới, 14 lữ đoàn trượt
tuyết.nhỏ|250px|DJIA (từ 19 tháng 7 năm 1987 đến 19 tháng 1 năm 1988)Thứ Hai Đen là tên mà
giới tài chính đặt cho ngày thứ Hai, 19 tháng 10 năm 1987. Hôm đó, chỉ số bình quân công nghiệp
Dow Jones đã tụt tới 508 điểm xuống còn 1739 (22,6%). Tình trạng tương tự xảy ra đồng thời khắp
thế giới. Vào cuối tháng 10, các thị trường chứng khoán của Hồng Kông đã tụt 45,8%, Úc 41,8%, Tây
Ban Nha 31%, Anh Quốc 26,4%, Hoa Kỳ 22,68% và Canada 22,5%.Sụt giá chứng khoán trong ngày
Thứ Hai Đen là sự sụt giá chứng khoán trong ngày tính theo điểm phần trăm lớn nhất đến lúc""")

    # print(llama_content.generator())

    a = {
  "relationships": [
    {
      "source": {
        "name": "Ia Khai",
        "type_of_action": "Thành lập",
        "district": "Ia Grai"
      },
      "target": {
        "name": "Ia Krái",
        "part_of": "một phần xã"
      },
      "type_source": "Commune",
      "type_target": "Commune",
      "relation": "trên_cơ_sở"
    },
    {
      "source": {
        "name": "Ia Khai",
        "area_ha": 16518.5,
        "population": 2475
      },
      "target": {
        "name": "Ia Grai"
      },
      "type_source": "Commune",
      "type_target": "District",
      "relation": "thuộc"
    },
    {
      "source": {
        "name": "Ia Nhin",
        "type_of_action": "Thành lập",
        "district": "Chư Păh"
      },
      "target": {
        "name": "Ia Ka",
        "part_of": "một phần xã"
      },
      "type_source": "Commune",
      "type_target": "Commune",
      "relation": "trên_cơ_sở"
    },
    {
      "source": {
        "name": "Ia Nhin",
        "area_ha": 3205,
        "population": 3758
      },
      "target": {
        "name": "Chư Păh"
      },
      "type_source": "Commune",
      "type_target": "District",
      "relation": "thuộc"
    },
    {
      "source": {
        "name": "Chư Păh"
      },
      "target": {
        "name": "Ia Mơ Nông",
        "action": "Điều chỉnh địa giới hành chính"
      },
      "type_source": "District",
      "type_target": "Commune",
      "relation": "điều_chỉnh_địa_giới_hành_chính"
    },
    {
      "source": {
        "name": "Chư Păh"
      },
      "target": {
        "name": "Ia Phí",
        "action": "Điều chỉnh địa giới hành chính"
      },
      "type_source": "District",
      "type_target": "Commune",
      "relation": "điều_chỉnh_địa_giới_hành_chính"
    },
    {
      "source": {
        "name": "Ia Ly",
        "type_of_action": "Thành lập",
        "district": "Chư Păh"
      },
      "target": {
        "name": "Ia Mơ Nông",
        "part_of": "một phần xã"
      },
      "type_source": "Commune",
      "type_target": "Commune",
      "relation": "trên_cơ_sở"
    },
    {
      "source": {
        "name": "Ia Ly",
        "area_ha": 4844,
        "population": 4570
      },
      "target": {
        "name": "Chư Păh"
      },
      "type_source": "Commune",
      "type_target": "District",
      "relation": "thuộc"
    },
    {
      "source": {
        "name": "Ia Mơ Nông",
        "area_ha": 16951,
        "population": 4071
      },
      "target": {
        "name": "Chư Păh"
      },
      "type_source": "Commune",
      "type_target": "District",
      "relation": "thuộc"
    },
    {
      "source": {
        "name": "Ia Phí",
        "area_ha": 6995,
        "population": 5172
      },
      "target": {
        "name": "Chư Păh"
      },
      "type_source": "Commune",
      "type_target": "District",
      "relation": "thuộc"
    },
    {
      "source": {
        "name": "UDF 1.00",
        "release_date": "24 tháng 10 năm 1995",
        "description": "Bản phát hành gốc"
      },
      "target": {
        "name": "UDF"
      },
      "type_source": "SoftwareVersion",
      "type_target": "SoftwareStandard",
      "relation": "là_phiên_bản_của"
    },
    {
      "source": {
        "name": "UDF 1.01",
        "release_date": "3 tháng 11 năm 1995",
        "changes": "Thêm Phụ lục DVD và thực hiện một vài thay đổi nhỏ"
      },
      "target": {
        "name": "UDF"
      },
      "type_source": "SoftwareVersion",
      "type_target": "SoftwareStandard",
      "relation": "là_phiên_bản_của"
    },
    {
      "source": {
        "name": "UDF 1.02",
        "release_date": "30 tháng 8 năm 1996",
        "usage": "Định dạng này được đĩa DVD-Video sử dụng"
      },
      "target": {
        "name": "UDF"
      },
      "type_source": "SoftwareVersion",
      "type_target": "SoftwareStandard",
      "relation": "là_phiên_bản_của"
    },
    {
      "source": {
        "name": "UDF 1.02"
      },
      "target": {
        "name": "DVD-Video"
      },
      "type_source": "SoftwareVersion",
      "type_target": "DigitalMediaFormat",
      "relation": "được_sử_dụng_bởi"
    },
    {
      "source": {
        "name": "UDF 1.50",
        "release_date": "4 tháng 2 năm 1997",
        "features": "Đã thêm hỗ trợ ghi lại (ảo) trên phương tiện CDR/DVD-R bằng cách giới thiệu cấu trúc VAT."
      },
      "target": {
        "name": "UDF"
      },
      "type_source": "SoftwareVersion",
      "type_target": "SoftwareStandard",
      "relation": "là_phiên_bản_của"
    },
    {
      "source": {
        "name": "UDF 1.50"
      },
      "target": {
        "name": "CDR"
      },
      "type_source": "SoftwareVersion",
      "type_target": "MediaFormat",
      "relation": "hỗ_trợ"
    },
    {
      "source": {
        "name": "UDF 1.50"
      },
      "target": {
        "name": "DVD-R"
      },
      "type_source": "SoftwareVersion",
      "type_target": "MediaFormat",
      "relation": "hỗ_trợ"
    },
    {
      "source": {
        "name": "UDF 1.50"
      },
      "target": {
        "name": "CD-RW"
      },
      "type_source": "SoftwareVersion",
      "type_target": "MediaFormat",
      "relation": "hỗ_trợ"
    },
    {
      "source": {
        "name": "UDF 1.50"
      },
      "target": {
        "name": "DVD-RW"
      },
      "type_source": "SoftwareVersion",
      "type_target": "MediaFormat",
      "relation": "hỗ_trợ"
    },
    {
      "source": {
        "name": "UDF 1.50"
      },
      "target": {
        "name": "DVD+RW"
      },
      "type_source": "SoftwareVersion",
      "type_target": "MediaFormat",
      "relation": "hỗ_trợ"
    },
    {
      "source": {
        "name": "IELTS",
        "score_range": "1 – 9"
      },
      "target": {
        "name": "kỹ năng thi"
      },
      "type_source": "Exam",
      "type_target": "Concept",
      "relation": "thể_hiện_điểm_của"
    },
    {
      "source": {
        "name": "Điểm tổng",
        "calculation_method": "trung bình cộng của 4 kỹ năng"
      },
      "target": {
        "name": "IELTS"
      },
      "type_source": "Score",
      "type_target": "Exam",
      "relation": "là_của"
    },
    {
      "source": {
        "name": "Thí sinh",
        "example_scores": "6.5 (Nghe), 6.5 (Đọc), 5.0 (Viết), 7.0 (Nói)"
      },
      "target": {
        "name": "6.5",
        "context": "Điểm trung bình của thí sinh này"
      },
      "type_source": "Person",
      "type_target": "Score",
      "relation": "có_điểm_trung_bình"
    },
    {
      "source": {
        "name": "Lipa",
        "species": "M. elephantis",
        "gc_content": "67,8%",
        "genome_size": "5,19 Mb"
      },
      "target": {
        "name": "Mycobacterium elephantis"
      },
      "type_source": "BacteriumStrain",
      "type_target": "Bacterium",
      "relation": "là_chủng_của"
    },
    {
      "source": {
        "name": "Lipa"
      },
      "target": {
        "name": "pseudogenes",
        "count": 250
      },
      "type_source": "BacteriumStrain",
      "type_target": "GeneFeature",
      "relation": "chứa"
    },
    {
      "source": {
        "name": "Chuỗi gen 484 t",
        "identifier": "DSM 44368",
        "sequence_type": "16S rRNA"
      },
      "target": {
        "name": "mycobacterium phát triển nhanh",
        "similarity": "96,7+ 0,5%"
      },
      "type_source": "GeneticSequence",
      "type_target": "BacteriumGroup",
      "relation": "có_độ_tương_đồng_với"
    },
    {
      "source": {
        "name": "Chuỗi gen 484 t"
      },
      "target": {
        "name": "mycobacteria phát triển chậm",
        "similarity": "96,2+ 0,4%"
      },
      "type_source": "GeneticSequence",
      "type_target": "BacteriumGroup",
      "relation": "có_độ_tương_đồng_với"
    },
    {
      "source": {
        "name": "Chuỗi gen 484 t"
      },
      "target": {
        "name": "M. confluentis",
        "similarity": "97,8%"
      },
      "type_source": "GeneticSequence",
      "type_target": "Bacterium",
      "relation": "có_tương_đồng_nhất_với"
    },
    {
      "source": {
        "name": "Chuỗi gen 484 t"
      },
      "target": {
        "name": "M. phlei",
        "similarity": "97,7%"
      },
      "type_source": "GeneticSequence",
      "type_target": "Bacterium",
      "relation": "có_tương_đồng_nhất_với"
    },
    {
      "source": {
        "name": "Drupal 6",
        "release_date": "13/02/2008"
      },
      "target": {
        "name": "Drupal"
      },
      "type_source": "SoftwareVersion",
      "type_target": "CMS",
      "relation": "là_phiên_bản_của"
    },
    {
      "source": {
        "name": "Buytaert",
        "action": "thông báo đóng-băng-mã"
      },
      "target": {
        "name": "Drupal 7",
        "preparation": "chuẩn bị"
      },
      "type_source": "Person",
      "type_target": "SoftwareVersion",
      "relation": "thông_báo_về"
    },
    {
      "source": {
        "name": "Drupal 7",
        "release_date": "5/1/2011",
        "maintenance_end_date_planned": "tháng 11 năm 2021"
      },
      "target": {
        "name": "Drupal"
      },
      "type_source": "SoftwareVersion",
      "type_target": "CMS",
      "relation": "là_phiên_bản_của"
    },
    {
      "source": {
        "name": "Drupal 7",
        "actual_maintenance_end": "tháng 11 năm 2022",
        "reason_for_delay": "ảnh hưởng của dịch COVID-19"
      },
      "target": {
        "name": "COVID-19"
      },
      "type_source": "SoftwareVersion",
      "type_target": "Disease",
      "relation": "bị_ảnh_hưởng_bởi"
    },
    {
      "source": {
        "name": "Drupal 5",
        "maintenance_status": "chấm dứt"
      },
      "target": {
        "name": "Drupal"
      },
      "type_source": "SoftwareVersion",
      "type_target": "CMS",
      "relation": "là_phiên_bản_của"
    },
    {
      "source": {
        "name": "Drupal 8",
        "maintenance_end_date": "2 tháng 11 năm 2021"
      },
      "target": {
        "name": "Drupal"
      },
      "type_source": "SoftwareVersion",
      "type_target": "CMS",
      "relation": "là_phiên_bản_của"
    },
    {
      "source": {
        "name": "Ngôi sao",
        "discovery_context": "gần nhất được phát hiện có các ngoại hành tinh quá cảnh",
        "discovery_date": "tháng 10 năm 2017"
      },
      "target": {
        "name": "Hành tinh b",
        "radius_earth_ratio": 1.62,
        "orbital_period_days": 1.209
      },
      "type_source": "Star",
      "type_target": "Exoplanet",
      "relation": "có_hành_tinh_quá_cảnh"
    },
    {
      "source": {
        "name": "Ngôi sao"
      },
      "target": {
        "name": "Hành tinh c",
        "radius_earth_ratio": 1.27,
        "orbital_period_days": 3.648
      },
      "type_source": "Star",
      "type_target": "Exoplanet",
      "relation": "có_hành_tinh_quá_cảnh"
    },
    {
      "source": {
        "name": "Ngôi sao"
      },
      "target": {
        "name": "Hành tinh d",
        "radius_earth_ratio": 2.09,
        "orbital_period_days": 6.201
      },
      "type_source": "Star",
      "type_target": "Exoplanet",
      "relation": "có_hành_tinh_quá_cảnh"
    },
    {
      "source": {
        "name": "Kepler",
        "mission_type": "khảo sát K2"
      },
      "target": {
        "name": "K2"
      },
      "type_source": "Spacecraft",
      "type_target": "SpaceMission",
      "relation": "thực_hiện_nhiệm_vụ"
    },
    {
      "source": {
        "name": "Hành tinh b"
      },
      "target": {
        "name": "Trái Đất"
      },
      "type_source": "Exoplanet",
      "type_target": "Planet",
      "relation": "có_bán_kính_so_với"
    },
    {
      "source": {
        "name": "Hành tinh c"
      },
      "target": {
        "name": "Trái Đất"
      },
      "type_source": "Exoplanet",
      "type_target": "Planet",
      "relation": "có_bán_kính_so_với"
    },
    {
      "source": {
        "name": "Hành tinh d"
      },
      "target": {
        "name": "Trái Đất"
      },
      "type_source": "Exoplanet",
      "type_target": "Planet",
      "relation": "có_bán_kính_so_với"
    },
    {
      "source": {
        "name": "Clive Allen",
        "goals": 12,
        "record_type": "Cầu thủ ghi bàn nhiều nhất trong 1 mùa giải",
        "season": "1986–87"
      },
      "target": {
        "name": "Tottenham Hotspur"
      },
      "type_source": "FootballPlayer",
      "type_target": "FootballClub",
      "relation": "ghi_bàn_cho"
    },
    {
      "source": {
        "name": "Frankie Bunn",
        "goals": 6,
        "record_type": "Cầu thủ ghi bàn nhiều nhất trong 1 trận đấu",
        "match_date": "25 tháng 10 năm 1989"
      },
      "target": {
        "name": "Oldham Athletic"
      },
      "type_source": "FootballPlayer",
      "type_target": "FootballClub",
      "relation": "ghi_bàn_cho"
    },
    {
      "source": {
        "name": "Liverpool",
        "score": 10
      },
      "target": {
        "name": "Fulham",
        "score": 0,
        "match_date": "23 tháng 9 năm 1986",
        "stage": "vòng 2 lượt đi"
      },
      "type_source": "FootballClub",
      "type_target": "FootballClub",
      "relation": "thắng"
    },
    {
      "source": {
        "name": "West Ham United",
        "score": 10
      },
      "target": {
        "name": "Bury",
        "score": 0,
        "match_date": "25 tháng 10 năm 1983",
        "stage": "vòng 2 lượt về"
      },
      "type_source": "FootballClub",
      "type_target": "FootballClub",
      "relation": "thắng"
    },
    {
      "source": {
        "name": "Manchester City",
        "total_score": "10–0",
        "home_score": "9–0",
        "away_score": "1–0"
      },
      "target": {
        "name": "Burton Albion",
        "match_date": "23 tháng 1 năm 2019",
        "stage": "vòng bán kết"
      },
      "type_source": "FootballClub",
      "type_target": "FootballClub",
      "relation": "thắng"
    },
    {
      "source": {
        "name": "Thinkin Bout You",
        "release_date": "17 tháng 4",
        "artist": "Ocean"
      },
      "target": {
        "name": "Album",
        "purpose": "quảng bá"
      },
      "type_source": "Song",
      "type_target": "MusicAlbum",
      "relation": "là_đĩa_đơn_của"
    },
    {
      "source": {
        "name": "Pyramids",
        "release_date": "8 tháng 6",
        "artist": "Ocean"
      },
      "target": {
        "name": "Album",
        "purpose": "quảng bá"
      },
      "type_source": "Song",
      "type_target": "MusicAlbum",
      "relation": "là_đĩa_đơn_của"
    },
    {
      "source": {
        "name": "Sweet Life",
        "release_date": "6 tháng 7",
        "artist": "Ocean"
      },
      "target": {
        "name": "Album",
        "purpose": "quảng bá"
      },
      "type_source": "Song",
      "type_target": "MusicAlbum",
      "relation": "là_đĩa_đơn_của"
    },
    {
      "source": {
        "name": "Lost",
        "release_date": "17 tháng 12",
        "artist": "Ocean"
      },
      "target": {
        "name": "Album",
        "purpose": "quảng bá"
      },
      "type_source": "Song",
      "type_target": "MusicAlbum",
      "relation": "là_đĩa_đơn_của"
    },
    {
      "source": {
        "name": "Super Rich Kids",
        "release_date": "17 tháng 3 năm 2013",
        "artist": "Ocean"
      },
      "target": {
        "name": "Album",
        "purpose": "quảng bá"
      },
      "type_source": "Song",
      "type_target": "MusicAlbum",
      "relation": "là_đĩa_đơn_của"
    },
    {
      "source": {
        "name": "Thinkin Bout You",
        "highest_chart_us": 32,
        "chart_name": "Billboard Hot 100"
      },
      "target": {
        "name": "Hoa Kỳ"
      },
      "type_source": "Song",
      "type_target": "Country",
      "relation": "đạt_thứ_hạng_tại"
    },
    {
      "source": {
        "name": "Thinkin Bout You"
      },
      "target": {
        "name": "Billboard Hot 100"
      },
      "type_source": "Song",
      "type_target": "MusicChart",
      "relation": "đứng_trên_bảng_xếp_hạng"
    },
    {
      "source": {
        "name": "Ocean",
        "role": "nghệ sĩ"
      },
      "target": {
        "name": "Thinkin Bout You"
      },
      "type_source": "Person",
      "type_target": "Song",
      "relation": "biểu_diễn"
    },
    {
      "source": {
        "name": "Ocean",
        "performance_date": "6 tháng 9"
      },
      "target": {
        "name": "MTV Video Music Awards 2012"
      },
      "type_source": "Person",
      "type_target": "AwardShow",
      "relation": "biểu_diễn_tại"
    },
    {
      "source": {
        "name": "Ocean",
        "role": "khách mời",
        "performance_date": "15 tháng 9"
      },
      "target": {
        "name": "Saturday Night Live"
      },
      "type_source": "Person",
      "type_target": "TVShow",
      "relation": "biểu_diễn_trên"
    },
    {
      "source": {
        "name": "John Mayer",
        "role": "đệm đàn ghita"
      },
      "target": {
        "name": "Ocean"
      },
      "type_source": "Person",
      "type_target": "Person",
      "relation": "đệm_đàn_cho"
    },
    {
      "source": {
        "name": "Hoa Kỳ",
        "year": 2019,
        "ranking": "33 trong số 37 quốc gia",
        "mortality_rate": "6,5 trẻ em trên 1000 trẻ còn sống khi sinh"
      },
      "target": {
        "name": "OECD"
      },
      "type_source": "Country",
      "type_target": "Organization",
      "relation": "xếp_hạng_trong"
    },
    {
      "source": {
        "name": "Hoa Kỳ",
        "period": "2010-2012"
      },
      "target": {
        "name": "trẻ sơ sinh và trẻ em dưới 18 tuổi",
        "deaths": 57000,
        "percentage_of_total": "52%"
      },
      "type_source": "Country",
      "type_target": "AgeGroup",
      "relation": "có_số_tử_vong_ở"
    },
    {
      "source": {
        "name": "Hoa Kỳ",
        "year": 1987,
        "maternal_mortality_rate": "7,2 trên 100.000"
      },
      "target": {
        "name": "tử vong mẹ liên quan đến sinh đẻ"
      },
      "type_source": "Country",
      "type_target": "MedicalCondition",
      "relation": "ghi_nhận"
    },
    {
      "source": {
        "name": "Hoa Kỳ",
        "year": 2015,
        "comparison_rate": "cao gấp đôi",
        "type_of_mortality": "tỷ lệ tử vong mẹ"
      },
      "target": {
        "name": "Bỉ"
      },
      "type_source": "Country",
      "type_target": "Country",
      "relation": "có_tỷ_lệ_cao_hơn"
    },
    {
      "source": {
        "name": "Hoa Kỳ",
        "year": 2015,
        "comparison_rate": "cao gấp đôi",
        "type_of_mortality": "tỷ lệ tử vong mẹ"
      },
      "target": {
        "name": "Canada"
      },
      "type_source": "Country",
      "type_target": "Country",
      "relation": "có_tỷ_lệ_cao_hơn"
    },
    {
      "source": {
        "name": "Hoa Kỳ",
        "year": 2015,
        "comparison_rate": "cao hơn gấp ba lần",
        "type_of_mortality": "tỷ lệ tử vong mẹ"
      },
      "target": {
        "name": "Phần Lan"
      },
      "type_source": "Country",
      "type_target": "Country",
      "relation": "có_tỷ_lệ_cao_hơn"
    },
    {
      "source": {
        "name": "Anh",
        "total_cases": 233151,
        "total_deaths": 33614,
        "new_cases": 3446,
        "new_deaths": 428
      },
      "target": {
        "name": "nCoV"
      },
      "type_source": "Country",
      "type_target": "Virus",
      "relation": "có_ca_nhiễm_và_tử_vong_do"
    },
    {
      "source": {
        "name": "Italy",
        "total_cases": 223096,
        "total_deaths": 31368,
        "new_cases": 992,
        "new_deaths": 262
      },
      "target": {
        "name": "nCoV"
      },
      "type_source": "Country",
      "type_target": "Virus",
      "relation": "có_ca_nhiễm_và_tử_vong_do"
    },
    {
      "source": {
        "name": "Pháp",
        "total_cases": 178870,
        "total_deaths": 27425,
        "new_cases": 810,
        "new_deaths": 351
      },
      "type_source": "Country",
      "target": {
        "name": "nCoV"
      },
      "type_target": "Virus",
      "relation": "có_ca_nhiễm_và_tử_vong_do"
    },
    {
      "source": {
        "name": "Đức",
        "total_cases": 174975,
        "total_deaths": 7928,
        "new_cases": 877,
        "new_deaths": 67
      },
      "target": {
        "name": "nCoV"
      },
      "type_source": "Country",
      "type_target": "Virus",
      "relation": "có_ca_nhiễm_và_tử_vong_do"
    },
    {
      "source": {
        "name": "Đức",
        "action": "bãi bỏ"
      },
      "target": {
        "name": "Quy định cách ly",
        "reason": "nguy cơ nhiễm Coronavirus"
      },
      "type_source": "Country",
      "type_target": "Regulation",
      "relation": "bãi_bỏ"
    },
    {
      "source": {
        "name": "Quy định cách ly"
      },
      "target": {
        "name": "EU"
      },
      "type_source": "Regulation",
      "type_target": "PoliticalUnion",
      "relation": "áp_dụng_với"
    },
    {
      "source": {
        "name": "Quy định cách ly"
      },
      "target": {
        "name": "Schengen"
      },
      "type_source": "Regulation",
      "type_target": "Agreement",
      "relation": "áp_dụng_với"
    },
    {
      "source": {
        "name": "Tháng 1 năm 1943",
        "context": "Biên chế cơ bản"
      },
      "target": {
        "name": "Thiết giáp",
        "corps": 3,
        "tank_brigades": 44,
        "tank_battalions": 7
      },
      "type_source": "Date",
      "type_target": "MilitaryBranch",
      "relation": "có_biên_chế"
    },
    {
      "source": {
        "name": "Tháng 1 năm 1943",
        "context": "Biên chế cơ bản"
      },
      "target": {
        "name": "Không quân",
        "divisions": 11,
        "regiments": 15,
        "strategic_air_groups": 1
      },
      "type_source": "Date",
      "type_target": "MilitaryBranch",
      "relation": "có_biên_chế"
    },
    {
      "source": {
        "name": "Tháng 1 năm 1943",
        "context": "Biên chế cơ bản"
      },
      "target": {
        "name": "Công binh",
        "brigades": 4,
        "battalions": 58
      },
      "type_source": "Date",
      "type_target": "MilitaryBranch",
      "relation": "có_biên_chế"
    },
    {
      "source": {
        "name": "Tháng 1 năm 1943",
        "context": "Biên chế cơ bản"
      },
      "target": {
        "name": "Bộ binh",
        "corps": 3,
        "divisions": 65,
        "infantry_brigades": 7
      },
      "type_source": "Date",
      "type_target": "MilitaryBranch",
      "relation": "có_biên_chế"
    },
    {
      "source": {
        "name": "Thứ Hai Đen",
        "event_date": "19 tháng 10 năm 1987"
      },
      "target": {
        "name": "Giới tài chính"
      },
      "type_source": "HistoricalEvent",
      "type_target": "Group",
      "relation": "được_đặt_tên_bởi"
    },
    {
      "source": {
        "name": "Dow Jones",
        "drop_points": 508,
        "closing_value": 1739,
        "percentage_drop": "22,6%"
      },
      "target": {
        "name": "Thứ Hai Đen"
      },
      "type_source": "StockIndex",
      "type_target": "HistoricalEvent",
      "relation": "tụt_giá_vào"
    },
    {
      "source": {
        "name": "Hồng Kông",
        "stock_market_drop": "45,8%"
      },
      "target": {
        "name": "Thứ Hai Đen"
      },
      "type_source": "Country",
      "type_target": "HistoricalEvent",
      "relation": "có_thị_trường_chứng_khoán_tụt_giá_vào"
    },
    {
      "source": {
        "name": "Úc",
        "stock_market_drop": "41,8%"
      },
      "target": {
        "name": "Thứ Hai Đen"
      },
      "type_source": "Country",
      "type_target": "HistoricalEvent",
      "relation": "có_thị_trường_chứng_khoán_tụt_giá_vào"
    },
    {
      "source": {
        "name": "Tây Ban Nha",
        "stock_market_drop": "31%"
      },
      "target": {
        "name": "Thứ Hai Đen"
      },
      "type_source": "Country",
      "type_target": "HistoricalEvent",
      "relation": "có_thị_trường_chứng_khoán_tụt_giá_vào"
    },
    {
      "source": {
        "name": "Anh Quốc",
        "stock_market_drop": "26,4%"
      },
      "target": {
        "name": "Thứ Hai Đen"
      },
      "type_source": "Country",
      "type_target": "HistoricalEvent",
      "relation": "có_thị_trường_chứng_khoán_tụt_giá_vào"
    },
    {
      "source": {
        "name": "Hoa Kỳ",
        "stock_market_drop": "22,68%"
      },
      "target": {
        "name": "Thứ Hai Đen"
      },
      "type_source": "Country",
      "type_target": "HistoricalEvent",
      "relation": "có_thị_trường_chứng_khoán_tụt_giá_vào"
    },
    {
      "source": {
        "name": "Canada",
        "stock_market_drop": "22,5%"
      },
      "target": {
        "name": "Thứ Hai Đen"
      },
      "type_source": "Country",
      "type_target": "HistoricalEvent",
      "relation": "có_thị_trường_chứng_khoán_tụt_giá_vào"
    }
  ]
}
    b = {
  "relationships": [
    {
      "source": {
        "name": "Ia Khai",
        "diện tích": "16.518,5 ha",
        "nhân khẩu": "2.475"
      },
      "target": {
        "name": "Ia Grai"
      },
      "type_source": "Location",
      "type_target": "Location",
      "relation": "thuộc_về"
    },
    {
      "source": {
        "name": "Ia Nhin",
        "diện tích": "3.205 ha",
        "nhân khẩu": "3.758"
      },
      "target": {
        "name": "Chư Păh"
      },
      "type_source": "Location",
      "type_target": "Location",
      "relation": "thuộc_về"
    },
    {
      "source": {
        "name": "Ia Ly",
        "diện tích": "4.844 ha",
        "nhân khẩu": "4.570"
      },
      "target": {
        "name": "Chư Păh"
      },
      "type_source": "Location",
      "type_target": "Location",
      "relation": "thuộc_về"
    },
    {
      "source": {
        "name": "Ia Mơ Nông",
        "diện tích": "16.951 ha",
        "nhân khẩu": "4.071"
      },
      "target": {
        "name": "Chư Păh"
      },
      "type_source": "Location",
      "type_target": "Location",
      "relation": "thuộc_về"
    },
    {
      "source": {
        "name": "Ia Phí",
        "diện tích": "6.995 ha",
        "nhân khẩu": "5.172"
      },
      "target": {
        "name": "Chư Păh"
      },
      "type_source": "Location",
      "type_target": "Location",
      "relation": "thuộc_về"
    },
    {
      "source": {
        "name": "UDF",
        "phiên_bản": "1.00"
      },
      "target": {
        "name": "24 tháng 10 năm 1995"
      },
      "type_source": "Software",
      "type_target": "Date",
      "relation": "phát_hành_vào"
    },
    {
      "source": {
        "name": "UDF",
        "phiên_bản": "1.01"
      },
      "target": {
        "name": "3 tháng 11 năm 1995"
      },
      "type_source": "Software",
      "type_target": "Date",
      "relation": "phát_hành_vào"
    },
    {
      "source": {
        "name": "UDF",
        "phiên_bản": "1.02"
      },
      "target": {
        "name": "30 tháng 8 năm 1996"
      },
      "type_source": "Software",
      "type_target": "Date",
      "relation": "phát_hành_vào"
    },
    {
      "source": {
        "name": "UDF",
        "phiên_bản": "1.50"
      },
      "target": {
        "name": "4 tháng 2 năm 1997"
      },
      "type_source": "Software",
      "type_target": "Date",
      "relation": "phát_hành_vào"
    },
    {
      "source": {
        "name": "IELTS"
      },
      "target": {
        "name": "9"
      },
      "type_source": "Organization",
      "type_target": "Score",
      "relation": "có_điểm_tối_đa"
    },
    {
      "source": {
        "name": "Mycobacterium elephantis"
      },
      "target": {
        "name": "Lipa"
      },
      "type_source": "Bacteria",
      "type_target": "Strain",
      "relation": "có_chủng"
    },
    {
      "source": {
        "name": "Mycobacterium elephantis",
        "chủng": "Lipa"
      },
      "target": {
        "name": "67,8%"
      },
      "type_source": "Bacteria",
      "type_target": "GC_content",
      "relation": "có_hàm_lượng_GC"
    },
    {
      "source": {
        "name": "Mycobacterium elephantis",
        "chủng": "Lipa"
      },
      "target": {
        "name": "5,19 Mb"
      },
      "type_source": "Bacteria",
      "type_target": "Genome_size",
      "relation": "có_kích_thước_bộ_gen"
    },
    {
      "source": {
        "name": "Drupal"
      },
      "target": {
        "name": "6"
      },
      "type_source": "Software",
      "type_target": "Version",
      "relation": "có_phiên_bản"
    },
    {
      "source": {
        "name": "Drupal",
        "phiên_bản": "6"
      },
      "target": {
        "name": "13/02/2008"
      },
      "type_source": "Software",
      "type_target": "Date",
      "relation": "phát_hành_vào"
    },
    {
      "source": {
        "name": "Drupal",
        "phiên_bản": "7"
      },
      "target": {
        "name": "5/1/2011"
      },
      "type_source": "Software",
      "type_target": "Date",
      "relation": "phát_hành_vào"
    },
    {
      "source": {
        "name": "K2"
      },
      "target": {
        "name": "3 hành tinh quá cảnh"
      },
      "type_source": "Space_Mission",
      "type_target": "Number_of_planets",
      "relation": "khám_phá"
    },
    {
      "source": {
        "name": "K2",
        "hành_tinh": "3 hành tinh quá cảnh"
      },
      "target": {
        "name": "ngôi sao gần nhất"
      },
      "type_source": "Space_Mission",
      "type_target": "Star",
      "relation": "khám_phá"
    },
    {
      "source": {
        "name": "Cúp Liên đoàn bóng đá Anh"
      },
      "target": {
        "name": "12"
      },
      "type_source": "Football_Tournament",
      "type_target": "Number_of_goals",
      "relation": "có_số_bàn_thắng_nhiều_nhất"
    },
    {
      "source": {
        "name": "Cúp Liên đoàn bóng đá Anh"
      },
      "target": {
        "name": "6"
      },
      "type_source": "Football_Tournament",
      "type_target": "Number_of_goals",
      "relation": "có_số_bàn_thắng_nhiều_nhất_trong_1_trận_đấu"
    },
    {
      "source": {
        "name": "Cúp Liên đoàn bóng đá Anh"
      },
      "target": {
        "name": "10-0"
      },
      "type_source": "Football_Tournament",
      "type_target": "Score",
      "relation": "có_chênh_lệch_bàn_thắng_lớn_nhất"
    },
    {
      "source": {
        "name": "Channel Orange"
      },
      "target": {
        "name": "Thinkin Bout You"
      },
      "type_source": "Music_Album",
      "type_target": "Song",
      "relation": "có_đĩa_đơn"
    },
    {
      "source": {
        "name": "Channel Orange"
      },
      "target": {
        "name": "Pyramids"
      },
      "type_source": "Music_Album",
      "type_target": "Song",
      "relation": "có_đĩa_đơn"
    },
    {
      "source": {
        "name": "Channel Orange"
      },
      "target": {
        "name": "Sweet Life"
      },
      "type_source": "Music_Album",
      "type_target": "Song",
      "relation": "có_đĩa_đơn"
    },
    {
      "source": {
        "name": "Channel Orange"
      },
      "target": {
        "name": "Lost"
      },
      "type_source": "Music_Album",
      "type_target": "Song",
      "relation": "có_đĩa_đơn"
    },
    {
      "source": {
        "name": "Channel Orange"
      },
      "target": {
        "name": "Super Rich Kids"
      },
      "type_source": "Music_Album",
      "type_target": "Song",
      "relation": "có_đĩa_đơn"
    },
    {
      "source": {
        "name": "Hoa Kỳ"
      },
      "target": {
        "name": "6,5 trẻ em trên 1000 trẻ còn sống khi sinh"
      },
      "type_source": "Country",
      "type_target": "Mortality_rate",
      "relation": "có_tỷ_suất_tử_vong"
    },
    {
      "source": {
        "name": "Hoa Kỳ"
      },
      "target": {
        "name": "57.000 trẻ sơ sinh và trẻ em dưới 18 tuổi tử vong"
      },
      "type_source": "Country",
      "type_target": "Number_of_deaths",
      "relation": "có_số_trẻ_em_tử_vong"
    },
    {
      "source": {
        "name": "Anh"
      },
      "target": {
        "name": "233.151 ca nhiễm và 33.614 ca tử vong"
      },
      "type_source": "Country",
      "type_target": "Number_of_cases",
      "relation": "có_số_ca_nhiễm_và_tử_vong"
    },
    {
      "source": {
        "name": "Italy"
      },
      "target": {
        "name": "223.096 ca nhiễm và 31.368 ca tử vong"
      },
      "type_source": "Country",
      "type_target": "Number_of_cases",
      "relation": "có_số_ca_nhiễm_và_tử_vong"
    },
    {
      "source": {
        "name": "Pháp"
      },
      "target": {
        "name": "178.870 ca nhiễm và 27.425 ca tử vong"
      },
      "type_source": "Country",
      "type_target": "Number_of_cases",
      "relation": "có_số_ca_nhiễm_và_tử_vong"
    },
    {
      "source": {
        "name": "Đức"
      },
      "target": {
        "name": "174.975 ca nhiễm và 7.928 ca tử vong"
      },
      "type_source": "Country",
      "type_target": "Number_of_cases",
      "relation": "có_số_ca_nhiễm_và_tử_vong"
    },
    {
      "source": {
        "name": "Đức"
      },
      "target": {
        "name": "3 quân đoàn, 44 lữ đoàn và 7 tiểu đoàn xe tăng"
      },
      "type_source": "Country",
      "type_target": "Military_unit",
      "relation": "có_quân_đội"
    },
    {
      "source": {
        "name": "Đức"
      },
      "target": {
        "name": "11 sư đoàn, 15 trung đoàn và 1 Cụm không quân chiến lược"
      },
      "type_source": "Country",
      "type_target": "Military_unit",
      "relation": "có_quân_đội"
    },
    {
      "source": {
        "name": "Đức"
      },
      "target": {
        "name": "4 lữ đoàn và 58 tiểu đoàn công binh"
      },
      "type_source": "Country",
      "type_target": "Military_unit",
      "relation": "có_quân_đội"
    },
    {
      "source": {
        "name": "Thứ Hai Đen"
      },
      "target": {
        "name": "19 tháng 10 năm 1987"
      },
      "type_source": "Event",
      "type_target": "Date",
      "relation": "xảy_ra_vào"
    },
    {
      "source": {
        "name": "Thứ Hai Đen"
      },
      "target": {
        "name": "508 điểm"
      },
      "type_source": "Event",
      "type_target": "Stock_market_index",
      "relation": "có_sự_sụt_giảm"
    }
  ]
}

    print(len(a["relationships"]))
    print(len(b["relationships"]))

    # pdf = PDF(folder_pdf)

    # đọc tất cả nội dung trong thư mục chứa file pdf
    # sentences = pdf.read_chunks()
    # titles = []
    # llama_title.set_prompt(prompt.create_title())
    # for s in sentences:
    #     llama_title.set_text(s)
    #     title = llama_title.generator().lower()
    #     print(title)
    #     titles.append(pre_processing.string_to_json(title))
    # print(titles)

    # tạo ra entities và relationship
    # entities_relationship = []
    # llama_content.set_prompt(prompt.extract_entities_relationship_from_text())
    # for s in sentences:
    #     llama_content.set_text(s)
    #     response = llama_content.generator().lower()
    #     entity_relation = pre_processing.string_to_json(response)
    #     entities_relationship.append(entity_relation)
    # print(entities_relationship)

    # b1: nối general với uuid người dùng(document)
    # titles = [{'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'vương tế albert, katica illényi, timelapse of the future, thomas jefferson và sega genesis'}, {'title': 'tổng hợp các chủ đề về lịch sử, công nghệ, thể thao và âm nhạc'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, nghệ thuật, khoa học và thể thao'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về phim, nghệ thuật, thể thao, hóa học và công nghệ'}, {'title': 'tổng hợp các chủ đề về khoa học, nghệ thuật, lịch sử và chính trị'}, {'title': 'kim jong-un, william shakespeare và sư tử'}, {'title': 'tổng hợp các chủ đề về khoa học, quân sự, công ty, thời trang, địa lý, chính trị và văn hóa'}, {'title': 'tóm tắt các chủ đề về phim, máy bay tàng hình, tổng thống harry s. truman và manga bleach'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tóm tắt về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về địa lý, lịch sử, khoa học và ẩm thực'}, {'title': 'tổng hợp các chủ đề về văn hóa, khoa học, âm nhạc và tôn giáo'}, {'title': 'tổng hợp các chủ đề về khoa học, văn hóa, lịch sử và giải trí'}, {'title': 'tổng quan về các nhân vật và chủ đề nổi bật'}, {'title': 'tổng hợp các chủ đề về khoa học, lịch sử, công nghệ và văn hóa'}, {'title': 'dương thu hương, stephen hawking và văn hóa nga'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề văn hóa, địa lý và âm nhạc'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'f/a-18 hornet'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề lịch sử, khoa học, văn hóa và nhân vật'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về địa lý, khoa học, lịch sử và nghệ thuật'}, {'title': 'tóm tắt về các nhân vật và sự kiện nổi bật'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học, nghệ thuật và văn hóa'}, {'title': 'tổng hợp các chủ đề về phim ảnh, khảo cổ học, công ty ô tô, ẩm thực, chính trị, lý thuyết kinh tế và giải thưởng'}, {'title': 'giải mercury'}, {'title': 'tổng hợp kiến thức về các chủ đề khác nhau'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'benjamin franklin'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử, địa lý và khoa học'}, {'title': 'tổng hợp các thông tin về nhiều chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về nghệ thuật, lịch sử, khoa học và văn hóa'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'công thức 1 và các chủ đề khác'}, {'title': 'lịch sử và phát triển của úc, nghệ thuật, điện ảnh, chiến tranh thế giới thứ nhất, y học và thể thao'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các tổ chức, thành phố và nhân vật quan trọng'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về narendra modi, phương tiện truyền thông kỹ thuật số, argentina, ẩm thực châu âu, panipuri, primož roglič, hội họa và tu chính án thứ 19'}, {'title': 'tóm tắt các chủ đề khác nhau'}, {'title': 'tổng hợp các thông tin về các chủ đề khác nhau'}, {'title': 'tóm tắt các chủ đề'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về khoa học, lịch sử và thể thao'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề'}, {'title': 'nội dung tổng hợp về các chủ đề khác nhau'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'dune: hành tinh cát'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'nội dung tổng hợp về nhiều chủ đề'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về văn hóa, thể thao, nghệ thuật và khoa học'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, thể thao, nghệ thuật và khoa học'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa, thể thao và giải trí'}, {'title': 'tổng hợp các thông tin về nhiều chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp thông tin về mumbai, sugar ray robinson, virgin hotels las vegas, toyota và nba'}, {'title': 'tổng hợp các chủ đề về thể thao, khoa học, công nghệ và chính trị'}, {'title': 'tổng hợp kiến thức về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về khoa học, lịch sử, văn hóa và tôn giáo'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khoa học, lịch sử và công nghệ'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa, thể thao và ẩm thực'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử và khoa học'}, {'title': 'tổng hợp các chủ đề về lịch sử, âm nhạc, khoa học và văn hóa'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học và văn hóa'}, {'title': 'tổng quan về các chủ đề khoa học, văn học và động vật'}, {'title': 'tóm tắt về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về graz, trần hưng đạo, hamburger, claude monet, en plein air và e3 2021'}, {'title': 'tổng hợp các chủ đề về văn hóa, thể thao, chính trị và tổ chức quốc tế'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các nhân vật và chủ đề nổi bật'}, {'title': 'tổng hợp các chủ đề về kinh tế, khoa học, công nghệ và quân sự'}, {'title': 'tổng hợp các chủ đề về tên lửa, chính trị, thể thao, nghệ thuật, ẩm thực, y tế và công nghiệp'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề đa dạng'}, {'title': 'tổng hợp các chủ đề về khoa học, công nghệ, giải trí và thể thao'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử và khoa học'}, {'title': 'tổng quan về các chủ đề văn hóa, khoa học viễn tưởng và chính trị'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề đa dạng'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về địa lý, khoa học, lịch sử và văn hóa'}, {'title': 'tổng hợp các chủ đề về văn hóa, thể thao, nghệ thuật và công nghệ'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'sản xuất và phúc lợi kinh tế'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề đa dạng'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng quan về các nhân vật và chủ đề nổi bật'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'vũ khí hạt nhân và các chủ đề khác'}, {'title': 'rafael nadal, suy thận, kinh thánh, ký sinh trùng'}, {'title': 'tổng hợp các chủ đề về khoa học, văn hóa, địa lý và giải trí'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'nông nghiệp'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề đa dạng'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học, và địa lý'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tóm tắt về các chủ đề khoa học, nghệ thuật và công nghệ'}, {'title': 'tổng hợp các chủ đề về khoa học, nghệ thuật và thể thao'}, {'title': 'giới thiệu về các nhân vật và trào lưu nổi tiếng'}, {'title': 'nghệ thuật trừu tượng và các chủ đề khác'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học và chính trị'}, {'title': 'tổng quan về các nhân vật và sự kiện nổi bật'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về phim, hội khoa học, giáo dục, thể thao, y tế, thức uống và nghệ thuật'}, {'title': 'tổng quan về các chủ đề đa dạng'}, {'title': 'tổng quan về các nhân vật và chủ đề nổi bật'}, {'title': 'nguyễn duy nhuệ và các chủ đề khác'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các sự kiện và thông tin về khoa học, lịch sử, văn hóa và xã hội'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học, văn hóa và thể thao'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học, văn hóa và thể thao'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các thông tin về nhiều chủ đề'}, {'title': 'giới thiệu về các chủ đề khác nhau'}, {'title': 'tóm tắt về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, nghệ thuật, khoa học và công nghệ'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'kali'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'xe điện và các chủ đề khác'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về địa lý, lịch sử, khoa học, văn hóa và thể thao'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về nghệ thuật, lịch sử và khoa học'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về khoa học, nghệ thuật và kinh tế'}, {'title': 'tổng hợp các chủ đề về kinh tế, văn hóa và khoa học'}, {'title': 'đau thần kinh tọa'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa và khoa học'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa, địa lý và khoa học'}, {'title': 'tổng hợp các chủ đề về khoa học, lịch sử, văn hóa và thể thao'}, {'title': 'tổng hợp các thông tin về nhiều chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề đa dạng'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử, nghệ thuật và khoa học'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tóm tắt về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học và văn hóa'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về hóa học, lịch sử, địa lý và văn hóa'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về thể thao, khoa học và văn hóa'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về khoa học, văn hóa, và giải trí'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp kiến thức về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khoa học và nghệ thuật'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp kiến thức về nhiều chủ đề'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề đa dạng'}, {'title': 'tổng hợp các chủ đề về văn học, lịch sử, khoa học và công nghệ'}, {'title': 'tổng hợp các chủ đề về chính trị, khoa học, văn hóa và lịch sử'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử, khoa học và kinh doanh'}, {'title': 'jeff bezos, trận somme, năng lượng địa nhiệt và lý thuyết sản xuất'}, {'title': 'tổng hợp kiến thức về sản xuất, nguyên tử, táo tây, phản ứng thế, john f. kennedy, tôn đức thắng, adidas, keep running'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về địa lý, văn hóa, tôn giáo, khoa học và giải trí'}, {'title': 'tổng quan về các quốc gia và doanh nghiệp'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp kiến thức về các chủ đề khác nhau'}, {'title': 'thế vận hội trẻ, suy thận, dassault rafale, lockheed c-130 hercules, viêm tiền liệt tuyến, núi phú sĩ, nova scotia, đế quốc sikh'}, {'title': 'tổng quan về các chủ đề lịch sử, văn hóa và chính trị'}, {'title': 'tổng hợp các chủ đề'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử, khoa học và thể thao'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tóm tắt về các chủ đề khác nhau'}, {'title': 'nội dung đa dạng về lịch sử, khoa học, thể thao và ẩm thực'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'âm nhạc'}, {'title': 'jennifer lawrence và các chủ đề khác'}, {'title': 'tổng hợp các chủ đề về âm nhạc, khoa học và giải thưởng'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về địa lý, lịch sử, văn hóa và thể thao'}, {'title': 'văn miếu – quốc tử giám'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học, văn hóa và thể thao'}, {'title': 'trận hải chiến quần đảo santa cruz'}, {'title': 'thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa, khoa học và thể thao'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khoa học, lịch sử và văn hóa'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử, khoa học và công nghệ'}, {'title': 'tóm tắt về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về khoa học, lịch sử, địa lý, văn hóa và ẩm thực'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa, ẩm thực và nghệ thuật'}, {'title': 'tổng hợp các chủ đề về văn hóa, khoa học, nghệ thuật và lịch sử'}, {'title': 'tổng hợp các chủ đề về ẩm thực, thể thao, lịch sử và khoa học'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về văn hóa, thể thao, âm nhạc và lịch sử'}, {'title': 'tổng quan về các chủ đề văn học, nghệ thuật và lịch sử'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa, kinh tế và khoa học'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về khoa học, lịch sử, văn học và thể thao'}, {'title': 'tổng hợp các chủ đề đa dạng'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về y học, văn hóa, lịch sử và khoa học'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa, khoa học và chính trị'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa, khoa học và thể thao'}, {'title': 'tổng hợp các thông tin về nhiều chủ đề khác nhau'}, {'title': 'ngô đình diệm'}, {'title': 'tổng hợp tin tức về các sự kiện và nhân vật nổi bật'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tình yêu, kinh tế, nghệ thuật và văn hóa'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa, khoa học và công nghệ'}, {'title': 'tổng hợp các chủ đề về văn học, ẩm thực, thể thao, khoa học và lịch sử'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề lịch sử, văn hóa, nghệ thuật và khoa học'}, {'title': 'thiên tân'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về âm nhạc, bánh ngọt, động vật, lịch sử và văn hóa'}, {'title': 'tổng hợp kiến thức về các chủ đề khác nhau'}, {'title': 'cáp nhĩ tân'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về khoa học, công nghệ, văn hóa và y tế'}, {'title': 'tổng hợp các chủ đề về khoa học, lịch sử, văn hóa và giải trí'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'giới thiệu về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về nhiều chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về giáo dục, chính trị, thể thao và khoa học'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về khoa học, công nghệ, lịch sử và văn hóa'}, {'title': 'tổng hợp các chủ đề về văn hóa, khoa học và lịch sử'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử, giáo dục và âm nhạc'}, {'title': 'tổng hợp các chủ đề về âm nhạc, thể thao, địa lý và văn hóa'}, {'title': 'sarawak, unesco, liên kết pi, điện phân, nikola jokić, thuốc chống trầm cảm'}, {'title': 'tổng quan về các nhân vật và chủ đề nổi bật'}, {'title': 'tổng hợp các chủ đề về địa lý, văn hóa, lịch sử và nghệ thuật'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'stephen hawking, anime, homecoming và quản lý thông tin cá nhân'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề đa dạng'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các thông tin về các nhân vật và sự kiện nổi bật'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'giới thiệu về canada, hyundai, khoáng vật, vũ khí hạt nhân, nguyên tử, henri matisse và bệnh lao'}, {'title': 'tổng hợp các chủ đề về y tế, kinh tế, năng lượng, và địa chất'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'lực lượng phòng vệ israel và các sự kiện liên quan'}, {'title': 'tổng hợp các chủ đề về lịch sử, kinh tế, văn hóa và công nghệ'}, {'title': 'tổng hợp các chủ đề về khoa học, nghệ thuật, thể thao và công nghệ'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về nhân vật, khoa học và nghệ thuật'}, {'title': 'tổng quan về nhiều chủ đề'}, {'title': 'xe điện'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'thông tin về các quốc gia và nhân vật nổi tiếng'}, {'title': 'tóm tắt các chủ đề về tôn giáo, văn hóa, âm nhạc, thể thao và địa lý'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'ca trù'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử và thể thao'}, {'title': 'tổng quan về các chủ đề lịch sử, chính trị và văn hóa'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học, văn hóa và âm nhạc'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học, văn hóa và giải trí'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp kiến thức về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về nhân vật, khoa học và văn hóa'}, {'title': 'tổng hợp các chủ đề về văn hóa, khoa học và lịch sử'}, {'title': 'đế quốc songhai'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'trần hưng đạo'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học, thể thao và giải trí'}, {'title': 'tổng hợp các thông tin về phim, lịch sử và khoa học'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa, công nghệ và y học'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tóm tắt về các nhân vật và chủ đề nổi bật'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tóm tắt về các nhân vật và sự kiện nổi bật'}, {'title': 'tổng quan về các nhân vật và sự kiện lịch sử'}, {'title': 'tổng hợp thông tin về nhiều chủ đề'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'trận iwo jima'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các sự kiện và nhân vật lịch sử'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về ẩm thực, thể thao, y học và lịch sử'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học, thể thao và giải trí'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'phúc lợi kinh tế và các chủ đề liên quan'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học, công nghệ và thể thao'}, {'title': 'tổng hợp các chủ đề về lịch sử, nghệ thuật, khoa học và văn hóa'}, {'title': 'tổng hợp các chủ đề về kinh tế, văn hóa, thể thao và công nghệ'}, {'title': 'tổng hợp các chủ đề về khoa học, nghệ thuật và y tế'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về phim, ẩm thực, lịch sử và nhân vật'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khoa học, lịch sử và văn hóa'}, {'title': 'tổng hợp các chủ đề về lịch sử, địa lý, thể thao và khoa học'}, {'title': 'nội dung tổng hợp về lịch sử, văn hóa, âm nhạc và địa lý'}, {'title': 'ak-74, trái đất, công ty ford motor, văn học hậu hiện đại, ivan vasilyevich panfilov, carl edward sagan'}, {'title': 'carl sagan, lễ hội bon om touk, trình minh thế, paul adrien maurice dirac, di sản thế giới của brasil, đế chế mông cổ, máy ảnh, macaron, claude monet, large hadron collider'}, {'title': 'tổng hợp các chủ đề về khoa học, công nghệ và địa lý'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử và địa lý'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về khoa học, văn hóa, lịch sử và thể thao'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử, khoa học và nghệ thuật'}, {'title': 'thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về địa lý, văn hóa, lịch sử và khoa học'}, {'title': 'tổng hợp các thông tin về nhiều chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về y tế, lịch sử, chính trị, văn hóa và khoa học'}, {'title': 'tổng quan về các chủ đề đa dạng'}, {'title': 'giáo dục, y học hy lạp cổ đại, toyotomi hideyoshi, alexander zverev, ludwig boltzmann, giải thưởng âm nhạc mtv châu âu, khoáng vật học, viện bảo tàng orsay, viêm loét dạ dày - tá tràng, rối loạn ám ảnh cưỡng chế'}, {'title': 'tổng hợp các chủ đề về khoa học, lịch sử và văn hóa'}, {'title': 'tổng hợp các chủ đề về lịch sử, văn hóa, khoa học và kinh tế'}, {'title': 'tổng hợp các chủ đề về gia đình, quốc gia, phim ảnh, tôn giáo, chiến tranh và thể thao'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khoa học, nghệ thuật và thể thao'}, {'title': 'tán xạ coulomb, mansa musa, louis pasteur, galileo, thiệu trị, động cơ đốt trong'}, {'title': 'động cơ đốt trong và các chủ đề khác'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'giants của lịch sử'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về phim, lịch sử, văn hóa và khoa học'}, {'title': 'tổng quan về các chủ đề văn hóa, nghệ thuật và công nghệ'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử và khoa học'}, {'title': 'nội dung tổng hợp về nhiều chủ đề'}, {'title': 'tổng quan về các nhân vật và chủ đề nổi bật'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về khoa học, nghệ thuật và nhân vật nổi tiếng'}, {'title': 'nội dung tổng hợp'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về khoa học, văn hóa, lịch sử và công nghệ'}, {'title': 'thông tin về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các thông tin về e3 2021, người đi xuyên tường, học viện chính trị quốc gia hồ chí minh, matcha, liên hiệp các hội văn học nghệ thuật việt nam, trịnh đình thảo và ký sinh trùng'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp thông tin về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tóm tắt về các chủ đề khác nhau'}, {'title': 'tổng quan về một số nhân vật và chủ đề lịch sử'}, {'title': 'tổng quan về các nhân vật và tổ chức nổi tiếng'}, {'title': 'tổng quan về các chủ đề khoa học, lịch sử, văn hóa và y học'}, {'title': 'tổng hợp các chủ đề về lịch sử, khoa học và địa lý'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các thông tin về các nhân vật và địa điểm lịch sử'}, {'title': 'tổng hợp các chủ đề về lịch sử, âm nhạc, địa lý, văn học và khoa học'}, {'title': 'tổng hợp các chủ đề khác nhau'}, {'title': 'tổng hợp các thông tin về nhiều chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp kiến thức về nhiều chủ đề'}, {'title': 'tổng hợp các chủ đề về khoa học, lịch sử, văn hóa và chính trị'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về xã hội, kinh tế, khoa học và lịch sử'}, {'title': 'tổng hợp các chủ đề về văn hóa, lịch sử, khoa học và y học'}, {'title': 'tổng hợp thông tin về các nhân vật và chủ đề nổi bật'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng quan về các chủ đề khoa học và công nghệ'}, {'title': 'liên kết pi'}, {'title': 'vắc xin, ẩm thực anh, du lịch paris, thể thao dưới mặt nước, bộ trưởng ngân khố hoa kỳ, dmitri shostakovich'}, {'title': 'tổng quan về các chủ đề khác nhau'}, {'title': 'tổng hợp các chủ đề về âm nhạc, bệnh than, in 3d, lãnh đạo tôn giáo, quốc hội và các nhân vật nổi tiếng'}, {'title': 'tổng hợp các chủ đề về người, địa điểm, sự kiện và khái niệm'}, {'title': 'nội dung về tên lửa, ngô đình diệm, antoine laurent de lavoisier, năng lượng tái tạo, lý bạch và liên minh trung tâm'}, {'title': 'liên minh trung tâm và các sự kiện lịch sử'}]
    #
    # entities_relationship = []
    # a = []
    # with open(r"D:\PycharmProjects\dataset\vmlu\entities_vi_squad.json", 'r', encoding='utf-8-sig') as f:
    #     for line in f:
    #         line = line.strip()  # loại bỏ ký tự xuống dòng
    #         if line:  # bỏ qua dòng rỗng
    #             try:
    #                 data = ast.literal_eval(line)
    #                 entities_relationship.append(data['entity_relation'])
    #             except json.JSONDecodeError as e:
    #                 print(f"Lỗi đọc JSON: {e}")
    #
    # uuid_user = 'vi_squad'
    # print(uuid_user)
    # neo.add_single_relationship("tài liệu", "General", uuid_user, "Document", "BAO_GỒM")
    # print("b1 complete")
    # # b2: nối document với tiêu đề
    # for title in titles:
    #     neo.add_single_relationship(uuid_user, "Document", title["title"], "Part", "BAO_GỒM")
    # print("b2 complete")
    # # b3: nối tiêu đề với entities_relationship
    # for r, title in zip(entities_relationship, titles):
    #     neo.import_relationships(r, title["title"], "Part")
    #
    # print("Complete!")





