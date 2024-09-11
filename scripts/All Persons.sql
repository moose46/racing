select name, role_id from nascar_person, nascar_person_role
where nascar_person.id = nascar_person_role.person_id
order by name