import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

// Translation resources
const resources = {
  en: {
    translation: {
      // Common
      "app.title": "AI Chatbot",
      "app.loading": "Loading...",
      "app.error": "An error occurred",
      "app.darkMode": "Dark Mode",
      "app.lightMode": "Light Mode",
      "app.language": "Language",
      "settings": "Settings",
      "history": "History",
      "chat": "Chat",
      "profile": "Profile",
      "coming_soon": "Coming Soon",
      
      // Authentication
      "auth.login": "Login",
      "auth.register": "Register",
      "auth.logout": "Logout",
      "auth.success": "Authentication successful",
      "auth.failed": "Authentication failed",
      "forgot_password_title": "Forgot Password",
      "forgot_password_prompt": "Enter your email address to receive a password reset link",
      "email_placeholder": "Enter your email",
      "password_reset_sent": "Password reset link sent to your email",
      "password_reset_instructions": "Please check your email for instructions to reset your password",
      "back_to_login": "Back to Login",
      "remember_password": "Remember Password",
      "send_reset_link": "Send Reset Link",
      "username": "Username",
      "password_reset_failed": "Failed to send password reset link",
      "password": "Password",
      "email": "Email", 
      "confirm_password": "Confirm Password",
      "forgot_password": "Forgot Password?",
      "dont_have_account": "Don't have an account?",
      "already_have_account": "Already have an account?",
      "register_now": "Register Now",
      "register_here": "Register Here",
      "login_here": "Login Here",
      "welcome_back": "Welcome Back!",
      "i_agree":"I agree",
      "terms_conditions":"Terms and Conditions",
      "login_prompt": "Please sign in to your account",
      "login": "Login",
      "or":"or",
      "register": "Register",
      "create_account": "Create Account",
      "join_prompt": "Join our community today",
      "password_length": "Password must be at least 6 characters",
      "passwords_not_match": "Passwords do not match",
      "required_fields": "All fields are required",
      "invalid_email": "Please enter a valid email address",
      "registration_success": "Registration successful! Redirecting to login...",
      "reset_password": "Reset Password",
      "create_new_password": "Create your new password",
      "new_password": "New Password",
      "enter_new_password": "Enter new password",
      "confirm_new_password": "Confirm new password",
      "password_too_short": "Password must be at least 8 characters",
      "passwords_do_not_match": "Passwords do not match",
      "password_reset_success": "Password reset successful! Redirecting to login...",
      "password_reset_failed": "Failed to reset password",
      "invalid_or_expired_token": "Invalid or expired reset token",
      
      // Chat Interface
      "new_chat": "New Chat",
      "send": "Send",
      "type_message": "Type a message...",
      "how_help_today": "How can I help you today?",
      "start_message": "Type a message to start a conversation",
      "no_conversations": "No conversations yet",
      "load_failed": "Failed to load conversations",
      "error_start_conversation": "Error starting new conversation",
      "error_send_message": "Error sending message",
      "delete_confirm": "Are you sure you want to delete this conversation?",
      "delete_failed": "Failed to delete conversation",
      "delete_conversation": "Delete conversation",
      "loading_conversations": "Loading conversations...",
      "today": "Today",
      "yesterday": "Yesterday",
      "messages": "messages",
      "start_conversation": "Start a conversation",
      "conversation_history": "Conversation History",
      
      // User profile
      "profile.title": "Profile",
      "profile.save": "Save Changes",
      "profile.changePassword": "Change Password",
      "profile.currentPassword": "Current Password",
      "profile.newPassword": "New Password",
      "profile.confirmNewPassword": "Confirm New Password",
      "profile.confirmPassword": "Confirm Password",
      "profile.personalInfo": "Personal Information",
      "profile.username": "Username",
      "profile.email": "Email",
      "profile.updateProfile": "Update Profile",
      "profile.updatePassword": "Update Password",
      "profile.updating": "Updating...",
      "profile.updateSuccess": "Profile updated successfully",
      "profile.passwordUpdateSuccess": "Password updated successfully",
      "profile.passwordsMismatch": "New passwords don't match",
      
      // Settings
      "settings.title": "Settings",
      "settings.preferences": "Preferences",
      "settings.language": "Language",
      "settings.displayMode": "Display Mode",
      "settings.lightMode": "Light Mode",
      "settings.darkMode": "Dark Mode",
      "settings.enableNotifications": "Enable Notifications",
      "settings.notificationsHelp": "Receive notifications for new messages and updates",
      "settings.saveSettings": "Save Settings",
      "settings.saving": "Saving...",
      "settings.updateSuccess": "Settings updated successfully",
      
      // Error messages
      "error.generic": "An error occurred. Please try again later.",
      
      // Language specific
      "i18n.language": "en"
    }
  },
  vi: {
    translation: {
      // Common
      "app.title": "Trợ lý AI",
      "app.loading": "Đang tải...",
      "app.error": "Đã xảy ra lỗi",
      "app.darkMode": "Chế độ tối",
      "app.lightMode": "Chế độ sáng",
      "app.language": "Ngôn ngữ",
      "settings": "Cài đặt",
      "history": "Lịch sử",
      "chat": "Trò chuyện",
      "profile": "Hồ sơ",
      "coming_soon": "Sắp ra mắt",
      
      // Authentication
      "auth.login": "Đăng nhập",
      "auth.register": "Đăng ký",
      "auth.logout": "Đăng xuất",
      "auth.success": "Xác thực thành công",
      "auth.failed": "Xác thực thất bại",
      "username": "Tên đăng nhập",
      "forgot_password_title": "Quên mật khẩu",
      "forgot_password_prompt": "Nhập địa chỉ email của bạn để nhận liên kết đặt lại mật khẩu",
      "email_placeholder": "Nhập địa chỉ email",
      "remember_password": "Nhớ mật khẩu",
      "password_reset_failed": "Không thể gửi liên kết đặt lại mật khẩu",
      "password": "Mật khẩu",
      "email": "Email", 
      "confirm_password": "Xác nhận mật khẩu",
      "forgot_password": "Quên mật khẩu?",
      "dont_have_account": "Chưa có tài khoản?",
      "already_have_account": "Đã có tài khoản?",
      "send_reset_link": "Gửi liên kết đặt lại",
      "password_reset_sent": "Liên kết đặt lại mật khẩu đã được gửi đến email của bạn",
      "password_reset_instructions": "Vui lòng kiểm tra email của bạn để biết hướng dẫn đặt lại mật khẩu",
      "back_to_login": "Quay lại trang đăng nhập",
      "register_now": "Đăng ký ngay",
      "register_here": "Đăng ký tại đây",
      "login_here": "Đăng nhập tại đây",
      "welcome_back": "Chào mừng trở lại!",
      "login_prompt": "Vui lòng đăng nhập vào tài khoản của bạn",
      "login": "Đăng nhập",
      "register": "Đăng ký",
      "i_agree":"Tôi đồng ý",
      "or":"hoặc",
      "terms_conditions":"Điều khoản và điều kiện",
      "create_account": "Tạo tài khoản",
      "join_prompt": "Tham gia cộng đồng ngay hôm nay",
      "password_length": "Mật khẩu phải có ít nhất 6 ký tự",
      "passwords_not_match": "Mật khẩu không khớp",
      "required_fields": "Tất cả các trường đều bắt buộc",
      "invalid_email": "Vui lòng nhập địa chỉ email hợp lệ",
      "registration_success": "Đăng ký thành công! Đang chuyển hướng đến trang đăng nhập...",
      "reset_password": "Đặt Lại Mật Khẩu",
      "create_new_password": "Tạo mật khẩu mới của bạn",
      "new_password": "Mật Khẩu Mới",
      "enter_new_password": "Nhập mật khẩu mới",
      "confirm_new_password": "Xác nhận mật khẩu mới",
      "password_too_short": "Mật khẩu phải có ít nhất 8 ký tự",
      "passwords_do_not_match": "Mật khẩu không khớp",
      "password_reset_success": "Đặt lại mật khẩu thành công! Đang chuyển hướng đến trang đăng nhập...",
      "password_reset_failed": "Không thể đặt lại mật khẩu",
      "invalid_or_expired_token": "Mã đặt lại không hợp lệ hoặc đã hết hạn",
      
      // Chat Interface
      "new_chat": "Trò chuyện mới",
      "send": "Gửi",
      "type_message": "Nhập tin nhắn...",
      "how_help_today": "Tôi có thể giúp gì cho bạn?",
      "start_message": "Nhập tin nhắn để bắt đầu cuộc trò chuyện",
      "no_conversations": "Chưa có cuộc trò chuyện nào",
      "load_failed": "Không thể tải cuộc trò chuyện",
      "error_start_conversation": "Lỗi khi bắt đầu cuộc trò chuyện mới",
      "error_send_message": "Lỗi khi gửi tin nhắn",
      "delete_confirm": "Bạn có chắc muốn xóa cuộc trò chuyện này?",
      "delete_failed": "Không thể xóa cuộc trò chuyện",
      "delete_conversation": "Xóa cuộc trò chuyện",
      "loading_conversations": "Đang tải cuộc trò chuyện...",
      "today": "Hôm nay",
      "yesterday": "Hôm qua",
      "messages": "tin nhắn",
      "start_conversation": "Bắt đầu cuộc trò chuyện",
      "conversation_history": "Lịch sử cuộc trò chuyện",
      
      // User profile
      "profile.title": "Hồ sơ",
      "profile.save": "Lưu thay đổi",
      "profile.changePassword": "Đổi mật khẩu",
      "profile.currentPassword": "Mật khẩu hiện tại",
      "profile.newPassword": "Mật khẩu mới",
      "profile.confirmNewPassword": "Xác nhận mật khẩu mới",
      "profile.confirmPassword": "Xác nhận mật khẩu",
      "profile.personalInfo": "Thông tin cá nhân",
      "profile.username": "Tên đăng nhập",
      "profile.email": "Email",
      "profile.updateProfile": "Cập nhật hồ sơ",
      "profile.updatePassword": "Cập nhật mật khẩu",
      "profile.updating": "Đang cập nhật...",
      "profile.updateSuccess": "Hồ sơ đã được cập nhật thành công",
      "profile.passwordUpdateSuccess": "Mật khẩu đã được cập nhật thành công",
      "profile.passwordsMismatch": "Mật khẩu mới không khớp",
      
      // Settings
      "settings.title": "Cài đặt",
      "settings.preferences": "Tùy chọn",
      "settings.language": "Ngôn ngữ",
      "settings.displayMode": "Chế độ hiển thị",
      "settings.lightMode": "Chế độ sáng",
      "settings.darkMode": "Chế độ tối",
      "settings.enableNotifications": "Bật thông báo",
      "settings.notificationsHelp": "Nhận thông báo về tin nhắn mới và cập nhật",
      "settings.saveSettings": "Lưu cài đặt",
      "settings.saving": "Đang lưu...",
      "settings.updateSuccess": "Cài đặt đã được cập nhật thành công",
      
      // Error messages
      "error.generic": "Đã xảy ra lỗi. Vui lòng thử lại sau.",
      
      // Language specific
      "i18n.language": "vi"
    }
  }
};

// Initialize i18next
i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: localStorage.getItem('language') || 'en', // Default language
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false // React already escapes values
    }
  });

export default i18n;