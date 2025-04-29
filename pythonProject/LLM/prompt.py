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
Các có tài liệu để trả lời câu hỏi đã cho và mục tiêu là tìm kiếm các tài liệu hữu ích. Mỗi thực thể trong biểu đồ tri thức được liên kết với một tài liệu. 
Dựa trên các thực thể và quan hệ đã trích xuất, 'graph' hay 'text' hữu ích hơn để thu hẹp không gian tìm kiếm? Bạn phải trả lời bằng một trong hai từ, không quá hai từ."""

def reflection_stsv():
    return """
Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu. Hãy phản hồi dựa trên yêu cầu sau:
1. Nếu feedback là 'Tài liệu đã truy xuất không đúng. Mô-đun truy xuất hiện tại có thể không hữu ích để thu hẹp không gian tìm kiếm.' thì hãy sử dụng nguồn truy xuất khác với bước trước đó. Nếu trước đó dùng 'graph' thì chuyển sang 'text' và ngược lại, Bạn phải trả lời bằng một trong hai từ. Trả lời không quá hai từ.
Câu hỏi: {question}
feedback: {feedback}
"""

def generator_stsv():
    return """
Bạn là chuyên gia trả lời câu hỏi dựa trên tài liệu cung cấp, tuân theo khuôn mẫu. Nhiệm vụ:
1. Trả lời chính xác dựa trên tài liệu, không thêm, bớt, chỉnh sửa nội dung.
2. Trình bày rõ ràng, liệt kê (nếu có) đánh số thứ tự và in đậm.
3. Nếu thiếu thông tin, trả lời: "Không có thông tin". Nếu có, diễn đạt lại.
4. Chỉ trả lời, không giải thích thêm.

Câu hỏi: {question}
Tài liệu: {references}
"""
# Nếu không có thông tin thì nói 'không có thông tin'. Không giải thích gì thêm.
def valid_stsv():
    return """
Bạn là trợ lý phân tích câu trả lời theo khuôn mẫu.

Câu hỏi: {question}
Câu trả lời: {answer}

Nhiệm vụ:
1. Xác định đối tượng của câu trả lời (ai, bao nhiêu...).
2. Kiểm tra câu trả lời có khớp với câu hỏi không:
2.1 Nếu khớp, trả lời "yes".
2.2 Nếu không khớp hoặc câu trả lời là "Không có thông tin", trả lời "no".
Trả lời: Chỉ 1 từ ("yes" hoặc "no")."""

def commentor_stsv():
    return """
Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu.
Câu hỏi: {question}
Tài liệu khả thi: {references}
Nếu tài liệu khả thi không thể trả lời câu hỏi thì phản hồi 'Tài liệu đã truy xuất không đúng. Mô-đun truy xuất hiện tại {current_module} có thể không hữu ích để thu hẹp không gian tìm kiếm.'
"""

def extract_entities_relationship_from_text():
    return """
    Bạn là một hệ thống trích xuất thông tin từ văn bản. Tuân theo khuôn mẫu, Nhiệm vụ của bạn là:

1. Trích xuất tất cả các thực thể có trong đoạn văn bản.
   - Mỗi thực thể cần có tên(name) và loại(type).  
   - Loại của thực thể (ví dụ: person, organization, location, date, v.v.) phải được ghi bằng tiếng anh, nếu có 2 từ trở lên thì phân cách nhau bởi dấu "_".

2. Xác định các mối quan hệ giữa các thực thể.  
   - Mỗi mối quan hệ phải có nguồn(source), đích(target) và tên mối quan hệ(relation).  
   - Tên mối quan hệ phải được ghi thường, tiếng việt, có dấu, nếu có 2 từ trở lên thì phân cách nhau bởi dấu "_".(ví dụ: "THỦ_ĐÔ_CỦA", "TẠO_RA").  
   - Nếu một mối quan hệ có ý nghĩa giống nhau ở nhiều trường hợp, hãy thống nhất sử dụng một tên mối quan hệ duy nhất và không thêm từ gì khác. Ví dụ: nếu "tphcm ở việt nam" được quy định là mối quan hệ "Ở", thì với mọi trường hợp tương tự, mối quan hệ phải là "Ở".

3. Trả về kết quả dưới dạng JSON với các trường:
   - "entities": Danh sách các thực thể. Mỗi thực thể có các thuộc tính "name" và "type".
   - "relationships": Danh sách các mối quan hệ. Mỗi mối quan hệ có các thuộc tính "source", "target", "type_source", "type_target" và "relation".

Đoạn văn bản cần trích xuất:
{question}

Yêu cầu:
- Trả về kết quả dưới dạng JSON với các trường: entities, relationships.
- Mỗi entity cần có name và type.
- Mỗi relationship cần có source, target, type_source, type_target và relation.

---
### Giải thích:
1. **Entity**:
   - Là các đối tượng được nhắc đến trong văn bản, ví dụ: tên người, địa điểm, tổ chức, ngày tháng, v.v.
   - Mỗi entity cần được gán một loại phù hợp, ví dụ: person, organization, location, date, v.v

2. **Relationship**:
   - Là mối quan hệ giữa các entity, ví dụ: "Alice knows Bob" → quan hệ Biết giữa Alice và Bob.

3. **Định dạng đầu ra**:
   - Sử dụng JSON để trả về kết quả một cách có cấu trúc, dễ dàng xử lý tiếp theo. """

def extract_question_from_text():
    return """nhiệm vụ của bạn là sẽ tạo ra TẤT CẢ các câu hỏi từ văn bản từ đầu đến cuối mà không bỏ xót 1 chi tiết nào, các câu hỏi viết chữ thường, chỉ tạo ra danh sách câu hỏi và không thêm bất cứ thông tin gì"""

# yêu cầu llm dự đoán câu hỏi sẽ thuộc về phần nào trong sổ tay sinh viên
def predict_question_belong_to(question):
    return f"""
    Bạn là một trợ lý hữu ích, tuân theo khuôn mẫu. Nhiệm vụ của bạn: 
    Đầu tiên, cần dự đoán câu hỏi sau nằm trong phần nào trong mục lục mà tôi cung cấp:

    câu hỏi cần dự đoán: {question}
    Mục lục:
    "part: phần 1: nlu - định hướng trường đại học nghiên cứu
        section: quá trình hình thành và phát triển  
        section: sứ mạng  
        section: tầm nhìn  
        section: giá trị cốt lõi  
        section: mục tiêu chiến lược  
        section: cơ sở vật chất  
        section: các đơn vị trong trường  
        section: các khoa - ngành đào tạo
        section: tuần sinh hoạt công dân sinh viên  
        section: hoạt động phong trào sinh viên  
        section: câu lạc bộ (clb) - đội, nhóm  
        section: cơ sở đào tạo  
    part: phần 2: học tập và rèn luyện
        section: quy chế sinh viên  
           part: chương 2: quyền và nghĩa vụ của sinh viên  
             article: điều 4: quyền của sinh viên  
             article: điều 5: nghĩa vụ của sinh viên  
             article: điều 6: các hành vi sinh viên không được làm  
        section: quy chế học vụ  
           part: chương 2: lập kế hoạch và tổ chức giảng dạy  
             article: điều 9: tổ chức đăng ký học tập  
             article: điều 10: tổ chức lớp học phần  
           part: chương 3: đánh giá kết quả học tập và cấp bằng tốt nghiệp  
             article: điều 12: tổ chức thi kết thúc học phần  
             article: điều 13: đánh giá và tính điểm học phần  
             article: điều 14: xét tương đương và công nhận học phần của các cơ sở đào tạo khác  
             article: điều 15: đánh giá kết quả học tập theo học kỳ, năm học  
             article: điều 16: thông báo kết quả học tập  
             article: điều 17: điểm rèn luyện (đrl)  
             article: điều 18: xử lý kết quả học tập  
             article: điều 19: khóa luận, tiểu luận, tích lũy tín chỉ tốt nghiệp  
             article: điều 20: công nhận tốt nghiệp và cấp bằng tốt nghiệp  
           part: chương 4: những quy định khác đối với sinh viên  
             article: điều 21: nghỉ học tạm thời, thôi học  
             article: điều 24: học cùng lúc hai chương trình  
        section: quy định về việc đào tạo trực tuyến  
           article: điều 3: hệ thống đào tạo trực tuyến tại trường đại học nông lâm tp.hcm  
           article: điều 9: đánh giá kết quả học tập trực tuyến  
           article: điều 13: quyền và trách nhiệm của sinh viên  
        section: quy định khen thưởng, kỷ luật sinh viên  
           part: chương 2: khen thưởng  
             article: điều 4: nội dung khen thưởng  
             article: điều 5: khen thưởng đối với cá nhân và tập thể sinh viên đạt thành tích xứng đáng để biểu dương, khen thưởng  
             article: điều 6: khen thưởng đối với sinh viên tiêu biểu (svtb) vào cuối mỗi năm học  
             article: điều 7: khen thưởng đối với sinh viên là thủ khoa, á khoa kỳ tuyển sinh đầu vào  
             article: điều 8: khen thưởng đối với sinh viên tốt nghiệp  
           part: chương 3: kỷ luật  
             article: điều 11: hình thức kỷ luật và nội dung vi phạm  
             article: điều 12: trình tự, thủ tục và hồ sơ xét kỷ luật  
             article: điều 13: chấm dứt hiệu lực của quyết định kỷ luật  
             article: một số nội dung vi phạm và khung xử lý kỷ luật sinh viên  
        section: quy chế đánh giá kết quả rèn luyện  
           article: điều 3: nội dung đánh giá và thang điểm  
           article: điều 4: đánh giá về ý thức tham gia học tập  
           article: điều 5: đánh giá về ý thức chấp hành nội quy, quy chế, quy định trong cơ sở giáo dục đại học  
           article: điều 6: đánh giá về ý thức tham gia các hoạt động chính trị, xã hội, văn hóa, nghệ thuật, thể thao, phòng chống tội phạm và các tệ nạn xã hội  
           article: điều 7: đánh giá về ý thức công dân trong quan hệ cộng đồng  
           article: điều 8: đánh giá về ý thức và kết quả khi tham gia công tác cán bộ lớp, các đoàn thể, tổ chức trong cơ sở giáo dục đại học hoặc người học đạt được thành tích đặc biệt trong học tập, rèn luyện  
           article: điều 9: phân loại kết quả rèn luyện  
           article: điều 10: phân loại để đánh giá  
           article: điều 11: quy trình đánh giá kết quả rèn luyện  
        section: quy tắc ứng xử văn hóa của người học  
           article: điều 4: ứng xử với công tác học tập, nghiên cứu khoa học, rèn luyện  
           article: điều 5: ứng xử đối với giảng viên và nhân viên nhà trường  
           article: điều 6: ứng xử với bạn bè  
           article: điều 7: xử với cảnh quan môi trường và tài sản công  
        section: cố vấn học tập  
        section: danh hiệu sinh viên 5 tốt  
           article: đạo đức tốt  
           article: học tập tốt  
           article: thể lực tốt  
           article: tình nguyện tốt  
           article: hội nhập tốt  
           article: khái niệm  
           part: ngoài ra ưu tiên xét chọn những sinh viên đạt ít nhất 01 trong các tiêu chuẩn sau:  
             article: ưu tiên 1  
             article: ưu tiên 2  
             article: ưu tiên 3  
             article: ưu tiên 4  
             article: ưu tiên 5  
             article: ưu tiên 6  
        section: danh hiệu sinh viên tiêu biểu  
    part: phần 3: hỗ trợ và dịch vụ
        section: quy định phân cấp giải quyết thắc mắc của sinh viên  
           article: điều 2: hình thức thắc mắc, kiến nghị  
           article: điều 3: các bước gửi thắc mắc, kiến nghị  
           article: điều 4: những vấn đề trao đổi trực tiếp hoặc gửi thư qua email  
           article: điều 5: trách nhiệm của giảng viên và các bộ phận chức năng  
           article: điều 6: những vấn đề đã trao đổi trực tiếp hoặc gửi thư không được giải quyết thỏa đáng  
           article: điều 7: những vấn đề liên quan đến tổ chức lớp học phần  
           article: điều 8: những vấn đề liên quan đến điểm bộ phận, điểm thi kết thúc học phần, điểm thi học phần và tổ chức thi  
           article: điều 9: chuyển thắc mắc, kiến nghị của sinh viên  
           article: điều 10: những nội dung được nói trực tuyến trên website  
           article: điều 11: yêu cầu đối với sinh viên tham gia trực tuyến  
        section: thông tin học bổng tài trợ  
        section: vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên  
           article: đối tượng sinh viên được hỗ trợ vay tiền  
           article: điều kiện để được hỗ trợ vay tiền sinh viên  
           article: mức tiền và lãi suất hỗ trợ vay tiền sinh viên  
           article: phương thức cho vay tiền sinh viên  
           article: thông tin về vay vốn học tập từ ngân hàng chính sách xã hội dành cho sinh viên  
        section: quy trình xác nhận hồ sơ sinh viên  
           article: các loại giấy tờ được xác nhận  
           article: kênh đăng ký  
           article: đăng ký  
           article: quy trình  
        section: hồ sơ yêu cầu bồi thường bảo hiểm tai nạn sinh viên  
        section: thông tin về bảo hiểm y tế  
        section: hướng dẫn sử dụng các kênh thanh toán học phí, bhyt, lệ phí xét tốt nghiệp
           article: thanh toán tại quầy giao dịch của bidv
           article: thanh toán qua kênh bidv smart banking
           article: thanh toán qua kênh bidv online  
           article: thanh toán qua atm của bidv  
           article: thanh toán qua website sinh viên  
           article: hướng dẫn cài đặt sinh trắc học  
        section: tham vấn tâm lý học đường  
        section: trung tâm dịch vụ sinh viên  
        section: thông tin học bổng khuyến khích học tập  
            article: đối tượng  
            article: quỹ học bổng khuyến khích học tập  
            article: căn cứ để xét học bổng khuyến khích học tập  
            article: mức học bổng khuyến khích học tập  
            article: quy trình xét học bổng"

        
    Mô tả mục lục: mục lục gồm 3 chương. Mỗi chương có các cấu trúc khác nhau. Được tổ chức theo dạng phân cấp giống như thư mục.
            
    Thứ hai, sau khi xác định thuộc phần nào, bạn sẽ phải trả về câu cypher query theo mô tả sau:
    1. các phần như part, section, article được dùng làm "type"(tất cả đều ghi thường, tiếng anh)
    2. các phần nội dung là phần "name"(tất cả đều ghi thường, tiếng việt)
    
    Cypher query:
    MATCH (first:<type> {{name: '<name>'}})-[:bao_gồm]->(second:<type> {{name: '<name>'}})-[:bao_gồm]->(third:<type> {{name: '<name>'}})-[r*1..3]->(e)
    RETURN r as relation, e as target
    
    Trong đó:
        - type: Là loại của mục (part, section, hoặc article, viết thường, tiếng Anh).
        - name: Là nội dung của mục (viết thường, tiếng Việt, đúng như trong mục lục).
        - Các cấp (first, second, third, hoặc fourth) phải được sắp xếp theo thứ tự phân cấp (second là con của first, third là con của second, fourth là con của third).
        - Phần -[r*1..3]->(e) phải luôn có.
        - Các mục đồng cấp (ví dụ: hai section hoặc 2 part hoặc 2 article) không được nối tiếp nhau trong query.

    Lưu ý:
    - Mọi câu hỏi đều thuộc mục lục, không có trường hợp không tìm thấy.
    - Query phải đúng định dạng mẫu, không giải thích thêm.
    - câu cypher query buộc phải có từ second trở lên.
    - CHỈ PHẢN HỒI VỀ CYPHER QUERY VÀ KHÔNG GIẢI THÍCH GÌ THÊM.

    Ví dụ:
    Câu hỏi về "quyền của sinh viên":
    MATCH (first:part {{name: 'phần 2: học tập và rèn luyện'}})-[:bao_gồm]->(second:section {{name: 'quy chế sinh viên'}})-[:bao_gồm]->(third:part {{name: 'chương 2: quyền và nghĩa vụ của sinh viên'}})-[:bao_gồm]->(fourth:article {{name: 'điều 4: quyền của sinh viên'}})-[r*1..3]->(e)
    RETURN r as relation, e as target
    Câu hỏi về "quá trình hình thành và phát triển":
    MATCH (first:part {{name: 'phần 1: nlu - định hướng trường đại học nghiên cứu'}})-[:bao_gồm]->(second:section {{name: 'quá trình hình thành và phát triển'}})-[r*1..3]->(e)
    RETURN r as relation, e as target
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

def answer_by_context():
    return """
hãy dựa vào ngữ cảnh của các câu trả lời trước để trả lời câu hỏi {question}. Nếu không có ngữ cảnh để trả lời thì phản hổi 'Không có thông tin' và không giải thích gì thêm.        
"""

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

# dùng để trích xuất các chủ đề quan trọng. Được sử dụng để thêm thông tin vào chunk để tạo thuận lợi cho ss vector qdrant
def summary_document():
    return """
Bạn là một chuyên gia trích xuất chủ đề quan trọng trong văn bản. nhiệm vụ của bạn là hãy trích xuất chủ đề quan trọng theo các yêu cầu sau đây:
1. Nội dung không quá 2 dòng, phù hợp để tăng thêm ngữ cảnh thì truy xuất thông qua vector embedding.
2. Chỉ trích xuất các nội dung chính được nhắc đến trong đoạn văn.
Văn bản: {paragraph}
    """

def summary_answer():
    return """
Bạn là trợ lý hữu ích, tuân theo khuôn mẫu.
Nhiệm vụ: Dựa trên câu hỏi và câu trả lời, diễn đạt lại bằng ngôn ngữ tự nhiên, hoàn chỉnh.
1. Không thêm, bớt, chỉnh sửa nội dung.
2. Trình bày rõ ràng, liệt kê (nếu có) đánh số thứ tự và in đậm.
3. Nếu câu trả lời là "Không có thông tin", giữ nguyên. Nếu có thông tin, diễn đạt lại.
4. Chỉ trả lời, không lặp lại câu hỏi.

Câu hỏi: {question}
Câu trả lời: {answer}
"""

def separate_question():
    return """
Bạn là một chuyên gia phân tích câu hỏi. Dựa vào câu hỏi mà tôi cung cấp. Nhiệm vụ của bạn là tách câu hỏi ra thành nhiều phần khác nhau(nếu có).
Trả về dưới dạng json gồm các thuộc tính:
{{
    'question 1': '...',
    'question 2': '...',
    'question 3': '...',
    ...
}}
Câu hỏi: {question}
"""














