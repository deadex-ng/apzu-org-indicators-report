hiv_active = '''
    /* Denominator */
    /* Active in care based on end date */
    use openmrs_warehouse;
    ---
    SET @endDate = "2025-03-31";
    ---
    SET @defaultCutOff = 60;
    ---
    SET @location= {};
    ---
	SELECT
        index_desc,
            opi.patient_id,
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
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and opi.location=@location
            and state IN ("On Antiretrovirals")
            and opi.patient_id in (
            SELECT patient_id FROM mw_art_followup where floor(datediff(@endDate,next_appointment_date)) <=  @defaultCutOff)
    '''

hiv_mortality = '''
        /* HIV Mortality */
        /* Numerator */
        use openmrs_warehouse;
        ---
        SET @startDate = "2025-01-01"
        ---
        SET @endDate = "2025-03-31"
        ---
        SET @location= {};
        ---
	    SELECT
        index_desc,
            opi.patient_id,
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
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and state IN ("patient died")
            and start_date between @startDate and @endDate;
'''

mmd_6months = '''

use openmrs_warehouse;
---
SET @location = {};
---
SET @endDate = "2025-03-31";
---
/* Pepfar Cut-off = 30, MoH cut-off = 60 */
SET @defaultCutOff = 60;
---

call create_last_art_outcome_at_facility(@endDate,@location);
---

select 
/* COUNT(IF(((datediff(map.next_appointment_date,map.visit_date)) < 80), 1, NULL)) as less_than_three_months,
 COUNT(IF(((datediff(map.next_appointment_date,map.visit_date)) BETWEEN 80 and 168), 1, NULL))  as three_to_five_months,
 COUNT(IF(((datediff(map.next_appointment_date,map.visit_date)) > 168), 1, NULL))  as six_months_plus,*/


 lfo.identifier, lfo.location,
 FLOOR((DATEDIFF(@endDate, mp.birthdate) / 365.25)) as age, gender


 #datediff(map.next_appointment_date,map.visit_date) as days_diff
    from mw_art_followup map
join
(
	select patient_id,pregnant_or_lactating, MAX(visit_date) as visit_date ,MAX(next_appointment_date) as last_appt_date 
    from mw_art_followup where visit_date <= @endDate
	group by patient_id
	) map1
ON map.patient_id = map1.patient_id and map.visit_date = map1.visit_date
join mw_patient mp on map.patient_id=mp.patient_id
#join omrs_patient_identifier opi on opi.patient_id=map.patient_id and type='arv number'
join last_facility_outcome lfo on lfo.pat=map.patient_id
 where state = "On antiretrovirals"
 and datediff(map.next_appointment_date,map.visit_date) > 168
and floor(datediff(@endDate,map.next_appointment_date)) <=  @defaultCutOff
'''

mmd_3_5months = '''
use openmrs_warehouse;
---
SET @location = {};
---
SET @endDate = "2025-03-31";
---
/* Pepfar Cut-off = 30, MoH cut-off = 60 */
SET @defaultCutOff = 60;
---

call create_last_art_outcome_at_facility(@endDate,@location);
---

select 
/* COUNT(IF(((datediff(map.next_appointment_date,map.visit_date)) < 80), 1, NULL)) as less_than_three_months,
 COUNT(IF(((datediff(map.next_appointment_date,map.visit_date)) BETWEEN 80 and 168), 1, NULL))  as three_to_five_months,
 COUNT(IF(((datediff(map.next_appointment_date,map.visit_date)) > 168), 1, NULL))  as six_months_plus,*/


 lfo.identifier, lfo.location,
 FLOOR((DATEDIFF(@endDate, mp.birthdate) / 365.25)) as age, gender


 #datediff(map.next_appointment_date,map.visit_date) as days_diff
    from mw_art_followup map
join
(
	select patient_id,pregnant_or_lactating, MAX(visit_date) as visit_date ,MAX(next_appointment_date) as last_appt_date 
    from mw_art_followup where visit_date <= @endDate
	group by patient_id
	) map1
ON map.patient_id = map1.patient_id and map.visit_date = map1.visit_date
join mw_patient mp on map.patient_id=mp.patient_id
#join omrs_patient_identifier opi on opi.patient_id=map.patient_id and type='arv number'
join last_facility_outcome lfo on lfo.pat=map.patient_id
 where state = "On antiretrovirals"
 and datediff(map.next_appointment_date,map.visit_date) BETWEEN 80 and 168
and floor(datediff(@endDate,map.next_appointment_date)) <=  @defaultCutOff;
'''

active_24months_before = '''
    /* Denominator */
    /* Active in care based on end date */
    use openmrs_warehouse;
    ---
    SET @endDate = "2023-03-31";
    ---
    SET @defaultCutOff = 60;
    ---
    SET @location= {};
    ---
	SELECT
        index_desc,
            opi.patient_id,
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
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and opi.location=@location
            and state IN ("On Antiretrovirals")
            and opi.patient_id in (
            SELECT patient_id FROM mw_art_followup where floor(datediff(@endDate,next_appointment_date)) <=  @defaultCutOff)
'''

active_12months_before = '''
    /* Denominator */
    /* Active in care based on end date */
    use openmrs_warehouse;
    ---
    SET @endDate = "2024-03-31";
    ---
    SET @defaultCutOff = 60;
    ---
    SET @location= {};
    ---
	SELECT
        index_desc,
            opi.patient_id,
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
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and opi.location=@location
            and state IN ("On Antiretrovirals")
            and opi.patient_id in (
            SELECT patient_id FROM mw_art_followup where floor(datediff(@endDate,next_appointment_date)) <=  @defaultCutOff)
'''

vl_suppression_num = '''
/* 4. Viral Load suppression */
/* Numerator */
USE openmrs_warehouse;
---
/* Space to cover 1 year 3 months between start date and end date */
SET @startDate = '2023-12-01';
---
SET @endDate = "2025-03-31";
---
SET @location = {};
---
select count(*)
from mw_art_viral_load mavl
join (
SELECT patient_id as p_id, max(visit_date) as last_visit_date 
FROM mw_art_viral_load
where visit_date <= @endDate
group by patient_id
) x
ON x.p_id = mavl.patient_id
and mavl.visit_date = x.last_visit_date
where visit_date between @startDate and @endDate and location = @location
and (ldl = "True" or less_than_limit <= 200 or viral_load_result <= 200) and other_results is null;
'''

vl_suppression_den = '''
/* Denominator */
USE openmrs_warehouse;
---
/* Space to cover 1 year 3 months between start date and end date */
SET @startDate = '2023-12-01';
---
SET @endDate = "2025-03-31";
---
SET @location = {};
---
select count(*)
from mw_art_viral_load mavl
join (
SELECT patient_id as p_id, max(visit_date) as last_visit_date 
FROM mw_art_viral_load
where visit_date <= @endDate
group by patient_id
) x
ON x.p_id = mavl.patient_id
and mavl.visit_date = x.last_visit_date
where visit_date between @startDate and @endDate and location = @location
and (ldl is not null or less_than_limit is not null or viral_load_result is not null) and other_results is null;
'''

retention_in_care_for_hiv_at_12months = '''
/* 3. % of ART retention at 12 month */
---
/* Numerator - Result should subtract to denominator to get number of patients in care */
---
use openmrs_warehouse;
---
SET @endDate = "2024-03-01";
---
SET @endReportindDate = "2025-03-31";
---
SET @defaultCutOff = 60;
---
SET @location={};
---
SELECT
count(*)
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
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and state IN ("On Antiretrovirals")
            and opi.patient_id in (
            SELECT patient_id FROM mw_art_followup where floor(datediff(@endDate,next_appointment_date)) <=  @defaultCutOff
)
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
                    where program IN ("HIV program")
                    and start_date <= @endReportindDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1 and opi.location=@location
            and state IN ("Patient died","treatment stopped","patient defaulted")        
            )
'''

retention_in_care_for_hiv_at_24months = '''
/* 3. % of ART retention at 12 month */
---
/* Numerator - Result should subtract to denominator to get number of patients in care */
---
use openmrs_warehouse;
---
SET @endDate = "2023-03-01";
---
SET @endReportindDate = "2025-03-31";
---
SET @defaultCutOff = 60;
---
SET @location={};
---
SELECT
count(*)
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
                    where program IN ("HIV Program")
                    and start_date <= @endDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1
            and state IN ("On Antiretrovirals")
            and opi.patient_id in (
            SELECT patient_id FROM mw_art_followup where floor(datediff(@endDate,next_appointment_date)) <=  @defaultCutOff
)
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
                    where program IN ("HIV program")
                    and start_date <= @endReportindDate
                    and location =  @location
            ORDER BY patient_id DESC, start_date DESC, program_state_id DESC
            ) index_descending
            join omrs_patient_identifier opi on index_descending.patient_id = opi.patient_id
            and opi.location = index_descending.location
            and opi.type = "ARV Number"
            where index_desc = 1 and opi.location=@location
            and state IN ("Patient died","treatment stopped","patient defaulted")        
            )
'''
