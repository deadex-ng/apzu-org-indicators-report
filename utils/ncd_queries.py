ncd_active = '''
/* Denominaotr - # of NCD patients currently in care */
---
USE openmrs_warehouse;
---
SET @endDate = "2025-03-31";
---
SET @defaultCutOff = 60;
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
                    where program IN ("Chronic Care Program")
					and start_date <= @endDate
                                        and location =  @location
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
			where patient_id IN (SELECT patient_id FROM omrs_obs where encounter_type IN ("ASTHMA_FOLLOWUP","CHRONIC_CARE_FOLLOWUP",
"DIABETES HYPERTENSION FOLLOWUP","CKD_FOLLOWUP","CHF_FOLLOWUP","NCD_OTHER_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff);
'''

ncd_died = '''
/* NCD Mortality */
---
/* Numerator - Patient died */
---
use openmrs_warehouse;
---
SET @startDate = "2025-01-01";
---
SET @endDate = "2025-03-31";
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
                    where program IN ("Chronic Care Program")
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

ncd_active_12months_before='''
/* Denominaotr - # of NCD patients currently in care */
---
USE openmrs_warehouse;
---
SET @endDate = "2024-03-31";
---
SET @location = {};
---
SET @defaultCutOff = 60;
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
                    where program IN ("Chronic Care Program")
					and start_date <= @endDate
                                        and location =  @location
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
			where patient_id IN (SELECT patient_id FROM omrs_obs where encounter_type IN ("ASTHMA_FOLLOWUP","CHRONIC_CARE_FOLLOWUP",
"DIABETES HYPERTENSION FOLLOWUP","CKD_FOLLOWUP","CHF_FOLLOWUP","NCD_OTHER_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff);
'''

ncd_active_24months_before='''
/* Denominaotr - # of NCD patients currently in care */
---
USE openmrs_warehouse;
---
SET @endDate = "2023-03-31";
---
SET @location = {};
---
SET @defaultCutOff = 60;
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
                    where program IN ("Chronic Care Program")
					and start_date <= @endDate
                                        and location =  @location
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
			where patient_id IN (SELECT patient_id FROM omrs_obs where encounter_type IN ("ASTHMA_FOLLOWUP","CHRONIC_CARE_FOLLOWUP",
"DIABETES HYPERTENSION FOLLOWUP","CKD_FOLLOWUP","CHF_FOLLOWUP","NCD_OTHER_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff);
'''

ncd_visits = '''
use openmrs_warehouse;
---
set @startDate='2025-01-01';
---
set @endDate="2025-03-31";
---
SET @location = {};
---
SELECT 
    SUM(CASE
        WHEN diabetes_htn_followup = 1 THEN 1
        WHEN asthma_followup = 1 THEN 1
        WHEN ckd_followup = 1 THEN 1
        WHEN chf_followup = 1 THEN 1
        WHEN ncd_other_followup THEN 1
    END) AS ncd_visits
FROM
    mw_ncd_visits
WHERE
    visit_date BETWEEN @startDate AND @endDate  AND location = @location;
'''

retention_in_care_for_ncd_at_12months='''
/* 2.Retention In Care For Ncds At 12 And 24 Months */
---
/* Numerator - Result Should Subtract To Denominator To Get Number Of Patients In Care */
---
use openmrs_warehouse;
---
SET @endDate = "2024-03-01";
---
SET @endReportindDate = "2025-03-31";
---
SET @location = {};
---
SET @defaultCutOff = 60;
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
                    where program IN ("Chronic care program")
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
            SELECT patient_id FROM omrs_obs where encounter_type IN ("ASTHMA_FOLLOWUP","CHRONIC_CARE_FOLLOWUP",
"DIABETES HYPERTENSION FOLLOWUP","CKD_FOLLOWUP","CHF_FOLLOWUP","NCD_OTHER_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff)
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
                    where program IN ("Chronic care program")
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

retention_in_care_for_ncd_at_24months='''
/* 2.Retention In Care For Ncds At 12 And 24 Months */
---
/* Numerator - Result Should Subtract To Denominator To Get Number Of Patients In Care */
---
use openmrs_warehouse;
---
SET @endDate = "2023-03-01";
---
SET @endReportindDate = "2025-03-31";
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
                    where program IN ("Chronic care program")
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
            SELECT patient_id FROM omrs_obs where encounter_type IN ("ASTHMA_FOLLOWUP","CHRONIC_CARE_FOLLOWUP",
"DIABETES HYPERTENSION FOLLOWUP","CKD_FOLLOWUP","CHF_FOLLOWUP","NCD_OTHER_FOLLOWUP") and concept = "Appointment date" and floor(datediff(@endDate,value_date)) <=  @defaultCutOff)
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
                    where program IN ("Chronic care program")
                    and start_date <= @endReportindDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "Chronic Care Number"
            where index_desc = 1 and opi.location=@location
            and state IN ("Patient died","treatment stopped","patient defaulted")        
            );
'''