
---

## 💬 微信全生态使用指南
现在支持三种微信场景：个人微信、企业微信、微信公众号。

---

### 🏢 企业微信使用示例
#### 发送文本消息到企业微信
```yaml
steps:
  - name: 发送企业微信消息
    uses: wechat/work@1.0.0
    with:
      action: send_text
      corp_id: "wwxxxxxx"  # 企业ID
      corp_secret: "xxxxxx" # 应用Secret
      agent_id: 1000001    # 应用ID
      receiver: "zhangsan|lisi"  # 接收人userid，多个用|分隔，或者@all
      content: "今日销售报表已生成，请查收！"
```

#### 发送Markdown消息到企业微信群
```yaml
steps:
  - name: 发送Markdown到群
    uses: wechat/work@1.0.0
    with:
      action: send_to_group
      corp_id: "wwxxxxxx"
      corp_secret: "xxxxxx"
      agent_id: 1000001
      chat_id: "wrxxxxxx"  # 群ID
      msg_type: "markdown"
      content: |
        ## 📊 今日销售数据
        - 总销售额：¥123,456
        - 订单数：123
        - 转化率：35.2%
        > 数据截止到今日18:00
```

#### 获取企业通讯录
```yaml
steps:
  - name: 获取部门用户列表
    uses: wechat/work@1.0.0
    with:
      action: get_user_list
      corp_id: "wwxxxxxx"
      corp_secret: "xxxxxx"
      department_id: 1
      fetch_child: 1
    register: user_list
```

---

### 🔔 微信公众号使用示例
#### 发送模板消息给用户
```yaml
steps:
  - name: 发送订单通知
    uses: wechat/mp@1.0.0
    with:
      action: send_template
      app_id: "wxxxxxxx"  # 公众号AppID
      app_secret: "xxxxxx" # 公众号AppSecret
      openid: "o7xxxxxx"   # 用户openid
      template_id: "xxxxxx" # 模板ID
      url: "https://example.com/order/123" # 点击跳转链接
      data:
        first:
          value: "您的订单已发货"
          color: "#173177"
        order_no:
          value: "2024033012345"
          color: "#173177"
        product_name:
          value: "RPA机器人套餐"
          color: "#173177"
        remark:
          value: "点击查看物流详情"
          color: "#173177"
```

#### 发送客服消息
```yaml
steps:
  - name: 回复用户消息
    uses: wechat/mp@1.0.0
    with:
      action: send_custom_message
      app_id: "wxxxxxxx"
      app_secret: "xxxxxx"
      openid: "o7xxxxxx"
      content: "感谢您的咨询，有任何问题随时联系我们~"
```

#### 获取关注用户列表
```yaml
steps:
  - name: 获取公众号粉丝列表
    uses: wechat/mp@1.0.0
    with:
      action: get_user_list
      app_id: "wxxxxxxx"
      app_secret: "xxxxxx"
    register: fans_list
```

---

### 🔑 环境变量配置（推荐）
可以将密钥配置到环境变量中，避免在流程文件中明文存储：
```bash
# 个人微信无需配置，扫码登录
export WECHAT_WORK_CORP_ID="wwxxxxxx"
export WECHAT_WORK_CORP_SECRET="xxxxxx"
export WECHAT_WORK_AGENT_ID="1000001"
export WECHAT_MP_APP_ID="wxxxxxxx"
export WECHAT_MP_APP_SECRET="xxxxxx"
```
配置后流程文件中不需要再填这些参数，自动从环境变量读取。
