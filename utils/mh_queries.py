mh_active='''
/* 1. Active in Care */
---
USE openmrs_warehouse;
---
SET @defaultCutOff = '2024-10-01';
---
SET @endDate = "2024-12-31";
---
SET @location = {};
---
select count(distinct(patient_id))
from
(
select distinct(mwp.patient_id), opi.identifier, mwp.first_name, mwp.last_name, ops.program, ops.state,ops.start_date,program_state_id,  mwp.gender,
  ops.location, patient_visit.last_appt_date
from  mw_patient mwp  
join omrs_patient_identifier opi
on mwp.patient_id = opi.patient_id
join (
select patient_id,MAX(visit_date) as visit_date ,MAX(next_appointment_date) as last_appt_date from mw_ncd_visits where visit_date <= @endDate
group by patient_id
            ) patient_visit
            on patient_visit.patient_id = mwp.patient_id
JOIN
        (SELECT
index_desc,
            opi.patient_id as pat,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
start_date,
            program_state_id,
            end_date
FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
      FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program")
and start_date <= @endDate
and location = @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1)
            ops
            on opi.patient_id = ops.pat and opi.location = ops.location
            where opi.type = "Chronic Care Number"
            and state IN ("On Treatment","In advanced Care")
            ) x
            where patient_id IN (select patient_id from mw_mental_health_followup where next_appointment_date >=@defaultCutOff);
'''

mh_visits = '''
/* 3.Patients with a visit in last 3 months */
USE openmrs_warehouse;
---
SET @startDate = '2024-10-01';
---
SET @endDate = "2024-12-31";
---
SET @location = {};
---
select count(distinct(patient_id))
from mw_mental_health_followup
where location = @location and visit_date BETWEEN @startDate AND @endDate;
'''

mh_mortality = '''
/* MH Mortality */
---
/* Numerator - Patient died */
---
use openmrs_warehouse;
---
SET @startDate = "2024-10-01";
---
SET @endDate = "2024-12-31";
---
SET @location = {};
---
select count(*)
from
(
select distinct(mwp.patient_id), opi.identifier, mwp.first_name, mwp.last_name, ops.program, ops.state,ops.start_date,program_state_id,  mwp.gender,
  ops.location
from  mw_patient mwp  
join omrs_patient_identifier opi
on mwp.patient_id = opi.patient_id
JOIN
        (SELECT
index_desc,
            opi.patient_id as pat,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
start_date,
            program_state_id,
            end_date
FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
      FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program")
					and start_date <= @endDate
                 
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1)
            ops
            on opi.patient_id = ops.pat and opi.location = ops.location
            where opi.type = "Chronic Care Number"
            and state IN ("patient died")
            ) x
            where start_date between @startDate and @endDate and location = @location;
'''
mh_active_12months_before = '''
/* 1. Active in Care */
---
USE openmrs_warehouse;
---
SET @defaultCutOff = '2023-10-01';
---
SET @endDate = "2023-12-31";
---
SET @location = {};
---
select count(distinct(patient_id))
from
(
select distinct(mwp.patient_id), opi.identifier, mwp.first_name, mwp.last_name, ops.program, ops.state,ops.start_date,program_state_id,  mwp.gender,
  ops.location, patient_visit.last_appt_date
from  mw_patient mwp  
join omrs_patient_identifier opi
on mwp.patient_id = opi.patient_id
join (
select patient_id,MAX(visit_date) as visit_date ,MAX(next_appointment_date) as last_appt_date from mw_ncd_visits where visit_date <= @endDate
group by patient_id
            ) patient_visit
            on patient_visit.patient_id = mwp.patient_id
JOIN
        (SELECT
index_desc,
            opi.patient_id as pat,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
start_date,
            program_state_id,
            end_date
FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
      FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program")
and start_date <= @endDate
and location = @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1)
            ops
            on opi.patient_id = ops.pat and opi.location = ops.location
            where opi.type = "Chronic Care Number"
            and state IN ("On Treatment","In advanced Care")
            ) x
            where patient_id IN (select patient_id from mw_mental_health_followup where next_appointment_date >=@defaultCutOff);
'''
mh_active_24months_before = '''
/* 1. Active in Care */
---
USE openmrs_warehouse;
---
SET @defaultCutOff = '2022-10-01';
---
SET @endDate = "2022-12-31";
---
SET @location = {};
---
select count(distinct(patient_id))
from
(
select distinct(mwp.patient_id), opi.identifier, mwp.first_name, mwp.last_name, ops.program, ops.state,ops.start_date,program_state_id,  mwp.gender,
  ops.location, patient_visit.last_appt_date
from  mw_patient mwp  
join omrs_patient_identifier opi
on mwp.patient_id = opi.patient_id
join (
select patient_id,MAX(visit_date) as visit_date ,MAX(next_appointment_date) as last_appt_date from mw_ncd_visits where visit_date <= @endDate
group by patient_id
            ) patient_visit
            on patient_visit.patient_id = mwp.patient_id
JOIN
        (SELECT
index_desc,
            opi.patient_id as pat,
            opi.identifier,
            index_descending.state,
            index_descending.location,
            index_descending.program,
start_date,
            program_state_id,
            end_date
FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
      FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program")
and start_date <= @endDate
and location = @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1)
            ops
            on opi.patient_id = ops.pat and opi.location = ops.location
            where opi.type = "Chronic Care Number"
            and state IN ("On Treatment","In advanced Care")
            ) x
            where patient_id IN (select patient_id from mw_mental_health_followup where next_appointment_date >=@defaultCutOff);
'''

retention_in_care_for_mh_at_12months = '''
/* 2.Retention In Care For Ncds At 12 And 24 Months */
---
/* Numerator - Result Should Subtract To Denominator To Get Number Of Patients In Care */
---
use openmrs_warehouse;
---
SET @endDate = "2023-12-01";
---
SET @endReportindDate = "2024-12-31";
---
SET @defaultCutOff = 60;
---
SET @location = {};
---
	SELECT
    count(opi.patient_id)
FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
      FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1
            and state IN ("On treatment","In advanced care")
            and opi.patient_id in (
            SELECT patient_id FROM omrs_obs where encounter_type IN ("MENTAL_HEALTH_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff)
            and opi.patient_id in 
            (
    SELECT
            opi.patient_id as pat
FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
      FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program")
                    and start_date <= @endReportindDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1 and opi.location=@location
            and state IN ("Patient died","treatment stopped","patient defaulted")        
            )
'''

retention_in_care_for_mh_at_24months = '''
/* 2.Retention In Care For Ncds At 12 And 24 Months */
---
/* Numerator - Result Should Subtract To Denominator To Get Number Of Patients In Care */
---
use openmrs_warehouse;
---
SET @endDate = "2022-12-01";
---
SET @endReportindDate = "2024-12-31";
---
SET @defaultCutOff = 60;
---
SET @location = {};
---
	SELECT
    count(opi.patient_id)
FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
      FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1
            and state IN ("On treatment","In advanced care")
            and opi.patient_id in (
            SELECT patient_id FROM omrs_obs where encounter_type IN ("MENTAL_HEALTH_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff)
            and opi.patient_id in 
            (
    SELECT
            opi.patient_id as pat
FROM (SELECT
            @r:= IF(@u = patient_id, @r + 1,1) index_desc,
            location,
            state,
            program,
            start_date,
            end_date,
            patient_id,
            program_state_id,
            @u:= patient_id
      FROM omrs_program_state,
                    (SELECT @r:= 1) AS r,
                    (SELECT @u:= 0) AS u
                    where program IN ("Mental Health Care Program")
                    and start_date <= @endReportindDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1 and opi.location=@location
            and state IN ("Patient died","treatment stopped","patient defaulted")        
            )
'''