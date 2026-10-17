create database ReevaMehta;
use ReevaMehta;
create table Recruiter(
R_regno int primary key,
Rcontactno int,
R_name varchar(20),
R_design varchar(30)
);
describe Recruiter;
create table Candidate(
C_id int primary key,
C_name varchar(20) not null,
C_phoneno int,
C_add varchar(50) default='Mumbai',
C_exp varchar(50),
C_gender char(1) check(C_gender='M' OR C_gender='F'),
R_regno int,
Re_no int
);
describe Candidate;
drop table Candidate;
create table Resume(
Re_no int primary key,
Re_skills varchar(50),
C_id int
);
describe Resume;
alter table Candidate
add foreign key(Re_no) references Resume(Re_no);
alter table Resume
add foreign key(C_id) references Candidate(C_id);
alter table Candidate
alter table Recruiter 
modify column R_add varchar(40);
alter table Recruiter
drop column R_add;

insert into Recruiter values
(101,9825,'john','HR');
insert into Recruiter values
(102,9828,'marie','manager');
select * from Recruiter;
insert into Services values
(001,'fulltime',101);
insert into Services values
(002,'parttime',102);
select * from Services;
describe Candidate;
drop table Candidate;
alter table Candidate drop constraint Candidate_ibfk_2;
alter table Candidate drop column Re_no;
insert into Candidate values
(001,'Pam',9837,'default','intern at xyz','F',101);
insert into Candidate values
(002,'Jim',9833,'default','intern at abc','M',102);
insert into Resume values
(111,'Leadership',001);
insert into Resume values
(112,'Teamwork',002);

select * from Resume;
select * from Candidate;