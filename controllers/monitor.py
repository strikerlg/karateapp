# -*- coding: utf-8 -*-
# try something like
def index(): 

    sql ="""

with ganador as(
select athlete_win_id as at_id
 ,id as pelea_id,phase, subcategory_id  from fight 
where athlete_win_id is not null
),
 perdedor as(
select 
case when athlete_win_id<>athlete_blue_id then athlete_blue_id
 when athlete_win_id<>athlete_red_id then athlete_red_id
 end as at_id
 ,id as pelea_id,phase, subcategory_id  from fight 
where athlete_win_id is not null
)
, subcat as(
select subcategory_id as id,max(phase) as max_phase from fight
group by subcategory_id
),
ganador_med_tmp as (
select * , case when phase = max_phase  then 1 else 0 end as oro, case when phase = max_phase-1  then 1 else 0 end as bronce , 0 as plata from ganador a
join subcat b on a.subcategory_id=b.id
)
,
perdedor_med_tmp as (
select at_id,subcategory_id
 , 0 as oro, case when phase = max_phase-1  then 1 else 0 end as bronce, case when phase = max_phase  then 1 else 0 end as plata  from perdedor a
join subcat b on a.subcategory_id=b.id
),
ganador_med as (
select at_id,subcategory_id,sum(oro) as oro , case when sum(oro)=0 then sum(bronce) else 0 end as bronce , 0 as plata from ganador_med_tmp
group by at_id,subcategory_id
),
perdedor_med as (
select at_id,subcategory_id,0 as oro, sum(bronce) as bronce ,sum(plata) as plata  from perdedor_med_tmp
group by at_id,subcategory_id 
)
select count(*) as victorias ,c.name as escuela from ganador a
join athlete d on a.at_id=d.id
join dojo b on d.dojo_id=b.id
join school c on b.school_id=c.id
group by escuela 

order by 1 desc


     

    """
    rs = db.executesql(sql, as_dict=True)

    return dict(rs = rs)