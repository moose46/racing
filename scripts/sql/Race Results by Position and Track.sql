
select a.name, b.finish_pos,b.start_pos,b.car_no , c.name, c.race_date
from nascar_person a, nascar_raceresult b, nascar_race c 
where  a.id = b.driver_id and  c.name like 'Watkins Glen International' and b.race_id = c.id
and b.finish_pos <= 10 and race_date >= '2020-01-01' 
group by a.name,finish_pos,start_pos, car_no, c.name, race_date
having  count(a.name) > 0
order by c.race_date,finish_pos
