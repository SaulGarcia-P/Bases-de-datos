
CREATE TABLE patients (
	patient_id BIGINT, 
	age FLOAT(53), 
	gender TEXT, 
	ethnicity TEXT, 
	height FLOAT(53)
)

;


CREATE TABLE hospitals (
	hospital_id BIGINT
)

;


CREATE TABLE icus (
	icu_id BIGINT, 
	icu_type TEXT, 
	icu_stay_type TEXT
)

;


CREATE TABLE encounters (
	encounter_id BIGINT, 
	patient_id BIGINT, 
	hospital_id BIGINT, 
	bmi FLOAT(53), 
	elective_surgery BIGINT, 
	icu_admit_source TEXT, 
	icu_id BIGINT, 
	pre_icu_los_days FLOAT(53), 
	weight FLOAT(53), 
	apache_2_diagnosis FLOAT(53), 
	apache_3j_diagnosis FLOAT(53), 
	apache_post_operative BIGINT, 
	arf_apache FLOAT(53), 
	gcs_eyes_apache FLOAT(53), 
	gcs_motor_apache FLOAT(53), 
	gcs_unable_apache FLOAT(53), 
	gcs_verbal_apache FLOAT(53), 
	heart_rate_apache FLOAT(53), 
	intubated_apache FLOAT(53), 
	map_apache FLOAT(53), 
	resprate_apache FLOAT(53), 
	temp_apache FLOAT(53), 
	ventilated_apache FLOAT(53), 
	d1_diasbp_max FLOAT(53), 
	d1_diasbp_min FLOAT(53), 
	d1_diasbp_noninvasive_max FLOAT(53), 
	d1_diasbp_noninvasive_min FLOAT(53), 
	d1_heartrate_max FLOAT(53), 
	d1_heartrate_min FLOAT(53), 
	d1_mbp_max FLOAT(53), 
	d1_mbp_min FLOAT(53), 
	d1_mbp_noninvasive_max FLOAT(53), 
	d1_mbp_noninvasive_min FLOAT(53), 
	d1_resprate_max FLOAT(53), 
	d1_resprate_min FLOAT(53), 
	d1_spo2_max FLOAT(53), 
	d1_spo2_min FLOAT(53), 
	d1_sysbp_max FLOAT(53), 
	d1_sysbp_min FLOAT(53), 
	d1_sysbp_noninvasive_max FLOAT(53), 
	d1_sysbp_noninvasive_min FLOAT(53), 
	d1_temp_max FLOAT(53), 
	d1_temp_min FLOAT(53), 
	h1_diasbp_max FLOAT(53), 
	h1_diasbp_min FLOAT(53), 
	h1_diasbp_noninvasive_max FLOAT(53), 
	h1_diasbp_noninvasive_min FLOAT(53), 
	h1_heartrate_max FLOAT(53), 
	h1_heartrate_min FLOAT(53), 
	h1_mbp_max FLOAT(53), 
	h1_mbp_min FLOAT(53), 
	h1_mbp_noninvasive_max FLOAT(53), 
	h1_mbp_noninvasive_min FLOAT(53), 
	h1_resprate_max FLOAT(53), 
	h1_resprate_min FLOAT(53), 
	h1_spo2_max FLOAT(53), 
	h1_spo2_min FLOAT(53), 
	h1_sysbp_max FLOAT(53), 
	h1_sysbp_min FLOAT(53), 
	h1_sysbp_noninvasive_max FLOAT(53), 
	h1_sysbp_noninvasive_min FLOAT(53), 
	d1_glucose_max FLOAT(53), 
	d1_glucose_min FLOAT(53), 
	d1_potassium_max FLOAT(53), 
	d1_potassium_min FLOAT(53), 
	apache_4a_hospital_death_prob FLOAT(53), 
	apache_4a_icu_death_prob FLOAT(53), 
	aids FLOAT(53), 
	cirrhosis FLOAT(53), 
	diabetes_mellitus FLOAT(53), 
	hepatic_failure FLOAT(53), 
	immunosuppression FLOAT(53), 
	leukemia FLOAT(53), 
	lymphoma FLOAT(53), 
	solid_tumor_with_metastasis FLOAT(53), 
	apache_3j_bodysystem TEXT, 
	apache_2_bodysystem TEXT, 
	`Unnamed: 83` FLOAT(53), 
	hospital_death BIGINT
)

;

