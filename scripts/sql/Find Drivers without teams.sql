-- Active: 1726174757221@@127.0.0.1@1433
-- find persons without teams
select name
from nascar_person as p
where p.id not in (select tp.person_id
from nascar_person_team as tp
where p.id = tp.person_id )
order by name