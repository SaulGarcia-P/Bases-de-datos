
CREATE TABLE show_types (
	type_name TEXT, 
	type_id BIGINT
)

;


CREATE TABLE ratings (
	code TEXT, 
	rating_id BIGINT
)

;


CREATE TABLE actors (
	full_name TEXT, 
	actor_id BIGINT
)

;


CREATE TABLE directors (
	full_name TEXT, 
	director_id BIGINT
)

;


CREATE TABLE countries (
	country_name TEXT, 
	country_id BIGINT
)

;


CREATE TABLE categories (
	category_name TEXT, 
	category_id BIGINT
)

;


CREATE TABLE show_actor (
	show_id TEXT, 
	actor_id BIGINT
)

;


CREATE TABLE show_director (
	show_id TEXT, 
	director_id BIGINT
)

;


CREATE TABLE show_country (
	show_id TEXT, 
	country_id BIGINT
)

;


CREATE TABLE show_category (
	show_id TEXT, 
	category_id BIGINT
)

;


CREATE TABLE shows (
	show_id TEXT, 
	type_id BIGINT, 
	title TEXT, 
	release_year BIGINT, 
	rating_id FLOAT(53), 
	duration TEXT, 
	description TEXT, 
	date_added TEXT
)

;

