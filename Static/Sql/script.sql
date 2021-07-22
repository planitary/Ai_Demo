create table chat_resource_data
(
    id               int auto_increment comment 'id'
        primary key,
    ClientToken      varchar(255) not null comment '用户token',
    ClientAsk        varchar(512) not null comment '用户说的话',
    AskForResponseId int          null comment '用户说的话对应到回应的语句id',
    isStudy          tinyint(1)   null comment '是否曾经说过(标注是否已学习)',
    constraint ClientToken
        unique (ClientToken)
)
    comment '用户话语库';

create table chat_response_data
(
    id              int auto_increment comment 'id'
        primary key,
    ResponseToAskId int          null,
    Response        varchar(512) not null comment '回应话语'
)
    comment '回应话语库';


