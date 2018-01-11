station_list = ["成都","成都东","成都南","成都西","成都北","重庆","重庆北","重庆南"]
new_station_list = []
for str in station_list:
    if ("东" in str) or ("西" in str) or ("南" in str) or ("北" in str):
        new_str = str[:len(str) - 1]
        if new_str not in new_station_list:
            new_station_list.append(new_str)
print(new_station_list)

# delete traines
# where [id] not in (
# select max([id]) from traines
# group by (carname +fromstation+tostation+fromtime+totime+taketime+firstseat+secondseat+softbed+hardbed+hardseat+noseat))
#
# delete delete from traines a
# where (a.carname,a.fromstation,a.tostation,a.fromtime,a.totime,a.taketimea,a.firstseat,a.secondseat,a.softbed,a.hardbed,a.hardseat,a.noseat) in (select carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat from vitae group by carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat having count(*) > 1)
# and rowid not in (select min(rowid) from traines group by carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat having count(*)>1)
#
#
#
# create table tmp_relation_id2 as (select max(id) from traines group by carname,fromstation,tostation,fromtime,totime,taketime,firstseat,secondseat,softbed,hardbed,hardseat,noseat having count(*)>1)
#
# delete from traines where id in (select id from tmp_relation_id2)