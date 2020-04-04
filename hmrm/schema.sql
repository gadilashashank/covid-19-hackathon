create table users
(
    user_id serial primary key not null,
    fname varchar(50) not null,
    lname varchar(50) not null,
    email varchar(330) unique not null,
    password varchar(100) not null
);



create table hospitals
(
    hospital_id serial primary key not null,
    name varchar(100) not null,
    sname varchar(100) not null,
    admin varchar(330),
    phone_admin varchar(30) not null,
    phone_lab varchar(30) not null,
    address varchar(200),
    email_admin varchar(330),
    email_lab varchar(330),
    patient_capacity int,
    testing_capacity int,
    foreign key (admin) references users(email)
);


create type  state_patient AS ENUM ('DEAD', 'MILD', 'CRITICAL', 'ASYMPTOMATIC',
'DISCHARGE_SOON', 'SUSPECTED', 'RECOVERED');



create table patients
(
    patient_id serial primary key not null,
    name varchar(100) not null,
    sex varchar(10), -- "Handle genders?"
    hospital int not null,
    condition state_patient,
    age int,
    disease varchar(100), -- "Can be enumerated"
    history varchar(1000),
    foreign key (hospital) references hospitals(hospital_id)

);



create table administration
(
    doff_id serial primary key not null,
    name varchar(100),
    sname varchar(30),
    -- off_id int references users(user_id),
--    "Need to make a better location thing"
    --state varchar(30),
    --district varchar(50),
    region varchar(50)
);

create table history_hospital
(
    history_id int primary key not null,
    hospital_id int not null,
    date date,
    active int,
    recovered int,
    deaths int,
    foreign key (hospital_id) references hospitals(hospital_id)
);

create table history_patient
(
    patient_id_rec serial primary key not null,
    patient_id int not null,
    date date,
    condition state_patient,
    foreign key (patient_id) references patients(patient_id)
);

