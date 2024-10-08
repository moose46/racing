
select a.name, ro.name as role, a.website, slug, t.name as team, t.website as teamwebsite, t.[owner]
from nascar_person as a,
	nascar_person_role as pr,
	nascar_role as ro,
	nascar_team as t,
	nascar_person_team as pt
where a.id = pr.person_id and pr.role_id = ro.id and t.id = pt.team_id and a.id = pt.person_id
order by a.name
-- select *
-- from nascar_person