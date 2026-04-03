# 权限映射表

## 微信小程序权限 → Android 权限映射

| 微信权限 | Android 权限 | 说明 |
|---------|-------------|------|
| `scope.userLocation` | `ACCESS_FINE_LOCATION` | 精确定位 |
| `scope.userLocationBackground` | `ACCESS_BACKGROUND_LOCATION` | 后台定位 |
| `scope.userInfo` | - | 用户信息（微信特有） |
| `scope.camera` | `CAMERA` | 相机 |
| `scope.record` | `RECORD_AUDIO` | 录音 |
| `scope.writePhotosAlbum` | `WRITE_EXTERNAL_STORAGE` | 写入相册 |
| `scope.bluetooth` | `BLUETOOTH` | 蓝牙 |
| `scope.addPhoneContact` | `WRITE_CONTACTS` | 添加联系人 |
| `scope.addPhoneCalendar` | `WRITE_CALENDAR` | 添加日历 |
| `scope.werun` | `ACTIVITY_RECOGNITION` | 微信运动步数 |

## 38 项权限确认单

### 1. 基础信息（7项）
1. 用户微信昵称
2. 用户头像
3. 用户性别
4. 用户地区
5. 用户语言
6. 用户国家/地区
7. 用户手机号

### 2. 设备信息（8项）
8. 设备型号
9. 操作系统版本
10. 网络类型
11. IP地址
12. 设备标识符（IMEI/IDFA/IDFV）
13. MAC地址
14. 蓝牙设备列表
15. 已安装应用列表

### 3. 位置信息（4项）
16. 精确位置（GPS）
17. 粗略位置（网络定位）
18. 后台位置
19. 地理围栏

### 4. 媒体信息（6项）
20. 相机权限
21. 相册读取
22. 相册写入
23. 麦克风录音
24. 视频录制
25. 屏幕截图

### 6. 通讯录（3项）
26. 读取通讯录
27. 写入通讯录
28. 拨打电话

### 7. 日历（2项）
29. 读取日历
30. 写入日历

### 8. 其他（8项）
31. 剪贴板读取
32. 剪贴板写入
33. 文件读取
34. 文件写入
35. 传感器数据
36. 蓝牙通信
37. NFC通信
38. USB设备访问

---

## 使用方法

```bash
# 查看权限映射
grep "scope.userLocation" references/permission_mapping.md
```
