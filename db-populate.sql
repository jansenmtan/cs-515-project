USE cs_515_project;

INSERT IGNORE INTO Customer (
    cid,
    cname,
    email,
    address,
    password
) VALUES
(
    1,
    'John Doe',
    'jd@ex.io',
    '123 First Street',
    'jd'
),
(
    15,
    'Johnson Samuel',
	'js@ex.io',
    '123 E Montgomery Ln',
	'js'
),
(
	27,
	'Tanya Stevens',
	'ts@ex.io',
	'3280 S Michigan Rd',
	'ts'
),
(
	632,
	'Mark Halle',
	'mh@ex.io',
	'1555 W 155th Ln',
	'mh'
),
(
	93,
	'Hyden Hughes',
	'hh@ex.io',
	'665 N Otthat Cir',
	'hh'
);

INSERT IGNORE INTO City (
	cityid,
	title,
	state
) VALUES
(
	1,
	'Chicago',
	'IL'
),
(
	2,
	'Los Angeles',
	'CA'
),
(
	3,
	'Houston',
	'TX'
),
(
	4,
	'New York City',
	'NY'
),
(
	5,
	'Atlanta',
	'GA'
),
(
	6,
	'Seattle',
	'WA'
);

INSERT IGNORE INTO Flight (
	fid,
	fnumber,
	fdate,
	ftime,
	price,
	class,
	capacity,
	available,
	orig,
	dest
) VALUES
(
	1,
	102,
	'2022-12-21',
	'10:51:29',
	203.10,
	2,
	100,
	10,
	1,
	5
),
(
	2,
	521,
	'2023-02-01',
	'07:21:00',
	300.99,
	1,
	100,
	79,
	5,
	1
),
(
	21,
	125,
	'2023-01-13',
	'10:00:00',
	250.01,
	2,
	100,
	32,
	5,
	1
),
(
	22,
	125,
	'2023-01-15',
	'12:30:00',
	290.00,
	1,
	100,
	0,
	5,
	1
),
(
	3,
	192,
	'2023-01-21',
	'17:27:00',
	172.72,
	3,
	272,
	27,
	3,
	2
),
(
	4,
	944,
	'2022-12-29',
	'01:30:00',
	199.99,
	1,
	150,
	0,
	2,
	3
),
(
	5,
	231,
	'2023-03-23',
	'13:33:33',
	333.33,
	2,
	333,
	33,
	4,
	6
);

/* no need to populate reservations; */
/*	can do so during 'production' */
