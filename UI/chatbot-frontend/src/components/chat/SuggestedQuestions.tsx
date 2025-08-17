import React from 'react';
// import { useTranslation } from '../../utils/translations';
// import { useSettings } from '../../context/SettingsContext';

interface SuggestedQuestionsProps {
  onQuestionClick: (question: string) => void;
  documentId?: string;
  filename?: string;
}

const SuggestedQuestions: React.FC<SuggestedQuestionsProps> = ({ onQuestionClick, documentId, filename }) => {
  // const { settings } = useSettings();
  // const { t } = useTranslation(settings.language);

  // Different suggested questions based on document type
  const getSuggestedQuestions = () => {
    if (documentId === 'so_tay_sinh_vien_2024') {
      return [
        "Lịch sử trường đại học nông lâm tphcm",
        "Địa chỉ trường đại học nông lâm tphcm", 
        "Tổng quan về sổ tay sinh viên 2024",
        "Quy định về học phí và học bổng",
        "Thông tin về các khoa và ngành đào tạo",
        "Quy chế đào tạo và thi cử",
        "Hoạt động sinh viên và câu lạc bộ",
        "Thông tin về ký túc xá và chỗ ở",
        "Dịch vụ hỗ trợ sinh viên",
        "Quy định về thực tập và việc làm",
        "Thông tin liên hệ các phòng ban",
        "Lịch năm học và các sự kiện quan trọng"
      ];
    } else {
      // For uploaded documents
      return [
        `Tóm tắt nội dung chính của ${filename || 'tài liệu này'}`,
        `Những điểm quan trọng nhất trong ${filename || 'tài liệu này'} là gì?`,
        `Giải thích chi tiết về ${filename || 'tài liệu này'}`,
        `Phân tích cấu trúc của ${filename || 'tài liệu này'}`,
        `Những thông tin hữu ích từ ${filename || 'tài liệu này'}`,
        `Kết luận và đánh giá về ${filename || 'tài liệu này'}`
      ];
    }
  };

  const suggestedQuestions = getSuggestedQuestions();

  return (
    <div className="h-full flex flex-col">
      <div className="flex-1 p-8 animate-fade-in suggested-questions-scroll">
        <div className="max-w-2xl w-full mx-auto">
        {/* Welcome message */}
        <div className="text-center mb-8 animate-slide-up">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-blue-600 rounded-2xl mb-4 shadow-lg animate-float">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-2">
            Chào mừng bạn đến với Chatbot!
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Hãy chọn một trong những câu hỏi dưới đây để bắt đầu cuộc trò chuyện
          </p>
        </div>

        {/* Suggested questions card */}
        <div className="bg-white/95 dark:bg-slate-800/95 backdrop-blur-xl rounded-3xl shadow-2xl shadow-purple-100/50 dark:shadow-slate-900/50 border border-purple-200/30 dark:border-slate-700/50 p-8 transition-all duration-300 hover:shadow-3xl hover:shadow-purple-200/30 dark:hover:shadow-slate-900/70 animate-scale-in">
          
          
          <div className="grid gap-4">
            {suggestedQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => onQuestionClick(question)}
                className="group relative overflow-hidden bg-gradient-to-r from-purple-50/80 to-blue-50/80 dark:from-slate-700/50 dark:to-slate-600/50 hover:from-purple-100 hover:to-blue-100 dark:hover:from-slate-600/70 dark:hover:to-slate-500/70 rounded-2xl border border-purple-200/40 dark:border-slate-600/40 p-6 transition-all duration-300 hover:shadow-lg hover:shadow-purple-100/50 dark:hover:shadow-slate-900/30 hover:scale-[1.02] hover:border-purple-300/60 dark:hover:border-slate-500/60 animate-slide-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                {/* Background decoration */}
                <div className="absolute inset-0 bg-gradient-to-r from-purple-500/5 to-blue-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                
                <div className="relative flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-purple-500/20 to-blue-500/20 dark:from-purple-400/20 dark:to-blue-400/20 rounded-xl flex items-center justify-center group-hover:from-purple-500/30 group-hover:to-blue-500/30 transition-all duration-300">
                      <svg className="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <span className="text-left font-medium text-gray-700 dark:text-gray-200 group-hover:text-purple-700 dark:group-hover:text-purple-300 transition-colors duration-300">
                      {question}
                    </span>
                  </div>
                  <div className="flex-shrink-0 w-8 h-8 bg-purple-100/50 dark:bg-slate-600/50 rounded-full flex items-center justify-center group-hover:bg-purple-200/70 dark:group-hover:bg-slate-500/70 transition-all duration-300 group-hover:scale-110">
                    <svg 
                      className="w-4 h-4 text-purple-600 dark:text-purple-400 group-hover:text-purple-700 dark:group-hover:text-purple-300 transition-all duration-300 group-hover:translate-x-0.5" 
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </button>
            ))}
          </div>

          {/* Footer note */}
          <div className="mt-6 pt-6 border-t border-purple-200/30 dark:border-slate-700/50">
            <p className="text-sm text-gray-500 dark:text-gray-400 text-center">
              💡 Bạn cũng có thể nhập câu hỏi tùy chỉnh ở phía dưới
            </p>
          </div>
        </div>
        </div>
      </div>
    </div>
  );
};

export default SuggestedQuestions;