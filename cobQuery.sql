select department, max(case_enquiry_id) as [second to newest]
FROM caseFile
where case_enquiry_id not in
(
select max(case_enquiry_id) as myCase
from caseFile
group by department
)
group by department
