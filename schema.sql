create table users
(
    user_id serial primary key not null,
    fname varchar(50) not null,
    lname varchar(50) not null,
    email varchar(330) unique not null,
    password varchar(40) not null
);



create table hospitals
(
    hospital_id int primary key not null, "This can be something hospitals already have"
    name varchar(100) not null,
    max_bed int,
    current_bed int,
    "LOCATION to be added more efficiently"
    state varchar(30),
    district varchar(50),
    ventilator int,
    mask_needed int, "I don't know whether this is per day or the total numbers"
    mask_current int, "Current Inventory"
    testing_kits int,
    capability_day int, "Capability of doing number of tests"


);


create type  state_patient AS ENUM ('DEAD', 'MILD', 'CRITICAL', 'ASYMPTOMATIC',
'DISCHARGE_SOON', 'SUSPECTED', 'RECOVERED');



create table patients
(
    patient_id int primary key not null,
    name varchar(100) not null,
    sex varchar(4), "Handle genders?",
    hospital int references hospitals(hospital_id),

    condition state_patient,
    age int,
    disease varchar(100), "Can be enumerated"
    history varchar(1000),

);



create table administration
(
    doff_id primary key not null,
    off_id int references users(user_id),
    "Need to make a better location thing"
    state varchar(30),
    district varchar(50),
    designation varchar(50)


);

create table history
(
    history_id int primary key not null,
    hospital_id int references hospitals(hospital_id),
    date date,
    active int,
    recovered int,
    deaths int
);
