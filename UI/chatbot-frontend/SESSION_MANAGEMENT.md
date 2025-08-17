# Session Management - 1 Month TTL

## Overview
Hệ thống quản lý session đã được cập nhật để có TTL (Time To Live) là 1 tháng (30 ngày). Session sẽ tự động hết hạn sau 1 tháng kể từ lần đăng nhập cuối cùng.

## Features

### 1. Session TTL (1 month)
- Session có thời gian sống là 1 tháng (2,592,000,000 milliseconds)
- Timestamp được lưu trong localStorage khi user đăng nhập
- Session tự động hết hạn sau 1 tháng

### 2. Auto Session Validation
- Mỗi khi `getCurrentUser()` được gọi, hệ thống kiểm tra session có hết hạn không
- Nếu hết hạn, user data sẽ bị xóa tự động
- AuthContext kiểm tra session validity khi khởi tạo

### 3. Session Refresh
- Session được refresh tự động khi:
  - User thực hiện API call thành công
  - Auto-refresh mỗi 30 phút (nếu user đang active)
- Manual refresh thông qua `AuthService.refreshSession()`

### 4. Session Monitoring
- Hook `useSession` cung cấp thông tin real-time về session
- Component `SessionStatus` hiển thị trạng thái session
- Cảnh báo khi session sắp hết hạn (< 1 giờ)

## Implementation Details

### Constants
```typescript
// src/constants/api.ts
export const SESSION_CONFIG = {
  TTL: 30 * 24 * 60 * 60 * 1000, // 30 days (1 month) in milliseconds
  TIMESTAMP_KEY: 'session_timestamp',
} as const;
```

### AuthService Methods
- `setSessionTimestamp()`: Lưu timestamp hiện tại
- `getSessionTimestamp()`: Lấy timestamp từ localStorage
- `isSessionExpired()`: Kiểm tra session có hết hạn không
- `isSessionValid()`: Kiểm tra session có hợp lệ không
- `refreshSession()`: Refresh timestamp để extend session
- `clearSession()`: Xóa user data và timestamp

### Auto-refresh Strategy
1. **API Interceptor**: Refresh session sau mỗi API call thành công
2. **Interval Refresh**: Auto-refresh mỗi 30 phút nếu user active
3. **Manual Refresh**: User có thể extend session thủ công

## Usage

### Basic Usage
```typescript
import { useAuth } from '../context/AuthContext';

const MyComponent = () => {
  const { user, logout } = useAuth();
  
  // Session sẽ được kiểm tra tự động
  // Nếu hết hạn, user sẽ bị logout tự động
};
```

### Session Monitoring
```typescript
import { useSession } from '../hooks/useSession';

const MyComponent = () => {
  const { isValid, timeRemainingFormatted, refreshSession } = useSession();
  
  return (
    <div>
      <p>Session: {isValid ? 'Active' : 'Expired'}</p>
      <p>Time remaining: {timeRemainingFormatted}</p>
      <button onClick={refreshSession}>Extend Session</button>
    </div>
  );
};
```

### Session Status Component
```typescript
import { SessionStatus } from '../components/SessionStatus';

const Layout = () => {
  return (
    <div>
      {/* Show detailed session info */}
      <SessionStatus showDetails={true} />
      
      {/* Show only warning when expiring */}
      <SessionStatus />
    </div>
  );
};
```

## Configuration

### Changing TTL
Để thay đổi thời gian TTL, cập nhật `SESSION_CONFIG.TTL` trong `src/constants/api.ts`:

```typescript
export const SESSION_CONFIG = {
  TTL: 60 * 24 * 60 * 60 * 1000, // 60 days (2 months)
  TIMESTAMP_KEY: 'session_timestamp',
} as const;
```

### Changing Auto-refresh Interval
Cập nhật interval trong `AuthContext.tsx`:

```typescript
// Auto-refresh every 15 minutes instead of 30
}, 15 * 60 * 1000); // 15 minutes
```

## Security Considerations

1. **Client-side Only**: TTL chỉ được enforce ở client-side
2. **Server Validation**: Server vẫn cần validate token độc lập
3. **Token Expiry**: JWT token từ server có thể có expiry time riêng
4. **Logout on Expiry**: User được logout tự động khi session hết hạn

## Testing

### Manual Testing
1. Đăng nhập và kiểm tra timestamp trong localStorage
2. Thay đổi system time để test session expiry
3. Kiểm tra auto-refresh khi thực hiện API calls
4. Test warning khi session sắp hết hạn

### Debug Mode
Thêm console.log để theo dõi session lifecycle:
- Login: "User data saved to localStorage with session timestamp"
- Refresh: "Session refreshed" / "Session auto-refreshed"
- Expiry: "Session expired, clearing user data"
- Logout: "User logged out and session cleared"

## Migration Notes

### Existing Users
- Users đã đăng nhập trước khi update sẽ không có timestamp
- Họ sẽ bị logout khi `getCurrentUser()` được gọi lần đầu
- Cần đăng nhập lại để có session timestamp

### Backward Compatibility
- Code vẫn tương thích với localStorage format cũ
- Chỉ thêm timestamp, không thay đổi user data structure