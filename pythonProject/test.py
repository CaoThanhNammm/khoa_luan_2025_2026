import pandas as pd
import requests
import json
import os
import time
from uuid import uuid4

dialogue = [
  {
    "id": 1,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Xin chào các bạn đến với podcast của chúng tôi!"
  },
  {
    "id": 1,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Các bạn có nhớ cảm giác hồi năm 2020, khi cả thế giới như ngừng thở vì COVID-19 không?"
  },
  {
    "id": 1,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tôi vẫn nhớ những ngày đeo khẩu trang mọi lúc, rửa tay đến khô cả da, và lo lắng mỗi khi nghe ai đó ho."
  },
  {
    "id": 1,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tưởng rằng mọi thứ đã qua, nhưng gần đây, tôi đọc tin tức và thấy... COVID-19 đang trở lại, lặng lẽ nhưng đáng lo."
  },
  {
    "id": 1,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hôm nay, chúng ta sẽ cùng tìm hiểu xem chuyện gì đang xảy ra, liệu có đáng lo không, và chúng ta cần làm gì để bảo vệ bản thân."
  },
  {
    "id": 2,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Này Alex, COVID-19 giống như một  người yêu cũ  cứ quay lại đúng lúc mình không mong đợi!"
  },
  {
    "id": 2,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi thì bận hẹn hò, sáng tác nhạc, đâu có thời gian để ý, nhưng nghe nói nó đang gây sóng gió ở Thái Lan, Anh, Brazil..."
  },
  {
    "id": 2,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Có thật không mà mọi người lo thế?"
  },
  {
    "id": 3,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Thật đấy Vi Rút ạ, không phải tự nhiên mà người ta lo đâu."
  },
  {
    "id": 3,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tôi mới đọc báo tuần trước thấy số ca nhiễm đang tăng khá nhanh ở nhiều nước."
  },
  {
    "id": 4,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Thế thì phiền thật!"
  },
  {
    "id": 4,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi đang có kế hoạch ra mắt album mới, lại còn phải hẹn hò với ba người khác nhau trong tuần này."
  },
  {
    "id": 4,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Mà này, tôi luôn nói rằng hẹn hò chưa phải là yêu, nên việc gặp gỡ nhiều người cùng lúc là hoàn toàn bình thường mà, đúng không?"
  },
  {
    "id": 5,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Với triết lý sống của cậu thì đúng rồi."
  },
  {
    "id": 5,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhưng có lẽ cậu nên cẩn thận hơn trong thời điểm này."
  },
  {
    "id": 5,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "À, hôm nay chúng ta còn có một khách mời đặc biệt nữa."
  },
  {
    "id": 5,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chào Chây 97, rất vui khi được đón cậu đến với podcast của chúng tôi."
  },
  {
    "id": 6,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Chào Alex và Vi Rút."
  },
  {
    "id": 6,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Cảm ơn vì đã mời tôi."
  },
  {
    "id": 6,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi từng mắc COVID-19 hồi 2021, lúc đang ở đỉnh cao sự nghiệp."
  },
  {
    "id": 6,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Cảm giác như bị knock-out vậy, ho, sốt, mệt mỏi, rồi còn bị cách ly nữa."
  },
  {
    "id": 6,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Giờ nghe nói nó quay lại, tôi thấy hơi lo, nhất là khi nhiều người trẻ như tôi đang chủ quan."
  },
  {
    "id": 7,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Ồ, tôi không biết là cậu từng mắc COVID."
  },
  {
    "id": 7,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Chắc khó khăn lắm phải không?"
  },
  {
    "id": 7,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Đang trên đỉnh cao mà bị gián đoạn."
  },
  {
    "id": 8,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng vậy."
  },
  {
    "id": 8,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Sau đợt đó, công việc của tôi bị ảnh hưởng nhiều lắm."
  },
  {
    "id": 8,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Chưa kể là tôi còn gặp một số vấn đề khác nữa, khiến sự nghiệp không còn được như trước."
  },
  {
    "id": 9,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chây ạ, nhiều người vẫn rất yêu mến những sáng tác của cậu đấy."
  },
  {
    "id": 9,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tôi nghĩ đây là cơ hội tốt để cậu chia sẻ câu chuyện của mình và cảnh báo giới trẻ về những rủi ro của COVID-19."
  },
  {
    "id": 10,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Cảm ơn Alex."
  },
  {
    "id": 10,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng là tôi muốn nhắn nhủ với các bạn trẻ rằng đừng chủ quan."
  },
  {
    "id": 10,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "COVID không chỉ ảnh hưởng đến sức khỏe mà còn có thể tác động lớn đến sự nghiệp và cuộc sống của các bạn."
  },
  {
    "id": 11,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nhưng giờ có vắc-xin rồi, chắc không sao đâu nhỉ?"
  },
  {
    "id": 11,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi đã tiêm đến 3 mũi đấy."
  },
  {
    "id": 12,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Vắc-xin giúp giảm nguy cơ bệnh nặng, nhưng không có nghĩa là bạn không thể nhiễm bệnh."
  },
  {
    "id": 12,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi nghĩ chúng ta vẫn nên cẩn thận."
  },
  {
    "id": 13,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng vậy, Chây."
  },
  {
    "id": 13,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "COVID-19 có thể không còn là  cơn bão lớn  như trước, nhưng nó vẫn âm thầm len lỏi."
  },
  {
    "id": 13,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Để hiểu rõ hơn, chúng ta sẽ bắt đầu bằng việc nhìn vào bức tranh toàn cầu."
  },
  {
    "id": 13,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Liệu COVID-19 đang thực sự bùng phát trở lại?"
  },
  {
    "id": 13,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hãy cùng tìm hiểu ở chương đầu tiên!"
  },
  {
    "id": 13,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Như chúng ta đã trao đổi, COVID-19 có vẻ đang âm thầm quay trở lại."
  },
  {
    "id": 13,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hãy nhìn vào bức tranh toàn cầu nhé."
  },
  {
    "id": 13,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Ở Thái Lan, từ đầu năm đến 10/5/2025, họ đã ghi nhận 53676 ca nhiễm, với 16 ca tử vong."
  },
  {
    "id": 13,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Riêng Bangkok đã có 16.723 ca."
  },
  {
    "id": 13,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nguyên nhân chính là biến thể XBB.1.16 của Omicron, một biến thể lây lan nhanh nhưng may mắn là gây ra triệu chứng nhẹ hơn so với các biến thể trước đây."
  },
  {
    "id": 14,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nghe thì giống như COVID đang đi tour thế giới nhỉ?"
  },
  {
    "id": 14,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nhưng tại sao ở Thái Lan lại tăng mạnh thế, có phải vì lễ hội không?"
  },
  {
    "id": 14,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi đang lên kế hoạch sang đó biểu diễn tháng tới đấy."
  },
  {
    "id": 14,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Phải hủy không nhỉ?"
  },
  {
    "id": 15,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng là Thái Lan vừa trải qua lễ hội té nước Songkran, nơi hàng nghìn người tụ tập, tiếp xúc gần."
  },
  {
    "id": 15,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhưng chưa hẳn phải hủy kế hoạch của cậu đâu, chỉ là cần thêm biện pháp phòng ngừa thôi."
  },
  {
    "id": 15,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Còn ở Anh, tình hình có vẻ ổn định hơn một chút."
  },
  {
    "id": 15,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Số ca nhập viện giảm nhẹ vào tháng 4/2025, với khoảng 1.056 ca mỗi tuần."
  },
  {
    "id": 15,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tuy nhiên, đến tháng 5 này, đã có dấu hiệu tăng trở lại, mặc dù chúng ta chưa có số liệu cụ thể."
  },
  {
    "id": 16,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thấy nhiều bạn trẻ giờ đi du lịch, dự concert đông lắm."
  },
  {
    "id": 16,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nếu không cẩn thận, COVID có thể lây nhanh như cách một bài hit lan tỏa."
  },
  {
    "id": 16,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nhớ hồi tôi ra mắt single đầu tiên, chỉ trong một đêm đã có hàng triệu lượt nghe."
  },
  {
    "id": 16,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "COVID cũng  viral  kiểu đó đấy, nhưng là theo nghĩa đen."
  },
  {
    "id": 17,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nói đến viral, tôi tự hào là chuyên gia về việc làm mọi thứ lan truyền nhanh chóng."
  },
  {
    "id": 17,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nhưng thú thật là tôi không muốn liên quan gì đến người anh em COVID này đâu."
  },
  {
    "id": 17,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Mà này Alex, Brazil thì sao?"
  },
  {
    "id": 17,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi có kế hoạch sang đó  quẩy  mùa carnival năm sau."
  },
  {
    "id": 18,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Brazil từng là điểm nóng với hơn 37 triệu ca vào năm 2023."
  },
  {
    "id": 18,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hiện tại chúng ta chưa có số liệu chính xác cho tháng 5/2025, nhưng với việc giao thương, du lịch tăng cao, khả năng gia tăng ca nhiễm là điều đáng lo ngại."
  },
  {
    "id": 18,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tuy nhiên, nếu nhìn vào bức tranh toàn cầu, trong 28 ngày tính đến 27/4/2025, thế giới ghi nhận 25.463 ca nhiễm, giảm 56,9% so với chu kỳ trước đó."
  },
  {
    "id": 19,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Con số giảm nghe có vẻ tích cực, nhưng liệu có phải do chúng ta không xét nghiệm nhiều như trước không?"
  },
  {
    "id": 19,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi biết nhiều người bây giờ chỉ cần thấy ho sốt nhẹ là tự cách ly ở nhà, không đi xét nghiệm nữa."
  },
  {
    "id": 20,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Câu hỏi rất hay, Chây."
  },
  {
    "id": 20,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng là có thể có  con số tối  không được báo cáo."
  },
  {
    "id": 20,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhưng tin tốt là Tổ chức Y tế Thế giới WHO hiện chưa đưa ra cảnh báo mới về biến thể nguy hiểm nào."
  },
  {
    "id": 20,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Biến thể XBB.1.16 tuy lây lan nhanh nhưng ít gây ra triệu chứng nghiêm trọng, đặc biệt ở những người đã tiêm phòng."
  },
  {
    "id": 21,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nhưng tôi vẫn thắc mắc, tại sao lại có sự chênh lệch lớn giữa các quốc gia?"
  },
  {
    "id": 21,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Bangkok gần 17 nghìn ca, trong khi Anh lại giảm."
  },
  {
    "id": 21,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Phải chăng virus này cũng  biết chọn điểm đến  như tôi?"
  },
  {
    "id": 22,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Không hẳn là virus  biết chọn  đâu Vi Rút, mà là do nhiều yếu tố khác nhau."
  },
  {
    "id": 22,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Ví dụ như tỷ lệ tiêm chủng, mật độ dân số, các biện pháp phòng ngừa công cộng, thậm chí là thời tiết và thói quen sinh hoạt của người dân."
  },
  {
    "id": 22,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Ở các nước nhiệt đới như Thái Lan, mọi người thường tụ tập ngoài trời nhiều hơn."
  },
  {
    "id": 23,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi có một câu hỏi."
  },
  {
    "id": 23,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Với việc giao thương quốc tế đã trở lại bình thường, liệu chúng ta có nguy cơ lặp lại tình trạng như năm 2020 không?"
  },
  {
    "id": 23,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi đang có tour diễn châu Á vào cuối năm nay và hơi lo lắng."
  },
  {
    "id": 24,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là một lo ngại chính đáng."
  },
  {
    "id": 24,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tuy nhiên, điểm khác biệt lớn so với năm 2020 là giờ đây chúng ta đã có vắc-xin, thuốc điều trị, và hiểu biết tốt hơn về virus."
  },
  {
    "id": 24,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhiều người đã có miễn dịch tự nhiên sau khi nhiễm bệnh hoặc tiêm phòng."
  },
  {
    "id": 24,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Điều này không có nghĩa là chúng ta có thể chủ quan, nhưng cũng không cần phải hoảng sợ như trước."
  },
  {
    "id": 25,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nói đến vắc-xin, tôi tiêm mũi cuối cùng cách đây hơn một năm rồi."
  },
  {
    "id": 25,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Các bạn nghĩ tôi có nên tiêm nhắc lại không?"
  },
  {
    "id": 25,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Lịch trình của tôi dày đặc lắm, không muốn bị gián đoạn vì ốm đâu."
  },
  {
    "id": 26,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đây là câu hỏi mà nhiều người đang thắc mắc."
  },
  {
    "id": 26,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Theo khuyến cáo hiện tại, nhóm nguy cơ cao như người già, người có bệnh nền nên tiêm nhắc lại."
  },
  {
    "id": 26,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Với người khỏe mạnh như Vi Rút, bạn có thể tham khảo ý kiến bác sĩ."
  },
  {
    "id": 26,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhưng với lịch trình di chuyển nhiều của cậu, có lẽ việc tiêm nhắc lại là một ý tưởng không tồi."
  },
  {
    "id": 27,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi nghĩ giới trẻ cần nghiêm túc hơn với vấn đề này."
  },
  {
    "id": 27,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Hồi tôi bị COVID, không chỉ sức khỏe mà cả tinh thần cũng bị ảnh hưởng nặng nề."
  },
  {
    "id": 27,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Một tuần không thể ra khỏi phòng, không gặp gỡ, không biểu diễn... thật sự rất khó khăn."
  },
  {
    "id": 28,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cảm ơn Chây vì đã chia sẻ trải nghiệm cá nhân."
  },
  {
    "id": 28,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó chính là điều chúng ta cần nhấn mạnh: COVID-19 không chỉ ảnh hưởng đến sức khỏe thể chất mà còn tác động đến tinh thần, công việc, và cuộc sống hàng ngày."
  },
  {
    "id": 28,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tóm lại, bức tranh toàn cầu cho thấy COVID-19 đang có dấu hiệu trở lại, đặc biệt ở một số quốc gia châu Á."
  },
  {
    "id": 28,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Dù không đáng báo động như những đợt dịch trước, nhưng chắc chắn đây không phải là thời điểm để chúng ta chủ quan."
  },
  {
    "id": 28,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Sau khi chúng ta đã tìm hiểu về tình hình COVID-19 trên thế giới và các biến thể mới, giờ là lúc nói về điều mà tôi nghĩ rất nhiều người đang quan tâm: Việt Nam đã chuẩn bị gì để đối phó với làn sóng COVID mới này?"
  },
  {
    "id": 28,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Bộ Y tế của chúng ta đã có những biện pháp khá toàn diện, bao gồm việc chuẩn bị khu cách ly tại các bệnh viện, tăng cường giám sát tại cửa khẩu, và đảm bảo đủ thuốc cùng vật tư y tế."
  },
  {
    "id": 29,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nghe có vẻ họ đã lường trước được sự trở lại của tôi nhỉ?"
  },
  {
    "id": 29,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nhưng mà Alex này, cậu có thấy là dạo này khi đi ra đường, người ta không còn đeo khẩu trang nhiều như trước không?"
  },
  {
    "id": 29,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi thì đang băn khoăn xem có nên đeo khẩu trang khi đi biểu diễn không?"
  },
  {
    "id": 29,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Mặt tôi đẹp thế này mà che đi thì phí quá."
  },
  {
    "id": 30,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng là nhiều người đã chủ quan, Vi Rút ạ."
  },
  {
    "id": 30,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là lý do Bộ Y tế đang tăng cường truyền thông về việc đeo khẩu trang, rửa tay, và hạn chế tụ tập đông người."
  },
  {
    "id": 30,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đặc biệt là với các nhóm nguy cơ cao như người già, người có bệnh nền, hay phụ nữ mang thai."
  },
  {
    "id": 30,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Họ cũng đã chuẩn bị kế hoạch kiểm soát bền vững COVID-19 giai đoạn 2023-2025, sẵn sàng cho kịch bản nếu xuất hiện biến thể mới nguy hiểm hơn."
  },
  {
    "id": 31,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi đã thấy nhiều bạn trẻ bỏ qua khẩu trang vì nghĩ COVID không còn đáng sợ."
  },
  {
    "id": 31,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nhưng tin tôi đi, bị một lần là đủ sợ rồi!"
  },
  {
    "id": 31,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Khi tôi nhiễm COVID, mất cả hai tuần mới hồi phục hoàn toàn."
  },
  {
    "id": 31,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Hai buổi biểu diễn quan trọng phải hủy, và tôi còn lo lắng về các biến chứng dài hạn nữa."
  },
  {
    "id": 32,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Đeo khẩu trang à?"
  },
  {
    "id": 32,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi thấy hơi bất tiện khi đi hát, nhưng thôi, an toàn là trên hết."
  },
  {
    "id": 32,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Giống như chọn người yêu, cẩn thận vẫn hơn!"
  },
  {
    "id": 32,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Mà nói thật, tôi đang hẹn hò với ba người cùng lúc, cũng phải cẩn thận giữ gìn sức khỏe thôi."
  },
  {
    "id": 32,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi không muốn lây cho ai cả."
  },
  {
    "id": 33,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng là sức khỏe phải đặt lên hàng đầu."
  },
  {
    "id": 33,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Theo khuyến cáo của Bộ Y tế, chúng ta nên đeo khẩu trang ở nơi công cộng, rửa tay thường xuyên, và tránh tiếp xúc với người có triệu chứng hô hấp."
  },
  {
    "id": 33,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đặc biệt, nếu bạn có các triệu chứng như sốt, ho, khó thở, hãy đến cơ sở y tế ngay, đừng cố chịu đựng ở nhà."
  },
  {
    "id": 34,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng vậy, Alex."
  },
  {
    "id": 34,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi nhớ khi tôi bị, lúc đầu cứ nghĩ là cảm cúm thông thường thôi, nên ở nhà tự uống thuốc."
  },
  {
    "id": 34,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nhưng đến ngày thứ ba, khi bắt đầu khó thở, tôi mới đi khám và phát hiện đã bị viêm phổi."
  },
  {
    "id": 34,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "May mà phát hiện kịp thời, chứ không thì nguy hiểm lắm."
  },
  {
    "id": 35,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Chây này, thế sau khi bị COVID, cậu có thấy ảnh hưởng gì đến giọng hát không?"
  },
  {
    "id": 35,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Là ca sĩ mà bị ảnh hưởng đến giọng thì thật là thiệt thòi."
  },
  {
    "id": 35,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi đang lo lắng đấy."
  },
  {
    "id": 36,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Thực sự thì có đấy, Vi Rút à."
  },
  {
    "id": 36,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tầm hai tháng đầu sau khi khỏi bệnh, tôi thấy giọng không được như trước."
  },
  {
    "id": 36,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Hơi yếu và không giữ được những nốt cao."
  },
  {
    "id": 36,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Phải tập luyện rất nhiều mới lấy lại phong độ."
  },
  {
    "id": 36,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đó là lý do tôi khuyên mọi người, đặc biệt là các bạn trẻ, đừng coi thường virus này."
  },
  {
    "id": 37,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cảm ơn Chây vì chia sẻ rất thực tế."
  },
  {
    "id": 37,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tôi nghĩ điều này cũng góp phần giải thích tại sao Bộ Y tế nhấn mạnh đến việc phát hiện sớm và điều trị kịp thời."
  },
  {
    "id": 37,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Họ đã chỉ đạo các cơ sở y tế chuẩn bị đủ nhân lực, thuốc men để đáp ứng kịp thời nếu số ca bệnh tăng."
  },
  {
    "id": 37,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Các bệnh viện tuyến trung ương và địa phương đều đã có phương án sẵn sàng."
  },
  {
    "id": 38,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Mà này, tôi nghe nói có  2K  gì đó, là gì vậy Alex?"
  },
  {
    "id": 38,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Không phải là 2.000 đồng đúng không?"
  },
  {
    "id": 39,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Không phải đâu Vi Rút."
  },
  {
    "id": 39,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " 2K  là khẩu hiệu nhắc nhở mọi người về hai biện pháp phòng ngừa cơ bản: Khẩu trang và Khử khuẩn (rửa tay)."
  },
  {
    "id": 39,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Trước đây chúng ta có  5K , nhưng giờ đã đơn giản hóa thành  2K  để dễ nhớ và thực hiện hơn."
  },
  {
    "id": 40,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi nghĩ  2K  là đủ cho giai đoạn hiện tại."
  },
  {
    "id": 40,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đeo khẩu trang và rửa tay thường xuyên không khó, nhưng hiệu quả thì rất lớn."
  },
  {
    "id": 40,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Các bạn trẻ hay nghĩ mình khỏe mạnh nên chủ quan, nhưng thực ra ai cũng có thể bị nhiễm và gặp biến chứng."
  },
  {
    "id": 41,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Thế còn vắc-xin thì sao?"
  },
  {
    "id": 41,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi tiêm mũi cuối cùng cách đây hơn một năm rồi."
  },
  {
    "id": 41,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Có cần tiêm nhắc lại không?"
  },
  {
    "id": 42,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Theo thông tin từ Bộ Y tế, họ khuyến cáo các nhóm nguy cơ cao như người trên 65 tuổi, người có bệnh nền, nhân viên y tế nên tiêm nhắc lại."
  },
  {
    "id": 42,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Với người bình thường khỏe mạnh, miễn dịch từ các mũi tiêm trước vẫn còn hiệu quả trong việc giảm nguy cơ bệnh nặng và tử vong, dù không hoàn toàn ngăn được việc nhiễm bệnh."
  },
  {
    "id": 43,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi nghĩ chúng ta cũng nên nhắc đến những người làm việc trong môi trường tiếp xúc nhiều như nghệ sĩ chúng tôi."
  },
  {
    "id": 43,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Chúng tôi thường xuyên gặp gỡ nhiều người, biểu diễn ở những nơi đông đúc."
  },
  {
    "id": 43,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Vì vậy, cần cẩn trọng hơn người bình thường."
  },
  {
    "id": 44,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Đúng vậy!"
  },
  {
    "id": 44,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi có show diễn vào cuối tuần này với hơn 2000 khán giả."
  },
  {
    "id": 44,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Có lẽ tôi nên đeo khẩu trang khi không lên sân khấu, và chuẩn bị gel rửa tay trong phòng chờ."
  },
  {
    "id": 44,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Mà khán giả thì sao nhỉ?"
  },
  {
    "id": 44,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Chúng ta có nên yêu cầu họ đeo khẩu trang không?"
  },
  {
    "id": 45,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là một câu hỏi hay."
  },
  {
    "id": 45,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hiện tại, Bộ Y tế khuyến khích đeo khẩu trang ở nơi công cộng, đặc biệt là nơi đông người, nhưng chưa có quy định bắt buộc."
  },
  {
    "id": 45,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Các đơn vị tổ chức sự kiện có thể đưa ra khuyến cáo cho khán giả, cũng như chuẩn bị dung dịch khử khuẩn tay tại các điểm ra vào."
  },
  {
    "id": 46,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi cũng muốn nhấn mạnh một điều: nếu bạn có các triệu chứng như ho, sốt, khó thở, hãy ở nhà!"
  },
  {
    "id": 46,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đừng cố gắng đi xem concert hay tham gia sự kiện đông người."
  },
  {
    "id": 46,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đó không chỉ là bảo vệ bản thân mà còn là trách nhiệm với cộng đồng."
  },
  {
    "id": 47,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hoàn toàn đồng ý với Chây."
  },
  {
    "id": 47,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Ngoài ra, Bộ Y tế cũng khuyến cáo chúng ta nên chú ý đến chế độ ăn uống, nghỉ ngơi hợp lý để tăng cường sức đề kháng."
  },
  {
    "id": 47,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Vitamin C, D và kẽm có thể giúp hệ miễn dịch hoạt động tốt hơn."
  },
  {
    "id": 48,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi vẫn uống vitamin mỗi ngày đấy."
  },
  {
    "id": 48,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Công việc của tôi đòi hỏi phải luôn khỏe mạnh, năng động."
  },
  {
    "id": 48,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Không thể để COVID làm gián đoạn lịch trình được."
  },
  {
    "id": 49,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Việt Nam đã có sự chuẩn bị khá kỹ lưỡng để ứng phó với làn sóng COVID mới."
  },
  {
    "id": 49,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Các biện pháp của Bộ Y tế tập trung vào việc giám sát, phát hiện sớm, và điều trị kịp thời."
  },
  {
    "id": 49,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Còn về phía người dân, việc tuân thủ  2K  - đeo khẩu trang và khử khuẩn tay - vẫn là cách hiệu quả nhất để bảo vệ bản thân và cộng đồng."
  },
  {
    "id": 49,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Sau khi đã tìm hiểu về tình hình hiện tại và các biện pháp ứng phó, chúng ta hãy nhìn lại một chút."
  },
  {
    "id": 49,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhớ giai đoạn 2020-2022 không?"
  },
  {
    "id": 49,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Việt Nam từng ghi nhận hơn 11,6 triệu ca nhiễm và 43.000 ca tử vong, chủ yếu trong đợt bùng phát thứ tư."
  },
  {
    "id": 49,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhìn lại, sự thành công trong kiểm soát dịch bệnh của chúng ta đến từ chiến dịch tiêm chủng quy mô lớn và các biện pháp kiểm soát nghiêm ngặt."
  },
  {
    "id": 49,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tuy nhiên, nhiều người đã quên đi những bài học đắt giá đó."
  },
  {
    "id": 50,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Hồi 2020, doanh nghiệp của tôi suýt phá sản vì COVID."
  },
  {
    "id": 50,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Giờ tôi phải cẩn thận hơn, không chỉ với sức khỏe mà cả công việc."
  },
  {
    "id": 50,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nhớ lúc đó không?"
  },
  {
    "id": 50,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi đang chuẩn bị ra album mới, tour diễn đã lên lịch đầy đủ, rồi bùm - mọi thứ đóng cửa."
  },
  {
    "id": 50,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Album thì phát hành online, fan không thể đến gặp, quán bar đóng cửa hết."
  },
  {
    "id": 50,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Phải nói đó là thời kỳ tồi tệ nhất trong sự nghiệp của tôi."
  },
  {
    "id": 51,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng vậy, Vi Rút."
  },
  {
    "id": 51,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "COVID-19 không chỉ là vấn đề sức khỏe mà còn gây ra tác động kinh tế, giáo dục và xã hội rất lớn."
  },
  {
    "id": 51,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chứng khoán sụt giảm nghiêm trọng, trường học phải đóng cửa kéo dài, ngành du lịch gần như  đóng băng ."
  },
  {
    "id": 51,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhiều gia đình mất đi người thân, nhiều người mất việc làm."
  },
  {
    "id": 51,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chây, cậu còn nhớ thời điểm đó chứ?"
  },
  {
    "id": 52,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Sao quên được, Alex."
  },
  {
    "id": 52,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Hồi đó, tôi mất nhiều show diễn vì dịch."
  },
  {
    "id": 52,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Giờ thấy mọi người đi chơi đông, tôi lo nếu không cẩn thận, lịch sử có thể lặp lại."
  },
  {
    "id": 52,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi nhớ có giai đoạn phải học online, không được gặp bạn bè, không thể đi tập luyện, chỉ ở nhà và chờ đợi."
  },
  {
    "id": 52,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Thật sự rất khó khăn, nhất là với một người trẻ như tôi."
  },
  {
    "id": 52,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nhưng điều đáng lo là nhiều bạn trẻ bây giờ dường như đã quên đi giai đoạn khó khăn đó rồi."
  },
  {
    "id": 53,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi thấy những người trẻ bây giờ vô tư quá."
  },
  {
    "id": 53,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Họ đi chơi, tụ tập, concert nào cũng chen chúc."
  },
  {
    "id": 53,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi biết vì các show diễn của tôi vẫn đông nghẹt, không ai đeo khẩu trang cả."
  },
  {
    "id": 53,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Một mặt thì tôi vui vì kinh doanh tốt, mặt khác thì cũng hơi lo."
  },
  {
    "id": 54,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó chính là một trong những nguy cơ lớn nhất trong năm 2025 này."
  },
  {
    "id": 54,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Giao thương và du lịch đang tăng cao, đặc biệt khi chúng ta sắp bước vào dịp Tết Nguyên đán."
  },
  {
    "id": 54,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Lượng người di chuyển giữa các quốc gia, các vùng miền sẽ rất lớn, có thể làm lây lan dịch bệnh nhanh chóng nếu không có biện pháp phòng ngừa phù hợp."
  },
  {
    "id": 55,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng vậy."
  },
  {
    "id": 55,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi có nhiều bạn bè đang lên kế hoạch đi du lịch nước ngoài dịp Tết này."
  },
  {
    "id": 55,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Họ chọn các điểm đến như Thái Lan, Nhật Bản, Hàn Quốc - những nơi đang có số ca COVID tăng."
  },
  {
    "id": 55,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nhưng khi tôi nhắc họ nên chuẩn bị khẩu trang và các biện pháp phòng ngừa, họ chỉ cười và nói  COVID giờ nhẹ lắm, không sao đâu ."
  },
  {
    "id": 56,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Đó là điều đáng lo đấy."
  },
  {
    "id": 56,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi đang có kế hoạch mở rộng kinh doanh vào năm nay, không muốn lại bị gián đoạn vì COVID đâu."
  },
  {
    "id": 56,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Với tình hình dịch bệnh hiện tại, tôi thậm chí đã phải cân nhắc lại việc hẹn hò nhiều người cùng lúc."
  },
  {
    "id": 56,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Không phải vì tôi thay đổi quan điểm - tôi vẫn tin hẹn hò chưa phải là yêu - mà vì lý do an toàn sức khỏe thôi."
  },
  {
    "id": 57,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Ngoài giao thương và du lịch, chúng ta cũng phải nhắc đến một yếu tố khác: biến đổi khí hậu và đô thị hóa."
  },
  {
    "id": 57,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Các chuyên gia y tế cảnh báo rằng biến đổi khí hậu làm tăng nguy cơ các dịch bệnh truyền nhiễm, không chỉ COVID-19 mà còn cả sốt xuất huyết, sởi, và gần đây là mpox (đậu mùa khỉ)."
  },
  {
    "id": 57,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Với việc các thành phố ngày càng đông đúc, virus có điều kiện lây lan nhanh hơn."
  },
  {
    "id": 58,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi không nghĩ nhiều người nhận thức được mối liên hệ giữa biến đổi khí hậu và dịch bệnh."
  },
  {
    "id": 58,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nhưng nhìn lại, từ COVID-19, mpox đến cúm gia cầm, tất cả đều có phần liên quan đến sự xâm lấn của con người vào môi trường tự nhiên và biến đổi khí hậu."
  },
  {
    "id": 59,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Chây nói đúng đấy."
  },
  {
    "id": 59,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Thực tế, một trong những công ty của tôi đang hoạt động trong lĩnh vực năng lượng xanh."
  },
  {
    "id": 59,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi tin rằng kinh doanh có trách nhiệm không chỉ là làm ra tiền mà còn phải đóng góp vào việc bảo vệ môi trường."
  },
  {
    "id": 59,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Đó là cách chúng ta giảm nguy cơ dịch bệnh trong tương lai."
  },
  {
    "id": 60,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là một góc nhìn rất tích cực, Vi Rút."
  },
  {
    "id": 60,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và nói về tương lai, có một điều đáng lo ngại nữa là tâm lý chủ quan của người dân, đặc biệt là giới trẻ."
  },
  {
    "id": 60,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Sau nhiều năm đối phó với COVID-19, nhiều người đã mệt mỏi với các biện pháp phòng dịch và có xu hướng bỏ qua các khuyến cáo y tế."
  },
  {
    "id": 61,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thấy điều đó rõ ràng trong cộng đồng người trẻ."
  },
  {
    "id": 61,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Ở các buổi biểu diễn của tôi trước đây, chúng tôi yêu cầu khán giả đeo khẩu trang."
  },
  {
    "id": 61,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nhưng giờ, hầu như không ai làm vậy nữa."
  },
  {
    "id": 61,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi nghĩ chúng ta cần nhắc nhở giới trẻ rằng COVID-19 vẫn còn đó, và các biện pháp phòng ngừa vẫn cần thiết."
  },
  {
    "id": 62,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Với tư cách là một người nổi tiếng, tôi cũng cảm thấy mình có trách nhiệm nhắc nhở fan hâm mộ."
  },
  {
    "id": 62,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi đang cân nhắc việc phát khẩu trang miễn phí tại các show diễn sắp tới, và khuyến khích mọi người sử dụng."
  },
  {
    "id": 62,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Có thể sẽ in logo của tôi lên đó cho ngầu."
  },
  {
    "id": 63,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là ý tưởng rất hay, Vi Rút."
  },
  {
    "id": 63,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nghệ sĩ nổi tiếng như các bạn có sức ảnh hưởng lớn đến công chúng, đặc biệt là giới trẻ."
  },
  {
    "id": 63,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nếu họ thấy thần tượng của mình coi trọng việc phòng dịch, có thể họ cũng sẽ làm theo."
  },
  {
    "id": 64,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng vậy."
  },
  {
    "id": 64,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi sẽ cố gắng làm gương bằng cách đeo khẩu trang khi đi ra ngoài, và chia sẻ về điều này trên mạng xã hội."
  },
  {
    "id": 64,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi đã trải qua cảm giác bị COVID tấn công rồi, không muốn ai phải trải qua điều đó."
  },
  {
    "id": 65,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhìn lại quá khứ để rút kinh nghiệm cho tương lai, chúng ta có thể thấy rằng sự chủ quan từng dẫn đến hậu quả nghiêm trọng."
  },
  {
    "id": 65,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đầu năm 2020, nhiều người nghĩ COVID-19 chỉ là  cúm thường , và chúng ta đã phải trả giá đắt cho sự chủ quan đó."
  },
  {
    "id": 65,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Giờ đây, dù tình hình có vẻ khả quan hơn với sự xuất hiện của vắc-xin và thuốc điều trị, nhưng vẫn không nên lơ là."
  },
  {
    "id": 66,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi hoàn toàn đồng ý."
  },
  {
    "id": 66,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Với kinh nghiệm kinh doanh của mình, tôi luôn nói rằng  chuẩn bị cho điều tồi tệ nhất, hy vọng điều tốt đẹp nhất ."
  },
  {
    "id": 66,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Chúng ta không thể đoán trước được virus sẽ tiến hóa như thế nào, nên tốt nhất là luôn chuẩn bị."
  },
  {
    "id": 67,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nếu có điều gì tôi học được từ sự nghiệp của mình, đó là mọi thứ có thể thay đổi rất nhanh."
  },
  {
    "id": 67,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Một ngày bạn đang ở đỉnh cao, ngày sau bạn có thể mất tất cả."
  },
  {
    "id": 67,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tương tự với dịch bệnh, chúng ta không nên chủ quan chỉ vì hiện tại mọi thứ đang ổn."
  },
  {
    "id": 68,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Rất đúng."
  },
  {
    "id": 68,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "tôi muốn nhấn mạnh rằng: bài học lớn nhất từ đại dịch COVID-19 là sự chuẩn bị, cảnh giác và hành động sớm."
  },
  {
    "id": 68,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Các nguy cơ trong tương lai là có thật - từ giao thương tăng cao, biến đổi khí hậu đến tâm lý chủ quan - nhưng nếu chúng ta cùng nhau hành động, áp dụng những bài học đã học được, thì chúng ta hoàn toàn có thể vượt qua."
  },
  {
    "id": 68,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Sau khi đã tìm hiểu về tình hình COVID-19 trên thế giới và ở Việt Nam, giờ là lúc nói về điều mà tôi tin rằng tất cả chúng ta đều quan tâm nhất: làm thế nào để bảo vệ bản thân và những người xung quanh?"
  },
  {
    "id": 68,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chỉ cần vài bước đơn giản, chúng ta có thể bảo vệ chính mình và gia đình."
  },
  {
    "id": 69,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Đúng vậy, Alex."
  },
  {
    "id": 69,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Mặc dù mang tên  Vi Rút  nhưng tôi không muốn bị lây nhiễm COVID đâu!"
  },
  {
    "id": 69,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi vẫn đi hát, sáng tác, nhưng giờ luôn mang khẩu trang và nước rửa tay."
  },
  {
    "id": 69,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Vẫn sống vui, nhưng phải an toàn!"
  },
  {
    "id": 70,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi hoàn toàn đồng ý."
  },
  {
    "id": 70,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Các bạn trẻ ơi, đừng để COVID làm gián đoạn giấc mơ như tôi từng bị."
  },
  {
    "id": 70,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Chỉ cần đeo khẩu trang, rửa tay, là đã giúp chính mình rồi!"
  },
  {
    "id": 71,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng vậy."
  },
  {
    "id": 71,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hãy bắt đầu với những điều cơ bản nhất."
  },
  {
    "id": 71,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Thực hiện  2K  - đeo khẩu trang và khử khuẩn tay - vẫn là biện pháp hiệu quả nhất, đặc biệt ở những nơi đông người như trung tâm thương mại, rạp chiếu phim, concert, hay khi sử dụng phương tiện công cộng."
  },
  {
    "id": 71,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Khẩu trang không chỉ giúp chúng ta phòng COVID mà còn phòng được nhiều bệnh hô hấp khác nữa."
  },
  {
    "id": 72,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi thấy đeo khẩu trang hơi khó chịu khi biểu diễn, nhưng tôi đã thích nghi bằng cách chỉ bỏ ra khi lên sân khấu thôi."
  },
  {
    "id": 72,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Còn ở hậu trường hay khi gặp fan, tôi luôn đeo."
  },
  {
    "id": 72,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Mà này, tôi có một thắc mắc: loại khẩu trang nào là tốt nhất vậy Alex?"
  },
  {
    "id": 73,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Câu hỏi hay đấy."
  },
  {
    "id": 73,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Khẩu trang y tế thông thường hoặc khẩu trang N95 đều hiệu quả."
  },
  {
    "id": 73,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "N95 lọc được tốt hơn, nhưng đeo lâu có thể khó chịu."
  },
  {
    "id": 73,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Quan trọng là đeo đúng cách, che kín mũi và miệng, và thay mới khi bị ẩm hoặc bẩn."
  },
  {
    "id": 74,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Còn về việc rửa tay thì sao?"
  },
  {
    "id": 74,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thấy nhiều người chỉ rửa qua loa trong 5 giây là xong."
  },
  {
    "id": 75,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Rửa tay đúng cách phải mất ít nhất 20 giây với xà phòng, chà kỹ các kẽ ngón tay, mu bàn tay, và cổ tay."
  },
  {
    "id": 75,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nếu không có xà phòng và nước, dung dịch rửa tay chứa ít nhất 60% cồn là lựa chọn thay thế tốt."
  },
  {
    "id": 75,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Ngoài ra, việc tránh đưa tay lên mắt, mũi, miệng khi chưa rửa tay cũng rất quan trọng."
  },
  {
    "id": 76,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Khẩu trang, rửa tay, còn gì nữa không?"
  },
  {
    "id": 76,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi đang có kế hoạch tổ chức một buổi biểu diễn nhỏ tại quán café tuần tới, nên muốn đảm bảo an toàn cho mọi người."
  },
  {
    "id": 77,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Còn nhiều điều khác nữa, Vi Rút ạ."
  },
  {
    "id": 77,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tăng cường dinh dưỡng, tập thể dục đều đặn, và giữ ấm cơ thể là những cách hiệu quả để nâng cao sức đề kháng."
  },
  {
    "id": 77,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chế độ ăn giàu vitamin C, D, kẽm và protein sẽ giúp hệ miễn dịch hoạt động tốt hơn."
  },
  {
    "id": 77,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Ví dụ như cam, chanh, ớt chuông, các loại rau xanh đậm, cá và các loại hạt."
  },
  {
    "id": 78,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi đặc biệt chú ý đến dinh dưỡng sau khi bị COVID."
  },
  {
    "id": 78,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Mỗi sáng tôi đều uống một ly nước chanh mật ong ấm và tập thể dục 30 phút."
  },
  {
    "id": 78,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Cảm thấy sức đề kháng tốt hơn hẳn."
  },
  {
    "id": 79,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tập thể dục à?"
  },
  {
    "id": 79,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi thường nhảy múa khi biểu diễn, như vậy có tính là tập thể dục không?"
  },
  {
    "id": 80,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tất nhiên rồi!"
  },
  {
    "id": 80,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Bất kỳ hoạt động nào khiến cơ thể vận động và tăng nhịp tim đều có lợi."
  },
  {
    "id": 80,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhảy múa là một bài tập tuyệt vời đấy, Vi Rút ạ."
  },
  {
    "id": 81,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Mình thấy điều quan trọng nhất mà nhiều người trẻ bỏ qua là: đi khám ngay khi có triệu chứng!"
  },
  {
    "id": 81,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đừng nghĩ  chắc cảm thường thôi  rồi tự mua thuốc uống."
  },
  {
    "id": 81,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Khi tôi bị, ban đầu cũng nghĩ thế, nhưng đến ngày thứ ba thì tình trạng trở nên tệ hơn nhiều."
  },
  {
    "id": 82,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng vậy, Chây."
  },
  {
    "id": 82,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đi khám ngay khi có triệu chứng sốt, ho, khó thở là vô cùng quan trọng, đặc biệt với nhóm nguy cơ cao như người già, người có bệnh nền, phụ nữ mang thai."
  },
  {
    "id": 82,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Việc này không chỉ giúp bạn được điều trị kịp thời mà còn giúp ngăn chặn sự lây lan trong cộng đồng."
  },
  {
    "id": 83,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nhắc đến cộng đồng, tôi thấy có nhiều thông tin trái chiều về COVID trên mạng xã hội."
  },
  {
    "id": 83,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Điều này khiến nhiều người hoang mang, không biết tin vào đâu."
  },
  {
    "id": 84,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là một vấn đề lớn."
  },
  {
    "id": 84,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chúng ta cần tăng cường truyền thông chính xác và tránh lan truyền thông tin sai lệch về COVID-19."
  },
  {
    "id": 84,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chỉ tin vào các nguồn thông tin chính thống như Bộ Y tế, Tổ chức Y tế Thế giới, hoặc các cơ quan y tế địa phương."
  },
  {
    "id": 84,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đừng chia sẻ thông tin nếu chưa kiểm chứng nguồn gốc."
  },
  {
    "id": 85,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đặc biệt là các phương pháp phòng ngừa và điều trị  thần kỳ  lan truyền trên mạng."
  },
  {
    "id": 85,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi từng thấy người ta khuyên uống nước tỏi, hoặc xông hơi để tiêu diệt virus."
  },
  {
    "id": 85,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Những điều này không chỉ không hiệu quả mà còn có thể gây hại."
  },
  {
    "id": 86,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi cũng muốn nhắc đến việc hẹn hò trong thời điểm này."
  },
  {
    "id": 86,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Mặc dù tôi vẫn hẹn hò nhiều người, nhưng giờ tôi luôn hỏi về tình trạng sức khỏe của họ trước khi gặp mặt."
  },
  {
    "id": 86,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nếu ai đó có triệu chứng, tôi sẽ đề nghị hoãn lại."
  },
  {
    "id": 86,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Trách nhiệm với cộng đồng mà, đúng không?"
  },
  {
    "id": 87,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hoàn toàn đúng, Vi Rút."
  },
  {
    "id": 87,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là cách chúng ta bảo vệ không chỉ bản thân mà còn cả những người xung quanh."
  },
  {
    "id": 87,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nói đến trách nhiệm cộng đồng, chúng ta cũng nên nhắc đến việc hỗ trợ nhóm nguy cơ cao như người già, người có bệnh nền."
  },
  {
    "id": 87,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Có thể bằng cách nhắc nhở họ tuân thủ phòng ngừa, giúp họ mua sắm để hạn chế ra ngoài, hoặc hướng dẫn họ cách bảo vệ bản thân."
  },
  {
    "id": 88,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi có một cách hay là gọi điện thường xuyên cho ông bà."
  },
  {
    "id": 88,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Không chỉ để nhắc nhở về phòng bệnh mà còn giúp họ cảm thấy được quan tâm, giảm cảm giác cô đơn, lo lắng trong mùa dịch."
  },
  {
    "id": 89,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Đó là ý tưởng tuyệt vời, Chây."
  },
  {
    "id": 89,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi cũng sẽ gọi cho bố mẹ tối nay."
  },
  {
    "id": 89,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Mà này, nói đến người thân, nếu có người trong gia đình bị nhiễm thì chúng ta nên làm gì?"
  },
  {
    "id": 90,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Câu hỏi rất hay."
  },
  {
    "id": 90,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nếu có người trong gia đình nhiễm COVID, cần cách ly người bệnh trong một phòng riêng nếu có thể."
  },
  {
    "id": 90,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Người chăm sóc nên đeo khẩu trang, rửa tay thường xuyên, và hạn chế tiếp xúc gần."
  },
  {
    "id": 90,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Khử khuẩn các bề mặt thường xuyên tiếp xúc như tay nắm cửa, công tắc đèn, điện thoại."
  },
  {
    "id": 90,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và quan trọng nhất, theo dõi sát tình trạng sức khỏe của người bệnh, đặc biệt là các dấu hiệu như khó thở, đau ngực, để đưa đi cấp cứu kịp thời nếu cần."
  },
  {
    "id": 91,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi muốn nhắn nhủ với các bạn trẻ rằng: đừng nghĩ COVID chỉ ảnh hưởng nặng đến người già."
  },
  {
    "id": 91,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi mới ngoài 20 tuổi, khỏe mạnh, nhưng khi bị cũng rất mệt."
  },
  {
    "id": 91,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và còn có nguy cơ hậu COVID nữa, như mệt mỏi kéo dài, khó tập trung, thậm chí là mất khứu giác hoặc vị giác."
  },
  {
    "id": 92,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Đúng thế!"
  },
  {
    "id": 92,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi có một người bạn ca sĩ bị mất khứu giác sau khi mắc COVID, phải mất gần 6 tháng mới hồi phục."
  },
  {
    "id": 92,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tưởng tượng xem, không thể ngửi được mùi hương của hoa, của thức ăn, thật là tệ phải không?"
  },
  {
    "id": 93,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là lý do chúng ta không nên chủ quan."
  },
  {
    "id": 93,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "COVID-19 có thể không còn gây tử vong nhiều như trước, nhưng tác động của nó đến chất lượng cuộc sống là không thể xem nhẹ."
  },
  {
    "id": 93,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và để kết thúc chương này, tôi muốn nhấn mạnh: chỉ cần những biện pháp đơn giản như đeo khẩu trang, rửa tay, tăng cường dinh dưỡng, và đi khám kịp thời khi có triệu chứng, chúng ta đã có thể bảo vệ bản thân và cộng đồng rất hiệu quả."
  },
  {
    "id": 94,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi hoàn toàn ủng hộ!"
  },
  {
    "id": 94,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi sẽ nhắc nhở fan của mình về những điều này trong buổi biểu diễn sắp tới."
  },
  {
    "id": 94,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "An toàn trên hết!"
  },
  {
    "id": 95,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và hãy nhớ rằng, đây không phải là lúc để hoảng sợ, mà là lúc để cẩn trọng và có trách nhiệm."
  },
  {
    "id": 95,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Chúng ta đã trải qua đại dịch một lần, và chúng ta đã học được cách sống chung với virus này."
  },
  {
    "id": 96,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cảm ơn Vi Rút và Chây vì những chia sẻ quý báu."
  },
  {
    "id": 96,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và cảm ơn tất cả các bạn đã lắng nghe podcast của chúng tôi hôm nay."
  },
  {
    "id": 96,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hãy luôn giữ gìn sức khỏe, bảo vệ bản thân và cộng đồng."
  },
  {
    "id": 96,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "COVID-19 có thể đang trở lại, nhưng với sự chuẩn bị kỹ lưỡng, chúng ta hoàn toàn có thể vượt qua nó một cách an toàn."
  },
  {
    "id": 96,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chúng ta đã cùng nhau đi qua một hành trình khá dài về COVID-19 trong podcast này."
  },
  {
    "id": 96,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hôm nay, chúng ta đã cùng nhau nhìn lại bức tranh COVID-19 trên thế giới và tại Việt Nam, từ những con số đáng lo ở Thái Lan, Anh, đến sự kiểm soát tốt ở quê nhà."
  },
  {
    "id": 96,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chúng ta cũng học được rằng, dù COVID-19 không còn đáng sợ như trước, nhưng sự chủ quan có thể khiến mọi thứ tồi tệ hơn."
  },
  {
    "id": 96,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hãy nhớ: đeo khẩu trang, rửa tay, và đi khám sớm nếu có triệu chứng."
  },
  {
    "id": 96,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Vi Rút, cậu có thêm điều gì muốn chia sẻ với khán giả không?"
  },
  {
    "id": 97,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "COVID có thể giống như một vị khách không mời mà đến, nhưng chúng ta hoàn toàn có thể kiểm soát nó."
  },
  {
    "id": 97,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi vẫn sẽ sáng tác, hát vang, và hẹn hò – nhưng với khẩu trang và nước rửa tay bên cạnh!"
  },
  {
    "id": 97,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Đây là điều tôi luôn nói với các  người thương  của mình: sự chuẩn bị là chìa khóa của thành công."
  },
  {
    "id": 97,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Dù là trong âm nhạc, kinh doanh, hay tình yêu, và giờ là cả đối phó với COVID nữa."
  },
  {
    "id": 98,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cảm ơn Vi Rút về những chia sẻ rất thực tế."
  },
  {
    "id": 98,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Còn Chây, sau tất cả những gì cậu đã trải qua, cậu có lời khuyên gì cho khán giả của chúng ta không?"
  },
  {
    "id": 99,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi đã vượt qua COVID và cả những sóng gió trong sự nghiệp."
  },
  {
    "id": 99,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Các bạn trẻ, người lớn tuổi, hay bất kỳ ai từng đối mặt với COVID, hãy tin rằng chỉ cần cẩn thận, chúng ta sẽ giữ được sức khỏe và ước mơ."
  },
  {
    "id": 99,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi nhớ khi bị COVID, tôi đã nghĩ mọi thứ sẽ chẳng bao giờ như trước nữa."
  },
  {
    "id": 99,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nhưng giờ đây, tôi đã trở lại, có thể không giống như trước, nhưng tôi mạnh mẽ hơn."
  },
  {
    "id": 99,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và đó cũng là cách chúng ta nên nhìn nhận về COVID - nó vẫn ở đây, nhưng chúng ta đã mạnh mẽ hơn trong cách đối phó với nó."
  },
  {
    "id": 100,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Chây nói đúng đấy."
  },
  {
    "id": 100,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Mọi thử thách đều là cơ hội để chúng ta trưởng thành."
  },
  {
    "id": 100,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Giống như trong âm nhạc, đôi khi một nốt trầm lại tạo nên sự thăng hoa cho cả bản nhạc."
  },
  {
    "id": 100,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "COVID là một  nốt trầm  không ai mong muốn, nhưng nó đã dạy chúng ta rất nhiều về sức khỏe, về sự đoàn kết và về khả năng thích nghi."
  },
  {
    "id": 101,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tôi rất thích cách Vi Rút ví von COVID là một  nốt trầm ."
  },
  {
    "id": 101,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và tôi cũng đồng ý với cả hai bạn rằng, dù khó khăn đến đâu, chúng ta luôn có thể vượt qua nếu cùng nhau đoàn kết và hành động đúng đắn."
  },
  {
    "id": 102,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Mà này Alex, tôi nghĩ có một điều chúng ta chưa nói đến."
  },
  {
    "id": 102,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đó là sức mạnh của thông tin chính xác."
  },
  {
    "id": 102,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Trong thời đại mạng xã hội bùng nổ như hiện nay, có rất nhiều thông tin sai lệch về COVID."
  },
  {
    "id": 102,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi nghĩ khán giả nên tìm kiếm thông tin từ các nguồn đáng tin cậy như Bộ Y tế hay Tổ chức Y tế Thế giới."
  },
  {
    "id": 103,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Đúng vậy!"
  },
  {
    "id": 103,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi cũng từng bị  nhiễm  thông tin sai lệch và suýt không tiêm vắc-xin vì nghe một số tin đồn."
  },
  {
    "id": 103,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "May mắn là tôi đã tìm hiểu kỹ và nhận ra đó là quyết định đúng đắn."
  },
  {
    "id": 103,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nếu có điều gì tôi học được từ việc hẹn hò nhiều người, đó là luôn phải kiểm chứng thông tin trước khi tin tưởng."
  },
  {
    "id": 104,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hai bạn nói rất đúng."
  },
  {
    "id": 104,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Thông tin chính xác là vũ khí mạnh mẽ nhất trong cuộc chiến với COVID-19."
  },
  {
    "id": 104,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và đó cũng là lý do chúng tôi thực hiện podcast này - để mang đến những thông tin đáng tin cậy, dễ hiểu và gần gũi với tất cả mọi người."
  },
  {
    "id": 105,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thấy biết ơn vì được tham gia podcast này, Alex."
  },
  {
    "id": 105,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đây là cơ hội để tôi chia sẻ trải nghiệm của mình và hy vọng nó có thể giúp ích cho ai đó."
  },
  {
    "id": 106,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Tôi cũng vậy."
  },
  {
    "id": 106,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Dù tên tôi là Vi Rút nhưng tôi ghét COVID lắm đấy."
  },
  {
    "id": 106,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nếu podcast này giúp được một người thực hiện các biện pháp phòng ngừa, thì đó đã là một thành công lớn rồi."
  },
  {
    "id": 107,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cảm ơn Vi Rút và Chây 97 đã mang đến những góc nhìn thú vị."
  },
  {
    "id": 107,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Các bạn khán giả, hãy chia sẻ podcast này với bạn bè, gia đình, và cùng thực hiện những biện pháp đơn giản để bảo vệ cộng đồng."
  },
  {
    "id": 107,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "COVID-19 có thể quay lại, nhưng chúng ta đã sẵn sàng!"
  },
  {
    "id": 107,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Hẹn gặp lại ở tập sau!"
  },
  {
    "id": 108,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Chào tạm biệt các bạn!"
  },
  {
    "id": 108,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Nhớ mang theo  2K  - Khẩu trang và Khử khuẩn - bên mình nhé!"
  },
  {
    "id": 108,
    "speaker": "Vi Rút",
    "voice": "leminh",
    "text": "Giống như tôi luôn mang theo nhạc cụ vậy, không bao giờ biết khi nào mình sẽ sáng tác được một giai điệu mới."
  },
  {
    "id": 109,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tạm biệt mọi người!"
  },
  {
    "id": 109,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Hãy luôn khỏe mạnh và sẵn sàng đón nhận những điều tốt đẹp phía trước."
  },
  {
    "id": 109,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "COVID có thể quay lại, nhưng không có nghĩa là nó sẽ đánh bại được chúng ta!"
  }
]

# tts_url = "https://api.fpt.ai/hmi/tts/v5"
#
# api_key = "62gfNAl7kLqytB0P4G56jdcdal29Oj91"
#
# headers_template = {
#     "api-key": api_key,
#     "speed": "1.0",
#     "voice": ""
# }
#
# def generate_tts_audio(text, voice, segment_number):
#     # Update headers with the specified voice
#     headers = headers_template.copy()
#     headers["voice"] = voice
#
#     # Prepare payload
#     payload = text.encode("utf-8")
#
#     try:
#         # Send POST request to FPT TTS API
#         response = requests.post(tts_url, data=payload, headers=headers)
#         if response.status_code != 200:
#             print(f"Error in TTS API request for segment {segment_number}: Status code {response.status_code}")
#             return False
#
#         # Parse response
#         json_response = json.loads(response.text)
#         audio_url = json_response.get("async")
#
#         # Download the audio file
#         file_name = fr"D:\podcast_voice\segment_{segment_number}.mp3"
#         print(audio_url)
#
#         response = requests.get(audio_url)
#
#         if response.status_code == 200:
#             with open(file_name, "wb") as file:
#                 file.write(response.content)
#             print(f"File saved as {file_name}")
#             return True, audio_url
#         else:
#             print(f"Error downloading audio for segment {segment_number}: Status code {response.status_code}")
#             return False, audio_url
#
#     except Exception as e:
#         print(f"Exception occurred for segment {segment_number}: {str(e)}")
#         return False, audio_url
#
# def main():
#     # Process each dialogue segment
#     df_link = pd.DataFrame(columns=['url'])
#     for index, segment in enumerate(dialogue, start=1):
#         print(f"Processing segment {index} for {segment['speaker']}...")
#         success, audio_url = generate_tts_audio(segment["text"], segment["voice"], index)
#         new_row = pd.DataFrame({
#             'url': [audio_url]
#         })
#         print(segment["text"])
#         df_link = pd.concat([df_link, new_row], ignore_index=True)
#
#         df_link.to_csv(fr"C:\Users\Nam\Desktop\url.csv", encoding='utf-8-sig')
#         print(df_link)
#         if not success:
#             print(f"Failed to generate audio for segment {index}")
#         # Add a small delay to avoid overwhelming the API
#         time.sleep(1)
#
# if __name__ == "__main__":
#     main()


# import pandas as pd
# import requests
# import os
# from urllib.parse import urlparse
#
# # Define the target directory
# output_dir = r"D:\podcast_voice"
#
# # Ensure the output directory exists
# os.makedirs(output_dir, exist_ok=True)
#
# # Read the CSV file
# df_link = pd.read_csv(r"C:\Users\Nam\Desktop\url.csv")
#
# # Iterate over the URIs and download files
# for index, row_tuple in enumerate(df_link.itertuples(index=True, name='url'), start=1):
#     uri = row_tuple.url
#     print(f"Processing URI: {uri}")
#
#     try:
#         # Send HTTP GET request to download the file
#         response = requests.get(uri, stream=True)
#
#         # Check if the request was successful
#         if response.status_code == 200:
#             # Try to infer file extension from Content-Type
#             content_type = response.headers.get('Content-Type', '')
#             extension = '.mp3'  # Default extension for podcast audio
#             if 'audio/mpeg' in content_type:
#                 extension = '.mp3'
#             elif 'audio/wav' in content_type:
#                 extension = '.wav'
#             elif 'audio/ogg' in content_type:
#                 extension = '.ogg'
#
#             # Construct output file path
#             file_name = f"segment_{index}{extension}"
#             output_path = os.path.join(output_dir, file_name)
#
#             # Save the file
#             with open(output_path, 'wb') as f:
#                 for chunk in response.iter_content(chunk_size=8192):
#                     if chunk:
#                         f.write(chunk)
#             print(f"Successfully downloaded {file_name} to {output_path}")
#         else:
#             print(f"Failed to download {uri}. Status code: {response.status_code}")
#
#     except requests.exceptions.RequestException as e:
#         print(f"Error downloading {uri}: {str(e)}")
#     except IOError as e:
#         print(f"Error saving file for {uri}: {str(e)}")
#     except Exception as e:
#         print(f"Unexpected error for {uri}: {str(e)}")
#
# print("Download process completed.")


import os


def check_missing_segments(folder_path):
    # Lấy danh sách tất cả các file trong thư mục
    files = os.listdir(folder_path)

    # Trích xuất số từ tên file (bỏ phần "sengment_" và lấy số)
    numbers = []

    for file in files:
        if file.startswith("segment_") and file.endswith(".mp3"):
            try:
                num = int(file.replace("segment_", "").replace(".mp3", ""))
                numbers.append(num)
            except ValueError:
                continue

    # Nếu không có file hợp lệ
    if not numbers:
        print("Không tìm thấy file nào có định dạng 'sengment_<số>'")
        return

    # Tìm số nhỏ nhất và lớn nhất
    min_num = 1
    max_num = 386

    # Tạo danh sách các số bị thiếu
    missing = [i for i in range(min_num, max_num + 1) if i not in numbers]

    # In kết quả
    if missing:
        print(f"Các số bị thiếu: {', '.join(map(str, missing))}")
    else:
        print("Không có số nào bị thiếu")


# Gọi hàm với đường dẫn thư mục
folder_path = r"D:\podcast_voice"
check_missing_segments(folder_path)

















