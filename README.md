
# zLocket API

## Giới thiệu
API spam từ tool zLocket, có thể gọi từ web.

## Cách dùng

### Gửi request spam:
POST `/spam` với JSON body:
```json
{
  "username": "tên người dùng"
}
```

### Deploy trên Render:
- Push repo lên GitHub.
- Kết nối với Render, chọn `main.py` là entrypoint.
