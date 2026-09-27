create extension if not exists vector;

create table if not exists documents (
    document_id   text primary key,
    titel         text not null,
    artikelnummer text,
    impressum     text,
    sha256        text not null,
    quelle_url    text,
    abrufdatum    text
);

create table if not exists chunks (
    chunk_id            text primary key,
    document_id         text references documents(document_id),
    seite               int  not null,
    abschnitt           text,
    text                text not null,
    tokens              int,
    anwendbar_auf       text not null,
    ersetzt_grundregel  boolean default false,
    ersetzt_durch       text,
    embedding           vector(1536)
);

-- Bei rund 70 Chunks ist die exakte Suche schneller und genauer als ein
-- Naeherungsindex (ivfflat/hnsw); deshalb bewusst kein Vektorindex.

create or replace function match_chunks(
    query_embedding vector(1536),
    match_count     int,
    filter_variante text
) returns table (chunk_id text, similarity float)
language sql stable as $$
    select c.chunk_id, 1 - (c.embedding <=> query_embedding) as similarity
    from chunks c
    where case
        when filter_variante = 'grundspiel' then c.document_id = 'grundspiel'
        else c.document_id = 'staedte_ritter'
             or (c.document_id = 'grundspiel' and not c.ersetzt_grundregel)
    end
    order by c.embedding <=> query_embedding
    limit match_count;
$$;
