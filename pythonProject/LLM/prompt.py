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
    return """
Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu. Với câu hỏi sau, hãy trích xuất thông tin từ câu hỏi theo yêu cầu. 
Quy tắc: 
1. Thông tin quan hệ phải đến từ các loại quan hệ đã cho. 
2. Mỗi thực thể phải có chính xác một danh mục trong ngoặc đơn.

Với câu hỏi sau, dựa trên loại thực thể và loại quan hệ, hãy trích xuất các thực thể chủ đề và các quan hệ hữu ích từ câu hỏi. 
Loại thực thể: "phần 1: nlu - định hướng trường đại học nghiên cứu, quá trình hình thành và phát triển, sứ mạng, tầm nhìn, giá trị cốt lõi, mục tiêu chiến lược, cơ sở vật chất, các đơn vị trong trường, các khoa - ngành đào tạo, tuần sinh hoạt công dân - sinh viên, hoạt động phong trào sinh viên, câu lạc bộ (clb) - đội, nhóm, cơ sở đào tạo, phần 2: học tập và rèn luyện, quy chế sinh viên, quy chế học vụ, quy định về việc đào tạo trực tuyến, quy định khen thưởng, kỷ luật sinh viên, quy chế đánh giá kết quả rèn luyện, quy tắc ứng xử văn hóa của người học, cố vấn học tập, danh hiệu sinh viên 5 tốt, danh hiệu sinh viên tiêu biểu, phần 3: hỗ trợ và dịch vụ, quy định phân cấp giải quyết thắc mắc của sinh viên, thông tin học bổng, vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên, quy trình xác nhận hồ sơ sinh viên, hồ sơ yêu cầu bồi thường bảo hiểm tai nạn sinh viên, thông tin về bảo hiểm y tế, hướng dẫn sử dụng các kênh thanh toán học phí, bhyt, lệ phí xét tốt nghiệp, tham vấn tâm lý học đường, trung tâm dịch vụ sinh viên, trường đại học nông lâm tp. hồ chí minh, 12 phòng ban, 07 trung tâm, 01 viện nghiên cứu, 12 khoa đào tạo chuyên môn, 01 khoa cơ bản, phòng công tác sinh viên, 28.3897456, http://nls.hcmuaf.edu.vn, phòng đào tạo, 28.3896335, http://pdt.hcmuaf.edu.vn, phòng đào tạo sau đại học, 28.38963339, http://pgo.hcmuaf.edu.vn, phòng hành chính, 28.3896678, https://ado.hcmuaf.edu.vn, phòng hợp tác quốc tế, 28.38966946, http://iro.hcmuaf.edu.vn, phòng kế hoạch tài chính, 28.38963334, http://pkhtc.hcmuaf.edu.vn, phòng quản lý chất lượng, 283.724587, https://kdcl.hcmuaf.edu.vn, phòng ql nghiên cứu khoa học, 28.3896334, http://srmo.hcmuaf.edu.vn, phòng quản trị vật tư, 28.38961157, http://pqtvt.hcmuaf.edu.vn, phòng tổ chức cán bộ, 28.38963341, http://tccb.hcmuaf.edu.vn, phòng thanh tra giáo dục, 28.37245195, http://ttra.hcmuaf.edu.vn, phòng thông tin và truyền thông, 28.35359097, https://4t.hcmuaf.edu.vn, đoàn thanh niên, hội sinh viên, 283.7245396, https://www.tuoitrenonglam.com, tạp chí nông nghiệp và phát triển trường đại học nông lâm tp.hcm, 28.3724567, https://jad.hcmuaf.edu.vn, thư viện, 28.38963351, http://elib.hcmuaf.edu.vn, trung tâm dịch vụ sinh viên, 28.38963346, https://ttdvsv.hcmuaf.edu.vn, tt hỗ trợ sinh viên và quan hệ doanh nghiệp, 28.37245397, http://htsv.hcmuaf.edu.vn, tt nghiên cứu & chuyển giao khcn, 28.38966056, http://rttc.hcmuaf.edu.vn, trung tâm nghiên cứu biến đổi khí hậu, 28.37242522, https://rccc.hcmuaf.edu.vn, trung tâm nghiên cứu và ứng dụng công nghệ địa chính, 28.37245422, http://cadas.hcmuaf.edu.vn, tt ngoại ngữ, 28.38960109, http://cfs.hcmuaf.edu.vn, tt tin học ứng dụng, 28.38961713, http://aic.hcmuaf.edu.vn, tt ươm tạo doanh nghiệp công nghệ, 28.37245197, http://tbi.hcmuaf.edu.vn, viện nghiên cứu công nghệ sinh học và môi trường, 28.37220294, http://ribe.hcmuaf.edu.vn, khoa công nghệ hóa học và thực phẩm, 28.38960871, https://ceft.hcmuaf.edu.vn, khoa công nghệ thông tin, 28.37242623, http://fit.hcmuaf.edu.vn, khoa cơ khí công nghệ, 28.38960721, http://fme.hcmuaf.edu.vn, khoa chăn nuôi thú y, 28.38961711, https://cnty.hcmuaf.edu.vn, khoa kinh tế, 28.38961708, http://eco.hcmuaf.edu.vn, khoa khoa học, 28.37220262, http://fs.hcmuaf.edu.vn, khoa khoa học sinh học, 28.37245163, http://biotech.hcmuaf.edu.vn, khoa lâm nghiệp, 28.38975453, http://ff.hcmuaf.edu.vn, khoa môi trường và tài nguyên, 28.37220723, http://env.hcmuaf.edu.vn, khoa nông học, 28.3896171, http://fa.hcmuaf.edu.vn, khoa ngoại ngữ - sư phạm, 28.37220727, http://ffl.hcmuaf.edu.vn, khoa quản lý đất đai và bất động sản, 28.37220261, http://lrem.hcmuaf.edu.vn, khoa thủy sản, 28.38963343, https://fof.hcmuaf.edu.vn, bộ môn lý luận chính trị, 28.38963342, http://bmllct.hcmuaf.edu.vn, trường đại học nông lâm tp. hcm (nls), ngành công nghệ kỹ thuật cơ khí, cơ khí - công nghệ, công nghệ kỹ thuật cơ điện tử, công nghệ kỹ thuật ôtô, công nghệ kỹ thuật nhiệt, kỹ thuật điều khiển và tự động hóa, công nghệ kỹ thuật năng lượng tái tạo, khoa cơ khí - công nghệ, ngành công nghệ thông tin, ngành quả lý đất đai, bất động sản, ngành công nghệ chế biến lâm sản, lâm học, quản lý tài nguyên rừng, lâm nghiệp đô thị, ngành công nghệ kỹ thuật hóa học, công nghệ thực phẩm, ngành chăn nuôi, thú y, khoa chăn nuôi – thú y, ngành nông học, bảo vệ thực vật, khoa nông hoc, ngành khoa học sinh học, khoa công nghệ sinh học, ngành kỹ thuật môi trường, quản lý tài nguyên và môi trường, khoa học môi trường, hệ thống thông tin, tài nguyên và du lịch sinh thái, cảnh quan và kỹ thuật hoa viên, ngành nuôi trồng thủy sản, công nghệ chế biến thủy sản, ngành sư phạm kỹ thuật nông nghiệp, ngôn ngữ anh, ngành kinh tế, quản trị kinh doanh, kinh doanh nông nghiệp, phát triển nông thôn, kế toán, bác sĩ thú y, phân hiệu gia lai (nlg), phân hiệu ninh thuận (nln), giáo dục mầm non (trình độ cao đẳng), giáo dục mầm non (trình độ đại học), trường đại học nông lâm tp.hcm, clb cán bộ đoàn ngôi sao xanh, đoàn thanh niên, hồ thị thanh hồng, bec english club, đoàn–hội khoa khoa học sinh học, nguyễn lê thanh vy, clb bóng rổ đại học nông lâm, hội thể thao, hồ thanh tú, clb du lịch sinh thái, đoàn–hội khoa môi trường – tài nguyên, trần lê hiếu, clb dược thú y, đoàn – hội khoa chăn nuôi thú y, nguyễn nữ mai thơ, clb đồng hành – ac, phạm chí biết, fire english club, đoàn–hội khoa ngoại ngữ–sư phạm, nguyễn hoàng nam phương, clb học thuật–kỹ năng quản trị (b.a.s), võ lê bách, clb karate-do, lê quang trí, clb kết nối thành công, trung tâm hỗ trợ sinh viên & quan hệ doanh nghiệp, dương triệu duy, clb khởi nghiệp (nlu startup club) nsc, trung tâm ươm tạo doanh nghiệp công nghệ, trần phạm mỹ duyên, clb một sức khỏe tp.hcm (hcmc one health club), võ minh trường, clb sách và hành động nông lâm tp.hcm, phạm thị huyên, clb tiếng anh khoa công nghệ hóa học và thực phẩm (seeds for future) sff, đoàn - hội khoa công nghệ hóa học và thực phẩm, nguyễn thị ngọc hân, clb tiếng anh khoa kinh tế efb (english for business club) efb, đoàn - hội khoa kinh tế, nguyễn hoàng tuấn, clb thể thao điện tử pwf – clb pwf gaming, nguyễn võ hải triều, clb thú y engscope, nguyễn ngọc uyên nhi, clb truyền thông nông lâm radio, bùi thị thùy trang, wildlife vet student club, lê tường vi, clb yêu môi trường, trần ái thiên, tổ tu dưỡng rèn luyện hạt giống đỏ, dương quốc thái, đội công tác xã hội, hội sinh viên trường, võ công thương, đội khát vọng tuổi trẻ khoa chăn nuôi thú y, trần viết nguyên chương, đội nhiệt huyết rừng xanh, đoàn–hội khoa lâm nghiệp, nguyễn hữu hoàng, đội văn nghệ mfb–melody from bio, trần đức phúc, đội văn nghệ rạng đông, lê thành tài, đội văn nghệ xung kích nhịp điệu xanh, nguyễn nhu minh hạ, đội xung kích khoa khoa học sinh học, đỗ minh anh, hội cổ động viên (nong lam buffaloes) nlb, đoàn an bình, khu phố 22-23, phường linh trung, thành phố thủ đức, thành phố hồ chí minh, 0283.896.6780, https://www.hcmuaf.edu.vn, vphanhchinh@hcmuaf.edu.vn, phân hiệu trường đại học nông lâm tp.hcm tại ninh thuận, số 8 đường yên ninh, thị trấn khánh hải, huyện ninh hải, tỉnh ninh thuận, 0259.2472.252, https://phnt.hcmuaf.edu.vn/, phnt@hcmuaf.edu.vn, phân hiệu trường đại học nông lâm tp.hcm tại gia lai, đường trần nhật duật, thông 01, xã diên phú, thành phố pleiku, tỉnh gia lai, 0269.3877.035, https://phgl.hcmuaf.edu.vn/, phgl@hcmuaf.edu.vn, 6 giảng đường, 10 trung tâm, 01 viện nghiên cứu và ứng dụng, 01 thư viện trung tâm, 15.000 đầu sách, 01 bệnh viện thú y, 01 xưởng dược thú y, 01 trại thực nghiệm thủy sản, 04 trung tâm nghiên cứu thí nghiệm, thư viện điện tử, 6 ký túc xá, 350 phòng, 3.000 sinh viên, 1 sân đa môn, 3 sân bóng chuyền, 1 sân bóng đá, nhà thi đấu và luyện tập thể thao, 1, nhân văn, giá trị truyền thống nhân văn, dân tộc, nhân bản, tài năng, tính sáng tạo, kỹ năng, trách nhiệm nghề nghiệp, người học, phục vụ, lợi ích, cộng đồng, xã hội học tập, đổi mới, chất lượng, hiệu quả, nhà trường, hội nhập, hợp tác, chia sẻ, các hoạt động sinh viên cấp trường nổi bật hằng năm, các hoạt động nổi bật khác, hoạt động tự hào sinh viên nông lâm, ngày hội sinh viên nông lâm với pháp luật, hội thao sinh viên nông lâm, cuộc thi khởi nghiệp nông nghiệp, cuộc thi ý tưởng nghiên cứu khoa học, hội thảo nghiên cứu khoa học sinh viên, chiến dịch tình nguyện mùa hè xanh, chương trình vì màu xanh nông lâm, chiến dịch xuân tình nguyện, chương trình hiến máu tình nguyện, lễ tuyên dương thanh niên tiên tiến làm theo lời bác và trao giải thưởng nguyễn thái bình, lễ tuyên dương sinh viên 5 tốt, lễ tuyên dương hoạt động học thuật, khoa học công nghệ, khởi nghiệp, cuộc thi nét đẹp sinh viên nông lâm, hội thi bí thư chi đoàn giỏi, hội thi thủ lĩnh sinh viên, chương trình vì đàn em thân yêu, chương trình ánh trăng cho em, ngày thứ 7 tình nguyện, ngày chủ nhật xanh, chương trình vì nụ cười trẻ thơ, chương trình về nguồn, hành trình đi tìm địa chỉ đỏ, hành trình đến với bảo tàng, hội thi kiến thức chuyên ngành, đào tạo, nghiên cứu, chuyển giao công nghệ, hợp tác quốc tế, trường đại học tiên tiến, khu vực, thế giới, hệ thống quản lý, quản trị, nhân sự, tinh thần sáng tạo, khởi nghiệp, nguồn lực, môi trường học thuật, nghiên cứu khoa học, phục vụ cộng đồng, cơ sở giáo dục đại học, việt nam, hệ thống cơ sở vật chất, công nghệ thông tin, quản lý, kế hoạch chiến lược giai đoạn 2021-2025, 2035, 03 nhóm chiến lược cốt lõi, đào tạo, nghiên cứu và phát triển khoa học công nghệ, phục vụ cộng đồng, 06 nhóm chiến lược bổ trợ, phát triển nguồn nhân lực, bảo đảm chất lượng giáo dục, hợp tác trong nước và quốc tế, phát triển công nghệ thông tin, đầu tư phát triển cơ sở vật chất, phát triển tài chính, trường đại học nông lâm thành phố hồ chí minh, nong lam university - nlu, bộ giáo dục và đào tạo, thành phố thủ đức, thành phố hồ chí minh, thành phố dĩ an, tỉnh bình dương, 70 năm, huân chương lao động hạng ba, huân chương lao động hạng nhất, huân chương độc lập hạng ba, 1955, 1963, 1972, 1975, 1985, 1995, 2000, trường quốc gia nông lâm mục blao, trường cao đẳng nông lâm súc, học viện quốc gia nông nghiệp sài gòn, trường đại học nông nghiệp 4, trường đại học nông lâm nghiệp tp.hồ chí minh, trường đại học nông lâm (thành viên của học quốc gia tp.hồ chí minh), trường đại học đa ngành, nguồn nhân lực, chuyên môn, tư duy sáng tạo, phát triển, phổ biến, chuyển giao tri thức, công nghệ, phát triển bền vững, kinh tế - xã hội, trường đại học nghiên cứu, chất lượng quốc tế, sinh hoạt công dân - sinh viên (shcd - sv), https://go.hcmuaf.edu.vn/lichshcd2024, tân sinh viên, sinh viên năm 2, năm 3 và năm cuối, hướng dẫn phương pháp học đại học, sử dụng các tiện ích online, sử dụng thư viện, đăng ký môn học, phổ biến quy chế học vụ, giới thiệu các hoạt động đoàn - hội và phong trào sinh viên, định hướng nghề nghiệp - khởi nghiệp, thông tin tình hình kinh tế - chính trị - xã hội, học tập và làm theo tư tưởng, đạo đức, phong cách hồ chí minh, đại học nông lâm tp.hcm, ngành học, khoa, đội ngũ cố vấn học tập, sinh viên, chương trình đào tạo, kế hoạch học tập, học kỳ, khóa học, năng lực, hoàn cảnh, điều kiện học tập, học phần, kết quả học tập, biện pháp hỗ trợ, ban cố vấn học tập, website, phòng công tác sinh viên, http://nls.hcmuaf.edu.vn/, sinh viên 5 tốt, sinh viên việt nam, sinh viên trường đại học nông lâm tp.hcm, đảng, pháp luật, quy chế, nội quy, trường, nơi công cộng, điểm rèn luyện, năm học, sinh viên năm nhất, 21 điểm, 6 điểm, khoa/bộ môn, cuộc thi học thuật, clb học thuật, 06 tháng, bài viết, cơ quan truyền thông uy tín, báo, tạp chí khoa học chuyên ngành, hội đồng, sinh viên khuyết tật, giấy khen, sinh viên khối ngành ngoại ngữ, 7.0/10, câu lạc bộ, ủy viên ban chấp hành, cơ sở đoàn, hội, thành viên ban điều hành, hội sinh viên, bằng khen, đoàn – hội, hiến máu tình nguyện, 02 lần, đội, nhóm, tuyên truyền, vận động hiến máu tình nguyện, xã, phường, phương tiện truyền thông đại chúng, thanh niên tiêu biểu, lễ tuyên dương sinh viên tiêu biểu, sinh viên tiêu biểu, thành tích học tập, rèn luyện, danh hiệu sinh viên tiêu biểu, loại khá, loại tốt, hoạt động đoàn-hội sv, điểm, hoạt động chính trị, hoạt động xã hội, hoạt động văn hóa, hoạt động văn nghệ, hoạt động thể thao, tội phạm, tệ nạn xã hội, cán bộ lớp, đoàn thể, tổ chức, thành tích, học tập, 100 điểm, ý thức, thái độ, câu lạc bộ học thuật, hoạt động học thuật, hoạt động ngoại khóa, kỳ thi, cuộc thi, ngành, cơ quan chỉ đạo cấp trên, quy định, hoạt động rèn luyện, hoạt động công ích, hoạt động tình nguyện, công tác xã hội, nhà nước, chính sách, xuất sắc, tốt, khá, trung bình, yếu, kém, 90 điểm, 80 điểm, 65 điểm, 50 điểm, 35 điểm, khiển trách, cảnh cáo, đình chỉ học tập, buộc thôi học, http://sv.hc-muaf.edu.vn/diemrenluyen, thủ khoa, á khoa, olympic các môn học, cuộc thi sáng tạo kỹ thuật, cuộc thi văn hóa, cuộc thi văn nghệ, cuộc thi thể thao, ký túc xá, phong trào toàn dân bảo vệ an ninh tổ quốc, 500 sinh viên, 01 svtb, 500 đến 1.000 sinh viên, 02 svtb, 1.000 sinh viên, 04 svtb, 5%, đtbtl, 90 sinh viên, 01 thủ khoa, 01 á khoa, 25 đến 89 sinh viên, 25 sinh viên, hội đồng khen thưởng và kỷ luật sinh viên, khối lớp, 60 sinh viên, hiệu trưởng, 03 tháng, hội đồng khen thưởng, kỷ luật sinh viên, trưởng khoa, bản tường trình, bản tự kiểm điểm, lớp trưởng, trợ lý quản lý sinh viên, biên bản họp, tài liệu, quyết định kỷ luật, gia đình sinh viên, địa phương, giờ học, giờ thực tập, 5-10 điểm rèn luyện, thầy, cô giáo, cbvc nhà trường, thi, kiểm tra, tiểu luận, đồ án, khóa luận tốt nghiệp, cơ quan chức năng, pháp luật, phòng thi, đề thi, bài thi, học phí, bảo hiểm y tế, ktx, tài sản, rượu, bia, đình chỉ có thời hạn, thuốc lá, đánh bạc, sản phẩm văn hóa đồi trụy, hoạt động mê tín dị đoan, hoạt động tôn giáo trái phép, ma túy, mại dâm, vũ khí, chất nổ, hàng cấm, phần tử xấu, đánh nhau, biểu tình, truyền đơn, áp phích, hình ảnh, an ninh quốc gia, internet, quấy rối, dâm ô, an toàn giao thông, hồ sơ, văn bằng, chứng chỉ, văn bằng tốt nghiệp, lần 1, lần 2, lần 3, quy chế đào tạo, quy chế công tác hssv, quy định đối với hssv nội ngoại trú, quy định về việc thực hiện nếp sống văn hóa học đường, quy định về giờ giấc học tập, thầy cô, bài tập, đề tài, hoạt động học tập, phong trào thi đua, tổ chức đoàn thể, hoạt động khởi nghiệp, hoạt động phục vụ cộng đồng, giảng viên, nhân viên nhà trường, bạn bè, cử chỉ, cơ sở vật chất, thiết bị dạy và học, môi trường sống, khu vực hiệu bộ, giờ làm việc, khu giảng đường, phòng học, thông tin học bổng khuyến khích học tập, bidv, khách hàng, mã sinh viên, 01 liên chứng từ, cán bộ bidv, bidv smart banking, điện thoại di động, số điện thoại di động, mật khẩu, học phí_lệ phí thi, nhà cung cấp, mã khách hàng, otp, hóa đơn, báo cáo giao dịch, www.bidv.com.vn, tên đăng nhập, thanh toán hóa đơn, thanh toán hóa đơn từng lần, tài khoản, số hóa đơn, số tiền, bidv online, hộp thư/hộp thư đến, atm, thanh toán, tài khoản thanh toán, học phí– lệ phí thi, có, biên lai, chuyển khoản, https://dkmh.hcmuaf.edu.vn/, đóng tiền học phí, bill, thanh toán học phí qua bidv, hình thức thanh toán, số tài khoản, bidv smartbanking, cài đặt sinh trắc học, 10.000.000 đồng, giấy tờ tùy thân, cccd, qr, chip cccd, khuôn mặt, đã thu nhập cấp độ 2, người có thẩm quyền, email, đơn, bản in, điện thoại, phòng đào tạo, giáo viên chủ nhiệm, cố vấn học tập, số tín chỉ, chuyên ngành đào tạo, giáo viên giảng dạy, đề cương chi tiết học phần, điểm bộ phận, ngân hàng câu hỏi thi, tài liệu học tập, tài liệu tham khảo, khiếu nại, đình chỉ thi, khoa chuyên môn, giáo vụ khoa, ban chủ nhiệm khoa, điều kiện tốt nghiệp, thẻ sinh viên, bộ phận quản lý đăng ký trực tuyến, 3 tuần, môn học, thời khóa biểu, cơ sở dữ liệu, trang web, lớp học phần, văn bản pháp lý, tài khoản cá nhân, cán bộ giảng dạy, trợ lý giáo vụ, phòng chức năng, thông tin, điều 4, đơn vị chức năng, ban giám hiệu, chương 3, bcn khoa, trưởng phòng đào tạo, danh sách lớp học phần, danh sách bổ sung, đăng ký, rút học phần, điểm thi kết thúc học phần, điểm thi, trưởng bộ môn, bộ môn, điểm học phần, giáo viên, giấy tờ, vay vốn ngân hàng chính sách xã hội, tạm hoãn nghĩa vụ quân sự, đi xe buýt, bổ sung hồ sơ nhận trợ cấp, bổ sung hồ sơ làm lại thẻ sinh viên, bổ sung hồ sơ thuế cho người thân, bổ sung hồ sơ ký túc xá đại học quốc gia tp.hcm, bổ sung hồ sơ thi học kỳ, bổ sung hồ sơ thi acces, bổ sung hồ sơ lý lịch cá nhân, bổ sung hồ sơ nhận học bổng, bổ sung hồ sơ giảm trừ gia cảnh, bổ sung hồ sơ đi làm, bổ sung hồ sơ đi thực tập, https://nlsonline.hcmuaf.edu.vn/gxn/dangnhap.php, trình duyệt web, máy tính để bàn, máy tính xách tay, máy tính bảng, thông tin cá nhân, giấy xác nhận, cán bộ phòng công tác sinh viên, thời gian, hệ thống, bước 4, tổ tham vấn tâm lý học đường, tham vấn trực tiếp, tham vấn online, radio nông lâm, chuyên gia tư vấn, cán bộ, tổ tư vấn tâm lý học đường, g.05, nhà thiên lý, tuvantamly@hcmuaf.edu.vn, https://nls.hcmuaf.edu.vn, 0283 897 4560, sinh viên hệ chính quy, thời gian thiết kế chương trình đào tạo, học bổng, 01 suất học bổng, học bổng chính sách, trợ cấp xã hội, chính sách ưu đãi, học bổng khuyến khích học tập, khối học bổng, chương trình tiên tiến, giai đoạn dự bị anh văn, trình độ anh văn, quỹ học bổng khuyến khích học tập, chương trình đại trà, 8%, tổng thu học phí, chương trình chất lượng cao, 3%, cơ sở chính, khối ngành 1, khối ngành 3, khối ngành 4, khối ngành 5, khối ngành 7, ngành công nghệ thực phẩm, ngành chăn nuôi thú y, phân hiệu gia lai, phân hiệu ninh thuận, khối cao đẳng, công thức, 𝑞𝑖, 𝑄, 𝑛𝑖, 𝑁, điểm trung bình chung học bổng, thang điểm 10, 15 tín chỉ, học kỳ cuối, 08 tín chỉ, 7,0, 5 điểm, 70, học bổng loại khá, học bổng loại giỏi, 8,0, 80, học bổng loại xuất sắc, 9,0, 90, mức trần học phí, nhóm ngành, chính phủ, 20%, 30%, hội đồng xét duyệt, điểm trung bình chung tích lũy, 2 chữ số thập phân, học bổng tài trợ, quỹ “đồng hành cùng trường đại học nông lâm tp.hcm”, cựu sinh viên, doanh nghiệp, cá nhân, hoàn cảnh khó khăn, hộ nghèo, mồ côi cha mẹ, hoàn cảnh khó khăn đột xuất, thiên tai, tai nạn, thành tích cao, hoạt động cộng đồng, đoàn - hội, chương trình học bổng, 6 tỷ đồng, tiền mặt, khóa học đào tạo ngắn hạn, tin học, ngoại ngữ, học bổng đồng hành, điều kiện, đối tượng, quy trình, thủ tục, hồ sơ học bổng, email sinh viên, website phòng công tác sinh viên, https://nls.hcmuaf.edu.vn/, bảo hiểm tai nạn, tai nạn giao thông, tai nạn sinh hoạt, tiêm ngừa bệnh dại, động vật cắn, giờ hành chính, thứ 2 đến thứ 6, hàng tuần, hồ sơ yêu cầu bồi thường, giấy yêu cầu trả tiền bảo hiểm, biên bản tường trình tai nạn, giấy phép lái xe, cà vẹt xe, hồ sơ điều trị thương tật, giấy ra viện, giấy phẫu thuật, phim x.quang, phim mri, đơn thuốc, bệnh viện/cơ sở y tế, biên bản tai nạn giao thông, chính quyền, giấy chứng tử, ủy quyền thừa kế, kết quả nồng độ cồn, sổ tiêm ngừa bệnh dại, luật bảo hiểm y tế 2008, 2014, thẻ bảo hiểm y tế, cn, bt, hn, dt, dk, xd, ts, tc, tq, tv, ta, ty, hg, pv, mức đóng, 4,5%, mức lương cơ sở, số tháng, 70%, quốc hội, https://bhytsv.hcmuaf.edu.vn, thẻ, baohiemxahoi.gov.vn, trung tâm dịch vụ sinh viên, sinh viên nội trú, ăn, ở, sinh hoạt, dịch vụ, kỹ năng ngoại khóa, nhà khách, giữ xe, căn tin, photocopy, internet, phương tiện vận chuyển, văn phòng trung tâm dịch vụ sinh viên, đường số 6, 028-38963346, ttdvsv@hcmuaf.edu.vn, quỹ tín dụng học tập, 1998, ngân hàng chính sách xã hội (nhcsxh), vốn vay, phương tiện học tập, sách vở, ăn, ở, đi lại, sinh viên mồ côi, hộ gia đình, hộ cận nghèo, mức sống trung bình, gia đình, bệnh tật, hỏa hoạn, dịch bệnh, ủy ban nhân dân xã, phường, thị trấn, học sinh, sinh viên, giấy báo trúng tuyển, cờ bạc, nghiện hút, trộm cắp, buôn lậu, 4.000.000 đ/tháng/sinh viên, 0,65%/tháng, ngân hàng chính sách xã hội, giấy xác nhận vay vốn, đảng cộng sản việt nam, đoàn tncs hồ chí minh, hội sinh viên việt nam, hội liên hiệp thanh niên việt nam, nhà giáo, ctđt, cvht, khht, học phần, website, điểm f, 12 tín chỉ, lý thuyết, thực hành, giáo dục thể chất, 30 sinh viên, 60 sinh viên, 200 sinh viên, 20 sinh viên, 25 sinh viên, 50 sinh viên, 40 sinh viên, phòng quản lý chất lượng, bộ môn lý luận chính trị, điểm i, điểm 0, điểm thực hành, điểm thi kết thúc học phần, hội đồng khoa, điểm m, điểm d, đtbchk, đtbcnh, đtbctl, trung bình, cử nhân, kỹ sư, 50%, bảng điểm cá nhân, điểm rèn luyện, học kỳ chính, học kỳ phụ, thang điểm 100, thông tư số 16/2015/tt-bgdđt, đrl, hồ sơ quản lý sinh viên, bảng điểm toàn khóa, học bổng, khóa luận, tiểu luận, 10 tín chỉ, bác sỹ thú y, 5 tín chỉ, 6 tín chỉ, chuẩn đầu ra, ngoại ngữ không chuyên, tin học không chuyên, điểm trung bình tích lũy, bằng tốt nghiệp, chứng nhận, hội đồng xét tốt nghiệp khoa, hội đồng xét tốt nghiệp trường, biên bản xét tốt nghiệp, phụ lục văn bằng, giấy chứng nhận tốt nghiệp tạm thời, bản sao bằng tốt nghiệp, bản sao phụ lục văn bằng, kết quả đã học, lực lượng vũ trang, cơ quan có thẩm quyền, giải đấu quốc tế, bộ y tế, học phí, kết quả học phần, minh chứng, chương trình, ngành, quyền lợi, tốt nghiệp, điểm c, giảng dạy trực tuyến, giảng dạy online – offline, dịch bệnh, thiên tai, hệ thống đào tạo trực tuyến, e-learning – nlu, cổng đào tạo trực tuyến, hệ thống quản lý học tập, học liệu điện tử, diễn đàn trao đổi, thảo luận trực tuyến, hệ thống kiểm tra, đánh giá sinh viên, edmodo, thi cuối kỳ, thực hành, thực tập, tài khoản, lớp học, diễn đàn thảo luận, hồ sơ cá nhân, hình đại diện, chữ ký, đường link lớp học, nhiệm vụ, 05 - 10 phút, email, micro, camera, raise hand, lower hand, màn hình cá nhân"
Loại quan hệ: "website, có, là, tôn_trọng, theo, hủy, in, dưới, bị, mời, đối_với, của, gửi, không, gồm, trong, từ, email, công_bố, BAO_GỒM, sở_hữu, số_điện_thoại, thuộc_khoa, chương_trình_tiên_tiến_tại, chương_trình_nâng_cao_tại, chương_trình_đào_tạo_tại, quản_lý_bởi, chủ_nhiệm, trưởng_ban_điều_hành, đội_trưởng, số_lượng_sách, sử_dụng, số_lượng_phòng, sức_chứa, bao_gồm, về, sánh_vai, trên, đổi_mới, thúc_đẩy, phát_huy, xây_dựng, trở_thành, hàng_đầu, đáp_ứng, tầm_nhìn, tên_khác, trực_thuộc, tọa_lạc_tại, thuộc, thời_gian_hoạt_động, nhận_giải_thưởng, thành_lập, phục_vụ, đào_tạo, và, mục_tiêu_đến, sẽ_trở_thành, với, tổ_chức_bởi, được_đăng_tại, gìn_giữ_và_phát_huy, phát_hiện, nâng_đỡ, cho, đề_cao, hoạt_động_của, dành_cho, hỗ_trợ, tư_vấn, phù_hợp, hướng_dẫn, đăng_ký, ở, điều_chỉnh, xác_nhận, theo_dõi, cập_nhật_trên, không_dưới, ít_nhất, xem_xét, cấp, tham_gia, trường, tổ_chức, vào_cuối, tuyên_dương, khen_thưởng, căn_cứ, đánh_giá, phòng_chống, đạt, thang_điểm, chấp_hành, đến, không_vượt_quá, đánh_giá_qua, đoạt_giải, có_thành_tích, đóng_góp, hoạt_động_tại, thực_hiện, bảo_đảm_an_ninh, ít_hơn_hoặc_bằng, chọn, cao_nhất, cao_thứ_hai, bằng_nhau, công_nhận, xét, áp_dụng_bởi, thông_báo, gửi_thông_báo, làm, tham_dự, sau, chấm_dứt, trừ, vô_lễ, lần_1, giao_cho, hạ_điểm, tài_sản_trong, làm_hư_hỏng, lần_2, lần_3, trái, xâm_phạm, chống_phá, thu_hồi, lắng_nghe, hoàn_thành, nghiêm_túc, phát_động, hỏi, trả_lời, làm_phiền, quan_hệ, không_gây_ồn_ào, giữ_gìn, cung_cấp, nhận, dấu_và_chữ_ký, truy_cập, nhập, thanh_toán, hiển_thị, lưu, tại, tương_ứng, phản_hồi, đăng_nhập, chụp_ảnh, quét, đọc, lấy_ảnh, kiểm_tra, trạng_thái, chuyển_tới, viết, trực_tuyến, không_chấp_nhận, nộp, trao_đổi, thắc_mắc, đề_nghị, mang, được_hỗ_trợ, đi_học, chưa_được_sửa, mất, giúp_đỡ, nêu, hoặc, ghi, chuyển, ký, đã, kèm, giải_quyết, loại, bổ_sung, cập_nhật, trình_ký, đóng_dấu, hoạt_động, liên_hệ, như, cùng, xếp, so_sánh, không_cần, bằng, bố_trí, trọng_số, không_bị, quyết_định, cao_hơn, hơn, lập, trình, làm_tròn, trích_từ, do, phối_hợp, trị_giá, một_lần, qua, mỗi, đóng_mộc, sửa_đổi, mã, nhân, tra_cứu, quản_lý, điện_thoại, thành_lập_từ, vay, để, giúp, thủ_tục, gặp_khó_khăn, cư_trú, sinh_sống, đủ_tiêu_chuẩn, tối_đa, lãi_suất, thông_qua, trả_nợ, đóng_trụ_sở, tuân_thủ_quy_định_của, học_tập_tại, được_tôn_trọng_bởi, được_cung_cấp, được_sử_dụng, hoạt_động_trong, kiến_nghị_với, đề_đạt_nguyện_vọng_lên, được_ở, được_nhận, tuân_thủ_chủ_trương_của, tuân_thủ_pháp_luật_của, tuân_thủ_quy_chế_của, đóng, không_được_xúc_phạm, không_được_tham_gia, không_được, không_được_tổ_chức_hoạt_động_mà_chưa_được_cho_phép, cung_cấp_ctđt_cho, tư_vấn_xây_dựng_khht_cho, thông_báo_học_phần_cho, hướng_dẫn_đăng_ký_cho, thực_hiện_theo, đăng_ký_học_lại, cải_thiện_điểm, cho_phép_đăng_ký_ít_hơn_14_tín_chỉ, rút, không_đi_học, không_dự_thi, nhận_điểm_r, nhận_điểm_f, rút_học_phần_trên, đề_xuất_hủy_hoặc_mở_thêm, đăng_ký_trực_tuyến, công_bố_kết_quả_đăng_ký_cho, cải_thiện_kết_quả, đề_xuất, duy_trì, phê_duyệt_duy_trì, đề_xuất_mở_thêm, chấp_thuận_mở_thêm, mở_thêm, dự_thi, đề_xuất_cấm_thi, duyệt_danh_sách_cấm_thi, tối_thiểu, chuẩn, được_quy_định_trong, thông_báo_cho, thông_báo_lịch_thi, hưởng, chấp_thuận, duyệt_đơn, tổ_chức_thi_cho, xét_tương_đương, quy_định, rà_soát, phê_duyệt, xác_định, đồng_ý, không_đạt, tính_vào, xử_lý, xem_kết_quả, được_đánh_giá, tính, không_tính, dựa_vào, trung_bình_cộng, kỷ_luật, không_tham_gia, xếp_loại, lưu_trong, ghi_vào, đình_chỉ, tiêu_chí, cho_phép, chuyển_sang, cấp_bằng, chấm, thỏa_mản, phân_công, tổ_chức_bảo_vệ, thảo_luận, gia_hạn, quyết_định_gia_hạn, không_hoàn_thành, tích_lũy, ra_quyết_định, được_cấp, báo, bảo_lưu, được_điều_động, cần, theo_quy_định, học_xong, nghỉ, được_công_nhận, học, vượt_quá, nghiên_cứu, bổ_sung_vào, tăng_cường, áp_dụng, chỉ_đạo, phát_triển_trên, không_tổ_chức, giữ_bí_mật, bảo_vệ, chịu_trách_nhiệm, trước, nhấn, mở, tắt, bấm, chia_sẻ"

Câu hỏi: {question}
Cần có tài liệu để trả lời câu hỏi đã cho, và mục tiêu là tìm kiếm các tài liệu hữu ích. Mỗi thực thể trong biểu đồ tri thức được liên kết với một tài liệu. 
Dựa trên các thực thể và quan hệ đã trích xuất, graph hay text hữu ích hơn để thu hẹp không gian tìm kiếm? Bạn phải trả lời bằng một trong hai từ, không quá hai từ."""
#     return """
# Bạn là một tác tử thông minh có nhiệm vụ trả lời câu hỏi của người dùng bằng cách sử dụng một trong các công cụ sau:
# Công cụ tìm kiếm văn bản: Dùng để tìm kiếm thông tin trong tài liệu văn bản.
# Công cụ truy vấn đồ thị: Dùng để tìm kiếm thông tin về các thực thể và mối quan hệ trong đồ thị tri thức.
# Câu hỏi: {question}
# Hãy suy nghĩ về loại thông tin cần thiết để trả lời câu hỏi này.
# Nếu câu hỏi chủ yếu cần thông tin chi tiết hoặc ngữ cảnh, bạn nên sử dụng công cụ tìm kiếm văn bản(text).
# Nếu câu hỏi chủ yếu hỏi về mối quan hệ giữa các đối tượng hoặc thực thể, bạn nên sử dụng công cụ truy vấn đồ thị(graph).
# Dựa trên phân tích của bạn, hãy chọn công cụ phù hợp nhất để thu hẹp không gian tìm kiếm và trả lời 'graph' hoặc 'text'. Trả lời không quá 2 từ"""

def reflection_stsv():
    return """
Tài liệu đã truy xuất không chính xác.
Câu hỏi: {question}
Phản hồi: {feedback}
Tài liệu đã truy xuất không chính xác. Hãy trả lời lại dựa trên các thực thể chủ đề và quan hệ hữu ích mới được trích xuất. graph hay text hữu ích hơn để thu hẹp không gian tìm kiếm? Bạn phải trả lời bằng một trong hai từ, không quá hai từ."""
#     return """
# Câu hỏi: {question}
# Phản hồi: {feedback}
# Dựa trên phản hồi từ người bình luận, hãy suy nghĩ về những điều sau để cải thiện trong lần thử tiếp theo:
# 1. Nếu người bình luận cho rằng bạn đã chọn sai công cụ, thì hãy chọn công cụ khác(nếu graph thì text, nếu text thì graph)
# 2. Nếu người bình luận chỉ ra các thực thể hoặc mối quan hệ bị bỏ lỡ hoặc xác định sai, hãy đảm bảo bạn tập trung vào những yếu tố này trong lần truy xuất tiếp theo.
# 3. Hãy ghi nhớ mọi phản hồi khác và cố gắng điều chỉnh hành động của bạn để giải quyết những vấn đề đó.
# Trả lời bằng 'graph' hoặc 'text'. Trả lời không quá 2 từ
# """

def generator_stsv():
    return """
Nhiệm vụ của bạn là dựa vào câu hỏi và các tài liệu khả thi mà tôi cung cấp, hãy trả lời câu hỏi:
Câu hỏi: {question}
Tài liệu khả thi: {references}
Nếu tài liệu khả thi không có câu trả lời thì phản hồi 'Tài liệu không có thông tin'
Nếu tài liệu khả thi bị lặp lại thì hãy phản hồi 'Câu trả lời không đổi' """

def valid_stsv():
    return """
Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu.
Câu hỏi: {question}
Câu trả lời: {answer}
Tài liệu khả thi: {references}
Nhiệm vụ: Tài liệu có phù hợp với các yêu cầu của câu hỏi không? Trả lời chỉ bằng 'yes' hoặc 'no'."""
#     return """
# Bạn là một trình xác thực có nhiệm vụ đánh giá tính chính xác của một câu trả lời. Dưới đây là thông tin liên quan:
# Câu hỏi: {question}
# Câu trả lời: {answer}
# Tài liệu khả thi: {references}
# Để biết câu trả lời có đầy đủ chi tiết, đúng ý nghĩa câu hỏi và không bỏ sót bất kỳ thông tin nào cần dựa vào các yếu tố sau:
# Dựa trên những thông tin này, hãy trả lời 'yes' hoặc 'no'. Trả lời không quá 2 từ"""

def commentor_stsv():
    return """
Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu.
Câu hỏi: {question}
Thực thể chủ đề: <<<các thực thể đã trích xuất>>>
Quan hệ hữu ích: <<<các quan hệ đã trích xuất>>>
Vui lòng chỉ ra thực thể hoặc quan hệ nào được trích xuất sai từ câu hỏi, nếu có.
    """
#     return """
# Bạn là một người bình luận có nhiệm vụ cung cấp phản hồi mang tính xây dựng cho tác tử để cải thiện khả năng trả lời câu hỏi. Dưới đây là thông tin liên quan:
# Câu hỏi: {question}
# Câu trả lời: {answer}
# Tài liệu khả thi: {references}
# Trình xác thực đã đánh giá rằng câu trả lời này không chính xác. Hãy phân tích quá trình truy xuất của tác tử và đưa ra phản hồi cụ thể để giúp tác tử cải thiện.
# Bạn có nghĩ tác tử đã chọn sai công cụ truy xuất không? Nếu có, hãy phản hồi "Tác tử đã chọn sai công cụ"
# Có thực thể hoặc mối quan hệ nào trong câu hỏi mà tác tử có thể đã bỏ lỡ hoặc xác định sai không?
# Phản hồi khác (nếu có):"""

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
    trong đó:
        Thuộc tính 'episode': lấy tất cả thông tin
        Thuộc tính 'part': chỉ lấy từ đầu cho đến ký tự "<<"
    
    câu hỏi cần dự đoán: {question}
    
    Dưới đây là mục lục mà bạn cần dự đoán
    "Phần 1: NLU - Định hướng trường đại học nghiên cứu:
    Quá trình hình thành và phát triển<<Lịch sử và các giai đoạn phát triển của trường>>.
    Sứ mạng<<Mục đích tồn tại và đóng góp của trường>>.
    Tầm nhìn<<Định hướng phát triển tương lai của trường>>.
    Giá trị cốt lõi <<Những nguyên tắc và niềm tin cơ bản của trường>>.
    Mục tiêu chiến lược <<Các mục tiêu cụ thể trường hướng tới>>.
    Cơ sở vật chất <<Giảng đường, thư viện, ký túc xá, trang thiết bị>>.
    Các đơn vị trong trường <<Danh sách các phòng, ban, trung tâm, viện>>.
    Các khoa - ngành đào tạo <<Danh sách các khoa và các ngành học>>.
    Tuần sinh hoạt công dân - sinh viên <<Hoạt động định hướng đầu khóa cho tân sinh viên>>.
    Hoạt động phong trào sinh viên <<Các hoạt động ngoại khóa, tình nguyện, văn nghệ, thể thao>>.
    Câu lạc bộ (CLB) - Đội, Nhóm <<Danh sách các CLB, đội, nhóm sinh viên hoạt động>>.
    Cơ sở đào tạo <<Địa chỉ các cơ sở chính và phân hiệu>>.
    
    Phần 2: HỌC TẬP VÀ RÈN LUYỆN:
    Quy chế sinh viên <<Quyền lợi, nghĩa vụ và những điều sinh viên không được làm>>.
    Quy chế học vụ <<Quy định về đăng ký, học tập, thi cử, đánh giá, tốt nghiệp>>.
    Quy định về việc đào tạo trực tuyến <<Quy tắc và cách thức học tập online tại trường>>.
    Quy định khen thưởng, kỷ luật sinh viên <<Các hình thức, tiêu chuẩn khen thưởng và xử lý vi phạm>>.
    Quy chế đánh giá kết quả rèn luyện <<Tiêu chí và cách thức đánh giá điểm rèn luyện>>.
    Quy tắc ứng xử văn hóa của người học <<Chuẩn mực giao tiếp, hành vi trong môi trường học đường>>.
    Cố vấn học tập <<Vai trò và nhiệm vụ của người hỗ trợ sinh viên học tập>>.
    Danh hiệu sinh viên 5 tốt <<Tiêu chí phấn đấu để đạt danh hiệu cao quý này>>.
    Danh hiệu sinh viên tiêu biểu << Tiêu chí xét chọn sinh viên xuất sắc hàng năm>>.
    
    Phần 3: HỖ TRỢ VÀ DỊCH VỤ:
    Quy định phân cấp giải quyết thắc mắc của sinh viên <<Quy trình gửi và giải đáp các vấn đề của sinh viên>>.
    Thông tin học bổng <<Các loại học bổng (khuyến khích, tài trợ) và cách xét duyệt>>.
    Vay vốn học tập từ ngân hàng chính sách xã hội <<Hướng dẫn thủ tục vay vốn hỗ trợ học phí, sinh hoạt>>.
    Quy trình xác nhận hồ sơ sinh viên <<Cách đăng ký và nhận các giấy xác nhận cần thiết>>.
    Hồ sơ yêu cầu bồi thường bảo hiểm tai nạn <<thủ tục cần chuẩn bị khi có tai nạn xảy ra>>.
    Thông tin về bảo hiểm y tế <<Quy định bắt buộc và cách thức tham gia BHYT>>.
    Thông tin học bổng tài trợ <<Học bổng tài trợ (>6 tỷ/năm) từ Quỹ Đồng hành hỗ trợ SV khó khăn/thành tích cao/năng động>>
    Hướng dẫn sử dụng các kênh thanh toán <<Cách nộp học phí, BHYT qua ngân hàng, website>>.
    Tham vấn tâm lý học đường <<Dịch vụ hỗ trợ tinh thần, giải tỏa căng thẳng cho sinh viên>>.
    Trung tâm Dịch vụ Sinh viên <<hông tin về ký túc xá, nhà ăn và các dịch vụ hỗ trợ khác>>."
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
