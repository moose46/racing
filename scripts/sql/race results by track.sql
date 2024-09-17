use racing
go
select p.name, rr.car_no, race_date, rr.finish_pos, rr.start from dbo.nascar_raceresult rr, dbo.nascar_race r, dbo.nascar_track t, nascar_person p
where r.id = rr.race_id and r.track_id = t.id and t.name like 'Wat%' and rr.finish_pos < 6 and p.id = rr.driver_id
order by r.race_date desc