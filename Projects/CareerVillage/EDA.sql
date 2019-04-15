create schema kaggle;
use  kaggle; #synonymous with database 

show databases;

#Groups answers
select * from kaggle.groups limit 10;
select groups_group_type, count(*) from kaggle.groups group by 1;

select * from group_memberships limit 100;

#STudents 
select * from students limit 200;
select * from students where students_location != '';# 30971
select distinct students_id, count(*) c from students group by 1 having c > 1; #no duplicates 
#students have joined from 2011 to latest data is 2019. 
select min(students_date_joined), max(students_date_joined) from students; 


#splitting the location to get an idea of where students are
select students_location 
		,SUBSTRING_INDEX(students_location, ',', 1) city
        ,substring_index(students_location, ',', 1) state_or_country
from students where students_location != '';


#Professionals 
select * from professionals where professionals_location !='' and professionals_industry!= '';
# try to get topic from questions and map to industry or headline of professional 


## Answers 
select * from answers limit 100;
select count(*) from answers;