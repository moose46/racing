select a.name, b.finish_pos, b.car_no , c.name, c.race_date
from nascar_person a, nascar_raceresult b, nascar_race c 
where a.name = 'Ryan Blaney' and a.id = b.driver_id and c.name = 'Atlanta Motor Speedway' and b.race_id = c.id
order by c.race_date