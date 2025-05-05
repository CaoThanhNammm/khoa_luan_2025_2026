# import pandas as pd
# import requests
# import json
# import os
# import time
# from uuid import uuid4
#
dialogue  = [
  {
    "id": 1,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Xin chào tất cả các bạn đang lắng nghe chúng tôi! Đây là Alex từ podcast \"Góc nhìn đa chiều\". Hôm nay chúng ta sẽ cùng nhau đi vào một đề tài mà có lẽ không ai là không biết, không ai là không từng bị cuốn vào - đó chính là các drama trên mạng xã hội! Ôi những drama - vừa ghét mà vừa yêu, phải không các bạn?"
  },
  {
    "id": 2,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và để cùng tôi khám phá thế giới drama đầy màu sắc này, tôi có hai vị khách mời cực kỳ đặc biệt. Đầu tiên, xin được giới thiệu anh Vai Rớt - nhạc sĩ, ca sĩ, streamer đang làm mưa làm gió trên các nền tảng mạng xã hội. Anh Rớt, xin chào anh!"
  },
  {
    "id": 3,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chào Alex, chào các bạn nghe đài. Drama à? Tôi có thể nói tôi đã trải qua đủ thứ drama để viết được cả một cuốn sách đấy."
  },
  {
    "id": 4,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và vị khách mời thứ hai của chúng ta - người anh em Chây 97, ca sĩ trẻ với những bản hit làm giới trẻ điên đảo. Chây đâu rồi?"
  },
  {
    "id": 5,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Có mặt! Nghe đến drama là tôi phải có mặt ngay thôi. Kiểu như thấy mùi drama là tôi tự động xuất hiện ấy."
  },
  {
    "id": 6,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Này, Chây, tôi biết cậu có hàng tá chuyện drama để kể đây. Cậu có thể cho chúng tôi một ví dụ nhỏ không?"
  },
  {
    "id": 7,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Thật ra là mới tuần trước, tôi vừa post một cái story ăn bún đậu, vậy mà không hiểu sao có đến mấy trăm comment bảo tôi đang \"đá xéo\" một nghệ sĩ nào đó. Trong khi tôi chỉ đăng vì... tôi đang ăn bún đậu thật mà! Kiểu như bạn đăng ảnh ly cà phê thôi mà cũng bị bảo là đang \"cà khịa\" người khác vậy!"
  },
  {
    "id": 8,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đó, đó! Đấy là vấn đề của mạng xã hội hiện nay. Mọi thứ đều bị phân tích quá mức, bị soi mói từng chi tiết. Chúng ta đang sống trong một thời đại mà mỗi hành động online đều có thể bị hiểu lầm và biến thành drama."
  },
  {
    "id": 9,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và đó chính xác là điều chúng ta sẽ thảo luận hôm nay. Tại sao drama lại có sức hút ghê gớm đến vậy? Tại sao chúng ta vừa tuyên bố ghét drama, vừa không thể ngừng theo dõi drama? Liệu drama có mang lại điều gì tích cực không, hay chỉ toàn tiêu cực?"
  },
  {
    "id": 10,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Tôi nghĩ chúng ta cần nhìn nhận vấn đề này một cách nghiêm túc hơn. Drama không chỉ đơn thuần là giải trí, nó còn phản ánh nhiều vấn đề xã hội đáng quan tâm."
  },
  {
    "id": 11,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Còn tôi thì nghĩ drama cũng như gia vị vậy, thiếu một chút thì nhạt, nhưng nhiều quá thì... chết luôn! Tôi nhớ hồi trước..."
  },
  {
    "id": 12,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Khoan, Chây! Để dành câu chuyện của cậu cho phần sau nhé! Các bạn thính giả thân mến, hãy cùng chúng tôi bước vào thế giới drama đầy màu sắc trong tập podcast hôm nay nhé. Chúng ta sẽ khám phá từ những drama cá nhân cho đến những drama làm rung chuyển cả mạng xã hội Việt Nam và thế giới. Có thể nói, đây sẽ là một hành trình đầy bất ngờ và thú vị!"
  },
  {
    "id": 13,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Alô alô, chúng ta quay trở lại với podcast \"Góc nhìn đa chiều\". Trước khi đi sâu vào các drama cụ thể, tôi nghĩ chúng ta nên làm rõ một chút - drama thực sự là gì? Từ này được dùng quá nhiều, nhưng liệu mọi người có hiểu giống nhau không?"
  },
  {
    "id": 14,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Theo tôi, drama trên mạng xã hội là khi có xung đột, mâu thuẫn giữa các cá nhân, nhóm người, và điều này được phơi bày công khai, thu hút sự chú ý và bình luận của công chúng. Drama không chỉ là cãi nhau đơn thuần, mà còn liên quan đến cách nó được khuếch đại bởi nền tảng mạng xã hội."
  },
  {
    "id": 15,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng vậy! Và tôi nghĩ nó cũng có yếu tố kịch tính, giống như tên gọi \"drama\" vậy."
  },
  {
    "id": 16,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Theo kinh nghiệm của tôi, drama là khi bạn đăng một tấm ảnh bình thường, rồi bỗng nhiên có 300 bình luận với 298 bình luận không liên quan gì đến bức ảnh của bạn cả.  Và bỗng nhiên, bạn thành nhân vật chính trong một câu chuyện mà bạn còn chẳng biết mình đang diễn vai gì!"
  },
  {
    "id": 17,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " Đúng là một cách nhìn rất thực tế! Vậy chúng ta thử phân loại các kiểu drama phổ biến trên mạng xã hội nhé. Tôi nghĩ có thể chia thành ba nhóm lớn. Đầu tiên là drama giữa cá nhân với cá nhân."
  },
  {
    "id": 18,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đúng. Đây là kiểu phổ biến nhất. Hai người - có thể là bạn bè, đồng nghiệp, hay thậm chí người yêu cũ - công khai \"đấu khẩu\" trên mạng. Từ chuyện hiểu lầm nhỏ có thể leo thang thành \"chiến tranh\" công khai. Điều khiến loại drama này hấp dẫn là tính cá nhân, tính tò mò về đời tư người khác."
  },
  {
    "id": 19,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Ôi, tôi nhớ năm ngoái, có hai rapper nổi tiếng cãi nhau trên Instagram vì một câu lyrics. Ban đầu chỉ là góp ý, sau thành đá xoáy, rồi thành \"diss\" công khai. Ai cũng hóng, cứ mỗi sáng dậy là mọi người lại check xem \"hôm nay ai đăng gì mới không?\". Tôi cũng theo dõi dù biết là không nên. "
  },
  {
    "id": 20,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đó chính là sức mạnh của drama cá nhân. Nó tạo cảm giác như chúng ta đang được chứng kiến một thứ rất riêng tư, rất thật, không qua biên tập hay PR. Và con người vốn tò mò về đời tư của người khác, đặc biệt là người nổi tiếng."
  },
  {
    "id": 21,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Kiểu drama thứ hai tôi nghĩ đến là drama tập thể, như giữa các nhóm KOL hay trong showbiz?"
  },
  {
    "id": 22,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chính xác. Và loại này thường mang tính \"phe phái\" cao. Người theo dõi không chỉ xem mà còn chọn đứng về một phía. Thường sẽ có hashtag, có thành viên từ mỗi bên lên tiếng. Kiểu drama này có sức lan tỏa lớn vì liên quan đến nhiều người, nhiều lĩnh vực."
  },
  {
    "id": 23,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi còn nhớ vụ drama giữa hai \"team\" influence cách đây vài năm. Nó bắt đầu từ một buổi sự kiện, một bên không được mời, và boom! Cả mạng xã hội như nổ tung. Rồi fans của mỗi bên bắt đầu \"cà khịa\" nhau, lục lại chuyện cũ từ ba đời nhà tổ... Tôi ngồi đọc mà như xem phim dài tập ấy!"
  },
  {
    "id": 24,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và thường những drama kiểu này sẽ kéo dài hơn, phải không?"
  },
  {
    "id": 25,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đúng vậy, Alex. Bởi vì có nhiều người tham gia, mỗi người lại có quan điểm và thông tin riêng. Một drama tập thể có thể kéo dài hàng tuần, thậm chí hàng tháng, với những \"plot twist\" bất ngờ khi người mới nhảy vào hoặc có thông tin mới được tiết lộ."
  },
  {
    "id": 26,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và loại thứ ba là gì nhỉ? À, drama lan truyền \"viral\"!"
  },
  {
    "id": 27,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Cái này là kiểu như thử thách \"Cinnamon Challenge\" ngày xưa, đúng không? Hay gần đây hơn là \"Silhouette Challenge\"? Những thứ bỗng dưng nổi lên, ai cũng làm theo, rồi sau đó lại có drama về việc nó nguy hiểm hay không phù hợp."
  },
  {
    "id": 28,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Nhưng tôi nghĩ cần phân biệt giữa xu hướng và drama viral. Drama viral thường liên quan đến thông tin sai lệch hoặc gây tranh cãi lan truyền nhanh chóng. Ví dụ như tin đồn về một nghệ sĩ, hoặc một clip được cắt ghép thiếu context. Loại drama này đặc biệt nguy hiểm vì tốc độ lan truyền của nó quá nhanh, trong khi việc đính chính thường chậm hơn và ít người đọc hơn."
  },
  {
    "id": 29,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tại sao mỗi loại drama lại thu hút người xem theo những cách khác nhau nhỉ?"
  },
  {
    "id": 30,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đó là cả một vấn đề tâm lý phức tạp. Drama cá nhân thu hút vì tính voyeuristic - người ta thích \"nhìn lén\" vào đời tư người khác. Drama tập thể hấp dẫn vì cho chúng ta cơ hội \"chọn phe\" và cảm giác thuộc về một cộng đồng. Còn drama viral thu hút vì tạo cảm giác khẩn cấp và FOMO - sợ bỏ lỡ."
  },
  {
    "id": 31,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "FOMO là gì vậy, anh Rớt?"
  },
  {
    "id": 32,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Fear Of Missing Out - nỗi sợ bỏ lỡ. Đây là hiện tượng tâm lý khi người ta lo sợ mình sẽ không biết đến những thông tin, sự kiện mà người khác đang tham gia. Trong thời đại thông tin bùng nổ như hiện nay, FOMO là một động lực rất lớn khiến người ta theo dõi drama."
  },
  {
    "id": 33,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thấy còn có yếu tố \"đánh lạc hướng\" nữa. Kiểu như... cuộc sống của bạn có thể đang rất nhàm chán, nhưng khi theo dõi drama của người khác, bạn cảm thấy đỡ buồn hơn, thậm chí còn tự an ủi \"ít ra mình còn đỡ hơn họ\". "
  },
  {
    "id": 34,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cậu nói đúng đấy, Chây! Đôi khi drama trở thành một dạng giải trí thay thế. Nhưng anh Rớt này, anh nhắc đến tâm lý đám đông, anh có thể giải thích rõ hơn không?"
  },
  {
    "id": 35,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Tâm lý đám đông là khi một nhóm người cùng hành động theo cách mà có thể họ sẽ không làm nếu ở một mình. Trên mạng xã hội, điều này đặc biệt rõ ràng. Một người bình thường, lý trí có thể trở nên cực đoan, thiếu kiểm chứng khi tham gia vào một \"cuộc chiến\" online. Đó là lý do tại sao drama dễ bùng nổ và lan rộng nhanh chóng."
  },
  {
    "id": 36,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng vậy! Tôi còn nhớ vụ \"bóc phốt\" một nhà hàng năm ngoái. Ban đầu chỉ là một người phàn nàn về dịch vụ, nhưng sau đó hàng nghìn người nhảy vào \"review bombing\" mà nhiều người thậm chí chưa từng đến nhà hàng đó. Kiểu như họ cảm thấy có trách nhiệm phải \"trừng phạt\" doanh nghiệp này vậy."
  },
  {
    "id": 37,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cậu có một ví dụ cụ thể về drama mà cậu từng chứng kiến không, Chây?"
  },
  {
    "id": 38,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Ối, nhiều lắm! Nhưng có một vụ khá hài. Năm ngoái, tôi vô tình đăng một tấm ảnh selfie với caption \"Hôm nay trời đẹp quá!\". Bình thường phải không? Nhưng hôm đó lại trùng với ngày một nghệ sĩ khác vừa ra MV mới có tên là \"Trời Đẹp\". Thế là fan của họ nghĩ tôi đang cố tình \"đánh lận\" SEO, lấy traffic. "
  },
  {
    "id": 39,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Đó là điều phi lý của drama. Mọi thứ đều có thể bị diễn giải theo hướng tiêu cực nếu người ta muốn."
  },
  {
    "id": 40,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng vậy! Và buồn cười nhất là tôi phải đăng story giải thích rằng tôi thậm chí không biết MV đó tồn tại! Nhưng dù tôi có nói gì, vẫn có người không tin. Họ đã quyết định câu chuyện trong đầu họ rồi."
  },
  {
    "id": 41,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó chính là điều đáng sợ của drama trên mạng - một khi \"kịch bản\" đã hình thành trong đầu công chúng, rất khó để thay đổi."
  },
  {
    "id": 42,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Và điều này liên quan đến một khái niệm tâm lý học gọi là \"confirmation bias\" - thiên kiến xác nhận. Khi người ta đã tin vào một điều gì đó, họ sẽ chỉ chú ý đến những thông tin ủng hộ niềm tin đó và bỏ qua những thông tin trái ngược."
  },
  {
    "id": 43,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Anh nói chính xác! Vậy theo anh, tại sao drama lại dễ bùng nổ đến vậy trên mạng xã hội so với đời thực?"
  },
  {
    "id": 44,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Có nhiều yếu tố. Thứ nhất là sự vô danh. Khi bạn không phải đối mặt trực tiếp với người khác, bạn dễ nói những điều mà bình thường bạn sẽ không dám nói. Thứ hai là thiếu ngữ cảnh - văn bản không thể hiện được ngữ điệu, nên dễ bị hiểu lầm. Và thứ ba là thuật toán - các nền tảng mạng xã hội thường đẩy nội dung gây tranh cãi lên cao vì nó tạo ra nhiều tương tác."
  },
  {
    "id": 45,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi cũng nghĩ là vì tốc độ nữa. Ở đời thực, nếu hai người cãi nhau, chỉ có người xung quanh mới biết. Nhưng trên mạng, chỉ trong vài phút, hàng nghìn, thậm chí hàng triệu người có thể chứng kiến và tham gia. Drama không có thời gian để \"nguội đi\" như ngoài đời."
  },
  {
    "id": 46,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Còn về mặt tâm lý, có phải chúng ta thường ham drama của người khác hơn là của chính mình?"
  },
  {
    "id": 47,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chắc chắn rồi! Khi là người trong cuộc, drama là căng thẳng, áp lực. Nhưng khi là người ngoài cuộc, nó lại trở thành giải trí. Đó là lý do tại sao chúng ta thích xem phim drama, đọc truyện có nhiều mâu thuẫn. Nó thỏa mãn nhu cầu cảm xúc mà không phải chịu hậu quả thực tế."
  },
  {
    "id": 48,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng rồi đấy! Giống như tôi thích xem phim kinh dị nhưng chắc chắn không muốn bị ma đuổi ngoài đời thật. "
  },
  {
    "id": 49,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Vậy là chúng ta đã phân loại drama thành ba nhóm chính: drama cá nhân, drama tập thể, và drama viral. Mỗi loại đều có những đặc điểm và lý do hấp dẫn riêng. Nhưng tôi tự hỏi, liệu drama trên mạng xã hội chỉ toàn tiêu cực, hay nó cũng có mặt tích cực?"
  },
  {
    "id": 50,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Theo tôi, drama không hoàn toàn tiêu cực. Đôi khi nó là cách để những vấn đề xã hội được công chúng chú ý. Nhiều vụ lạm dụng, gian lận đã được phanh phui nhờ drama trên mạng xã hội. Vấn đề là ở cách chúng ta tham gia và phản ứng với drama."
  },
  {
    "id": 51,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi đồng ý. Drama cũng giống như lửa vậy - có thể sưởi ấm hoặc thiêu rụi, tùy vào cách sử dụng.  Tôi còn nhớ vụ drama về một nghệ sĩ nổi tiếng không trả tiền cho ekip. Ban đầu nó là drama, nhưng sau đó nó thực sự giúp cải thiện điều kiện làm việc cho nhiều người trong ngành."
  },
  {
    "id": 52,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng vậy! Và tôi nghĩ đây là điểm chuyển hoàn hảo để chúng ta bước vào phần tiếp theo - những tác động của drama đối với cá nhân và xã hội. Nhưng trước khi sang phần đó, tôi muốn hỏi nhanh - anh Rớt, từng là người trong cuộc của nhiều drama, anh có lời khuyên nào cho những ai đang bị cuốn vào drama không?"
  },
  {
    "id": 53,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Hãy luôn nhớ rằng mạng xã hội chỉ là một phần của cuộc sống, không phải toàn bộ. Trước khi phản ứng, hãy dừng lại và tự hỏi: \"Điều này có quan trọng đến mức tôi phải hy sinh sự bình yên của mình không?\" Và đôi khi, câu trả lời đơn giản nhất là tắt điện thoại đi."
  },
  {
    "id": 54,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Còn Chây thì sao?"
  },
  {
    "id": 55,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thì cho rằng... luôn giữ được sự hài hước! Đừng bao giờ nghiêm trọng hóa mọi thứ. Nhiều khi tôi chỉ đăng một cái emoji cười, và boom - drama kết thúc vì người ta không biết phản ứng thế nào! "
  },
  {
    "id": 56,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " Hai cách tiếp cận rất khác nhau nhưng đều hiệu quả theo cách riêng! Cảm ơn cả hai vì những chia sẻ thú vị. Trong phần tiếp theo, chúng ta sẽ đi sâu vào những tác động của drama - cả tích cực lẫn tiêu cực - đối với cá nhân và xã hội. Các bạn đã sẵn sàng chưa?"
  },
  {
    "id": 57,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Hoàn toàn sẵn sàng!"
  },
  {
    "id": 58,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Let's go!"
  },
  {
    "id": 59,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chào mừng quý vị và các bạn quay trở lại với podcast \"Góc nhìn đa chiều\". Sau khi đã tìm hiểu về khái niệm và phân loại drama, giờ chúng ta sẽ đi sâu vào \"bản đồ drama\" trên mạng xã hội Việt Nam. Phải nói là thị trường drama Việt cực kỳ sôi động phải không các bạn?"
  },
  {
    "id": 60,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Sôi động là còn nhẹ đấy! Tôi nghĩ Việt Nam có thể xuất khẩu drama, Alex ạ.  Đặc biệt là drama showbiz, có những vụ còn kịch tính hơn cả phim Netflix!"
  },
  {
    "id": 61,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Đúng là không thiếu. Nhưng tôi nghĩ chúng ta nên tìm hiểu tại sao drama ở Việt Nam lại có những đặc điểm riêng biệt, không giống các nơi khác."
  },
  {
    "id": 62,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó chính là điều chúng ta sẽ làm! Hãy bắt đầu với drama showbiz nhé - lĩnh vực mà cả hai người đều hoạt động. Các bạn nghĩ sao về các drama ca sĩ, streamer hay những scandal tình ái?"
  },
  {
    "id": 63,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Drama showbiz Việt có đặc điểm là thường xoay quanh chuyện tình cảm hoặc \"đá xéo\" nhau về chuyên môn. Ví dụ như vụ \"bè phái\" trong các gameshow âm nhạc, hay việc \"đạo nhạc\". Thực ra, ở thị trường âm nhạc nhỏ như Việt Nam, việc va chạm là không tránh khỏi. Nhưng điều khiến nó trở thành drama là cách mà mọi người đổ dầu vào lửa."
  },
  {
    "id": 64,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi nhớ vụ \"Rap Việt\" mùa đầu tiên, khi hai team HLV đấu khẩu trên sân khấu về việc sản phẩm của thí sinh nào tốt hơn. Ban đầu chỉ là góp ý chuyên môn, nhưng sau đó fan hai bên biến nó thành cuộc chiến trên mạng xã hội, thậm chí đào bới quá khứ, soi mói đời tư."
  },
  {
    "id": 65,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng là từ chuyện chuyên môn có thể biến thành \"chiến tranh\" thật sự!"
  },
  {
    "id": 66,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Và đó là điều tôi quan ngại. Drama showbiz ở Việt Nam rất thường đi kèm với việc đào bới đời tư. Khán giả thường quên mất ranh giới giữa nghệ thuật và cuộc sống cá nhân. Tôi từng chứng kiến một đồng nghiệp bị \"đào\" lại chuyện tình cảm từ 10 năm trước chỉ vì họ đang có một sản phẩm âm nhạc thành công."
  },
  {
    "id": 67,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nhưng phải công nhận, drama tình ái là \"đỉnh\" nhất. Toàn view \"khủng\"!  Tôi còn nhớ vụ \"Tuesday\" nổi tiếng năm 2020, khi một influencer bị tố là người thứ ba. Chỉ trong một ngày, cô ấy mất hàng trăm nghìn followers, nhưng hai tuần sau lại tăng gấp đôi số đó vì độ nổi tiếng từ drama!"
  },
  {
    "id": 68,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cậu nói đúng, Chây! Vụ đó thật sự gây chấn động. Nhưng anh Rớt, tại sao drama tình cảm lại thu hút người xem đến vậy?"
  },
  {
    "id": 69,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đơn giản vì nó chạm đến thứ cảm xúc nguyên thủy nhất. Tình yêu, ghen tuông, phản bội - đây là những đề tài universal mà ai cũng hiểu. Không cần biết bạn có học thức hay không, bạn đều có thể \"nhập cuộc\" dễ dàng. Ngoài ra, còn có yếu tố \"máu Candy Crush\" - tức là sự tò mò, muốn biết \"phần tiếp theo\" của câu chuyện."
  },
  {
    "id": 70,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "\"Máu Candy Crush\" là gì vậy?"
  },
  {
    "id": 71,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Đó là thuật ngữ tôi dùng để mô tả sự nghiện theo dõi tiến triển của một câu chuyện - giống như khi bạn chơi Candy Crush, luôn muốn biết màn tiếp theo sẽ như thế nào. Drama tốt giống như một series phim dài tập, luôn giữ được sự tò mò của khán giả."
  },
  {
    "id": 72,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Chính xác! Và đặc điểm của drama tình ái là luôn có \"plot twist\"! Kiểu như \"crush của tôi hóa ra là người yêu bạn thân\", hoặc \"Tuesday hóa ra lại là main chính\" - những tình tiết bất ngờ khiến người xem không thể ngừng theo dõi."
  },
  {
    "id": 73,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhưng ngoài showbiz, chúng ta còn có drama của các KOL bán hàng. Những drama này có đặc điểm gì?"
  },
  {
    "id": 74,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Drama KOL bán hàng thường xoay quanh vấn đề chất lượng sản phẩm và độ tin cậy. Điều khiến loại drama này đặc biệt là nó có tác động trực tiếp đến kinh tế - cả của KOL lẫn người tiêu dùng."
  },
  {
    "id": 75,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi còn nhớ vụ \"phốt\" mỹ phẩm làm trắng da năm ngoái. Ban đầu chỉ là một cô gái đăng story than phiền về mụn sau khi dùng, nhưng sau đó cả trăm người nhảy vào chia sẻ kinh nghiệm tương tự. KOL bán hàng đó từ 2 triệu followers \"bay\" xuống còn 500K chỉ trong một tuần!"
  },
  {
    "id": 76,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng vậy! Và sau đó còn có màn \"bóc phốt ngược\" khi KOL đó tố những người phàn nàn là \"hàng fake\", đúng không?"
  },
  {
    "id": 77,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Chính xác! Đó là điều thú vị của drama KOL - nó luôn có nhiều tầng lớp. Từ \"tố - phản tố - tố lại\" có thể kéo dài cả tháng. Và thường thì đến cuối cùng, chẳng ai biết sự thật là gì nữa. "
  },
  {
    "id": 78,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Nhưng tôi nghĩ loại drama này có một mặt tích cực: nó giúp người tiêu dùng cảnh giác hơn, thận trọng hơn với những quảng cáo phóng đại. Đồng thời, nó cũng buộc các KOL phải chân thành và minh bạch hơn."
  },
  {
    "id": 79,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nói về độ phức tạp, chúng ta không thể bỏ qua \"roleplay drama\" của các nhóm streamer/YouTuber. Đây là hiện tượng khá mới tại Việt Nam, đúng không?"
  },
  {
    "id": 80,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Ồ, cái này thú vị lắm! Là khi các streamer cố tình tạo ra drama để tăng view, tạo trend. Giống như một vở kịch vậy, nhưng khán giả không biết đó là kịch.  Tôi có quen một vài anh em làm YouTube gaming, họ cố tình \"beef\" nhau trên stream để các clip \"drama tổng hợp\" sau đó có thể đạt hàng triệu view."
  },
  {
    "id": 81,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Điều này phản ánh một thực tế mới trong nền \"kinh tế chú ý\". Khi sự chú ý của khán giả trở thành tài nguyên quý giá, drama là cách nhanh nhất để thu hút sự chú ý đó. Các streamer đã nhận ra điều này và biến nó thành chiến lược kinh doanh."
  },
  {
    "id": 82,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "\"Kinh tế chú ý\" là gì, anh Rớt?"
  },
  {
    "id": 83,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đó là khái niệm cho rằng trong thời đại thông tin bùng nổ, thứ quý giá nhất không phải là thông tin mà là sự chú ý của con người. Vì lượng thông tin quá nhiều, nhưng thời gian và sự chú ý của chúng ta lại có hạn, nên những ai thu hút được sự chú ý sẽ có lợi thế. Drama là công cụ hiệu quả để thu hút sự chú ý đó."
  },
  {
    "id": 84,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi có nghe một anh em streamer tâm sự rằng một video game bình thường chỉ được 50K view, nhưng nếu thêm drama vào title kiểu \"Tố đồng đội phản bội\" thì dễ dàng đạt 500K.  Business is business!"
  },
  {
    "id": 85,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Vậy là drama đã trở thành một công cụ marketing thực sự!"
  },
  {
    "id": 86,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Không chỉ marketing, nó còn là một hệ sinh thái kinh tế toàn diện. Từ các fanpage tổng hợp drama, các kênh YouTube chuyên \"bóc phốt\", đến các nhóm Facebook chuyên \"team qua đường\" - tất cả đều kiếm được tiền từ drama của người khác."
  },
  {
    "id": 87,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nói về các nền tảng mạng xã hội, theo các bạn, nền tảng nào \"đổ dầu vào lửa\" mạnh nhất khi nói đến drama Việt Nam?"
  },
  {
    "id": 88,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Theo kinh nghiệm của tôi là TikTok!  Drama trên TikTok lan nhanh như virus. Một video 15 giây có thể khiến một người nổi tiếng \"bay màu\" trong vài giờ. Và thuật toán TikTok còn đẩy drama đến những người thậm chí không quan tâm đến lĩnh vực đó."
  },
  {
    "id": 89,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Tôi lại nghĩ Facebook vẫn là \"ông trùm\" drama ở Việt Nam. Với cấu trúc comment đa tầng và các nhóm kín, Facebook tạo điều kiện cho drama phát triển theo chiều sâu hơn. Một drama trên Facebook có thể kéo dài hàng tuần, thậm chí hàng tháng, với những phe phái rõ rệt."
  },
  {
    "id": 90,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Còn YouTube thì sao?"
  },
  {
    "id": 91,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "YouTube là nơi drama được \"tái sản xuất\" và khai thác triệt để.  Các kênh \"Drama Queen\", \"Soi sao\", \"Tin nóng showbiz\" làm video phân tích từng chi tiết của drama, thậm chí còn thuê diễn viên tái hiện lại tình huống. Một drama kéo dài 2-3 ngày trên Facebook có thể được YouTube khai thác cả tháng!"
  },
  {
    "id": 92,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đúng vậy. Và điều đáng chú ý là mỗi nền tảng tạo ra một kiểu drama khác nhau. TikTok tạo ra drama ngắn, viral, giật gân. Facebook tạo ra drama có chiều sâu, nhiều layers. YouTube thì \"đào xới\" và kéo dài drama."
  },
  {
    "id": 93,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Vậy còn Zalo, Viber, Telegram thì sao? Những nền tảng nhắn tin riêng tư này có vai trò gì trong drama Việt Nam?"
  },
  {
    "id": 94,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "À, đây là backstage của drama!  Gần như mọi drama công khai đều bắt đầu từ những cuộc trò chuyện riêng tư bị leak. Tôi có một người bạn, chỉ vì quên đăng xuất Zalo trên máy tính công ty mà trở thành nhân vật chính của drama tình tay ba!"
  },
  {
    "id": 95,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Đúng là vậy. Trong giới nghệ sĩ, chúng tôi gọi nó là \"văn hóa chụp màn hình\". Bạn không bao giờ nói điều gì qua tin nhắn mà bạn không muốn cả thế giới biết. Vì chỉ cần một cú chụp màn hình, đó có thể là bằng chứng chống lại bạn trong drama tiếp theo."
  },
  {
    "id": 96,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Điều đó nghe thật căng thẳng! Các bạn có thể chia sẻ một vài \"bí kíp\" để tránh bị kéo vào drama không?"
  },
  {
    "id": 97,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Bí kíp số 1: Đừng nổi tiếng!  Không, nói thật thì tôi luôn có nguyên tắc là không bao giờ comment dưới bài đăng có drama. \"Thấy drama scroll đi, đừng dừng lại\"! Vì ngay cả khi bạn comment một emoji cười, người ta cũng có thể hiểu là bạn đang cười nhạo ai đó."
  },
  {
    "id": 98,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Tôi thì có cách tiếp cận khác. Tôi không tránh drama, nhưng tôi chọn drama để tham gia. Nếu đó là vấn đề tôi thực sự quan tâm và có kiến thức về nó, tôi sẽ lên tiếng. Còn nếu không, tôi giữ im lặng. Đừng bao giờ lên tiếng về điều bạn không hiểu rõ - đó là nguyên tắc tôi luôn tuân theo."
  },
  {
    "id": 99,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nhưng các bạn là người của công chúng, vậy khi bản thân trở thành trung tâm của drama, các bạn xử lý thế nào?"
  },
  {
    "id": 100,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Tôi có bí kíp riêng - \"ngủ một giấc\"! Thật đấy, khi thấy drama nổ ra về mình, tôi tắt điện thoại và đi ngủ. Sáng hôm sau, tình hình thường đã khác - hoặc drama đã lắng xuống, hoặc đã rõ ràng hơn để tôi biết phải phản ứng thế nào."
  },
  {
    "id": 101,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Còn tôi luôn nhớ rằng, drama chỉ là tạm thời, nhưng internet thì mãi mãi. Vì vậy, tôi cẩn trọng với mỗi từ ngữ khi phản hồi drama. Một câu trả lời nóng giận có thể theo bạn suốt sự nghiệp."
  },
  {
    "id": 102,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là những lời khuyên rất hữu ích! Này Chây, cậu có thể chia sẻ một trải nghiệm cá nhân về drama lớn nhất mà cậu từng trải qua không?"
  },
  {
    "id": 103,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Chắc phải kể về vụ \"tình tay năm\" năm ngoái. Một tối đẹp trời, tôi thấy tên mình trending trên Twitter với hashtag #ChâyVàBốCôNàng. Hóa ra có người đăng một bài viết dài phân tích rằng trong các bài hát gần đây của tôi, tôi đang hẹn hò với bốn cô gái cùng lúc! "
  },
  {
    "id": 104,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Trời ơi, vậy là sao?"
  },
  {
    "id": 105,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Ban đầu tôi hoảng lắm, định lên tiếng phủ nhận. Nhưng sau khi đọc kỹ bài phân tích, tôi nhận ra người ta đang phân tích... bốn nhân vật nữ trong MV của tôi!  Họ tưởng đó là người thật, còn viết cả \"điều tra\" về background các cô gái đó. Cuối cùng tôi phải lên story giải thích đó chỉ là diễn viên đóng MV thôi."
  },
  {
    "id": 106,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Đó là vấn đề của \"văn hóa soi\". Người ta quá chú trọng vào việc \"điều tra\", đến mức quên mất ranh giới giữa nghệ thuật và đời thực."
  },
  {
    "id": 107,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Vậy còn anh thì sao, anh Rớt? Drama lớn nhất với anh là gì?"
  },
  {
    "id": 108,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Có lẽ là vụ tôi bị tố \"đạo nhạc\" cách đây hai năm. Một sáng tác của tôi bị cho là giống 80% một bài hát nước ngoài. Drama lan rộng đến mức tôi phải hủy toàn bộ lịch diễn trong hai tuần."
  },
  {
    "id": 109,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Vậy sự thật là gì?"
  },
  {
    "id": 110,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Sự thật là cả hai bài đều lấy cảm hứng từ một bản nhạc dân gian. Tôi đã phải thuê chuyên gia âm nhạc phân tích, rồi làm video giải thích chi tiết quá trình sáng tác. May mắn là cộng đồng âm nhạc đã ủng hộ tôi. Nhưng đó là khoảng thời gian rất căng thẳng."
  },
  {
    "id": 111,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và anh biết không, Alex, sau vụ đó, nhiều nhạc sĩ bắt đầu quay lại toàn bộ quá trình sáng tác của họ để làm bằng chứng!  Drama thực sự đã thay đổi cách làm việc của chúng tôi."
  },
  {
    "id": 112,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là điều rất đáng suy ngẫm! Drama không chỉ ảnh hưởng đến danh tiếng mà còn cả cách làm việc của các nghệ sĩ. Nhưng ở góc độ tích cực, drama cũng có thể là động lực cho sự thay đổi, phải không?"
  },
  {
    "id": 113,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chắc chắn rồi. Sau những drama về bản quyền, ngành âm nhạc Việt Nam đã chú trọng hơn đến vấn đề sở hữu trí tuệ. Sau những drama về chất lượng sản phẩm, người tiêu dùng cũng trở nên thông thái hơn. Drama, dù tiêu cực, đôi khi lại là chất xúc tác cho những thay đổi tích cực."
  },
  {
    "id": 114,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Và tôi nghĩ, drama cũng giống như một tấm gương phản chiếu xã hội. Nó cho thấy chúng ta quan tâm đến điều gì, giá trị gì, và cả những vấn đề chúng ta đang phải đối mặt."
  },
  {
    "id": 115,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là một cách nhìn rất thú vị! Và tôi nghĩ đây là thời điểm tốt để chúng ta chuyển sang phần tiếp theo - so sánh drama Việt Nam với thế giới. Liệu drama ở Việt Nam có những nét đặc trưng riêng, hay nó cũng giống như drama ở các nước khác? Các khán giả đừng bỏ lỡ phần tiếp theo nhé!"
  },
  {
    "id": 116,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chào mừng các bạn quay trở lại với phần tiếp theo của podcast \"Góc nhìn đa chiều\"! Ở phần này, chúng ta sẽ mở rộng tầm nhìn ra toàn cầu và khám phá những drama \"bự\" trên thế giới. Hai người bạn của chúng ta vẫn đang ở đây - anh Vai Rớt và Chây 97. Chúng ta đã nói nhiều về drama trong nước, giờ hãy nhìn ra thế giới xem sao!"
  },
  {
    "id": 117,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Thế giới là một sân khấu lớn hơn nhiều, Alex ạ. Và trên sân khấu đó, drama cũng hoành tráng hơn, có sức ảnh hưởng lớn hơn, đôi khi còn thay đổi cả nền văn hóa."
  },
  {
    "id": 118,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Chưa kể tiền đô nhiều hơn, brand deals khủng hơn, followers triệu triệu!  Nhưng thật ra, tôi thấy drama là ngôn ngữ chung của nhân loại - dù là ở Việt Nam hay Hollywood, cốt lõi vẫn là người ta thích xem người khác \"lộn xộn\"."
  },
  {
    "id": 119,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " Đúng vậy! Hãy bắt đầu với một trong những nền tảng drama nổi tiếng nhất - Twitter, à xin lỗi, giờ là X nhỉ. Các bạn nghĩ sao về những scandal của người nổi tiếng trên nền tảng này?"
  },
  {
    "id": 120,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Twitter là nơi mà chỉ 280 ký tự có thể phá hủy cả sự nghiệp. Tôi nhớ vụ của Will Smith tát Chris Rock tại Oscar 2022. Chỉ trong vài giờ, toàn bộ Twitter đã chia thành hai phe rõ rệt, và điều này đã ảnh hưởng nghiêm trọng đến danh tiếng của Will Smith, khiến anh ta mất nhiều hợp đồng phim và phải rút khỏi Viện Hàn lâm."
  },
  {
    "id": 121,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Anh nhớ hashtag #SlapChris không? Nó trending cả tuần liền! Mà tôi thấy hài là ban đầu mọi người đều chỉ trích Will, sau lại chuyển sang bênh vực anh ấy vì bảo vệ vợ. Rồi lại quay ra ghét Jada.  Giống như một bộ phim nhiều tập với những plot twist không ngờ tới!"
  },
  {
    "id": 122,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng là một ví dụ điển hình! Nhưng còn nhiều vụ khác nữa. Tôi nhớ drama giữa Elon Musk và Twitter trước khi ông ta mua lại nền tảng này. Từ việc tuyên bố rút lui khỏi thương vụ, đến vụ kiện, rồi cuối cùng vẫn mua với giá 44 tỷ đô. Đó là một trong những drama doanh nghiệp lớn nhất những năm gần đây."
  },
  {
    "id": 123,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Và sau khi mua Twitter, Musk lại tạo thêm nhiều drama mới. Từ việc sa thải hàng loạt nhân viên, đến đổi tên thành X, rồi thay đổi thuật toán. Mỗi quyết định của ông ta đều tạo ra làn sóng tranh cãi khắp mạng xã hội. Đây là ví dụ điển hình về cách một cá nhân có thể tạo ra drama liên tục và sử dụng nó như một chiến lược truyền thông."
  },
  {
    "id": 124,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " \"Tôi sẽ mua Coca-Cola để cho cocaine trở lại!\"  Đó là một trong những tweet của Elon làm tôi cười đau cả bụng! Ông ấy như một drama king vậy - luôn biết cách giữ tên mình trên mặt báo. Nhưng phải công nhận, chiến lược này hiệu quả thật. Ai cũng biết đến X, dù để khen hay chê."
  },
  {
    "id": 125,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nói đến drama công nghệ, không thể không nhắc đến Reddit và những cuộc \"nổi loạn\" của người dùng. Như vụ \"Reddit Blackout\" năm 2023 khi hàng nghìn subreddit đóng cửa phản đối chính sách API mới."
  },
  {
    "id": 126,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đây là một hiện tượng rất đáng chú ý về sức mạnh của cộng đồng người dùng. Khi Reddit quyết định tính phí cho việc sử dụng API, điều này đe dọa sự tồn tại của nhiều ứng dụng bên thứ ba mà người dùng yêu thích. Kết quả là một cuộc biểu tình kỹ thuật số quy mô lớn, với hàng nghìn cộng đồng tạm thời hoặc vĩnh viễn đóng cửa."
  },
  {
    "id": 127,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi đã theo dõi vụ này! Cảm giác như xem một cuộc cách mạng online vậy.  Nhưng cuối cùng thì Reddit vẫn áp dụng chính sách mới, đúng không? Giống như mọi cuộc cách mạng, ban đầu rất hào hứng, nhưng rồi mọi thứ cũng trở lại bình thường."
  },
  {
    "id": 128,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Không hẳn là bình thường, Chây ạ. Mặc dù Reddit vẫn tiến hành thay đổi, nhưng họ đã phải nhượng bộ một số điểm. Và quan trọng hơn, sự kiện này đã thay đổi mối quan hệ giữa nền tảng và người dùng. Nó cho thấy người dùng có tiếng nói và sức mạnh nhất định, dù không phải là tuyệt đối."
  },
  {
    "id": 129,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Điều này dẫn chúng ta đến một hiện tượng lớn khác trên mạng xã hội toàn cầu - \"Cancel Culture\" hay văn hóa hủy bỏ. Các bạn nghĩ sao về hiện tượng này?"
  },
  {
    "id": 130,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Cancel culture là một hiện tượng phức tạp với những mặt tích cực và tiêu cực. Về bản chất, đó là khi công chúng từ chối ủng hộ một cá nhân hoặc tổ chức vì những hành vi, phát ngôn được cho là có hại hoặc xúc phạm. Trong một số trường hợp, nó giúp buộc những người quyền lực phải chịu trách nhiệm. Nhưng trong nhiều trường hợp khác, nó trở thành một công cụ săn phù thủy hiện đại."
  },
  {
    "id": 131,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thấy cancel culture kiểu như \"đánh hội đồng\" trên mạng ấy. Có những vụ đáng đời, như Harvey Weinstein chẳng hạn. Nhưng cũng có những vụ quá đáng, như vụ một nhà văn bị \"cancel\" vì một tweet đăng cách đây 10 năm. Tôi thấy con người có xu hướng muốn trở thành \"thẩm phán\" mà không cần tòa án."
  },
  {
    "id": 132,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Một trường hợp nổi tiếng của cancel culture là vụ James Gunn, đạo diễn của \"Guardians of the Galaxy\", bị Disney sa thải vì những tweet gây tranh cãi từ nhiều năm trước. Nhưng cuối cùng ông ấy đã được tái bổ nhiệm. Các bạn nghĩ gì về trường hợp này?"
  },
  {
    "id": 133,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đây là một ví dụ điển hình về sự phức tạp của cancel culture. Một mặt, những tweet của James Gunn thực sự có vấn đề. Mặt khác, chúng được đăng nhiều năm trước khi ông ấy làm việc cho Disney, và ông ấy đã xin lỗi trước khi bị \"đào\" lại. Việc ông ấy được tái bổ nhiệm cho thấy có thể có con đường trở lại sau khi bị \"cancel\", nếu sự hối lỗi là chân thành và hành vi không quá nghiêm trọng."
  },
  {
    "id": 134,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thích câu chuyện này vì nó có happy ending!  Tôi nghĩ cái quan trọng là phân biệt giữa việc chỉ trích hợp lý và \"witch-hunt\". Chỉ trích là nói \"Hành động này không ổn\", còn săn phù thủy là \"Người này là kẻ xấu mãi mãi, không bao giờ được tha thứ\". Ta cần nhiều chỉ trích hơn, ít săn phù thủy hơn."
  },
  {
    "id": 135,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Phân tích rất sâu sắc, Chây! Nhưng không phải mọi drama đều nghiêm trọng. Meme và reaction video đã trở thành một phần không thể thiếu của văn hóa internet và thường khuấy động drama theo cách hài hước. Các bạn nghĩ sao về hiện tượng này?"
  },
  {
    "id": 136,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Ôi, tôi SỐNG với meme luôn! Meme là ngôn ngữ của thế hệ internet. Nó giống như cách chúng ta bình luận về thế giới, nhưng hài hước và dễ lan truyền hơn. Nhớ vụ \"Woman Yelling at Cat\" không? Một bên là nhân vật trong show thực tế đang khóc, một bên là con mèo ngồi trước đĩa rau... Meme đó đã được dùng để bình luận về mọi thứ, từ chính trị đến phim ảnh!"
  },
  {
    "id": 137,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Meme và reaction video là cách mà cộng đồng mạng \"tiêu hóa\" và \"tái chế\" drama. Chúng biến những cuộc tranh cãi nghiêm túc thành nội dung giải trí, đôi khi làm giảm bớt căng thẳng, nhưng cũng có thể khiến drama kéo dài hơn và lan rộng hơn. Đây là một hiện tượng văn hóa đáng chú ý của thời đại internet."
  },
  {
    "id": 138,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Các bạn có nghĩ có sự khác biệt giữa cách mọi người phản ứng với drama ở Việt Nam và trên thế giới không?"
  },
  {
    "id": 139,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thấy khán giả quốc tế... họ \"ném đá\" chuyên nghiệp hơn!  Kiểu như họ có hashtag riêng, có chiến dịch riêng, thậm chí có cả song ca hợp xướng ấy! Còn ở Việt Nam thì mình vẫn đang trong giai đoạn \"phát triển nghề ném đá\". Nhưng mình đang học hỏi rất nhanh!"
  },
  {
    "id": 140,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Tôi nghĩ có một điểm khác biệt đáng chú ý là tính chất tập thể. Ở các nước phương Tây, drama thường tập trung vào cá nhân và hành vi của họ. Ở Việt Nam và nhiều nước châu Á, drama thường liên quan đến gia đình, cộng đồng, và truyền thống. Điều này phản ánh sự khác biệt văn hóa giữa chủ nghĩa cá nhân và chủ nghĩa tập thể."
  },
  {
    "id": 141,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chúng ta hãy nói về một drama toàn cầu lớn gần đây - vụ Johnny Depp và Amber Heard. Đây là một ví dụ điển hình về việc drama cá nhân trở thành vấn đề xã hội."
  },
  {
    "id": 142,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Vụ Depp-Heard là một trong những drama có sức ảnh hưởng lớn nhất những năm gần đây. Nó không chỉ là tranh chấp giữa hai nghệ sĩ, mà còn trở thành một cuộc tranh luận rộng lớn về bạo lực gia đình, giới tính, và độ tin cậy của phong trào #MeToo. Điều đáng chú ý là cách công chúng và truyền thông thay đổi lập trường nhiều lần trong suốt vụ việc."
  },
  {
    "id": 143,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Vụ này thiệt là \"sốc\" luôn! Tất cả các clip đều viral, mọi người đều có ý kiến. Tôi thấy nhiều người xem phiên tòa như một show truyền hình. Và TikTok thì ngập tràn những video phân tích cử chỉ, ánh mắt của cả hai. Giống như cả thế giới đột nhiên trở thành chuyên gia tâm lý và luật sư vậy!"
  },
  {
    "id": 144,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng vậy! Và điều này dẫn đến một vấn đề lớn của drama trên mạng xã hội - sự mờ nhòa giữa giải trí và những vấn đề nghiêm túc. Phiên tòa Depp-Heard lẽ ra phải là về công lý, nhưng nó đã trở thành một show truyền hình thực tế toàn cầu."
  },
  {
    "id": 145,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chính xác. Và đây là một xu hướng đáng lo ngại. Khi chúng ta biến những vấn đề nghiêm túc như bạo lực gia đình thành nội dung giải trí, chúng ta có nguy cơ làm mất đi sự nghiêm túc của vấn đề. Nhưng đồng thời, nó cũng mang những vấn đề này đến với sự chú ý của công chúng rộng rãi hơn."
  },
  {
    "id": 146,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi cũng thấy một điều thú vị là cách mà drama thay đổi sự nghiệp. Sau vụ này, Johnny Depp mất vai trong \"Fantastic Beasts\" nhưng lại được fan ủng hộ nhiệt tình hơn. Còn Amber Heard thì...  Khó khăn lắm."
  },
  {
    "id": 147,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Một ví dụ khác về drama toàn cầu là hiện tượng \"K-pop fanwars\". Cộng đồng fan K-pop nổi tiếng với sự nhiệt tình, đôi khi quá khích, và điều này tạo ra nhiều drama giữa các fandom."
  },
  {
    "id": 148,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Ôi, đừng nhắc đến K-pop fanwars! Tôi từng bị \"tấn công\" vì vô tình nói nhóm này không bằng nhóm kia. Tưởng đâu chỉ là comment bình thường, ai ngờ hôm sau mở điện thoại ra thấy hàng trăm tin nhắn chửi bới. Army, Blink, EXO-L... từng fandom như một đội quân thật sự!"
  },
  {
    "id": 149,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "K-pop fanwars là một hiện tượng thú vị về mặt xã hội học. Nó cho thấy cách mà danh tính cá nhân có thể gắn liền với sở thích văn hóa, và cách mà con người tạo ra \"bộ lạc\" trong thời đại số. Khi bạn không chỉ thích một nghệ sĩ mà còn coi họ là một phần danh tính của mình, mọi chỉ trích đối với nghệ sĩ đó sẽ được cảm nhận như một cuộc tấn công cá nhân."
  },
  {
    "id": 150,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và không thể không nhắc đến drama công nghệ - cuộc chiến giữa các gã khổng lồ như Apple, Google, Meta... Những công ty này không chỉ cạnh tranh về sản phẩm mà còn về câu chuyện, hình ảnh và drama."
  },
  {
    "id": 151,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đúng vậy. Nhớ vụ Mark Zuckerberg và Tim Cook \"đấu khẩu\" về quyền riêng tư không? Hay việc Elon Musk thách đấu Mark Zuckerberg? Đây không chỉ là những tranh chấp kinh doanh, mà còn là những drama được dàn dựng kỹ lưỡng để thu hút sự chú ý của công chúng và truyền thông."
  },
  {
    "id": 152,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Tôi vẫn nhớ khi Elon Musk đăng \"Zuck is a cuck\" trên Twitter sau khi Meta ra mắt Threads. Kiểu CEO mà đăng nội dung như vậy thì... chỉ có Elon Musk! Nhưng phải thừa nhận rằng drama kiểu này rất hiệu quả cho marketing. Người ta nói về Threads nhiều hơn hẳn so với nếu không có drama!"
  },
  {
    "id": 153,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và một trong những drama gần đây nhất trên mạng xã hội toàn cầu là sự ra đời của các công nghệ AI như ChatGPT, với những lo ngại về quyền tác giả, việc làm, và tương lai của nhân loại."
  },
  {
    "id": 154,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đây là một drama mang tính bước ngoặt. Nó không chỉ là về công nghệ, mà còn về triết học, đạo đức, và tương lai của công việc và sáng tạo. Chúng ta đang chứng kiến những cuộc tranh luận sôi nổi giữa những người ủng hộ AI như một công cụ giải phóng sức lao động, và những người lo ngại về việc AI sẽ thay thế con người và làm xói mòn tính sáng tạo."
  },
  {
    "id": 155,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thấy vụ này hơi \"sợ\" đấy! Tôi đã thử dùng AI để viết lời bài hát, và... wow, nó không tệ! Không phải là xuất sắc, nhưng đủ để làm tôi lo lắng về công việc của mình trong 5 năm tới.  Nhưng tôi vẫn hy vọng con người sẽ luôn muốn nghe nhạc do con người tạo ra. Vì âm nhạc là về cảm xúc, mà AI có cảm xúc không?"
  },
  {
    "id": 156,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là câu hỏi triệu đô! Trước khi kết thúc phần này, tôi muốn hỏi các bạn: Nếu so sánh drama ở Việt Nam và thế giới, đâu là điểm chung và khác biệt lớn nhất?"
  },
  {
    "id": 157,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Điểm chung lớn nhất là động lực cơ bản: tò mò, phán xét, và mong muốn thuộc về một nhóm. Dù ở đâu, drama cũng đáp ứng những nhu cầu tâm lý này. Điểm khác biệt lớn nhất là quy mô và hậu quả. Drama ở phương Tây có thể ảnh hưởng đến chính sách công ty, thay đổi luật pháp, thậm chí ảnh hưởng đến bầu cử. Ở Việt Nam, tác động thường giới hạn hơn, mặc dù đang ngày càng mở rộng."
  },
  {
    "id": 158,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thấy điểm chung là \"drama ở đâu cũng vui\"!  Nhưng nghiêm túc mà nói, tôi thấy drama ở Việt Nam cá nhân hơn, gần gũi hơn - giống như chuyện hàng xóm. Còn drama quốc tế giống như một bộ phim bom tấn - hoành tráng, nhiều plot twist, nhiều special effects hơn. Nhưng cốt lõi vẫn là thứ làm chúng ta thích thú: chuyện người khác!"
  },
  {
    "id": 159,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cảm ơn hai bạn! Chúng ta đã cùng nhau khám phá những drama \"bự\" trên thế giới, từ cuộc chiến của các nghệ sĩ, công ty công nghệ, đến những tranh cãi xã hội sâu sắc. Trong phần tiếp theo, chúng ta sẽ bàn về cách ứng phó với drama - làm sao để không bị cuốn vào vòng xoáy drama vô tận, và cách tận dụng drama một cách tích cực nếu bạn là một cá nhân hoặc thương hiệu. Các bạn có sẵn sàng không?"
  },
  {
    "id": 160,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Tôi nghĩ đây sẽ là phần thực tế nhất, có ích nhất cho người nghe."
  },
  {
    "id": 161,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Sẵn sàng! Tôi có nhiều \"bí kíp sống sót qua drama\" lắm đây!"
  },
  {
    "id": 162,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chúng ta đã thấy drama xuất hiện khắp nơi trên mạng xã hội, nhưng câu hỏi lớn hơn là: nó thực sự ảnh hưởng đến chúng ta như thế nào? Hôm nay, chúng ta sẽ mổ xẻ cả mặt tích cực lẫn tiêu cực của drama. Anh Rớt, với kinh nghiệm của mình, anh nghĩ drama ảnh hưởng đến tâm lý người trong cuộc như thế nào?"
  },
  {
    "id": 163,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Ảnh hưởng rất lớn, Alex à. Tôi từng trải qua những đêm không ngủ vì drama. Khi bạn là tâm điểm của một drama lớn, đó là áp lực 24/7. Bạn liên tục kiểm tra điện thoại, lo lắng về những bình luận mới, những người \"đào\" thêm chuyện cũ. Nó tạo ra một vòng xoáy stress không có điểm dừng."
  },
  {
    "id": 164,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Có thể nói đó là một dạng FOMO đặc biệt phải không? Fear Of Missing Out - sợ bỏ lỡ những gì người khác đang nói về mình?"
  },
  {
    "id": 165,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chính xác. Nhưng nó thậm chí còn tệ hơn FOMO thông thường. Đây là nỗi sợ bỏ lỡ những thông tin có thể ảnh hưởng trực tiếp đến danh tiếng, sự nghiệp, và cuộc sống của bạn. Một comment có sức mạnh hủy diệt có thể xuất hiện bất cứ lúc nào. Tôi gọi đó là \"thảo mai reaction\" - nghĩa là luôn cảnh giác, luôn sẵn sàng phản ứng."
  },
  {
    "id": 166,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Ối giời ơi, \"thảo mai reaction\", tôi thích cụm từ này! Nó như kiểu bạn đang lướt Facebook bình thường, nhưng tay thì đã sẵn sàng gõ phản hồi, não thì đã chuẩn bị 5 kịch bản đối phó khác nhau!"
  },
  {
    "id": 167,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " Đúng là một hình ảnh sinh động! Chây, với tư cách là người nổi tiếng trẻ hơn, cậu cảm thấy thế nào về áp lực tâm lý này?"
  },
  {
    "id": 168,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Thú thật là ban đầu tôi cũng rất sợ hãi, kiểu như \"Ôi không, mọi người ghét mình rồi, sự nghiệp tôi sẽ tiêu tan\". Nhưng dần dần tôi học được cách... không quan tâm quá nhiều.  Không phải là không quan tâm hoàn toàn, mà là biết phân biệt đâu là ý kiến đáng nghe, đâu là noise vô nghĩa."
  },
  {
    "id": 169,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Nhưng để đạt được trạng thái đó không dễ. Nhiều nghệ sĩ, KOL đã rơi vào trầm cảm, lo âu vì drama. Tôi có một người bạn đồng nghiệp từng phải dùng thuốc an thần trong 6 tháng sau một vụ drama lớn. Mỗi lần cô ấy cầm điện thoại lên, tay còn run rẩy."
  },
  {
    "id": 170,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là mặt tiêu cực rõ ràng. Nhưng chúng ta cũng phải thừa nhận, drama đôi khi mang lại những \"lợi ích\" nhất định về mặt lượt xem và người theo dõi, phải không?"
  },
  {
    "id": 171,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " À, cái này tôi phải thừa nhận! Sau mỗi drama, followers của tôi thường tăng đột biến. Thậm chí có những video reaction về drama còn có lượt xem cao hơn cả MV chính thức của tôi!  Nghĩ cũng buồn cười, tôi làm nhạc cả tháng trời nhưng chẳng ai quan tâm, vậy mà chỉ cần tôi đăng một cái story \"đá xéo\" ai đó là cả Internet \"dậy sóng\"!"
  },
  {
    "id": 172,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Đó chính là điều nguy hiểm. Nó tạo ra một động lực sai lầm, khiến nhiều người cố tình tạo drama để đánh bóng tên tuổi. Tôi gọi đó là \"Drama Marketing\" - một chiến thuật nguy hiểm mà nhiều KOL, influencer đang áp dụng."
  },
  {
    "id": 173,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Ừm, nhưng mặt trái của nó là gì, anh Rớt?"
  },
  {
    "id": 174,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Mặt trái à? Bạn có thể đánh mất những hợp đồng quảng cáo lớn chỉ sau một đêm. Các thương hiệu ngày nay rất nhạy cảm với scandal. Họ không muốn hình ảnh của mình gắn liền với những drama tiêu cực. Tôi biết một nghệ sĩ đã mất gần 2 tỷ đồng tiền hợp đồng chỉ vì một drama liên quan đến phát ngôn không phù hợp."
  },
  {
    "id": 175,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng vậy! Tôi từng mất một hợp đồng quảng cáo với một nhãn hàng lớn chỉ vì vô tình xuất hiện trong background của một video có drama. Tôi thậm chí không liên quan gì, chỉ là đứng gần đó thôi! "
  },
  {
    "id": 176,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nói về tác động nghề nghiệp, có vẻ như drama là con dao hai lưỡi: có thể tăng độ nhận diện nhanh chóng nhưng cũng có thể hủy hoại danh tiếng dài hạn?"
  },
  {
    "id": 177,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chính xác. Và tôi nghĩ nhiều người không nhìn thấy bức tranh dài hạn. Họ chỉ thấy lượt view tăng vọt tạm thời mà quên mất rằng danh tiếng cần thời gian xây dựng nhưng chỉ cần một giây để mất đi. Drama có thể giúp bạn viral trong một tuần, nhưng có thể khiến người ta nhớ đến bạn như một \"kẻ thích gây drama\" trong nhiều năm."
  },
  {
    "id": 178,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nhưng nói thật, có những drama mà tôi không hề muốn, vậy mà nó lại xảy đến. Như kiểu số phận vậy!  Tôi không cố tình tạo drama, nhưng đôi khi cứ tự nhiên... boom! Tôi đã học được cách \"ăn theo\" nó một cách thông minh hơn. Kiểu như, nếu đã viral thì mình phải tận dụng cơ hội này để quảng bá điều gì đó tích cực."
  },
  {
    "id": 179,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "\"Ăn theo\" drama là sao, Chây?"
  },
  {
    "id": 180,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "À, ví dụ như khi tôi bị đồn hẹn hò với một nữ diễn viên nổi tiếng. Ban đầu tôi rất bực, nhưng sau đó tôi nghĩ: \"Được rồi, mọi người đang chú ý đến mình, vậy thì mình sẽ dùng cơ hội này\". Tôi đã phát hành một single mới ngay lúc đó, và nó đạt top trending chỉ trong 24 giờ!  Drama là cơ hội nếu bạn biết cách xử lý."
  },
  {
    "id": 181,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Nhưng đó vẫn là một cách tiếp cận ngắn hạn. Về lâu dài, công chúng sẽ mệt mỏi với những người liên tục xuất hiện trong drama. Họ muốn thần tượng của mình có tài năng thực sự, không chỉ là những \"drama queen\"."
  },
  {
    "id": 182,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Ngoài tác động đến cá nhân, drama còn ảnh hưởng đến xã hội như thế nào? Anh Rớt có thể chia sẻ góc nhìn của mình không?"
  },
  {
    "id": 183,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Drama trên mạng xã hội đang góp phần tạo ra một xã hội phân cực. Mọi người dần mất đi khả năng lắng nghe và tôn trọng quan điểm khác biệt. Drama thường thúc đẩy phản ứng cảm xúc nhanh chóng thay vì suy nghĩ thấu đáo. Và nguy hiểm hơn, nó tạo điều kiện cho tin giả lan truyền."
  },
  {
    "id": 184,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tin giả là một vấn đề nghiêm trọng trong thời đại thông tin bùng nổ. Cậu nghĩ sao, Chây?"
  },
  {
    "id": 185,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thấy nhiều người chia sẻ thông tin mà không hề kiểm chứng, chỉ vì nó \"juicy\" hoặc phù hợp với quan điểm của họ. Ví dụ, có lần tôi bị đồn là sử dụng chất cấm chỉ vì tôi đăng một tấm ảnh cầm chai nước detox màu xanh lá!  Mà chai đó là do một nhãn hàng gửi tôi quảng cáo!"
  },
  {
    "id": 186,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đó là điều tôi lo ngại. Trong thời đại \"post-truth\" này, sự thật không còn quan trọng bằng cảm xúc và niềm tin cá nhân. Drama càng khuếch đại xu hướng này. Nó tạo ra những \"bong bóng thông tin\" - nơi mọi người chỉ tiếp xúc với những quan điểm tương tự và ngày càng cực đoan hơn."
  },
  {
    "id": 187,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Nói về chia rẽ cộng đồng, các bạn có nghĩ rằng drama góp phần tạo ra những \"bộ lạc kỹ thuật số\" không - nơi mọi người chia phe, chọn bên?"
  },
  {
    "id": 188,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chắc chắn rồi. Trong nhiều drama, bạn sẽ thấy hashtag kiểu \"#TeamA\" hay \"#TeamB\". Điều này có vẻ vô hại, nhưng nó đang dần thay đổi cách chúng ta tương tác với nhau. Chúng ta không còn xem nhau như những cá nhân phức tạp mà chỉ là \"người của phe ta\" hay \"kẻ thù\". Điều này đặc biệt nguy hiểm trong các vấn đề chính trị và xã hội."
  },
  {
    "id": 189,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Tôi thấy điều này rõ nhất trong fandom. Các fan của nghệ sĩ này sẽ \"beef\" với fan của nghệ sĩ khác, đôi khi còn toxic hơn cả chính nghệ sĩ! Tôi từng phải đăng story yêu cầu fan của mình ngừng tấn công một nghệ sĩ khác vì tôi và người đó thậm chí còn là bạn!"
  },
  {
    "id": 190,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Vậy là drama có thể chia rẽ cộng đồng, lan truyền tin giả... còn điểm tích cực nào không? Hay nó hoàn toàn là một \"vũ khí hủy diệt\"?"
  },
  {
    "id": 191,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Tôi nghĩ drama cũng có mặt tích cực nếu được sử dụng đúng cách. Nó có thể nâng cao nhận thức về các vấn đề xã hội quan trọng. Ví dụ, drama về phát ngôn phân biệt giới tính của một nghệ sĩ có thể dẫn đến những cuộc thảo luận sâu rộng hơn về bình đẳng. Drama về plagia có thể nâng cao ý thức bản quyền. Vấn đề là ở cách chúng ta phản ứng và tham gia vào drama."
  },
  {
    "id": 192,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng vậy! Những drama \"có ý nghĩa\" đã giúp thay đổi nhận thức của nhiều người, kể cả tôi. Có những vấn đề mà trước đây tôi không quan tâm, nhưng sau khi chứng kiến drama liên quan, tôi đã học hỏi và thay đổi. Ví dụ như vấn đề body-shaming hay phân biệt đối xử. Vậy nên drama không hoàn toàn xấu, chỉ là nó cần được \"định hướng\" đúng đắn."
  },
  {
    "id": 193,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Điều đó dẫn chúng ta đến một câu hỏi thú vị: Drama là một \"công cụ marketing\" hay một \"vũ khí hủy diệt\"?"
  },
  {
    "id": 194,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Nó là cả hai. Giống như năng lượng hạt nhân - có thể cung cấp điện cho cả thành phố hoặc phá hủy nó. Drama là một công cụ truyền thông mạnh mẽ, nhưng đầy rủi ro. Điều quan trọng là người sử dụng phải có đạo đức và trách nhiệm."
  },
  {
    "id": 195,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Tôi nhìn drama như một món ăn cay! Một chút drama làm cho cuộc sống thêm hấp dẫn, nhưng quá nhiều thì... anh biết đấy, hậu quả không dễ chịu! "
  },
  {
    "id": 196,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " Một so sánh rất thực tế! Vậy làm thế nào để chúng ta - những người sáng tạo nội dung và người dùng mạng xã hội - có thể tận dụng mặt tích cực của drama mà không bị cuốn vào mặt tiêu cực?"
  },
  {
    "id": 197,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Điều quan trọng nhất là xác định ranh giới. Tôi có ba nguyên tắc: Không drama về đời tư, không drama với người yếu thế, và luôn xác minh thông tin trước khi phát ngôn. Nếu mọi người đều tuân thủ những nguyên tắc cơ bản này, mạng xã hội sẽ lành mạnh hơn nhiều."
  },
  {
    "id": 198,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Còn tôi thì nghĩ chúng ta cần biết \"lùi một bước\". Kiểu như, trước khi nhảy vào một drama, hãy tự hỏi: \"Mình có thực sự hiểu toàn bộ câu chuyện không? Bình luận của mình có giúp ích gì không, hay chỉ đổ thêm dầu vào lửa?\" Tôi đã học được cách im lặng quan sát trước khi phản ứng."
  },
  {
    "id": 199,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là những lời khuyên rất giá trị. Và với tư cách là người tiêu thụ nội dung, chúng ta cũng cần phải thông minh hơn khi tiếp nhận drama, phải không?"
  },
  {
    "id": 200,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chính xác. Hãy đọc nhiều nguồn, xác minh thông tin, và không vội vàng kết luận. Drama thường chỉ cho chúng ta một phần của câu chuyện - thường là phần gây sốc nhất. Nhưng để hiểu đúng, chúng ta cần nhìn nhận toàn cảnh."
  },
  {
    "id": 201,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và hãy nhớ rằng, đằng sau mỗi drama là con người thật với cảm xúc thật. Đôi khi chúng ta quên mất điều đó khi ngồi sau màn hình. Tôi từng bị tổn thương sâu sắc bởi những bình luận mà người viết có thể chỉ coi là \"cho vui\"."
  },
  {
    "id": 202,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cậu có thể chia sẻ một kinh nghiệm cụ thể không, Chây?"
  },
  {
    "id": 203,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Năm ngoái, tôi vướng vào một drama về chuyện hẹn hò. Có người tung tin tôi là \"người thứ ba\" phá vỡ một mối quan hệ. Sự thật là tôi thậm chí không biết người kia đã có bạn gái! Nhưng chỉ trong một đêm, tôi nhận hàng nghìn tin nhắn tấn công, thậm chí là đe dọa. Tôi không dám ra đường trong hai tuần. Về mặt lượt view, đúng là MV mới của tôi tăng vọt. Nhưng cái giá phải trả là sức khỏe tinh thần của tôi. Đó là khi tôi nhận ra, không drama nào đáng để đánh đổi sự bình yên."
  },
  {
    "id": 204,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Đó là điều nhiều người không thấy - cái giá \"ẩn\" của drama. Stress, lo âu, mất ngủ... không con số nào đo đếm được những tổn thất này."
  },
  {
    "id": 205,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Vậy nếu nhìn về tương lai, xu hướng drama trên mạng xã hội sẽ đi về đâu? Anh Rớt có dự đoán gì không?"
  },
  {
    "id": 206,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Tôi nghĩ chúng ta đang bước vào thời kỳ \"drama mệt mỏi\". Người dùng mạng xã hội dần trở nên thông minh hơn, họ bắt đầu nhận ra nhiều drama được dàn dựng hoặc phóng đại. Trong tương lai, tôi tin rằng drama cần có chiều sâu và ý nghĩa xã hội mới thực sự gây chú ý."
  },
  {
    "id": 207,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi cũng thấy vậy! Gần đây, những drama \"có chiều sâu\" như về môi trường, bình đẳng giới, hay quyền động vật lại thu hút nhiều sự quan tâm hơn những drama hẹn hò nhạt nhẽo. Có thể nói, khán giả đang \"nâng cấp\" khẩu vị drama của mình! "
  },
  {
    "id": 208,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là một quan sát thú vị! Vậy có thể nói, trong tương lai, drama sẽ trở thành một công cụ thúc đẩy thay đổi xã hội tích cực?"
  },
  {
    "id": 209,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Có thể, nếu chúng ta biết cách sử dụng nó. Drama có sức mạnh tập trung sự chú ý của công chúng vào một vấn đề. Nếu vấn đề đó có ý nghĩa xã hội, drama có thể trở thành chất xúc tác cho những thay đổi tích cực."
  },
  {
    "id": 210,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và với tư cách là người có ảnh hưởng, chúng ta có trách nhiệm \"lái\" drama theo hướng tích cực. Thay vì drama về \"ai mặc đẹp hơn\", chúng ta có thể tạo ra những cuộc thảo luận sôi nổi về các vấn đề quan trọng hơn."
  },
  {
    "id": 211,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cảm ơn cả hai vì những chia sẻ sâu sắc. Để tổng kết lại, drama trên mạng xã hội có cả tác động tích cực lẫn tiêu cực. Nó có thể gây stress, lo âu, chia rẽ cộng đồng, nhưng cũng có thể nâng cao nhận thức, thúc đẩy thay đổi xã hội. Điều quan trọng là cách chúng ta - những người sáng tạo và người tiêu thụ nội dung - tham gia vào nó."
  },
  {
    "id": 212,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chính xác. Và tôi tin rằng, với sự trưởng thành của cộng đồng mạng, drama sẽ dần trở nên có ý nghĩa hơn."
  },
  {
    "id": 213,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Còn tôi thì vẫn sẽ tiếp tục đăng ảnh bún đậu mà không sợ bị hiểu lầm! "
  },
  {
    "id": 214,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " Đó mới là tinh thần! Và đây cũng là một điểm chuyển hoàn hảo để chúng ta bước vào phần cuối cùng của podcast hôm nay - những kỹ năng để sống sót và phát triển trong thời đại drama. Làm thế nào để bảo vệ bản thân khỏi tác động tiêu cực của drama? Làm thế nào để nhận diện drama có giá trị? Hãy cùng tìm hiểu sau phần quảng cáo ngắn này!"
  },
  {
    "id": 215,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chào mừng các bạn quay trở lại với podcast \"Góc nhìn đa chiều\"! Sau khi tìm hiểu tất tần tật về drama, từ định nghĩa, phân loại, cho đến những tác động của nó, giờ là lúc để chúng ta bàn về điều mà có lẽ ai cũng đang chờ đợi - làm thế nào để đối phó với drama một cách hiệu quả? Và quan trọng hơn, chúng ta có thể rút ra những bài học gì từ những \"cơn bão drama\" này?"
  },
  {
    "id": 216,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Đây đúng là vấn đề quan trọng nhất, Alex à. Tôi nghĩ nhiều người trong chúng ta, đặc biệt là những người làm nghề nghệ thuật, giải trí như tôi và Chây, đều đã từng tự hỏi: \"Nếu một ngày mình bị cuốn vào drama, mình sẽ xử lý thế nào?\""
  },
  {
    "id": 217,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": " Nếu là tôi của 5 năm trước, câu trả lời chắc là: \"Khóc một trận rồi bay thẳng sang Thái Lan trốn luôn!\" Nhưng giờ thì tôi đã có... kinh nghiệm hơn rồi."
  },
  {
    "id": 218,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " Vậy chúng ta hãy bắt đầu với câu hỏi này nhé: Khi một cá nhân, đặc biệt là KOL hoặc người nổi tiếng, bị dính vào drama, họ nên làm gì đầu tiên?"
  },
  {
    "id": 219,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Điều đầu tiên và quan trọng nhất là giữ bình tĩnh. Tôi biết nói thì dễ nhưng làm thì khó. Khi thấy hàng trăm, hàng nghìn bình luận tiêu cực về mình, phản ứng tự nhiên là hoảng loạn, giận dữ. Nhưng đó chính là lúc bạn cần phải bình tĩnh nhất."
  },
  {
    "id": 220,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng vậy! Tôi có một chiêu rất hay đó là... tắt điện thoại và đi ngủ một giấc!  Nói thật đấy. Khi drama mới nổ ra, mọi thứ rất hỗn loạn. Nếu bạn phản ứng ngay lúc đó, rất có thể bạn sẽ nói hoặc làm những điều mà sau này bạn hối hận."
  },
  {
    "id": 221,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tôi thấy điều đó rất có lý! Thực tế thì có một nguyên tắc trong xử lý khủng hoảng gọi là \"quy tắc vàng 24 giờ\" - hãy chờ ít nhất 24 giờ trước khi đưa ra phản hồi chính thức về một vấn đề nghiêm trọng."
  },
  {
    "id": 222,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đúng vậy, Alex. Trong 24 giờ đó, bạn cần thu thập thông tin. Hiểu rõ vấn đề đang là gì, từ đâu bắt đầu, ai đang nói gì. Đừng chỉ đọc vài bình luận rồi đưa ra kết luận. Và đặc biệt quan trọng: tham khảo ý kiến những người bạn tin tưởng, tốt nhất là những người có kinh nghiệm trong ngành truyền thông."
  },
  {
    "id": 223,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Ừm, đừng như tôi hồi trước. Có lần tôi thấy hashtag tên mình trending, panic luôn, vội vàng viết một status dài 2000 chữ phản bác. Sau đó mới biết là hashtag đó trending vì... fan đang khen MV mới của tôi đẹp trai. "
  },
  {
    "id": 224,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " Đó chính là lý do vì sao cần thu thập thông tin đầy đủ! Nhưng nói về chiến lược cụ thể, tôi nghĩ có một framework 5 bước mà mọi người có thể áp dụng. Tôi gọi nó là \"ADMIT\": A - Assess (Đánh giá tình hình) D - Decide (Quyết định có cần phản hồi không) M - Message (Soạn thông điệp cẩn thận) I - Implement (Triển khai phản hồi) T - Track (Theo dõi phản ứng và điều chỉnh)"
  },
  {
    "id": 225,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": " Framework này khá toàn diện. Tôi đặc biệt muốn nhấn mạnh về bước D - Decide. Không phải mọi drama đều cần phản hồi. Đôi khi, im lặng là vàng."
  },
  {
    "id": 226,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng vậy! Anh có thể chia sẻ thêm về điều này không?"
  },
  {
    "id": 227,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Có những tình huống mà phản hồi chỉ làm drama to hơn. Ví dụ như khi drama dựa trên thông tin hoàn toàn sai lệch và không có nhiều người quan tâm. Hoặc khi đối phương cố tình khiêu khích để bạn phản ứng. Trong những trường hợp này, sự im lặng khôn ngoan có thể là chiến lược tốt nhất."
  },
  {
    "id": 228,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Nhưng cũng có lúc phải lên tiếng ngay, đúng không? Ví dụ như khi có thông tin sai sự thật ảnh hưởng nghiêm trọng đến danh dự, hình ảnh."
  },
  {
    "id": 229,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chính xác. Và đó là lúc bạn cần áp dụng bước M - Message. Thông điệp của bạn phải chân thành, thẳng thắn, nhưng không mang tính phòng thủ quá mức."
  },
  {
    "id": 230,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Chây, với kinh nghiệm của mình, cậu có tips nào để soạn một thông điệp hiệu quả không?"
  },
  {
    "id": 231,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Có! Đầu tiên, hãy viết tất cả những gì bạn muốn nói ra giấy - mọi cảm xúc, phản bác, giải thích. Sau đó... xé nó đi và viết lại từ đầu!  Bản thảo đầu tiên thường quá dài dòng và đầy cảm xúc. Bản thứ hai sẽ súc tích và chuyên nghiệp hơn."
  },
  {
    "id": 232,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " Cách tiếp cận thú vị đấy!"
  },
  {
    "id": 233,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và một tip khác: hãy dùng ngôn ngữ đời thường, không quá formal hoặc PR. Khán giả rất nhạy cảm với những thông điệp nghe như viết bởi đội ngũ PR. Họ muốn nghe giọng nói thật của bạn."
  },
  {
    "id": 234,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Tôi đồng ý. Sự chân thành là chìa khóa. Và nếu bạn đã sai, hãy thừa nhận. Đừng đổ lỗi hay tìm cách biện minh. Khán giả thường tha thứ cho những lỗi lầm, nhưng họ không dễ dàng bỏ qua sự không chân thành."
  },
  {
    "id": 235,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng vậy! Và về bước cuối cùng, Track - theo dõi phản ứng và điều chỉnh, điều này có nghĩa là gì?"
  },
  {
    "id": 236,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Sau khi bạn đã phản hồi, công việc vẫn chưa kết thúc. Bạn cần theo dõi xem phản ứng của công chúng như thế nào. Có khi nào bạn cần làm rõ thêm không? Có ai đang cố tình xuyên tạc phản hồi của bạn không? Đôi khi bạn cần phải \"follow-up\" nhưng đừng bao giờ rơi vào tình trạng liên tục phản hồi, phản hồi về phản hồi, và cứ thế... nó sẽ chẳng có hồi kết."
  },
  {
    "id": 237,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và luôn nhớ rằng: drama rồi sẽ qua đi. Tôi từng trải qua một drama mà tưởng như nó sẽ là dấu chấm hết cho sự nghiệp. Nhưng bạn biết không, hai tuần sau, mọi người đã chuyển sang drama khác rồi! "
  },
  {
    "id": 238,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Vậy theo anh, Vai Rớt, với tư cách là một người làm nghề streamer, ca sĩ, có chiến lược nào để \"phòng bệnh hơn chữa bệnh\" không?"
  },
  {
    "id": 239,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Tất nhiên rồi. Tôi có vài nguyên tắc cá nhân mà tôi luôn tuân thủ: Thứ nhất, xây dựng một hình ảnh nhất quán. Khán giả cần biết họ đang theo dõi ai, và họ có thể mong đợi điều gì từ bạn. Khi hình ảnh của bạn rõ ràng, mọi drama không phù hợp với hình ảnh đó sẽ ít được tin hơn. Thứ hai, tạo mối quan hệ chân thành với cộng đồng fan. Họ sẽ là lá chắn đầu tiên và mạnh mẽ nhất khi drama xảy ra. Thứ ba, set ranh giới. Biết rõ những gì bạn sẽ chia sẻ và những gì giữ riêng tư. Càng chia sẻ nhiều về đời tư, bạn càng dễ bị cuốn vào drama. Và cuối cùng, thường xuyên \"self-audit\" các nội dung bạn đã đăng. Nhìn lại nội dung cũ từ góc nhìn của một người ngoài và tự hỏi: \"Điều này có thể bị hiểu sai không?\""
  },
  {
    "id": 240,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Còn tôi có một bí kíp riêng, đó là... luôn có sẵn content tích cực để \"chữa cháy\"!  Mỗi khi có drama, tôi sẽ tung ra một MV hậu trường vui nhộn, một challenge dễ thương, hay một livestream làm từ thiện. Nó không phải để \"chuyển hướng dư luận\" kiểu PR, mà là để nhắc nhở mọi người về con người thật của mình."
  },
  {
    "id": 241,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đó là chiến lược rất thông minh! Giờ chúng ta hãy nói về vai trò của cộng đồng mạng. Mọi người bình thường như chúng ta nên làm gì để không vô tình \"đổ thêm dầu vào lửa\"?"
  },
  {
    "id": 242,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đây là điểm quan trọng. Mỗi lượt like, share, bình luận đều có thể khiến drama lan rộng hơn. Tôi nghĩ chúng ta cần thực hành \"tiêu thụ thông tin có trách nhiệm\": Kiểm chứng trước khi tin, đọc toàn bộ nội dung trước khi share, và suy nghĩ về động cơ đằng sau mỗi bài đăng drama."
  },
  {
    "id": 243,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Đúng vậy! Và một điều tôi nghĩ rất quan trọng: hãy tự hỏi \"mình có liên quan gì đến drama này không?\" trước khi bình luận. Nhiều lúc chúng ta nhảy vào drama của người lạ không phải vì quan tâm đến vấn đề, mà chỉ vì... nó vui! "
  },
  {
    "id": 244,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tôi nghĩ có một checklist đơn giản mà mọi người có thể áp dụng trước khi tham gia vào một drama: Thông tin này có đầy đủ không? Nguồn thông tin có đáng tin không? Việc tôi share/comment có giúp giải quyết vấn đề không? Tôi có sẵn sàng chịu trách nhiệm về việc lan truyền thông tin này không?"
  },
  {
    "id": 245,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Tôi muốn thêm một câu hỏi nữa: \"Nếu tôi là người trong drama đó, tôi sẽ cảm thấy thế nào khi đọc bình luận này?\" Đôi khi chúng ta quên mất rằng phía sau mỗi drama là những con người thật với cảm xúc thật."
  },
  {
    "id": 246,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và đừng quên câu hỏi quan trọng nhất: \"Liệu 3 năm nữa tôi có còn quan tâm đến drama này không?\"  Hầu hết câu trả lời là: không! Vậy thì sao phải bỏ quá nhiều năng lượng vào nó ngay bây giờ?"
  },
  {
    "id": 247,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " Đúng là một góc nhìn thực tế! Vậy nếu nhìn rộng hơn, chúng ta có thể rút ra những bài học gì từ \"kỷ nguyên drama\" này?"
  },
  {
    "id": 248,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Tôi nghĩ bài học lớn nhất là về cách chúng ta tiêu thụ và xử lý thông tin. Internet đã cho chúng ta khả năng tiếp cận lượng thông tin khổng lồ, nhưng không dạy chúng ta cách lọc và phân tích thông tin đó. Đây là kỹ năng mà mỗi người cần tự học."
  },
  {
    "id": 249,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Còn tôi nghĩ đó là bài học về sự cân bằng giữa đời thực và đời ảo. Drama có sức nặng là vậy, nhưng đôi khi bước ra ngoài, hít thở không khí trong lành, bạn sẽ nhận ra là... à, thế giới vẫn quay mà không cần biết ai đó vừa \"đá xéo\" ai trên Instagram! "
  },
  {
    "id": 250,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Tôi nghĩ một bài học quan trọng khác là về tính hai mặt của mạng xã hội. Nó có thể là nơi lan tỏa thông tin tích cực, kết nối mọi người, nhưng cũng có thể là nơi chia rẽ và tạo ra những hiểu lầm không đáng có. Mỗi chúng ta đều có trách nhiệm trong việc định hình môi trường online này."
  },
  {
    "id": 251,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đúng vậy. Và điều quan trọng nhất có lẽ là khả năng thích nghi. Mạng xã hội và drama sẽ luôn tồn tại và thay đổi. Thay vì chống lại nó, chúng ta cần học cách sống chung với nó một cách khôn ngoan và lành mạnh."
  },
  {
    "id": 252,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi có một câu nói mà tôi luôn tâm niệm: \"Đừng để drama của người khác trở thành drama của mình\". Cuộc sống đã đủ phức tạp rồi, phải không? "
  },
  {
    "id": 253,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Một câu nói rất hay! Và để tổng kết lại, tôi nghĩ chúng ta đều đồng ý rằng drama không hoàn toàn xấu và cũng không hoàn toàn tốt - nó là một phần tất yếu của cuộc sống online hiện đại. Điều quan trọng là cách chúng ta ứng phó với nó."
  },
  {
    "id": 254,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Chính xác. Và nếu bạn là người trong cuộc của một drama, hãy nhớ rằng đây không phải là kết thúc thế giới. Hãy giữ bình tĩnh, thu thập thông tin, tham khảo ý kiến những người bạn tin tưởng, và phản hồi một cách khôn ngoan nếu cần thiết."
  },
  {
    "id": 255,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và nhớ rằng: \"This too shall pass\" - rồi mọi thứ sẽ qua đi! Drama hôm nay là tin cũ của ngày mai.  Hãy cứ sống thật với bản thân, và đừng quên cười - ngay cả khi bạn đang ở giữa tâm bão!"
  },
  {
    "id": 256,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cảm ơn hai vị khách mời vì những chia sẻ vô cùng bổ ích hôm nay! Trước khi kết thúc, anh Vai Rớt và Chây có lời khuyên cuối cùng nào dành cho khán giả của chúng ta không?"
  },
  {
    "id": 257,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Tôi nghĩ điều quan trọng nhất là đừng bao giờ đánh mất bản thân vì drama. Danh tiếng, hình ảnh có thể xây dựng lại được, nhưng sự bình an trong tâm hồn mới là điều cần trân trọng nhất."
  },
  {
    "id": 258,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và hãy nhớ, cuộc sống ngoài kia còn rất nhiều điều thú vị để khám phá! Drama thì vui, nhưng đi ăn bún đậu với bạn bè còn vui hơn nhiều! "
  },
  {
    "id": 259,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": " Một lời kết hoàn hảo! Cảm ơn anh Vai Rớt và Chây 97 rất nhiều vì đã tham gia podcast của chúng ta hôm nay! Và cảm ơn các bạn đã lắng nghe. Trong tập tiếp theo, chúng ta sẽ tổng kết lại toàn bộ hành trình khám phá thế giới drama, và đưa ra những dự đoán về tương lai của drama trên mạng xã hội. Các bạn nhớ đón nghe nhé!"
  },
  {
    "id": 260,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Cảm ơn Alex và cảm ơn các bạn thính giả!"
  },
  {
    "id": 261,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Bye bye mọi người! Nhớ follow để không bỏ lỡ drama tiếp theo... của podcast chúng tôi! "
  },
  {
    "id": 262,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Và thế là chúng ta đã cùng nhau khám phá thế giới drama trên mạng xã hội! Thật sự là một hành trình đầy thú vị và nhiều điều bất ngờ, phải không hai anh?"
  },
  {
    "id": 263,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Đúng vậy, Alex. Tôi nghĩ cuộc trò chuyện hôm nay đã mang đến nhiều góc nhìn thú vị về một hiện tượng mà tất cả chúng ta đều gặp hàng ngày nhưng có lẽ chưa từng dừng lại để suy ngẫm kỹ về nó."
  },
  {
    "id": 264,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Tôi thật sự thích thú với buổi nói chuyện này. Cảm giác như được nhìn lại bản thân mình mỗi khi lướt feed và bắt gặp drama ấy! "
  },
  {
    "id": 265,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Để tóm tắt lại những gì chúng ta đã thảo luận, tôi nghĩ có một vài điểm quan trọng mà các bạn thính giả có thể ghi nhớ. Đầu tiên, drama không phải lúc nào cũng tiêu cực - đôi khi nó là cách để những vấn đề xã hội được chú ý và giải quyết."
  },
  {
    "id": 266,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Điểm thứ hai tôi muốn nhấn mạnh là về sự tỉnh táo khi tiếp nhận thông tin. Trong thời đại \"post-truth\" này, việc kiểm chứng thông tin trước khi chia sẻ hay bình luận là vô cùng quan trọng. Đừng để mình trở thành một phần của drama toxic chỉ vì thiếu suy xét."
  },
  {
    "id": 267,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và điểm thứ ba, theo tôi, là hãy luôn giữ được sự hài hước! Tôi nghĩ nhiều drama sẽ không leo thang nếu chúng ta biết cách nhìn nhận mọi thứ nhẹ nhàng hơn, không cần phải nghiêm trọng hóa mọi vấn đề."
  },
  {
    "id": 268,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Điểm cuối cùng tôi muốn nhắc đến là về sự cân bằng. Mạng xã hội là công cụ tuyệt vời để kết nối, nhưng đừng để nó chi phối cuộc sống thực của bạn. Đôi khi, việc tắt điện thoại và dành thời gian cho những mối quan hệ trực tiếp là điều quý giá nhất."
  },
  {
    "id": 269,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Hoàn toàn đồng ý. Tôi đã có những khoảng thời gian \"digital detox\" - tạm ngưng sử dụng mạng xã hội, và đó thực sự là những khoảng thời gian mà tôi cảm thấy tâm trí mình được thông suốt và sáng tạo nhất."
  },
  {
    "id": 270,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Các bạn thính giả thân mến, chúng tôi rất muốn nghe về trải nghiệm của các bạn với drama trên mạng xã hội. Các bạn đã từng vô tình trở thành một phần của drama nào không? Hoặc các bạn có chiến lược gì để tránh bị cuốn vào những drama tiêu cực? Hãy chia sẻ trong phần bình luận dưới podcast này nhé!"
  },
  {
    "id": 271,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Và nếu các bạn thích podcast hôm nay, đừng quên đăng ký kênh để không bỏ lỡ những tập tiếp theo! Tôi nghe nói tập tới sẽ về chủ đề \"Nghệ thuật trong thời đại AI\" - một chủ đề mà tôi cực kỳ quan tâm đấy!"
  },
  {
    "id": 272,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Đúng vậy, Chây! Tập tới chúng ta sẽ thảo luận về cách AI đang thay đổi ngành nghệ thuật, từ âm nhạc, hội họa đến văn học. Và chúng tôi sẽ có những khách mời đặc biệt từ ngành công nghiệp sáng tạo!"
  },
  {
    "id": 273,
    "speaker": "Vai Rớt",
    "voice": "leminh",
    "text": "Tôi chắc chắn sẽ không bỏ lỡ tập đó. Và gửi đến tất cả các bạn thính giả, hãy nhớ rằng - mạng xã hội chỉ là một phần của cuộc sống. Hãy sống thật, sống trọn vẹn, và đừng để những drama online làm ảnh hưởng đến hạnh phúc của bạn."
  },
  {
    "id": 274,
    "speaker": "Chây 97",
    "voice": "minhquang",
    "text": "Chúc các bạn một cuối tuần tuyệt vời! Nhớ là hết drama rồi thì... vẫn phải sống tốt nhé! "
  },
  {
    "id": 275,
    "speaker": "Alex",
    "voice": "giahuy",
    "text": "Cảm ơn hai anh Vai Rớt và Chây 97 đã tham gia cùng chúng tôi hôm nay. Cảm ơn tất cả các bạn đã lắng nghe. Đây là Alex từ podcast Góc nhìn đa chiều, hẹn gặp lại các bạn trong tập tới!"
  }
]

#
#
#
# tts_url = "https://api.fpt.ai/hmi/tts/v5"
#
#
# api_key = "E3ZGNreWqkJYzpuz6ORc2MeIPLO98NZk"
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
# for index, row_tuple in enumerate(df_link.itertuples(index=True, name='uri'), start=1):
#     uri = row_tuple.uri
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
    max_num = 275

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

















