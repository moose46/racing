select a.name,b.start_pos, b.finish_pos, b.car_no , c.name, c.race_date
from nascar_person a, nascar_raceresult b, nascar_race c 
where  a.id = b.driver_id and c.name like 'Kansas%' and b.race_id = c.id and b.finish_pos < 5

order by a.name --, c.race_date desc

select a.name, count(a.name) cnt
from nascar_person a, nascar_raceresult b, nascar_race c 
where  a.id = b.driver_id and c.name like 'Kansas%' and b.race_id = c.id and b.finish_pos < 5
group by a.name
order by a.name --, c.race_date desc