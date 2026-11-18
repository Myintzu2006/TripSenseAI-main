% Asia travel recommender facts and rules
% Separate from the Python system. Query with SWI-Prolog.
:- discontiguous destination/1.
:- discontiguous country/2.
:- discontiguous region/2.
:- discontiguous place_type/2.
:- discontiguous budget/2.
:- discontiguous weather/2.
:- discontiguous trip_days/3.
:- discontiguous culture/2.
:- discontiguous food/2.
:- discontiguous nature/2.
:- discontiguous nightlife/2.
:- discontiguous shopping/2.
:- discontiguous quiet/2.
:- discontiguous adventure/2.
:- discontiguous transport/2.

destination(bagan).
country(bagan, myanmar).
region(bagan, southeast_asia).
place_type(bagan, historical).
budget(bagan, low).
weather(bagan, hot).
trip_days(bagan, 2, 4).
culture(bagan, 5).
food(bagan, 3).
nature(bagan, 3).
nightlife(bagan, 1).
shopping(bagan, 2).
quiet(bagan, 4).
adventure(bagan, 3).
transport(bagan, 2).

destination(inle_lake).
country(inle_lake, myanmar).
region(inle_lake, southeast_asia).
place_type(inle_lake, nature).
budget(inle_lake, low).
weather(inle_lake, warm).
trip_days(inle_lake, 2, 4).
culture(inle_lake, 4).
food(inle_lake, 4).
nature(inle_lake, 5).
nightlife(inle_lake, 1).
shopping(inle_lake, 2).
quiet(inle_lake, 5).
adventure(inle_lake, 2).
transport(inle_lake, 2).

destination(yangon).
country(yangon, myanmar).
region(yangon, southeast_asia).
place_type(yangon, city).
budget(yangon, low).
weather(yangon, hot).
trip_days(yangon, 2, 3).
culture(yangon, 4).
food(yangon, 4).
nature(yangon, 2).
nightlife(yangon, 2).
shopping(yangon, 3).
quiet(yangon, 2).
adventure(yangon, 2).
transport(yangon, 3).

destination(mandalay).
country(mandalay, myanmar).
region(mandalay, southeast_asia).
place_type(mandalay, historical).
budget(mandalay, low).
weather(mandalay, hot).
trip_days(mandalay, 2, 4).
culture(mandalay, 5).
food(mandalay, 3).
nature(mandalay, 2).
nightlife(mandalay, 1).
shopping(mandalay, 2).
quiet(mandalay, 3).
adventure(mandalay, 2).
transport(mandalay, 3).

destination(ngapali).
country(ngapali, myanmar).
region(ngapali, southeast_asia).
place_type(ngapali, beach).
budget(ngapali, medium).
weather(ngapali, hot).
trip_days(ngapali, 3, 5).
culture(ngapali, 2).
food(ngapali, 3).
nature(ngapali, 3).
nightlife(ngapali, 1).
shopping(ngapali, 1).
quiet(ngapali, 4).
adventure(ngapali, 2).
transport(ngapali, 2).

destination(hpa_an).
country(hpa_an, myanmar).
region(hpa_an, southeast_asia).
place_type(hpa_an, adventure).
budget(hpa_an, low).
weather(hpa_an, hot).
trip_days(hpa_an, 2, 4).
culture(hpa_an, 3).
food(hpa_an, 3).
nature(hpa_an, 5).
nightlife(hpa_an, 1).
shopping(hpa_an, 1).
quiet(hpa_an, 4).
adventure(hpa_an, 5).
transport(hpa_an, 2).

destination(bangkok).
country(bangkok, thailand).
region(bangkok, southeast_asia).
place_type(bangkok, city).
budget(bangkok, medium).
weather(bangkok, hot).
trip_days(bangkok, 3, 5).
culture(bangkok, 4).
food(bangkok, 5).
nature(bangkok, 2).
nightlife(bangkok, 5).
shopping(bangkok, 5).
quiet(bangkok, 1).
adventure(bangkok, 2).
transport(bangkok, 5).

destination(chiang_mai).
country(chiang_mai, thailand).
region(chiang_mai, southeast_asia).
place_type(chiang_mai, historical).
budget(chiang_mai, low).
weather(chiang_mai, warm).
trip_days(chiang_mai, 3, 5).
culture(chiang_mai, 5).
food(chiang_mai, 5).
nature(chiang_mai, 4).
nightlife(chiang_mai, 2).
shopping(chiang_mai, 3).
quiet(chiang_mai, 3).
adventure(chiang_mai, 3).
transport(chiang_mai, 4).

destination(phuket).
country(phuket, thailand).
region(phuket, southeast_asia).
place_type(phuket, beach).
budget(phuket, medium).
weather(phuket, hot).
trip_days(phuket, 4, 7).
culture(phuket, 2).
food(phuket, 4).
nature(phuket, 3).
nightlife(phuket, 5).
shopping(phuket, 3).
quiet(phuket, 2).
adventure(phuket, 4).
transport(phuket, 3).

destination(krabi).
country(krabi, thailand).
region(krabi, southeast_asia).
place_type(krabi, adventure).
budget(krabi, medium).
weather(krabi, hot).
trip_days(krabi, 3, 5).
culture(krabi, 2).
food(krabi, 4).
nature(krabi, 5).
nightlife(krabi, 2).
shopping(krabi, 2).
quiet(krabi, 3).
adventure(krabi, 5).
transport(krabi, 3).

destination(ayutthaya).
country(ayutthaya, thailand).
region(ayutthaya, southeast_asia).
place_type(ayutthaya, historical).
budget(ayutthaya, low).
weather(ayutthaya, hot).
trip_days(ayutthaya, 1, 2).
culture(ayutthaya, 5).
food(ayutthaya, 3).
nature(ayutthaya, 2).
nightlife(ayutthaya, 1).
shopping(ayutthaya, 2).
quiet(ayutthaya, 3).
adventure(ayutthaya, 2).
transport(ayutthaya, 4).

destination(pai).
country(pai, thailand).
region(pai, southeast_asia).
place_type(pai, nature).
budget(pai, low).
weather(pai, warm).
trip_days(pai, 2, 4).
culture(pai, 3).
food(pai, 3).
nature(pai, 5).
nightlife(pai, 2).
shopping(pai, 2).
quiet(pai, 4).
adventure(pai, 3).
transport(pai, 2).

destination(chiang_rai).
country(chiang_rai, thailand).
region(chiang_rai, southeast_asia).
place_type(chiang_rai, historical).
budget(chiang_rai, low).
weather(chiang_rai, warm).
trip_days(chiang_rai, 2, 3).
culture(chiang_rai, 5).
food(chiang_rai, 3).
nature(chiang_rai, 4).
nightlife(chiang_rai, 1).
shopping(chiang_rai, 2).
quiet(chiang_rai, 4).
adventure(chiang_rai, 2).
transport(chiang_rai, 3).

destination(koh_samui).
country(koh_samui, thailand).
region(koh_samui, southeast_asia).
place_type(koh_samui, romantic).
budget(koh_samui, medium).
weather(koh_samui, hot).
trip_days(koh_samui, 4, 7).
culture(koh_samui, 2).
food(koh_samui, 4).
nature(koh_samui, 3).
nightlife(koh_samui, 3).
shopping(koh_samui, 3).
quiet(koh_samui, 3).
adventure(koh_samui, 3).
transport(koh_samui, 3).

destination(hanoi).
country(hanoi, vietnam).
region(hanoi, southeast_asia).
place_type(hanoi, city).
budget(hanoi, low).
weather(hanoi, warm).
trip_days(hanoi, 3, 4).
culture(hanoi, 5).
food(hanoi, 5).
nature(hanoi, 2).
nightlife(hanoi, 3).
shopping(hanoi, 3).
quiet(hanoi, 2).
adventure(hanoi, 2).
transport(hanoi, 4).

destination(ho_chi_minh_city).
country(ho_chi_minh_city, vietnam).
region(ho_chi_minh_city, southeast_asia).
place_type(ho_chi_minh_city, city).
budget(ho_chi_minh_city, low).
weather(ho_chi_minh_city, hot).
trip_days(ho_chi_minh_city, 3, 5).
culture(ho_chi_minh_city, 4).
food(ho_chi_minh_city, 5).
nature(ho_chi_minh_city, 1).
nightlife(ho_chi_minh_city, 5).
shopping(ho_chi_minh_city, 4).
quiet(ho_chi_minh_city, 1).
adventure(ho_chi_minh_city, 2).
transport(ho_chi_minh_city, 4).

destination(hoi_an).
country(hoi_an, vietnam).
region(hoi_an, southeast_asia).
place_type(hoi_an, romantic).
budget(hoi_an, low).
weather(hoi_an, warm).
trip_days(hoi_an, 3, 5).
culture(hoi_an, 5).
food(hoi_an, 5).
nature(hoi_an, 3).
nightlife(hoi_an, 2).
shopping(hoi_an, 3).
quiet(hoi_an, 4).
adventure(hoi_an, 2).
transport(hoi_an, 3).

destination(ha_long_bay).
country(ha_long_bay, vietnam).
region(ha_long_bay, southeast_asia).
place_type(ha_long_bay, nature).
budget(ha_long_bay, medium).
weather(ha_long_bay, warm).
trip_days(ha_long_bay, 2, 3).
culture(ha_long_bay, 3).
food(ha_long_bay, 3).
nature(ha_long_bay, 5).
nightlife(ha_long_bay, 1).
shopping(ha_long_bay, 1).
quiet(ha_long_bay, 4).
adventure(ha_long_bay, 3).
transport(ha_long_bay, 2).

destination(sapa).
country(sapa, vietnam).
region(sapa, southeast_asia).
place_type(sapa, mountain).
budget(sapa, low).
weather(sapa, cool).
trip_days(sapa, 2, 4).
culture(sapa, 4).
food(sapa, 3).
nature(sapa, 5).
nightlife(sapa, 1).
shopping(sapa, 2).
quiet(sapa, 4).
adventure(sapa, 4).
transport(sapa, 2).

destination(hue).
country(hue, vietnam).
region(hue, southeast_asia).
place_type(hue, historical).
budget(hue, low).
weather(hue, warm).
trip_days(hue, 2, 3).
culture(hue, 5).
food(hue, 4).
nature(hue, 3).
nightlife(hue, 1).
shopping(hue, 2).
quiet(hue, 4).
adventure(hue, 2).
transport(hue, 3).

destination(da_nang).
country(da_nang, vietnam).
region(da_nang, southeast_asia).
place_type(da_nang, beach).
budget(da_nang, medium).
weather(da_nang, warm).
trip_days(da_nang, 3, 5).
culture(da_nang, 3).
food(da_nang, 4).
nature(da_nang, 3).
nightlife(da_nang, 3).
shopping(da_nang, 3).
quiet(da_nang, 2).
adventure(da_nang, 3).
transport(da_nang, 4).

destination(ninh_binh).
country(ninh_binh, vietnam).
region(ninh_binh, southeast_asia).
place_type(ninh_binh, nature).
budget(ninh_binh, low).
weather(ninh_binh, warm).
trip_days(ninh_binh, 2, 3).
culture(ninh_binh, 4).
food(ninh_binh, 3).
nature(ninh_binh, 5).
nightlife(ninh_binh, 1).
shopping(ninh_binh, 1).
quiet(ninh_binh, 5).
adventure(ninh_binh, 3).
transport(ninh_binh, 3).

destination(siem_reap).
country(siem_reap, cambodia).
region(siem_reap, southeast_asia).
place_type(siem_reap, historical).
budget(siem_reap, low).
weather(siem_reap, hot).
trip_days(siem_reap, 3, 5).
culture(siem_reap, 5).
food(siem_reap, 4).
nature(siem_reap, 3).
nightlife(siem_reap, 3).
shopping(siem_reap, 3).
quiet(siem_reap, 3).
adventure(siem_reap, 2).
transport(siem_reap, 3).

destination(phnom_penh).
country(phnom_penh, cambodia).
region(phnom_penh, southeast_asia).
place_type(phnom_penh, city).
budget(phnom_penh, low).
weather(phnom_penh, hot).
trip_days(phnom_penh, 2, 3).
culture(phnom_penh, 4).
food(phnom_penh, 4).
nature(phnom_penh, 1).
nightlife(phnom_penh, 3).
shopping(phnom_penh, 3).
quiet(phnom_penh, 2).
adventure(phnom_penh, 2).
transport(phnom_penh, 3).

destination(kampot).
country(kampot, cambodia).
region(kampot, southeast_asia).
place_type(kampot, nature).
budget(kampot, low).
weather(kampot, hot).
trip_days(kampot, 2, 4).
culture(kampot, 3).
food(kampot, 4).
nature(kampot, 4).
nightlife(kampot, 2).
shopping(kampot, 1).
quiet(kampot, 5).
adventure(kampot, 2).
transport(kampot, 2).

destination(kep).
country(kep, cambodia).
region(kep, southeast_asia).
place_type(kep, nature).
budget(kep, low).
weather(kep, hot).
trip_days(kep, 1, 3).
culture(kep, 2).
food(kep, 5).
nature(kep, 3).
nightlife(kep, 1).
shopping(kep, 1).
quiet(kep, 5).
adventure(kep, 2).
transport(kep, 2).

destination(battambang).
country(battambang, cambodia).
region(battambang, southeast_asia).
place_type(battambang, historical).
budget(battambang, low).
weather(battambang, hot).
trip_days(battambang, 2, 3).
culture(battambang, 4).
food(battambang, 3).
nature(battambang, 3).
nightlife(battambang, 1).
shopping(battambang, 2).
quiet(battambang, 4).
adventure(battambang, 2).
transport(battambang, 2).

destination(koh_rong).
country(koh_rong, cambodia).
region(koh_rong, southeast_asia).
place_type(koh_rong, beach).
budget(koh_rong, medium).
weather(koh_rong, hot).
trip_days(koh_rong, 3, 5).
culture(koh_rong, 1).
food(koh_rong, 3).
nature(koh_rong, 4).
nightlife(koh_rong, 3).
shopping(koh_rong, 1).
quiet(koh_rong, 3).
adventure(koh_rong, 4).
transport(koh_rong, 1).

destination(kuala_lumpur).
country(kuala_lumpur, malaysia).
region(kuala_lumpur, southeast_asia).
place_type(kuala_lumpur, city).
budget(kuala_lumpur, medium).
weather(kuala_lumpur, hot).
trip_days(kuala_lumpur, 3, 5).
culture(kuala_lumpur, 4).
food(kuala_lumpur, 5).
nature(kuala_lumpur, 2).
nightlife(kuala_lumpur, 4).
shopping(kuala_lumpur, 5).
quiet(kuala_lumpur, 1).
adventure(kuala_lumpur, 2).
transport(kuala_lumpur, 5).

destination(penang).
country(penang, malaysia).
region(penang, southeast_asia).
place_type(penang, historical).
budget(penang, medium).
weather(penang, hot).
trip_days(penang, 3, 5).
culture(penang, 5).
food(penang, 5).
nature(penang, 2).
nightlife(penang, 3).
shopping(penang, 3).
quiet(penang, 2).
adventure(penang, 2).
transport(penang, 4).

destination(langkawi).
country(langkawi, malaysia).
region(langkawi, southeast_asia).
place_type(langkawi, beach).
budget(langkawi, medium).
weather(langkawi, hot).
trip_days(langkawi, 4, 6).
culture(langkawi, 2).
food(langkawi, 4).
nature(langkawi, 4).
nightlife(langkawi, 2).
shopping(langkawi, 3).
quiet(langkawi, 3).
adventure(langkawi, 3).
transport(langkawi, 3).

destination(cameron_highlands).
country(cameron_highlands, malaysia).
region(cameron_highlands, southeast_asia).
place_type(cameron_highlands, nature).
budget(cameron_highlands, medium).
weather(cameron_highlands, cool).
trip_days(cameron_highlands, 2, 3).
culture(cameron_highlands, 2).
food(cameron_highlands, 3).
nature(cameron_highlands, 5).
nightlife(cameron_highlands, 1).
shopping(cameron_highlands, 2).
quiet(cameron_highlands, 4).
adventure(cameron_highlands, 2).
transport(cameron_highlands, 3).

destination(malacca).
country(malacca, malaysia).
region(malacca, southeast_asia).
place_type(malacca, historical).
budget(malacca, medium).
weather(malacca, hot).
trip_days(malacca, 1, 3).
culture(malacca, 5).
food(malacca, 4).
nature(malacca, 1).
nightlife(malacca, 2).
shopping(malacca, 3).
quiet(malacca, 3).
adventure(malacca, 1).
transport(malacca, 4).

destination(kota_kinabalu).
country(kota_kinabalu, malaysia).
region(kota_kinabalu, southeast_asia).
place_type(kota_kinabalu, adventure).
budget(kota_kinabalu, medium).
weather(kota_kinabalu, hot).
trip_days(kota_kinabalu, 3, 5).
culture(kota_kinabalu, 3).
food(kota_kinabalu, 4).
nature(kota_kinabalu, 5).
nightlife(kota_kinabalu, 2).
shopping(kota_kinabalu, 2).
quiet(kota_kinabalu, 3).
adventure(kota_kinabalu, 5).
transport(kota_kinabalu, 3).

destination(taman_negara).
country(taman_negara, malaysia).
region(taman_negara, southeast_asia).
place_type(taman_negara, nature).
budget(taman_negara, medium).
weather(taman_negara, hot).
trip_days(taman_negara, 2, 4).
culture(taman_negara, 2).
food(taman_negara, 2).
nature(taman_negara, 5).
nightlife(taman_negara, 1).
shopping(taman_negara, 1).
quiet(taman_negara, 4).
adventure(taman_negara, 5).
transport(taman_negara, 2).

destination(singapore_city).
country(singapore_city, singapore).
region(singapore_city, southeast_asia).
place_type(singapore_city, city).
budget(singapore_city, high).
weather(singapore_city, hot).
trip_days(singapore_city, 3, 5).
culture(singapore_city, 4).
food(singapore_city, 5).
nature(singapore_city, 2).
nightlife(singapore_city, 4).
shopping(singapore_city, 5).
quiet(singapore_city, 1).
adventure(singapore_city, 2).
transport(singapore_city, 5).

destination(sentosa).
country(sentosa, singapore).
region(sentosa, southeast_asia).
place_type(sentosa, beach).
budget(sentosa, high).
weather(sentosa, hot).
trip_days(sentosa, 1, 2).
culture(sentosa, 2).
food(sentosa, 3).
nature(sentosa, 3).
nightlife(sentosa, 3).
shopping(sentosa, 3).
quiet(sentosa, 2).
adventure(sentosa, 3).
transport(sentosa, 5).

destination(pulau_ubin).
country(pulau_ubin, singapore).
region(pulau_ubin, southeast_asia).
place_type(pulau_ubin, nature).
budget(pulau_ubin, medium).
weather(pulau_ubin, hot).
trip_days(pulau_ubin, 1, 1).
culture(pulau_ubin, 3).
food(pulau_ubin, 2).
nature(pulau_ubin, 5).
nightlife(pulau_ubin, 1).
shopping(pulau_ubin, 1).
quiet(pulau_ubin, 5).
adventure(pulau_ubin, 3).
transport(pulau_ubin, 2).

destination(mandai).
country(mandai, singapore).
region(mandai, southeast_asia).
place_type(mandai, nature).
budget(mandai, high).
weather(mandai, hot).
trip_days(mandai, 1, 2).
culture(mandai, 2).
food(mandai, 2).
nature(mandai, 5).
nightlife(mandai, 1).
shopping(mandai, 1).
quiet(mandai, 3).
adventure(mandai, 2).
transport(mandai, 5).

destination(jakarta).
country(jakarta, indonesia).
region(jakarta, southeast_asia).
place_type(jakarta, city).
budget(jakarta, medium).
weather(jakarta, hot).
trip_days(jakarta, 2, 4).
culture(jakarta, 4).
food(jakarta, 5).
nature(jakarta, 1).
nightlife(jakarta, 4).
shopping(jakarta, 4).
quiet(jakarta, 1).
adventure(jakarta, 2).
transport(jakarta, 3).

destination(yogyakarta).
country(yogyakarta, indonesia).
region(yogyakarta, southeast_asia).
place_type(yogyakarta, historical).
budget(yogyakarta, low).
weather(yogyakarta, hot).
trip_days(yogyakarta, 3, 5).
culture(yogyakarta, 5).
food(yogyakarta, 4).
nature(yogyakarta, 3).
nightlife(yogyakarta, 2).
shopping(yogyakarta, 3).
quiet(yogyakarta, 3).
adventure(yogyakarta, 2).
transport(yogyakarta, 3).

destination(ubud).
country(ubud, indonesia).
region(ubud, southeast_asia).
place_type(ubud, nature).
budget(ubud, medium).
weather(ubud, warm).
trip_days(ubud, 4, 6).
culture(ubud, 5).
food(ubud, 4).
nature(ubud, 5).
nightlife(ubud, 2).
shopping(ubud, 3).
quiet(ubud, 4).
adventure(ubud, 3).
transport(ubud, 2).

destination(seminyak).
country(seminyak, indonesia).
region(seminyak, southeast_asia).
place_type(seminyak, beach).
budget(seminyak, medium).
weather(seminyak, hot).
trip_days(seminyak, 4, 7).
culture(seminyak, 2).
food(seminyak, 4).
nature(seminyak, 2).
nightlife(seminyak, 5).
shopping(seminyak, 4).
quiet(seminyak, 1).
adventure(seminyak, 2).
transport(seminyak, 3).

destination(uluwatu).
country(uluwatu, indonesia).
region(uluwatu, southeast_asia).
place_type(uluwatu, romantic).
budget(uluwatu, medium).
weather(uluwatu, hot).
trip_days(uluwatu, 3, 5).
culture(uluwatu, 4).
food(uluwatu, 4).
nature(uluwatu, 3).
nightlife(uluwatu, 3).
shopping(uluwatu, 2).
quiet(uluwatu, 3).
adventure(uluwatu, 3).
transport(uluwatu, 2).

destination(lombok).
country(lombok, indonesia).
region(lombok, southeast_asia).
place_type(lombok, beach).
budget(lombok, medium).
weather(lombok, hot).
trip_days(lombok, 4, 7).
culture(lombok, 3).
food(lombok, 3).
nature(lombok, 5).
nightlife(lombok, 2).
shopping(lombok, 2).
quiet(lombok, 4).
adventure(lombok, 4).
transport(lombok, 2).

destination(bandung).
country(bandung, indonesia).
region(bandung, southeast_asia).
place_type(bandung, city).
budget(bandung, medium).
weather(bandung, cool).
trip_days(bandung, 2, 4).
culture(bandung, 3).
food(bandung, 4).
nature(bandung, 3).
nightlife(bandung, 3).
shopping(bandung, 4).
quiet(bandung, 3).
adventure(bandung, 2).
transport(bandung, 3).

destination(labuan_bajo).
country(labuan_bajo, indonesia).
region(labuan_bajo, southeast_asia).
place_type(labuan_bajo, adventure).
budget(labuan_bajo, high).
weather(labuan_bajo, hot).
trip_days(labuan_bajo, 3, 5).
culture(labuan_bajo, 2).
food(labuan_bajo, 3).
nature(labuan_bajo, 5).
nightlife(labuan_bajo, 2).
shopping(labuan_bajo, 1).
quiet(labuan_bajo, 3).
adventure(labuan_bajo, 5).
transport(labuan_bajo, 2).

destination(manila).
country(manila, philippines).
region(manila, southeast_asia).
place_type(manila, city).
budget(manila, medium).
weather(manila, hot).
trip_days(manila, 2, 3).
culture(manila, 3).
food(manila, 4).
nature(manila, 1).
nightlife(manila, 4).
shopping(manila, 4).
quiet(manila, 1).
adventure(manila, 2).
transport(manila, 3).

destination(cebu).
country(cebu, philippines).
region(cebu, southeast_asia).
place_type(cebu, city).
budget(cebu, medium).
weather(cebu, hot).
trip_days(cebu, 3, 5).
culture(cebu, 3).
food(cebu, 4).
nature(cebu, 3).
nightlife(cebu, 3).
shopping(cebu, 3).
quiet(cebu, 2).
adventure(cebu, 4).
transport(cebu, 3).

destination(el_nido).
country(el_nido, philippines).
region(el_nido, southeast_asia).
place_type(el_nido, beach).
budget(el_nido, medium).
weather(el_nido, hot).
trip_days(el_nido, 4, 6).
culture(el_nido, 2).
food(el_nido, 3).
nature(el_nido, 5).
nightlife(el_nido, 3).
shopping(el_nido, 2).
quiet(el_nido, 3).
adventure(el_nido, 5).
transport(el_nido, 2).

destination(coron).
country(coron, philippines).
region(coron, southeast_asia).
place_type(coron, adventure).
budget(coron, medium).
weather(coron, hot).
trip_days(coron, 3, 5).
culture(coron, 2).
food(coron, 3).
nature(coron, 5).
nightlife(coron, 2).
shopping(coron, 1).
quiet(coron, 3).
adventure(coron, 5).
transport(coron, 2).

destination(boracay).
country(boracay, philippines).
region(boracay, southeast_asia).
place_type(boracay, beach).
budget(boracay, medium).
weather(boracay, hot).
trip_days(boracay, 3, 5).
culture(boracay, 1).
food(boracay, 4).
nature(boracay, 3).
nightlife(boracay, 5).
shopping(boracay, 3).
quiet(boracay, 2).
adventure(boracay, 3).
transport(boracay, 3).

destination(bohol).
country(bohol, philippines).
region(bohol, southeast_asia).
place_type(bohol, nature).
budget(bohol, medium).
weather(bohol, hot).
trip_days(bohol, 3, 5).
culture(bohol, 3).
food(bohol, 3).
nature(bohol, 5).
nightlife(bohol, 1).
shopping(bohol, 2).
quiet(bohol, 4).
adventure(bohol, 3).
transport(bohol, 3).

destination(siargao).
country(siargao, philippines).
region(siargao, southeast_asia).
place_type(siargao, adventure).
budget(siargao, medium).
weather(siargao, hot).
trip_days(siargao, 4, 7).
culture(siargao, 1).
food(siargao, 3).
nature(siargao, 5).
nightlife(siargao, 3).
shopping(siargao, 1).
quiet(siargao, 3).
adventure(siargao, 5).
transport(siargao, 2).

destination(tokyo).
country(tokyo, japan).
region(tokyo, east_asia).
place_type(tokyo, city).
budget(tokyo, high).
weather(tokyo, cool).
trip_days(tokyo, 4, 7).
culture(tokyo, 4).
food(tokyo, 5).
nature(tokyo, 2).
nightlife(tokyo, 5).
shopping(tokyo, 5).
quiet(tokyo, 1).
adventure(tokyo, 2).
transport(tokyo, 5).

destination(kyoto).
country(kyoto, japan).
region(kyoto, east_asia).
place_type(kyoto, historical).
budget(kyoto, medium).
weather(kyoto, cool).
trip_days(kyoto, 4, 6).
culture(kyoto, 5).
food(kyoto, 5).
nature(kyoto, 4).
nightlife(kyoto, 2).
shopping(kyoto, 3).
quiet(kyoto, 4).
adventure(kyoto, 2).
transport(kyoto, 5).

destination(osaka).
country(osaka, japan).
region(osaka, east_asia).
place_type(osaka, city).
budget(osaka, medium).
weather(osaka, cool).
trip_days(osaka, 3, 5).
culture(osaka, 3).
food(osaka, 5).
nature(osaka, 1).
nightlife(osaka, 5).
shopping(osaka, 4).
quiet(osaka, 1).
adventure(osaka, 2).
transport(osaka, 5).

destination(nara).
country(nara, japan).
region(nara, east_asia).
place_type(nara, historical).
budget(nara, medium).
weather(nara, cool).
trip_days(nara, 1, 2).
culture(nara, 5).
food(nara, 4).
nature(nara, 4).
nightlife(nara, 1).
shopping(nara, 2).
quiet(nara, 5).
adventure(nara, 1).
transport(nara, 5).

destination(sapporo).
country(sapporo, japan).
region(sapporo, east_asia).
place_type(sapporo, city).
budget(sapporo, high).
weather(sapporo, cold).
trip_days(sapporo, 3, 5).
culture(sapporo, 3).
food(sapporo, 5).
nature(sapporo, 4).
nightlife(sapporo, 3).
shopping(sapporo, 4).
quiet(sapporo, 2).
adventure(sapporo, 3).
transport(sapporo, 5).

destination(okinawa).
country(okinawa, japan).
region(okinawa, east_asia).
place_type(okinawa, beach).
budget(okinawa, medium).
weather(okinawa, warm).
trip_days(okinawa, 4, 7).
culture(okinawa, 4).
food(okinawa, 4).
nature(okinawa, 4).
nightlife(okinawa, 2).
shopping(okinawa, 2).
quiet(okinawa, 3).
adventure(okinawa, 3).
transport(okinawa, 3).

destination(hiroshima).
country(hiroshima, japan).
region(hiroshima, east_asia).
place_type(hiroshima, historical).
budget(hiroshima, medium).
weather(hiroshima, cool).
trip_days(hiroshima, 2, 3).
culture(hiroshima, 5).
food(hiroshima, 4).
nature(hiroshima, 3).
nightlife(hiroshima, 2).
shopping(hiroshima, 3).
quiet(hiroshima, 3).
adventure(hiroshima, 2).
transport(hiroshima, 5).

destination(kanazawa).
country(kanazawa, japan).
region(kanazawa, east_asia).
place_type(kanazawa, historical).
budget(kanazawa, medium).
weather(kanazawa, cool).
trip_days(kanazawa, 2, 4).
culture(kanazawa, 5).
food(kanazawa, 4).
nature(kanazawa, 3).
nightlife(kanazawa, 1).
shopping(kanazawa, 3).
quiet(kanazawa, 4).
adventure(kanazawa, 1).
transport(kanazawa, 4).

destination(seoul).
country(seoul, south_korea).
region(seoul, east_asia).
place_type(seoul, city).
budget(seoul, medium).
weather(seoul, cool).
trip_days(seoul, 4, 6).
culture(seoul, 4).
food(seoul, 5).
nature(seoul, 2).
nightlife(seoul, 5).
shopping(seoul, 5).
quiet(seoul, 1).
adventure(seoul, 2).
transport(seoul, 5).

destination(busan).
country(busan, south_korea).
region(busan, east_asia).
place_type(busan, city).
budget(busan, medium).
weather(busan, cool).
trip_days(busan, 3, 5).
culture(busan, 3).
food(busan, 5).
nature(busan, 3).
nightlife(busan, 4).
shopping(busan, 3).
quiet(busan, 2).
adventure(busan, 3).
transport(busan, 5).

destination(jeju).
country(jeju, south_korea).
region(jeju, east_asia).
place_type(jeju, romantic).
budget(jeju, medium).
weather(jeju, cool).
trip_days(jeju, 3, 5).
culture(jeju, 3).
food(jeju, 4).
nature(jeju, 5).
nightlife(jeju, 2).
shopping(jeju, 2).
quiet(jeju, 4).
adventure(jeju, 4).
transport(jeju, 3).

destination(gyeongju).
country(gyeongju, south_korea).
region(gyeongju, east_asia).
place_type(gyeongju, historical).
budget(gyeongju, medium).
weather(gyeongju, cool).
trip_days(gyeongju, 2, 3).
culture(gyeongju, 5).
food(gyeongju, 3).
nature(gyeongju, 3).
nightlife(gyeongju, 1).
shopping(gyeongju, 2).
quiet(gyeongju, 4).
adventure(gyeongju, 2).
transport(gyeongju, 3).

destination(jeonju).
country(jeonju, south_korea).
region(jeonju, east_asia).
place_type(jeonju, historical).
budget(jeonju, medium).
weather(jeonju, cool).
trip_days(jeonju, 1, 2).
culture(jeonju, 5).
food(jeonju, 5).
nature(jeonju, 2).
nightlife(jeonju, 2).
shopping(jeonju, 2).
quiet(jeonju, 3).
adventure(jeonju, 1).
transport(jeonju, 4).

destination(sokcho).
country(sokcho, south_korea).
region(sokcho, east_asia).
place_type(sokcho, mountain).
budget(sokcho, medium).
weather(sokcho, cool).
trip_days(sokcho, 2, 4).
culture(sokcho, 3).
food(sokcho, 4).
nature(sokcho, 5).
nightlife(sokcho, 1).
shopping(sokcho, 2).
quiet(sokcho, 4).
adventure(sokcho, 4).
transport(sokcho, 3).

destination(vientiane).
country(vientiane, laos).
region(vientiane, southeast_asia).
place_type(vientiane, city).
budget(vientiane, low).
weather(vientiane, hot).
trip_days(vientiane, 2, 4).
culture(vientiane, 4).
food(vientiane, 4).
nature(vientiane, 2).
nightlife(vientiane, 2).
shopping(vientiane, 3).
quiet(vientiane, 3).
adventure(vientiane, 2).
transport(vientiane, 3).

destination(luang_prabang).
country(luang_prabang, laos).
region(luang_prabang, southeast_asia).
place_type(luang_prabang, historical).
budget(luang_prabang, medium).
weather(luang_prabang, warm).
trip_days(luang_prabang, 3, 5).
culture(luang_prabang, 5).
food(luang_prabang, 4).
nature(luang_prabang, 4).
nightlife(luang_prabang, 2).
shopping(luang_prabang, 3).
quiet(luang_prabang, 5).
adventure(luang_prabang, 3).
transport(luang_prabang, 3).

destination(vang_vieng).
country(vang_vieng, laos).
region(vang_vieng, southeast_asia).
place_type(vang_vieng, adventure).
budget(vang_vieng, low).
weather(vang_vieng, warm).
trip_days(vang_vieng, 3, 5).
culture(vang_vieng, 3).
food(vang_vieng, 3).
nature(vang_vieng, 5).
nightlife(vang_vieng, 3).
shopping(vang_vieng, 2).
quiet(vang_vieng, 3).
adventure(vang_vieng, 5).
transport(vang_vieng, 2).

destination(kuang_si_falls).
country(kuang_si_falls, laos).
region(kuang_si_falls, southeast_asia).
place_type(kuang_si_falls, nature).
budget(kuang_si_falls, low).
weather(kuang_si_falls, warm).
trip_days(kuang_si_falls, 1, 2).
culture(kuang_si_falls, 2).
food(kuang_si_falls, 2).
nature(kuang_si_falls, 5).
nightlife(kuang_si_falls, 1).
shopping(kuang_si_falls, 1).
quiet(kuang_si_falls, 5).
adventure(kuang_si_falls, 4).
transport(kuang_si_falls, 2).

destination(nong_khiaw).
country(nong_khiaw, laos).
region(nong_khiaw, southeast_asia).
place_type(nong_khiaw, mountain).
budget(nong_khiaw, low).
weather(nong_khiaw, cool).
trip_days(nong_khiaw, 3, 5).
culture(nong_khiaw, 3).
food(nong_khiaw, 3).
nature(nong_khiaw, 5).
nightlife(nong_khiaw, 1).
shopping(nong_khiaw, 1).
quiet(nong_khiaw, 5).
adventure(nong_khiaw, 5).
transport(nong_khiaw, 2).

destination(dhaka).
country(dhaka, bangladesh).
region(dhaka, south_asia).
place_type(dhaka, city).
budget(dhaka, low).
weather(dhaka, hot).
trip_days(dhaka, 2, 4).
culture(dhaka, 4).
food(dhaka, 5).
nature(dhaka, 1).
nightlife(dhaka, 3).
shopping(dhaka, 4).
quiet(dhaka, 1).
adventure(dhaka, 2).
transport(dhaka, 4).

destination(bagerhat).
country(bagerhat, bangladesh).
region(bagerhat, south_asia).
place_type(bagerhat, historical).
budget(bagerhat, low).
weather(bagerhat, hot).
trip_days(bagerhat, 1, 3).
culture(bagerhat, 5).
food(bagerhat, 3).
nature(bagerhat, 3).
nightlife(bagerhat, 1).
shopping(bagerhat, 2).
quiet(bagerhat, 4).
adventure(bagerhat, 2).
transport(bagerhat, 2).

destination('cox''s_bazar').
country('cox''s_bazar', bangladesh).
region('cox''s_bazar', south_asia).
place_type('cox''s_bazar', beach).
budget('cox''s_bazar', low).
weather('cox''s_bazar', hot).
trip_days('cox''s_bazar', 3, 5).
culture('cox''s_bazar', 3).
food('cox''s_bazar', 4).
nature('cox''s_bazar', 5).
nightlife('cox''s_bazar', 3).
shopping('cox''s_bazar', 3).
quiet('cox''s_bazar', 3).
adventure('cox''s_bazar', 4).
transport('cox''s_bazar', 3).

destination(sundarbans).
country(sundarbans, bangladesh).
region(sundarbans, south_asia).
place_type(sundarbans, nature).
budget(sundarbans, medium).
weather(sundarbans, hot).
trip_days(sundarbans, 3, 5).
culture(sundarbans, 3).
food(sundarbans, 3).
nature(sundarbans, 5).
nightlife(sundarbans, 1).
shopping(sundarbans, 1).
quiet(sundarbans, 5).
adventure(sundarbans, 5).
transport(sundarbans, 2).

destination(bandarban).
country(bandarban, bangladesh).
region(bandarban, south_asia).
place_type(bandarban, adventure).
budget(bandarban, low).
weather(bandarban, warm).
trip_days(bandarban, 3, 5).
culture(bandarban, 4).
food(bandarban, 3).
nature(bandarban, 5).
nightlife(bandarban, 1).
shopping(bandarban, 2).
quiet(bandarban, 5).
adventure(bandarban, 5).
transport(bandarban, 2).

destination(thimphu).
country(thimphu, bhutan).
region(thimphu, south_asia).
place_type(thimphu, city).
budget(thimphu, high).
weather(thimphu, cool).
trip_days(thimphu, 2, 4).
culture(thimphu, 5).
food(thimphu, 3).
nature(thimphu, 4).
nightlife(thimphu, 1).
shopping(thimphu, 3).
quiet(thimphu, 4).
adventure(thimphu, 3).
transport(thimphu, 3).

destination(punakha).
country(punakha, bhutan).
region(punakha, south_asia).
place_type(punakha, historical).
budget(punakha, high).
weather(punakha, warm).
trip_days(punakha, 2, 4).
culture(punakha, 5).
food(punakha, 3).
nature(punakha, 5).
nightlife(punakha, 1).
shopping(punakha, 2).
quiet(punakha, 5).
adventure(punakha, 3).
transport(punakha, 3).

destination(phobjikha_valley).
country(phobjikha_valley, bhutan).
region(phobjikha_valley, south_asia).
place_type(phobjikha_valley, nature).
budget(phobjikha_valley, high).
weather(phobjikha_valley, cool).
trip_days(phobjikha_valley, 2, 4).
culture(phobjikha_valley, 4).
food(phobjikha_valley, 2).
nature(phobjikha_valley, 5).
nightlife(phobjikha_valley, 1).
shopping(phobjikha_valley, 1).
quiet(phobjikha_valley, 5).
adventure(phobjikha_valley, 4).
transport(phobjikha_valley, 2).

destination(paro_taktsang).
country(paro_taktsang, bhutan).
region(paro_taktsang, south_asia).
place_type(paro_taktsang, adventure).
budget(paro_taktsang, high).
weather(paro_taktsang, cool).
trip_days(paro_taktsang, 2, 3).
culture(paro_taktsang, 5).
food(paro_taktsang, 2).
nature(paro_taktsang, 5).
nightlife(paro_taktsang, 1).
shopping(paro_taktsang, 1).
quiet(paro_taktsang, 5).
adventure(paro_taktsang, 5).
transport(paro_taktsang, 2).

destination(bumthang).
country(bumthang, bhutan).
region(bumthang, south_asia).
place_type(bumthang, romantic).
budget(bumthang, high).
weather(bumthang, cool).
trip_days(bumthang, 3, 5).
culture(bumthang, 5).
food(bumthang, 3).
nature(bumthang, 5).
nightlife(bumthang, 1).
shopping(bumthang, 2).
quiet(bumthang, 5).
adventure(bumthang, 3).
transport(bumthang, 2).

destination(kathmandu).
country(kathmandu, nepal).
region(kathmandu, south_asia).
place_type(kathmandu, historical).
budget(kathmandu, low).
weather(kathmandu, cool).
trip_days(kathmandu, 3, 5).
culture(kathmandu, 5).
food(kathmandu, 4).
nature(kathmandu, 4).
nightlife(kathmandu, 3).
shopping(kathmandu, 4).
quiet(kathmandu, 3).
adventure(kathmandu, 4).
transport(kathmandu, 4).

destination(pokhara).
country(pokhara, nepal).
region(pokhara, south_asia).
place_type(pokhara, mountain).
budget(pokhara, low).
weather(pokhara, cool).
trip_days(pokhara, 4, 6).
culture(pokhara, 3).
food(pokhara, 4).
nature(pokhara, 5).
nightlife(pokhara, 3).
shopping(pokhara, 2).
quiet(pokhara, 5).
adventure(pokhara, 5).
transport(pokhara, 3).

destination(everest_region).
country(everest_region, nepal).
region(everest_region, south_asia).
place_type(everest_region, mountain).
budget(everest_region, high).
weather(everest_region, cold).
trip_days(everest_region, 8, 14).
culture(everest_region, 4).
food(everest_region, 3).
nature(everest_region, 5).
nightlife(everest_region, 1).
shopping(everest_region, 1).
quiet(everest_region, 5).
adventure(everest_region, 5).
transport(everest_region, 2).

destination(chitwan).
country(chitwan, nepal).
region(chitwan, south_asia).
place_type(chitwan, nature).
budget(chitwan, medium).
weather(chitwan, warm).
trip_days(chitwan, 2, 4).
culture(chitwan, 3).
food(chitwan, 4).
nature(chitwan, 5).
nightlife(chitwan, 2).
shopping(chitwan, 2).
quiet(chitwan, 5).
adventure(chitwan, 5).
transport(chitwan, 3).

destination(lumbini).
country(lumbini, nepal).
region(lumbini, south_asia).
place_type(lumbini, historical).
budget(lumbini, low).
weather(lumbini, warm).
trip_days(lumbini, 1, 3).
culture(lumbini, 5).
food(lumbini, 3).
nature(lumbini, 3).
nightlife(lumbini, 1).
shopping(lumbini, 1).
quiet(lumbini, 5).
adventure(lumbini, 2).
transport(lumbini, 3).

destination(colombo).
country(colombo, sri_lanka).
region(colombo, south_asia).
place_type(colombo, city).
budget(colombo, medium).
weather(colombo, hot).
trip_days(colombo, 2, 4).
culture(colombo, 4).
food(colombo, 5).
nature(colombo, 3).
nightlife(colombo, 4).
shopping(colombo, 5).
quiet(colombo, 2).
adventure(colombo, 3).
transport(colombo, 5).

destination(kandy).
country(kandy, sri_lanka).
region(kandy, south_asia).
place_type(kandy, historical).
budget(kandy, low).
weather(kandy, warm).
trip_days(kandy, 2, 4).
culture(kandy, 5).
food(kandy, 4).
nature(kandy, 4).
nightlife(kandy, 2).
shopping(kandy, 3).
quiet(kandy, 4).
adventure(kandy, 3).
transport(kandy, 4).

destination(ella).
country(ella, sri_lanka).
region(ella, south_asia).
place_type(ella, mountain).
budget(ella, low).
weather(ella, cool).
trip_days(ella, 3, 5).
culture(ella, 3).
food(ella, 4).
nature(ella, 5).
nightlife(ella, 2).
shopping(ella, 2).
quiet(ella, 5).
adventure(ella, 5).
transport(ella, 3).

destination(galle).
country(galle, sri_lanka).
region(galle, south_asia).
place_type(galle, historical).
budget(galle, medium).
weather(galle, hot).
trip_days(galle, 2, 4).
culture(galle, 5).
food(galle, 5).
nature(galle, 4).
nightlife(galle, 3).
shopping(galle, 4).
quiet(galle, 4).
adventure(galle, 3).
transport(galle, 4).

destination(mirissa).
country(mirissa, sri_lanka).
region(mirissa, south_asia).
place_type(mirissa, beach).
budget(mirissa, medium).
weather(mirissa, hot).
trip_days(mirissa, 3, 5).
culture(mirissa, 2).
food(mirissa, 4).
nature(mirissa, 5).
nightlife(mirissa, 3).
shopping(mirissa, 2).
quiet(mirissa, 4).
adventure(mirissa, 5).
transport(mirissa, 3).

destination(delhi).
country(delhi, india).
region(delhi, south_asia).
place_type(delhi, historical).
budget(delhi, low).
weather(delhi, hot).
trip_days(delhi, 3, 5).
culture(delhi, 5).
food(delhi, 5).
nature(delhi, 2).
nightlife(delhi, 4).
shopping(delhi, 5).
quiet(delhi, 2).
adventure(delhi, 3).
transport(delhi, 5).

destination(mumbai).
country(mumbai, india).
region(mumbai, south_asia).
place_type(mumbai, city).
budget(mumbai, medium).
weather(mumbai, hot).
trip_days(mumbai, 3, 5).
culture(mumbai, 4).
food(mumbai, 5).
nature(mumbai, 3).
nightlife(mumbai, 5).
shopping(mumbai, 5).
quiet(mumbai, 1).
adventure(mumbai, 3).
transport(mumbai, 5).

destination(jaipur).
country(jaipur, india).
region(jaipur, south_asia).
place_type(jaipur, historical).
budget(jaipur, low).
weather(jaipur, hot).
trip_days(jaipur, 2, 4).
culture(jaipur, 5).
food(jaipur, 5).
nature(jaipur, 3).
nightlife(jaipur, 2).
shopping(jaipur, 5).
quiet(jaipur, 3).
adventure(jaipur, 4).
transport(jaipur, 4).

destination(goa).
country(goa, india).
region(goa, south_asia).
place_type(goa, beach).
budget(goa, medium).
weather(goa, hot).
trip_days(goa, 4, 7).
culture(goa, 4).
food(goa, 5).
nature(goa, 5).
nightlife(goa, 5).
shopping(goa, 3).
quiet(goa, 3).
adventure(goa, 5).
transport(goa, 3).

destination(kerala).
country(kerala, india).
region(kerala, south_asia).
place_type(kerala, nature).
budget(kerala, medium).
weather(kerala, warm).
trip_days(kerala, 5, 8).
culture(kerala, 5).
food(kerala, 5).
nature(kerala, 5).
nightlife(kerala, 2).
shopping(kerala, 3).
quiet(kerala, 5).
adventure(kerala, 4).
transport(kerala, 3).

destination('malé').
country('malé', maldives).
region('malé', south_asia).
place_type('malé', city).
budget('malé', high).
weather('malé', hot).
trip_days('malé', 1, 2).
culture('malé', 3).
food('malé', 4).
nature('malé', 2).
nightlife('malé', 2).
shopping('malé', 3).
quiet('malé', 2).
adventure('malé', 1).
transport('malé', 3).

destination(maafushi).
country(maafushi, maldives).
region(maafushi, south_asia).
place_type(maafushi, beach).
budget(maafushi, medium).
weather(maafushi, hot).
trip_days(maafushi, 3, 5).
culture(maafushi, 2).
food(maafushi, 3).
nature(maafushi, 4).
nightlife(maafushi, 2).
shopping(maafushi, 2).
quiet(maafushi, 3).
adventure(maafushi, 4).
transport(maafushi, 2).

destination('north_malé_atoll').
country('north_malé_atoll', maldives).
region('north_malé_atoll', south_asia).
place_type('north_malé_atoll', romantic).
budget('north_malé_atoll', high).
weather('north_malé_atoll', hot).
trip_days('north_malé_atoll', 4, 7).
culture('north_malé_atoll', 2).
food('north_malé_atoll', 4).
nature('north_malé_atoll', 5).
nightlife('north_malé_atoll', 2).
shopping('north_malé_atoll', 2).
quiet('north_malé_atoll', 4).
adventure('north_malé_atoll', 3).
transport('north_malé_atoll', 2).

destination(ari_atoll).
country(ari_atoll, maldives).
region(ari_atoll, south_asia).
place_type(ari_atoll, adventure).
budget(ari_atoll, high).
weather(ari_atoll, hot).
trip_days(ari_atoll, 4, 7).
culture(ari_atoll, 2).
food(ari_atoll, 3).
nature(ari_atoll, 5).
nightlife(ari_atoll, 1).
shopping(ari_atoll, 1).
quiet(ari_atoll, 4).
adventure(ari_atoll, 5).
transport(ari_atoll, 1).

destination(addu_atoll).
country(addu_atoll, maldives).
region(addu_atoll, south_asia).
place_type(addu_atoll, beach).
budget(addu_atoll, high).
weather(addu_atoll, hot).
trip_days(addu_atoll, 4, 6).
culture(addu_atoll, 3).
food(addu_atoll, 3).
nature(addu_atoll, 5).
nightlife(addu_atoll, 1).
shopping(addu_atoll, 1).
quiet(addu_atoll, 4).
adventure(addu_atoll, 3).
transport(addu_atoll, 2).

destination(beijing).
country(beijing, china).
region(beijing, east_asia).
place_type(beijing, historical).
budget(beijing, medium).
weather(beijing, cool).
trip_days(beijing, 4, 6).
culture(beijing, 5).
food(beijing, 5).
nature(beijing, 3).
nightlife(beijing, 3).
shopping(beijing, 5).
quiet(beijing, 2).
adventure(beijing, 4).
transport(beijing, 5).

destination(shanghai).
country(shanghai, china).
region(shanghai, east_asia).
place_type(shanghai, city).
budget(shanghai, high).
weather(shanghai, warm).
trip_days(shanghai, 3, 5).
culture(shanghai, 4).
food(shanghai, 5).
nature(shanghai, 2).
nightlife(shanghai, 5).
shopping(shanghai, 5).
quiet(shanghai, 1).
adventure(shanghai, 3).
transport(shanghai, 5).

destination('xi''an').
country('xi''an', china).
region('xi''an', east_asia).
place_type('xi''an', historical).
budget('xi''an', low).
weather('xi''an', cool).
trip_days('xi''an', 3, 5).
culture('xi''an', 5).
food('xi''an', 5).
nature('xi''an', 3).
nightlife('xi''an', 3).
shopping('xi''an', 3).
quiet('xi''an', 3).
adventure('xi''an', 4).
transport('xi''an', 4).

destination(guilin).
country(guilin, china).
region(guilin, east_asia).
place_type(guilin, nature).
budget(guilin, medium).
weather(guilin, warm).
trip_days(guilin, 4, 6).
culture(guilin, 3).
food(guilin, 4).
nature(guilin, 5).
nightlife(guilin, 2).
shopping(guilin, 2).
quiet(guilin, 5).
adventure(guilin, 5).
transport(guilin, 3).

destination(chengdu).
country(chengdu, china).
region(chengdu, east_asia).
place_type(chengdu, city).
budget(chengdu, low).
weather(chengdu, cool).
trip_days(chengdu, 3, 5).
culture(chengdu, 4).
food(chengdu, 5).
nature(chengdu, 5).
nightlife(chengdu, 3).
shopping(chengdu, 3).
quiet(chengdu, 3).
adventure(chengdu, 4).
transport(chengdu, 4).

destination(ulaanbaatar).
country(ulaanbaatar, mongolia).
region(ulaanbaatar, east_asia).
place_type(ulaanbaatar, city).
budget(ulaanbaatar, medium).
weather(ulaanbaatar, cold).
trip_days(ulaanbaatar, 2, 4).
culture(ulaanbaatar, 4).
food(ulaanbaatar, 3).
nature(ulaanbaatar, 2).
nightlife(ulaanbaatar, 3).
shopping(ulaanbaatar, 3).
quiet(ulaanbaatar, 2).
adventure(ulaanbaatar, 2).
transport(ulaanbaatar, 4).

destination(karakorum).
country(karakorum, mongolia).
region(karakorum, east_asia).
place_type(karakorum, historical).
budget(karakorum, medium).
weather(karakorum, cool).
trip_days(karakorum, 2, 4).
culture(karakorum, 5).
food(karakorum, 2).
nature(karakorum, 4).
nightlife(karakorum, 1).
shopping(karakorum, 1).
quiet(karakorum, 5).
adventure(karakorum, 3).
transport(karakorum, 2).

destination(gobi_desert).
country(gobi_desert, mongolia).
region(gobi_desert, east_asia).
place_type(gobi_desert, adventure).
budget(gobi_desert, high).
weather(gobi_desert, cool).
trip_days(gobi_desert, 4, 7).
culture(gobi_desert, 3).
food(gobi_desert, 2).
nature(gobi_desert, 5).
nightlife(gobi_desert, 1).
shopping(gobi_desert, 1).
quiet(gobi_desert, 5).
adventure(gobi_desert, 5).
transport(gobi_desert, 1).

destination(lake_khuvsgul).
country(lake_khuvsgul, mongolia).
region(lake_khuvsgul, east_asia).
place_type(lake_khuvsgul, nature).
budget(lake_khuvsgul, medium).
weather(lake_khuvsgul, cold).
trip_days(lake_khuvsgul, 3, 5).
culture(lake_khuvsgul, 3).
food(lake_khuvsgul, 2).
nature(lake_khuvsgul, 5).
nightlife(lake_khuvsgul, 1).
shopping(lake_khuvsgul, 1).
quiet(lake_khuvsgul, 5).
adventure(lake_khuvsgul, 4).
transport(lake_khuvsgul, 2).

destination(altai_tavan_bogd).
country(altai_tavan_bogd, mongolia).
region(altai_tavan_bogd, east_asia).
place_type(altai_tavan_bogd, mountain).
budget(altai_tavan_bogd, high).
weather(altai_tavan_bogd, cold).
trip_days(altai_tavan_bogd, 4, 8).
culture(altai_tavan_bogd, 4).
food(altai_tavan_bogd, 2).
nature(altai_tavan_bogd, 5).
nightlife(altai_tavan_bogd, 1).
shopping(altai_tavan_bogd, 1).
quiet(altai_tavan_bogd, 5).
adventure(altai_tavan_bogd, 5).
transport(altai_tavan_bogd, 1).

destination(taipei).
country(taipei, taiwan).
region(taipei, east_asia).
place_type(taipei, city).
budget(taipei, medium).
weather(taipei, warm).
trip_days(taipei, 3, 5).
culture(taipei, 4).
food(taipei, 5).
nature(taipei, 3).
nightlife(taipei, 4).
shopping(taipei, 5).
quiet(taipei, 2).
adventure(taipei, 2).
transport(taipei, 5).

destination(taroko_gorge).
country(taroko_gorge, taiwan).
region(taroko_gorge, east_asia).
place_type(taroko_gorge, nature).
budget(taroko_gorge, medium).
weather(taroko_gorge, warm).
trip_days(taroko_gorge, 2, 3).
culture(taroko_gorge, 3).
food(taroko_gorge, 3).
nature(taroko_gorge, 5).
nightlife(taroko_gorge, 1).
shopping(taroko_gorge, 1).
quiet(taroko_gorge, 4).
adventure(taroko_gorge, 4).
transport(taroko_gorge, 3).

destination(tainan).
country(tainan, taiwan).
region(tainan, east_asia).
place_type(tainan, historical).
budget(tainan, medium).
weather(tainan, warm).
trip_days(tainan, 2, 4).
culture(tainan, 5).
food(tainan, 5).
nature(tainan, 2).
nightlife(tainan, 2).
shopping(tainan, 3).
quiet(tainan, 3).
adventure(tainan, 1).
transport(tainan, 4).

destination(kenting).
country(kenting, taiwan).
region(kenting, east_asia).
place_type(kenting, beach).
budget(kenting, medium).
weather(kenting, hot).
trip_days(kenting, 3, 5).
culture(kenting, 2).
food(kenting, 3).
nature(kenting, 4).
nightlife(kenting, 3).
shopping(kenting, 2).
quiet(kenting, 3).
adventure(kenting, 3).
transport(kenting, 3).

destination(sun_moon_lake).
country(sun_moon_lake, taiwan).
region(sun_moon_lake, east_asia).
place_type(sun_moon_lake, romantic).
budget(sun_moon_lake, medium).
weather(sun_moon_lake, warm).
trip_days(sun_moon_lake, 2, 3).
culture(sun_moon_lake, 3).
food(sun_moon_lake, 3).
nature(sun_moon_lake, 5).
nightlife(sun_moon_lake, 1).
shopping(sun_moon_lake, 2).
quiet(sun_moon_lake, 4).
adventure(sun_moon_lake, 2).
transport(sun_moon_lake, 3).

destination(bandar_seri_begawan).
country(bandar_seri_begawan, brunei).
region(bandar_seri_begawan, southeast_asia).
place_type(bandar_seri_begawan, city).
budget(bandar_seri_begawan, medium).
weather(bandar_seri_begawan, hot).
trip_days(bandar_seri_begawan, 2, 3).
culture(bandar_seri_begawan, 4).
food(bandar_seri_begawan, 4).
nature(bandar_seri_begawan, 2).
nightlife(bandar_seri_begawan, 2).
shopping(bandar_seri_begawan, 3).
quiet(bandar_seri_begawan, 4).
adventure(bandar_seri_begawan, 1).
transport(bandar_seri_begawan, 4).

destination(kampong_ayer).
country(kampong_ayer, brunei).
region(kampong_ayer, southeast_asia).
place_type(kampong_ayer, historical).
budget(kampong_ayer, medium).
weather(kampong_ayer, hot).
trip_days(kampong_ayer, 2, 3).
culture(kampong_ayer, 4).
food(kampong_ayer, 4).
nature(kampong_ayer, 2).
nightlife(kampong_ayer, 1).
shopping(kampong_ayer, 2).
quiet(kampong_ayer, 3).
adventure(kampong_ayer, 1).
transport(kampong_ayer, 3).

destination(ulu_temburong_national_park).
country(ulu_temburong_national_park, brunei).
region(ulu_temburong_national_park, southeast_asia).
place_type(ulu_temburong_national_park, nature).
budget(ulu_temburong_national_park, medium).
weather(ulu_temburong_national_park, hot).
trip_days(ulu_temburong_national_park, 3, 5).
culture(ulu_temburong_national_park, 2).
food(ulu_temburong_national_park, 2).
nature(ulu_temburong_national_park, 5).
nightlife(ulu_temburong_national_park, 1).
shopping(ulu_temburong_national_park, 1).
quiet(ulu_temburong_national_park, 5).
adventure(ulu_temburong_national_park, 4).
transport(ulu_temburong_national_park, 2).

destination(muara_beach).
country(muara_beach, brunei).
region(muara_beach, southeast_asia).
place_type(muara_beach, beach).
budget(muara_beach, medium).
weather(muara_beach, hot).
trip_days(muara_beach, 2, 4).
culture(muara_beach, 1).
food(muara_beach, 3).
nature(muara_beach, 4).
nightlife(muara_beach, 2).
shopping(muara_beach, 1).
quiet(muara_beach, 4).
adventure(muara_beach, 2).
transport(muara_beach, 2).

destination(jerudong).
country(jerudong, brunei).
region(jerudong, southeast_asia).
place_type(jerudong, city).
budget(jerudong, medium).
weather(jerudong, hot).
trip_days(jerudong, 1, 3).
culture(jerudong, 2).
food(jerudong, 3).
nature(jerudong, 3).
nightlife(jerudong, 2).
shopping(jerudong, 3).
quiet(jerudong, 3).
adventure(jerudong, 2).
transport(jerudong, 3).

destination(dili).
country(dili, timor_leste).
region(dili, southeast_asia).
place_type(dili, city).
budget(dili, medium).
weather(dili, hot).
trip_days(dili, 2, 4).
culture(dili, 4).
food(dili, 4).
nature(dili, 2).
nightlife(dili, 3).
shopping(dili, 3).
quiet(dili, 3).
adventure(dili, 2).
transport(dili, 3).

destination(atauro_island).
country(atauro_island, timor_leste).
region(atauro_island, southeast_asia).
place_type(atauro_island, beach).
budget(atauro_island, medium).
weather(atauro_island, hot).
trip_days(atauro_island, 3, 5).
culture(atauro_island, 3).
food(atauro_island, 3).
nature(atauro_island, 5).
nightlife(atauro_island, 2).
shopping(atauro_island, 1).
quiet(atauro_island, 4).
adventure(atauro_island, 5).
transport(atauro_island, 2).

destination(baucau).
country(baucau, timor_leste).
region(baucau, southeast_asia).
place_type(baucau, historical).
budget(baucau, medium).
weather(baucau, hot).
trip_days(baucau, 2, 3).
culture(baucau, 4).
food(baucau, 3).
nature(baucau, 3).
nightlife(baucau, 1).
shopping(baucau, 2).
quiet(baucau, 4).
adventure(baucau, 2).
transport(baucau, 2).

destination(mount_ramelau).
country(mount_ramelau, timor_leste).
region(mount_ramelau, southeast_asia).
place_type(mount_ramelau, mountain).
budget(mount_ramelau, medium).
weather(mount_ramelau, cool).
trip_days(mount_ramelau, 2, 4).
culture(mount_ramelau, 2).
food(mount_ramelau, 3).
nature(mount_ramelau, 5).
nightlife(mount_ramelau, 1).
shopping(mount_ramelau, 1).
quiet(mount_ramelau, 5).
adventure(mount_ramelau, 5).
transport(mount_ramelau, 2).

destination(jaco_island).
country(jaco_island, timor_leste).
region(jaco_island, southeast_asia).
place_type(jaco_island, beach).
budget(jaco_island, medium).
weather(jaco_island, hot).
trip_days(jaco_island, 2, 4).
culture(jaco_island, 2).
food(jaco_island, 3).
nature(jaco_island, 5).
nightlife(jaco_island, 1).
shopping(jaco_island, 1).
quiet(jaco_island, 5).
adventure(jaco_island, 4).
transport(jaco_island, 2).

destination(hong_kong___central).
country(hong_kong___central, hong_kong).
region(hong_kong___central, east_asia).
place_type(hong_kong___central, city).
budget(hong_kong___central, high).
weather(hong_kong___central, hot).
trip_days(hong_kong___central, 3, 5).
culture(hong_kong___central, 4).
food(hong_kong___central, 5).
nature(hong_kong___central, 3).
nightlife(hong_kong___central, 5).
shopping(hong_kong___central, 5).
quiet(hong_kong___central, 2).
adventure(hong_kong___central, 2).
transport(hong_kong___central, 5).

destination('kowloon_/_tsim_sha_tsui').
country('kowloon_/_tsim_sha_tsui', hong_kong).
region('kowloon_/_tsim_sha_tsui', east_asia).
place_type('kowloon_/_tsim_sha_tsui', city).
budget('kowloon_/_tsim_sha_tsui', high).
weather('kowloon_/_tsim_sha_tsui', hot).
trip_days('kowloon_/_tsim_sha_tsui', 3, 5).
culture('kowloon_/_tsim_sha_tsui', 4).
food('kowloon_/_tsim_sha_tsui', 5).
nature('kowloon_/_tsim_sha_tsui', 3).
nightlife('kowloon_/_tsim_sha_tsui', 5).
shopping('kowloon_/_tsim_sha_tsui', 5).
quiet('kowloon_/_tsim_sha_tsui', 2).
adventure('kowloon_/_tsim_sha_tsui', 2).
transport('kowloon_/_tsim_sha_tsui', 5).

destination('lantau_/_big_buddha').
country('lantau_/_big_buddha', hong_kong).
region('lantau_/_big_buddha', east_asia).
place_type('lantau_/_big_buddha', historical).
budget('lantau_/_big_buddha', high).
weather('lantau_/_big_buddha', hot).
trip_days('lantau_/_big_buddha', 3, 5).
culture('lantau_/_big_buddha', 4).
food('lantau_/_big_buddha', 3).
nature('lantau_/_big_buddha', 4).
nightlife('lantau_/_big_buddha', 2).
shopping('lantau_/_big_buddha', 2).
quiet('lantau_/_big_buddha', 4).
adventure('lantau_/_big_buddha', 3).
transport('lantau_/_big_buddha', 3).

destination('sai_kung_/_geopark').
country('sai_kung_/_geopark', hong_kong).
region('sai_kung_/_geopark', east_asia).
place_type('sai_kung_/_geopark', nature).
budget('sai_kung_/_geopark', medium).
weather('sai_kung_/_geopark', hot).
trip_days('sai_kung_/_geopark', 2, 4).
culture('sai_kung_/_geopark', 2).
food('sai_kung_/_geopark', 3).
nature('sai_kung_/_geopark', 5).
nightlife('sai_kung_/_geopark', 1).
shopping('sai_kung_/_geopark', 2).
quiet('sai_kung_/_geopark', 5).
adventure('sai_kung_/_geopark', 3).
transport('sai_kung_/_geopark', 2).

destination('stanley_/_cheung_chau').
country('stanley_/_cheung_chau', hong_kong).
region('stanley_/_cheung_chau', east_asia).
place_type('stanley_/_cheung_chau', beach).
budget('stanley_/_cheung_chau', medium).
weather('stanley_/_cheung_chau', hot).
trip_days('stanley_/_cheung_chau', 3, 5).
culture('stanley_/_cheung_chau', 2).
food('stanley_/_cheung_chau', 3).
nature('stanley_/_cheung_chau', 4).
nightlife('stanley_/_cheung_chau', 2).
shopping('stanley_/_cheung_chau', 2).
quiet('stanley_/_cheung_chau', 4).
adventure('stanley_/_cheung_chau', 3).
transport('stanley_/_cheung_chau', 3).

destination(macau_historic_centre).
country(macau_historic_centre, macau).
region(macau_historic_centre, east_asia).
place_type(macau_historic_centre, historical).
budget(macau_historic_centre, medium).
weather(macau_historic_centre, hot).
trip_days(macau_historic_centre, 2, 3).
culture(macau_historic_centre, 5).
food(macau_historic_centre, 4).
nature(macau_historic_centre, 2).
nightlife(macau_historic_centre, 2).
shopping(macau_historic_centre, 4).
quiet(macau_historic_centre, 3).
adventure(macau_historic_centre, 2).
transport(macau_historic_centre, 4).

destination(coloane).
country(coloane, macau).
region(coloane, east_asia).
place_type(coloane, beach).
budget(coloane, medium).
weather(coloane, hot).
trip_days(coloane, 2, 3).
culture(coloane, 4).
food(coloane, 3).
nature(coloane, 3).
nightlife(coloane, 1).
shopping(coloane, 1).
quiet(coloane, 4).
adventure(coloane, 2).
transport(coloane, 3).

destination(taipa_village).
country(taipa_village, macau).
region(taipa_village, east_asia).
place_type(taipa_village, historical).
budget(taipa_village, medium).
weather(taipa_village, hot).
trip_days(taipa_village, 1, 2).
culture(taipa_village, 4).
food(taipa_village, 4).
nature(taipa_village, 2).
nightlife(taipa_village, 1).
shopping(taipa_village, 3).
quiet(taipa_village, 3).
adventure(taipa_village, 1).
transport(taipa_village, 3).

destination(cotai_strip).
country(cotai_strip, macau).
region(cotai_strip, east_asia).
place_type(cotai_strip, city).
budget(cotai_strip, medium).
weather(cotai_strip, hot).
trip_days(cotai_strip, 1, 3).
culture(cotai_strip, 2).
food(cotai_strip, 3).
nature(cotai_strip, 1).
nightlife(cotai_strip, 5).
shopping(cotai_strip, 5).
quiet(cotai_strip, 1).
adventure(cotai_strip, 2).
transport(cotai_strip, 4).

destination('almaty_(kazakhstan)').
country('almaty_(kazakhstan)', kazakhstan).
region('almaty_(kazakhstan)', central_asia).
place_type('almaty_(kazakhstan)', city).
budget('almaty_(kazakhstan)', medium).
weather('almaty_(kazakhstan)', cold).
trip_days('almaty_(kazakhstan)', 3, 5).
culture('almaty_(kazakhstan)', 4).
food('almaty_(kazakhstan)', 3).
nature('almaty_(kazakhstan)', 4).
nightlife('almaty_(kazakhstan)', 2).
shopping('almaty_(kazakhstan)', 4).
quiet('almaty_(kazakhstan)', 3).
adventure('almaty_(kazakhstan)', 2).
transport('almaty_(kazakhstan)', 4).

destination('astana_(kazakhstan)').
country('astana_(kazakhstan)', kazakhstan).
region('astana_(kazakhstan)', central_asia).
place_type('astana_(kazakhstan)', city).
budget('astana_(kazakhstan)', medium).
weather('astana_(kazakhstan)', cold).
trip_days('astana_(kazakhstan)', 2, 4).
culture('astana_(kazakhstan)', 3).
food('astana_(kazakhstan)', 3).
nature('astana_(kazakhstan)', 2).
nightlife('astana_(kazakhstan)', 3).
shopping('astana_(kazakhstan)', 4).
quiet('astana_(kazakhstan)', 2).
adventure('astana_(kazakhstan)', 2).
transport('astana_(kazakhstan)', 4).

destination(charyn_canyon).
country(charyn_canyon, kazakhstan).
region(charyn_canyon, central_asia).
place_type(charyn_canyon, adventure).
budget(charyn_canyon, medium).
weather(charyn_canyon, warm).
trip_days(charyn_canyon, 1, 3).
culture(charyn_canyon, 2).
food(charyn_canyon, 2).
nature(charyn_canyon, 5).
nightlife(charyn_canyon, 1).
shopping(charyn_canyon, 1).
quiet(charyn_canyon, 5).
adventure(charyn_canyon, 5).
transport(charyn_canyon, 2).

destination(bishkek).
country(bishkek, kyrgyzstan).
region(bishkek, central_asia).
place_type(bishkek, city).
budget(bishkek, low).
weather(bishkek, cool).
trip_days(bishkek, 2, 3).
culture(bishkek, 3).
food(bishkek, 3).
nature(bishkek, 2).
nightlife(bishkek, 2).
shopping(bishkek, 3).
quiet(bishkek, 3).
adventure(bishkek, 2).
transport(bishkek, 4).

destination(issyk_kul).
country(issyk_kul, kyrgyzstan).
region(issyk_kul, central_asia).
place_type(issyk_kul, nature).
budget(issyk_kul, low).
weather(issyk_kul, warm).
trip_days(issyk_kul, 3, 5).
culture(issyk_kul, 3).
food(issyk_kul, 3).
nature(issyk_kul, 5).
nightlife(issyk_kul, 2).
shopping(issyk_kul, 1).
quiet(issyk_kul, 4).
adventure(issyk_kul, 3).
transport(issyk_kul, 2).

destination(karakol).
country(karakol, kyrgyzstan).
region(karakol, central_asia).
place_type(karakol, mountain).
budget(karakol, low).
weather(karakol, cool).
trip_days(karakol, 3, 5).
culture(karakol, 3).
food(karakol, 3).
nature(karakol, 5).
nightlife(karakol, 1).
shopping(karakol, 1).
quiet(karakol, 5).
adventure(karakol, 5).
transport(karakol, 2).

destination(osh).
country(osh, kyrgyzstan).
region(osh, central_asia).
place_type(osh, historical).
budget(osh, low).
weather(osh, warm).
trip_days(osh, 1, 3).
culture(osh, 5).
food(osh, 3).
nature(osh, 2).
nightlife(osh, 1).
shopping(osh, 2).
quiet(osh, 4).
adventure(osh, 2).
transport(osh, 3).

destination(song_kul).
country(song_kul, kyrgyzstan).
region(song_kul, central_asia).
place_type(song_kul, mountain).
budget(song_kul, medium).
weather(song_kul, cool).
trip_days(song_kul, 3, 5).
culture(song_kul, 2).
food(song_kul, 2).
nature(song_kul, 5).
nightlife(song_kul, 1).
shopping(song_kul, 1).
quiet(song_kul, 5).
adventure(song_kul, 5).
transport(song_kul, 1).

destination(samarkand).
country(samarkand, uzbekistan).
region(samarkand, central_asia).
place_type(samarkand, historical).
budget(samarkand, medium).
weather(samarkand, warm).
trip_days(samarkand, 2, 4).
culture(samarkand, 5).
food(samarkand, 4).
nature(samarkand, 2).
nightlife(samarkand, 1).
shopping(samarkand, 2).
quiet(samarkand, 4).
adventure(samarkand, 3).
transport(samarkand, 3).

destination(bukhara).
country(bukhara, uzbekistan).
region(bukhara, central_asia).
place_type(bukhara, historical).
budget(bukhara, medium).
weather(bukhara, warm).
trip_days(bukhara, 2, 4).
culture(bukhara, 5).
food(bukhara, 4).
nature(bukhara, 2).
nightlife(bukhara, 1).
shopping(bukhara, 2).
quiet(bukhara, 5).
adventure(bukhara, 2).
transport(bukhara, 3).

destination(khiva).
country(khiva, uzbekistan).
region(khiva, central_asia).
place_type(khiva, historical).
budget(khiva, medium).
weather(khiva, warm).
trip_days(khiva, 2, 3).
culture(khiva, 5).
food(khiva, 3).
nature(khiva, 2).
nightlife(khiva, 1).
shopping(khiva, 2).
quiet(khiva, 5).
adventure(khiva, 2).
transport(khiva, 2).

destination(tashkent).
country(tashkent, uzbekistan).
region(tashkent, central_asia).
place_type(tashkent, city).
budget(tashkent, medium).
weather(tashkent, warm).
trip_days(tashkent, 2, 3).
culture(tashkent, 4).
food(tashkent, 4).
nature(tashkent, 2).
nightlife(tashkent, 3).
shopping(tashkent, 4).
quiet(tashkent, 2).
adventure(tashkent, 2).
transport(tashkent, 4).

destination(dushanbe).
country(dushanbe, tajikistan).
region(dushanbe, central_asia).
place_type(dushanbe, city).
budget(dushanbe, low).
weather(dushanbe, cool).
trip_days(dushanbe, 1, 3).
culture(dushanbe, 3).
food(dushanbe, 3).
nature(dushanbe, 3).
nightlife(dushanbe, 1).
shopping(dushanbe, 2).
quiet(dushanbe, 3).
adventure(dushanbe, 2).
transport(dushanbe, 3).

destination(pamir_highway).
country(pamir_highway, tajikistan).
region(pamir_highway, central_asia).
place_type(pamir_highway, adventure).
budget(pamir_highway, medium).
weather(pamir_highway, cool).
trip_days(pamir_highway, 5, 9).
culture(pamir_highway, 2).
food(pamir_highway, 2).
nature(pamir_highway, 5).
nightlife(pamir_highway, 1).
shopping(pamir_highway, 1).
quiet(pamir_highway, 5).
adventure(pamir_highway, 5).
transport(pamir_highway, 2).

destination(iskanderkul_lake).
country(iskanderkul_lake, tajikistan).
region(iskanderkul_lake, central_asia).
place_type(iskanderkul_lake, nature).
budget(iskanderkul_lake, medium).
weather(iskanderkul_lake, cool).
trip_days(iskanderkul_lake, 1, 3).
culture(iskanderkul_lake, 2).
food(iskanderkul_lake, 2).
nature(iskanderkul_lake, 5).
nightlife(iskanderkul_lake, 1).
shopping(iskanderkul_lake, 1).
quiet(iskanderkul_lake, 5).
adventure(iskanderkul_lake, 4).
transport(iskanderkul_lake, 1).

destination(ashgabat).
country(ashgabat, turkmenistan).
region(ashgabat, central_asia).
place_type(ashgabat, city).
budget(ashgabat, high).
weather(ashgabat, hot).
trip_days(ashgabat, 1, 3).
culture(ashgabat, 4).
food(ashgabat, 2).
nature(ashgabat, 2).
nightlife(ashgabat, 1).
shopping(ashgabat, 4).
quiet(ashgabat, 3).
adventure(ashgabat, 1).
transport(ashgabat, 4).

destination(darvaza_gas_crater).
country(darvaza_gas_crater, turkmenistan).
region(darvaza_gas_crater, central_asia).
place_type(darvaza_gas_crater, adventure).
budget(darvaza_gas_crater, high).
weather(darvaza_gas_crater, hot).
trip_days(darvaza_gas_crater, 1, 2).
culture(darvaza_gas_crater, 1).
food(darvaza_gas_crater, 2).
nature(darvaza_gas_crater, 4).
nightlife(darvaza_gas_crater, 1).
shopping(darvaza_gas_crater, 1).
quiet(darvaza_gas_crater, 5).
adventure(darvaza_gas_crater, 5).
transport(darvaza_gas_crater, 1).

destination(merv).
country(merv, turkmenistan).
region(merv, central_asia).
place_type(merv, historical).
budget(merv, medium).
weather(merv, hot).
trip_days(merv, 1, 2).
culture(merv, 5).
food(merv, 2).
nature(merv, 3).
nightlife(merv, 1).
shopping(merv, 1).
quiet(merv, 4).
adventure(merv, 3).
transport(merv, 2).

destination(yangykala_canyon).
country(yangykala_canyon, turkmenistan).
region(yangykala_canyon, central_asia).
place_type(yangykala_canyon, adventure).
budget(yangykala_canyon, medium).
weather(yangykala_canyon, warm).
trip_days(yangykala_canyon, 2, 4).
culture(yangykala_canyon, 1).
food(yangykala_canyon, 2).
nature(yangykala_canyon, 5).
nightlife(yangykala_canyon, 1).
shopping(yangykala_canyon, 1).
quiet(yangykala_canyon, 5).
adventure(yangykala_canyon, 5).
transport(yangykala_canyon, 1).

destination(tbilisi).
country(tbilisi, georgia).
region(tbilisi, central_asia).
place_type(tbilisi, city).
budget(tbilisi, medium).
weather(tbilisi, cool).
trip_days(tbilisi, 3, 5).
culture(tbilisi, 5).
food(tbilisi, 5).
nature(tbilisi, 3).
nightlife(tbilisi, 4).
shopping(tbilisi, 4).
quiet(tbilisi, 3).
adventure(tbilisi, 2).
transport(tbilisi, 4).

destination(kazbegi).
country(kazbegi, georgia).
region(kazbegi, central_asia).
place_type(kazbegi, mountain).
budget(kazbegi, medium).
weather(kazbegi, cool).
trip_days(kazbegi, 2, 4).
culture(kazbegi, 3).
food(kazbegi, 3).
nature(kazbegi, 5).
nightlife(kazbegi, 1).
shopping(kazbegi, 1).
quiet(kazbegi, 5).
adventure(kazbegi, 4).
transport(kazbegi, 2).

destination(svaneti).
country(svaneti, georgia).
region(svaneti, central_asia).
place_type(svaneti, mountain).
budget(svaneti, medium).
weather(svaneti, cool).
trip_days(svaneti, 3, 6).
culture(svaneti, 4).
food(svaneti, 3).
nature(svaneti, 5).
nightlife(svaneti, 1).
shopping(svaneti, 1).
quiet(svaneti, 5).
adventure(svaneti, 5).
transport(svaneti, 2).

destination(batumi).
country(batumi, georgia).
region(batumi, central_asia).
place_type(batumi, beach).
budget(batumi, medium).
weather(batumi, warm).
trip_days(batumi, 2, 4).
culture(batumi, 3).
food(batumi, 4).
nature(batumi, 3).
nightlife(batumi, 4).
shopping(batumi, 3).
quiet(batumi, 2).
adventure(batumi, 3).
transport(batumi, 4).

% Basic classification rules
historical_destination(X) :-
    place_type(X, historical).

southeast_asia_destination(X) :-
    region(X, southeast_asia).

east_asia_destination(X) :-
    region(X, east_asia).

south_asia_destination(X) :-
    region(X, south_asia).

central_asia_destination(X) :-
    region(X, central_asia).

low_budget_destination(X) :-
    budget(X, low).

cool_east_asia(X) :-
    region(X, east_asia),
    weather(X, cool).

% Multi-criteria and high-rating inference rules
historical_southeast_asia(X) :-
    region(X, southeast_asia),
    place_type(X, historical).

quiet_historical(X) :-
    place_type(X, historical),
    quiet(X, Q),
    Q >= 4.

nature_escape(X) :-
    nature(X, N),
    N >= 4,
    quiet(X, Q),
    Q >= 3.

foodie_paradise(X) :-
    food(X, F),
    F >= 4.

nightlife_hub(X) :-
    nightlife(X, NL),
    NL >= 4.

adventure_seeker(X) :-
    adventure(X, A),
    A >= 4.

cultural_explorer(X) :-
    culture(X, C),
    C >= 4.

budget_foodie_southeast_asia(X) :-
    region(X, southeast_asia),
    budget(X, low),
    food(X, F),
    F >= 4.

short_trip_destination(X) :-
    trip_days(X, _, Max),
    Max =< 3.

budget_short_trip(X) :-
    budget(X, low),
    trip_days(X, _, Max),
    Max =< 3.

easy_transit_city(X) :-
    place_type(X, city),
    transport(X, T),
    T >= 3.

% Flexible query predicate
recommend_trip(X, Region, Budget, MinNature, MinCulture) :-
    region(X, Region),
    budget(X, Budget),
    nature(X, N),
    N >= MinNature,
    culture(X, C),
    C >= MinCulture.

