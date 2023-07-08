create table if not exists cpas (
    id serial not null primary key,
    name text not null
);

create table if not exists clients (
    id serial not null primary key,
    name text not null,
    address text not null,
    income int not null,
    materials_provided_at timestamp,
    cpa_id int not null references cpas(id)
);

create table if not exists assistants (
    id serial not null primary key,
    name text not null,
    cpa_id int not null references cpas(id)
);

create table if not exists tax_returns (
    id serial not null primary key,
    client_id int not null references clients(id),
    assistant_id int references assistants(id),
    cpa_id int not null references cpas(id),
    status text not null,
    filed_at timestamp,
    reviewed_at timestamp
);