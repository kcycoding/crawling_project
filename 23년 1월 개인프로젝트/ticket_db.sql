-- Drop database plane_ticket_db;
CREATE database plane_ticket_db;
use plane_ticket_db;

CREATE TABLE passenger_info -- 탑승객 정보
(passenger_id char(15) NOT NULL primary key, -- 아이디
passenger_pw char(15) NOT NULL, -- 비밀번호
passenger_name1 char(5) NOT NULL, -- 한글 이름
passenger_name2 char(20) NOT NULL, -- 영문이름
passenger_gender char(2) NOT NULL, -- 성별
passenger_birth int(6) NOT NULL, -- 생년s월일
passenger_email char(20) NOT NULL, -- 이메일
passenger_passport char(15) NOT NULL -- 여권 번호
);

CREATE TABLE ticket_basket -- 티켓 장바구니
(num 		INT AUTO_INCREMENT NOT NULL PRIMARY KEY, -- 순번(PK)
passenger_id char(15) NOT NULL, -- 아이디
basket1 char(255) -- 장바구니
);

CREATE TABLE ticket_buy -- 티켓 구매
(num 		INT AUTO_INCREMENT NOT NULL PRIMARY KEY, -- 순번(PK)
passenger_id char(15) NOT NULL, -- 아이디
buy char(255) -- 장바구니
);