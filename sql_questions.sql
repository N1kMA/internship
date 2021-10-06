
SELECT u.id
FROM users u
    left join departments d on u.id=d.user_id
WHERE d.department_id = 1;

select lastname from "user"
group by lastname
having count(*)> 1;

select * from (
select id, username, salary, rank() over (order by salary desc) as salary_rank from "user" u
left join salary s on u.id = s.user_id) as result
where salary_rank = 2