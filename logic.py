"""
逻辑
访问所有页面都需要 登录
    登录页面， 登录表单， 注册连接
    注册页面， 注册表单， 个人信息填写
    修改个人信息页面 修改个人信息
    修改密码页面 修改密码
    用户初始信用值 credit 是 0

主题 / 帖子 Topic
    所有帖子列表 （分页 todo） 展示 标题、用户名、时间
    点击 帖子进入详情页 帖子内容 和 评论列表  添加评论表单
    添加 帖子 页面
    帖子 编辑
    评论 编辑
    每发一篇帖子 credit 加 10

版块
    版块 列表 点击版块 进入 该版块下的帖子列表
    添加、修改、删除 版块 按钮
    版块权限 版主
    版块 初始 设定 权限信用值 permit 用户 credit 大于等于 permit 时可以发帖
    版块初始时设置 master (user.id) 版主
    只有版主 / 超级管理员 (role 为 1） 可以修改 版块

问题
    问题 列表 展示 标题、用户名、时间
    点击 问题进入详情页 问题 内容等 和 答案列表 添加回答
    添加问题 页面

博客
    博客列表展示页 标题、缩略图、用户名、发布时间
    博客详情页 点赞 记录浏览量
    发表博客
    编辑博客
    删除博客

"""