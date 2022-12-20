# 建表

1.测试表
```angular2html
create table test_user (id bigint unsigned NOT NULl AUTO_INCREMENT COMMENT '自增主键',nickname text NOT NULl COMMENT '用户昵称',password varbinary NOT NULl COMMENT '密码')；
insert into test_user values(zhangsan,123456)
insert into test_user values(lisi,123456)
```