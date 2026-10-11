import csv, urllib.parse, sys
OUT = sys.argv[1]
APP = {"P": ("Platts 1884", "platts_query.py"), "H": ("Dasa Hindi sabdasagara", "dasa-hindi_query.py"),
       "J": ("J. Dasa Bangala bhashara abhidhana", "dasa_query.py"), "T": ("Turner CDIAL", "soas_query.py")}
def url(s, q, mode):
    hws = "" if mode == "ft" else "&searchhws=yes"
    return f"https://dsal.uchicago.edu/cgi-bin/app/{APP[s][1]}?qs={urllib.parse.quote(q)}&matchtype={'default' if mode=='ft' else mode}{hws}"
NQ = ("T", None, None, "not queried", "—", "No Indo-Aryan etymon is proposed by the language dictionary, so no Turner head-word was looked up (deviation from v1.1 §6′, logged)", "—", "—")
# item: (id, lang, lemma, sense, label, pathway, mia, strength, conf, flags, notes, [checks])
# check: (src, query, mode, found, entry_ref, evidence paraphrase, route_asserted, loan_mark)
I = [
("1a61764406-1","hi","भेदना","to invade, penetrate","UNK","","","none","low","","Found only in the Hindi sabdasagara, which asserts no route under v1.1",[
 ("P","भेदना","ft","no","—","No headword for the verb; only the noun bhed (marked S) and derivatives","—",""),
 ("H","भेदना","exact","yes","p. 3694","Gives Sanskrit bhedana as source","not stated (lookup-only source)",""),
 ("T","bhednā","ft","no","—","No head-word bhēdana and no occurrence of the Hindi verb in a full-text search","—","form not listed")]),
("1e4399cb53-1","hi","रामराज्य","the rule of Rama; a righteous society","UNK","","","none","low","","Found only in the Hindi sabdasagara",[
 ("P","रामराज्य","ft","no","—","No result","—",""),
 ("H","रामराज्य","exact","yes","p. 4166","Marked as Sanskrit, no further etymology","not stated (lookup-only source)",""),
 ("T","rāmarājya","default","no","—","No head-word","—","form not listed")]),
("434bcca23a-1","hi","सैर","excursion, stroll","EXT","","","explicit","high","","HOMOGRAPH. Platts says Arabic, the Hindi sabdasagara says Persian; both external",[
 ("P","sair","exact","yes","p. 711, headword sair","Marked A (Arabic), verbal noun of an Arabic root","external (Arabic)",""),
 ("H","सैर","exact","yes","p. 5287, सैर 1","Marked as Persian","not stated (lookup-only source)",""), NQ]),
("434bcca23a-2","hi","सैर","relating to a plough","UNK","","","none","low","","HOMOGRAPH. Found only in the Hindi sabdasagara",[
 ("P","सैर","ft","no","—","No entry for this sense","—",""),
 ("H","सैर","exact","yes","p. 5287, सैर 2","Marked as Sanskrit","not stated (lookup-only source)",""),
 ("T","saira","default","yes","entry 13602a saira-","Lists West Pahari and Kumaoni forms; compares H. sīr; no Hindi form of this shape","not stated for Hindi","form not listed")]),
("507c3f7c13-1","hi","पुरा","formerly; till now","UNK","","","none","low","","HOMOGRAPH. Found only in the Hindi sabdasagara",[
 ("P","purā","exact","no","—","Only the 'village' homograph is a headword","—",""),
 ("H","पुरा","exact","yes","p. 3052, पुरा 1","Marked as Sanskrit (indeclinable)","not stated (lookup-only source)",""),
 ("T","purā","default","yes","entry 8281 purás (with purā́)","Lists Pali and other forms; no Hindi form","not stated for Hindi","form not listed")]),
("507c3f7c13-2","hi","पुरा","large village, town; ward","INH","REG-U","","structural","medium","","HOMOGRAPH. Rests on the Turner listing; Platts gives only a Sanskrit equivalent",[
 ("P","purā","exact","yes","p. 234, headword purā","Marked H with a Sanskrit formation in brackets; no Prakrit form","not stated",""),
 ("T","purā","default","yes","entry 8278 púra","Lists H. purā 'large village, town, ward' among the forms","inherited","none")]),
("632b7cea10-1","hi","दरस","sight, glance","UNK","","","none","low","","Sources give only the Sanskrit equivalent",[
 ("P","दरस","ft","yes","p. 512, headword dars / daras","Marked H; cross-referred to darś (marked S); no bracketed source","not stated",""),
 ("H","दरस","exact","yes","p. 2220","Gives Sanskrit darśa as source","not stated (lookup-only source)",""),
 ("T","darśa","default","yes","entry 6207 darśá","Lists Prakrit and Sindhi forms; no Hindi form","not stated for Hindi","form not listed")]),
("6d142d4fd8-1","hi","मसलना","to squish, crush","INH","REG-U","","structural","medium","","Rests on the Turner listing",[
 ("P","मसलना","ft","yes","p. 1035, headword masalnā","Marked H; derived from a Sanskrit root with a Hindi causative augment; no Prakrit form","not stated",""),
 ("H","मसलना","exact","yes","p. 3827","Refers to Hindi malnā","not stated (lookup-only source)",""),
 ("T","maṣati","exact","yes","entry 9919 maṣati","Lists H. masalnā 'to rub to pieces' among the -ll- extensions","inherited","none")]),
("821dd712f9-1","hi","पेंसिल","pencil","EXT","","","explicit","high","","",[
 ("P","pensil","ft","yes","p. 302, headword pensil / painsil","Marked H; stated to be a corruption from the English","external (English)",""),
 ("H","पेंसिल","exact","yes","p. 3092","Marked as English; cross-reference to another spelling","not stated (lookup-only source)",""), NQ]),
("86de5e37dd-1","hi","बाँचना","to read, decipher","INH","REG-A","Pk. vacca(i) (per Platts)","structural","medium","","HOMOGRAPH in the sources (a second verb 'to escape, remain'). Rests on Platts; Turner does not list this verb under vācayati",[
 ("P","बांचना","ft","yes","p. 126, first headword bāṅćnā","Marked H; a Prakrit verb form is cited, from a Sanskrit base","inherited",""),
 ("H","बाँचना","exact","yes","p. 3432, बाँचना 1","Gives Sanskrit vācana as source","not stated (lookup-only source)",""),
 ("T","vācayati","default","yes","entry 11471 vācayati","Lists Pali, Prakrit and Assamese forms; no Hindi form. A full-text search for the Hindi verb finds only the homograph under váñcati","not stated for Hindi","form not listed")]),
("89d35eb38d-1","hi","हान","alt form of हानि (loss)","INH","REG-U","","structural","low","","Rests on the Turner listing, which also lists the Sanskrit-identical H. hāni without a loan mark",[
 ("P","हान","ft","yes","p. 1217, headword hāni / hān","Marked H with the Sanskrit equivalent in brackets; no Prakrit form","not stated",""),
 ("H","हान","exact","yes","p. 5494, हान 1","Gives a Sanskrit source and refers to hāni","not stated (lookup-only source)",""),
 ("T","hāní","default","yes","entry 14055 hāní-","Lists H. hān and hāni 'loss' among the forms","inherited","none")]),
("a6642e98e1-1","hi","सेंत","something obtained free of charge","UNK","","","none","low","","HOMOGRAPH. Platts only cross-refers to a verb whose entry cites a Prakrit form; that is not a route statement for the noun under v1.1",[
 ("P","सेंत","ft","yes","p. 713, headword saiṅt / seṅt","Marked H; cross-reference to the verb saiṅtnā, whose own entry cites Prakrit forms","not stated",""),
 ("H","सेँत","exact","yes","p. 5265","Suggests a Sanskrit source or a deśī origin","not stated (lookup-only source)",""),
 ("T","sẽt","ft","no","—","Full-text searches for sẽt and saĩt find no Hindi form of this word","—","form not listed")]),
("a6642e98e1-2","hi","सेंत","collection, clump, mass","UNK","","","none","low","","HOMOGRAPH. Found only as sense 2 of the Hindi sabdasagara entry",[
 ("P","सेंत","ft","no","—","No entry with this sense","—",""),
 ("H","सेँत","exact","yes","p. 5265, sense 2","Same entry as the 'free of charge' sense","not stated (lookup-only source)",""),
 ("T","sẽt","ft","no","—","No Hindi form found","—","form not listed")]),
("cb94945a69-1","hi","अमावस","new moon","INH","REG-A","Pa. amāvasī-type and Pk. amāvassā (per Turner)","structural","medium","","Rests on the Turner listing",[
 ("P","अमावस","ft","yes","p. 80, headword amāvas","Marked H, with the Sanskrit formation in brackets; the fuller forms are marked S","not stated",""),
 ("H","अमावस","exact","yes","p. 293","Marked Hindi; refers to amāvasyā","not stated (lookup-only source)",""),
 ("T","amāvāsyā","default","yes","entry 565 amāvāsyā̀","Lists H. amāwas among the forms","inherited","none")]),
("d7f633ee5c-1","hi","ठंड","cold; winter","INH","REG-A","Pk. ṭhaḍḍhī (per Platts)","structural","medium","","Rests on Platts. Turner lists the variants ṭhaṇḍh, ṭhaṇḍhā, ṭhaṇḍā, not this exact form",[
 ("P","ठंड","ft","yes","p. 364, headword ṭhanḍ","Marked H; a Prakrit form and a Sanskrit equivalent are cited","inherited",""),
 ("H","ठंड","exact","yes","p. 1905","Marked Hindi; refers to another spelling","not stated (lookup-only source)",""),
 ("T","ṭhaṇḍ","ft","yes","p. 788, headword stabdha","Lists H. ṭhaṇḍh, ṭhaṇḍhā, ṭhaṇḍā 'cold', marked as the source of Panjabi and West Pahari forms","inherited for the variant forms","none (exact form not listed)")]),
("db7e20c432-1","hi","नाक","nose","INH","REG-A","Pk. ṇakka (per Platts and Turner)","structural","high","","HOMOGRAPH. Platts and Turner agree",[
 ("P","नाक","ft","yes","p. 1116, headword nāk","Marked H; a Prakrit form and a Sanskrit equivalent are cited","inherited",""),
 ("H","नाक","exact","yes","p. 2560, नाक 1","Gives a Sanskrit and a Pali form","not stated (lookup-only source)",""),
 ("T","nakka","default","yes","entry 6909 *nakka","Lists H. nāk, nā̃k among the forms","inherited","none")]),
("db7e20c432-2","hi","नाक","heaven","LRN","","","structural","medium","single_source_1884","HOMOGRAPH. Platts S only",[
 ("P","नाक","ft","yes","p. 1115, headword nāka / nāk","Marked S","learned (by Platts' S convention)",""),
 ("T","nāka","default","yes","entry 7036 nā́ka","Lists a Khowar form only; no Hindi form","not stated for Hindi","form not listed")]),
("dc04c1c9ed-1","hi","संवर्धन","rearing, fostering, developing","NSF","","","none","—","","Not found under either spelling (संवर्धन, संवर्द्धन)",[
 ("P","संवर्धन","ft","no","—","No result (also none for संवर्द्धन)","—",""),
 ("H","संवर्धन","exact","no","—","No result (also none for संवर्द्धन)","—",""),
 ("T","saṁvardhana","default","no","—","No head-word","—","form not listed")]),
("e98f43633d-1","hi","जामाता","son-in-law","LRN","","","structural","medium","single_source_1884","Turner lists distinct inherited Hindi forms (doublets)",[
 ("P","जामाता","ft","yes","p. 372, headword jāmātā","Marked S","learned (by Platts' S convention)",""),
 ("H","जामाता","exact","yes","p. 1744","Gives the Sanskrit stem as source","not stated (lookup-only source)",""),
 ("T","jāmātr̥","default","yes","entry 5198 jā́mātr̥","Lists H. jawā̃ī, jamāī, jawāī; not jāmātā","not stated for this form; inherited doublets exist","form not listed")]),
("ee2882ba7a-1","hi","बांटना","to distribute, divide","INH","REG-U","","structural","medium","","Rests on the Turner listing",[
 ("P","बांटना","ft","yes","p. 126, first headword bāṅṭnā","Marked H with a Sanskrit form in brackets; no Prakrit form","not stated",""),
 ("H","बाँटना","exact","yes","p. 3433, बाँटना 1","Offers three alternative Sanskrit sources","not stated (lookup-only source)",""),
 ("T","vaṇṭ","default","yes","entry 11238 váṇṭati","Lists H. bā̃ṭnā among the forms","inherited","none")]),
("f9b75d2302-1","hi","अगला","next; coming","UNK","","","none","low","","The Hindi sabdasagara cites a Prakrit form, but that source asserts no route under v1.1. Turner lists aglā for Lahnda and Panjabi, and H. āgal",[
 ("P","अगला","ft","yes","p. 71, headword aglā","Marked H with a Sanskrit formation in brackets; no Prakrit form","not stated",""),
 ("H","अगला","exact","yes","p. 91, अगला 1","Gives a Sanskrit and a Prakrit form","not stated (lookup-only source)",""),
 ("T","agra","exact","yes","entry 68 ágra","Among the -l- extensions lists L. P. aglā and H. āgal; no H. aglā","not stated for this form","form not listed")]),
("f9d1e53c34-1","hi","पूज्य","venerable; honoured","LRN","","","structural","medium","single_source_1884","Turner lists the distinct Hindi form pūj (doublet)",[
 ("P","पूज्य","ft","yes","p. 278, headword pūjya","Marked S; equated with pūj (marked H)","learned (by Platts' S convention)",""),
 ("H","पूज्य","exact","yes","p. 3074","Marked as Sanskrit","not stated (lookup-only source)",""),
 ("T","pūjya","default","yes","entry 8319 pūjya","Lists H. pūj 'worshipful'; not pūjya","not stated for this form; inherited doublet exists","form not listed")]),
("fab3254e0c-1","hi","रजत","silvery; white","LRN","","","structural","medium","single_source_1884","",[
 ("P","रजत","ft","yes","p. 588, headword rajat","Marked S","learned (by Platts' S convention)",""),
 ("H","रजत","exact","yes","p. 4106","Marked as Sanskrit","not stated (lookup-only source)",""),
 ("T","rajata","default","yes","entry 10576 rajatá","Lists Pali, Prakrit, Sinhalese and Maldivian forms; no Hindi form","not stated for Hindi","form not listed")]),
("0618434674-1","bn","পাহারা","watching, guarding; a watch","UNK","","","none","low","","J. Dasa cites a Hindi form and a chain from Sanskrit without a labelled MIA form. Turner lists the variant B. paharā, not this form, and suggests the Sanskrit word may itself be a Sanskritization of Persian",[
 ("J","পাহারা","exact","yes","p. 1334","Cites a Hindi form, then a chain from a Sanskrit word through an intermediate form; no form labelled Pali or Prakrit","not stated",""),
 ("T","prahar","default","yes","entry 8900 prahara","Lists N. B. paharā 'watch, guard'; head-word note raises a possible Persian source","not stated for this form","none (exact form not listed)")]),
("0b75c3f87a-1","bn","জ্বী","yes (agreement)","UNK","","","none","low","","Not found under this spelling. J. Dasa has জী (p. 859, a sense marked Hindi); Turner 5240 lists B. ji as a particle of assent. No source equates these with the spelling জ্বী",[
 ("J","জ্বী","exact","no","—","No result under this spelling (full-text search also empty)","—",""),
 ("T","jīvá","default","yes","entry 5240 jī́va (imperative, 'long live')","Lists B. ji among particles of assent or respect","inherited for B. ji; identity with the lemma not established","none (spelling identity unresolved)")]),
("1bd0c88f5c-1","bn","সর্বদা","always","UNK","","","none","low","","Sanskrit analysis only",[
 ("J","সর্ব্ব","exact","yes","p. 2028, sub-entry under সর্ব্ব","Analysed as a Sanskrit formation (sarva + dā)","not stated",""),
 ("T","sarvadā","default","no","—","No head-word","—","form not listed")]),
("20afb9f0d6-1","bn","সোয়ামি","synonym of স্বামী (husband, master)","NSF","","","none","—","","Turner has the etymon but lists only B. sā̃i",[
 ("J","সোয়ামি","exact","no","—","No result (also none for সোয়ামী, either encoding)","—",""),
 ("T","svāmin","default","yes","entry 13930 svāmín","Lists B. sā̃i 'master'; no form of this shape","not stated for this form","form not listed")]),
("32e0b38598-1","bn","জাইত","type; caste; community","NSF","","","none","—","","",[
 ("J","জাইত","exact","no","—","No headword; full-text hits are an unrelated verb form in old texts","—",""),
 ("T","jāti","default","yes","entry 5185 jāti","Lists Pali and Prakrit forms; no Bengali form","not stated for Bengali","form not listed")]),
("4cd53ca9f4-1","bn","জোছনা","alternative spelling of জ্যোৎস্না (moonlight)","UNK","","","none","low","","J. Dasa gives the Sanskrit word and register labels only (verse form; colloquial variants)",[
 ("J","জোছনা","ft","yes","p. 868, headword জোছনা / জোচ্ছনা","Sanskrit source cited; described as the soft form used in verse, with colloquial variants","not stated",""),
 ("T","jyṓtsnā","default","yes","entry 5301 jyṓtsnā","Bengali appears only with a 'firefly' word; no form of this shape","not stated for this form","form not listed")]),
("4ebd16e802-1","bn","গ্যালারি","gallery","NSF","","","none","—","","The word occurs inside a quotation in J. Dasa but has no entry",[
 ("J","গ্যালারি","ft","no","—","No headword (also none for গ্যালারী)","—",""), NQ]),
("8900de7aed-1","bn","পাদা","to fart","INH","REG-U","","structural","medium","","Rests on the Turner listing alone",[
 ("J","পাদা","default","no","—","No headword for the verb","—",""),
 ("T","pard","default","yes","entry 7933 párdatē","Lists B. pādā among the forms","inherited","none")]),
("8fd9a0b15d-1","bn","লব্ধ","obtained; gained","UNK","","","none","low","","Sanskrit analysis only",[
 ("J","লব্ধ","exact","yes","p. 1889, লব্ধ 1","Analysed as Sanskrit root plus suffix","not stated",""),
 ("T","labdha","default","yes","entry 10946 labdha","Long article; no Bengali form","not stated for Bengali","form not listed")]),
("92e21d6ebb-1","bn","ইহুদি","Jew; Jewish","EXT","","","explicit","high","","Found under the spelling ইহুদী",[
 ("J","ইহুদী","ft","yes","p. 285, headword ইহুদী","Etymology cites Hebrew and Arabic forms","external (Hebrew/Arabic)",""), NQ]),
("9512aa91f6-1","bn","প্রাচীর","wall; rampart","UNK","","","none","low","","J. Dasa marks the word Sanskrit and gives a colloquial variant; Turner lists only that variant (doublet)",[
 ("J","প্রাচীর","exact","yes","p. 1428","Marked Sanskrit; colloquial variant পাঁচীল noted","not stated",""),
 ("T","prācīra","default","yes","entry 8921 prācīra","Lists B. pā̃cil 'rampart' only","not stated for this form; inherited doublet exists","form not listed")]),
("981a823173-1","bn","বমি","vomit","UNK","","","none","low","","Sanskrit analysis only",[
 ("J","বমি","exact","yes","p. 1488","Analysed as Sanskrit root plus suffix","not stated",""),
 ("T","vamati","default","yes","entry 11294 vámati","Short article; no Bengali form. No head-word vami","not stated for Bengali","form not listed")]),
("a0e3c52f42-1","bn","সোয়াদ","(no definition line)","NSF","","","none","—","no_gloss","HOMOGRAPH. The Wiktionary section has no definition line, so no sense could be matched; the lemma is in no source",[
 ("J","সোয়াদ","exact","no","—","No result (also none for সোআদ, either encoding)","—","")]),
("a0e3c52f42-2","bn","সোয়াদ","the Arabic letter ṣād","NSF","","","none","—","","HOMOGRAPH",[
 ("J","সোয়াদ","exact","no","—","No result","—",""), NQ]),
("a0e3c52f42-3","bn","সোয়াদ","taste, flavour","NSF","","","none","—","","HOMOGRAPH. Turner has the etymon but no Bengali form",[
 ("J","সোয়াদ","exact","no","—","No result","—",""),
 ("T","svāda","default","yes","entry 13923 svāda","Lists Prakrit, Shina and Sindhi forms; no Bengali form","not stated for Bengali","form not listed")]),
("b314616373-1","bn","গৈরিক","saffron (colour)","UNK","","","none","low","","Sanskrit analysis only; Turner lists other Bengali forms (doublets)",[
 ("J","গৈরিক","exact","yes","p. 694","Analysed as a Sanskrit derivative of giri","not stated",""),
 ("T","gairika","default","yes","entry 4254 gairikā","Lists B. gerī, giri-māṭi, geruyā; not gairik","not stated for this form; inherited doublets exist","form not listed")]),
("ba2b5d05c9-1","bn","কমলা","orange (colour, fruit, tree)","INH","REG-U","","structural","low","","HOMOGRAPH. Rests on the Turner listing; the listed form is identical to the Sanskrit head-word form",[
 ("J","কমলা","exact","yes","p. 434, sense 6","Listed as one sense of a headword analysed as a Sanskrit formation","not stated",""),
 ("T","kamal","default","yes","entry 2763 kámala (with kamalā 'orange')","Lists N. B. kamalā 'orange' among the forms","inherited","none")]),
("ba2b5d05c9-2","bn","কমলা","form of an epithet (per Wiktionary gloss)","UNK","","","none","low","","HOMOGRAPH. The gloss is too thin to match a sense with confidence; J. Dasa's goddess-name senses are the nearest",[
 ("J","কমলা","exact","yes","p. 434, senses 1–5","Analysed as a Sanskrit formation","not stated","")]),
("e8a84295b0-1","bn","অর্পিতা","(no definition line)","NSF","","","none","—","no_gloss","The Wiktionary section has no definition line",[
 ("J","অর্পিতা","exact","no","—","No result","—",""),
 ("T","arpita","default","yes","entry 685 árpita-","Lists Pali, Prakrit, Old Gujarati and Sinhalese forms; no Bengali form","not stated for Bengali","form not listed")]),
("e9c488e1d5-1","bn","চুরি","theft","INH","REG-A","Pa. cōrikā; Pk. cōrī (per Turner)","structural","medium","","Rests on the Turner listing",[
 ("J","চুরি","exact","yes","p. 787, চুরি 2","Refers to a Sanskrit root and compares the Hindi form","not stated",""),
 ("T","caur","default","yes","entry 4937 caurikā","Lists B. cori, curi among the forms","inherited","none")]),
("eade04939b-1","bn","ভাল","good","INH","REG-U","","structural","medium","","HOMOGRAPH. Rests on the Turner listing",[
 ("J","ভাল","exact","yes","p. 1682, ভাল 2","Derived from Sanskrit bhadra, with no intermediate form given","not stated",""),
 ("T","bhalla","default","yes","entry 9408 bhalla","Lists B. bhāla 'good' among the forms","inherited","none")]),
("eade04939b-2","bn","ভাল","forehead; destiny","INH","REG-A","Pk. bhāla (per Turner)","structural","low","","HOMOGRAPH. Rests on the Turner listing; the listed form is identical to the Sanskrit head-word form",[
 ("J","ভাল","exact","yes","p. 1681, ভাল 1","Analysed as Sanskrit root plus suffix","not stated",""),
 ("T","bhāla","default","yes","entry 9472 bhāla","Lists A. B. Mth. H. bhāl among the forms","inherited","none")]),
("f5d702e794-1","bn","উড়ে","Odia; inhabitant of Odisha","NSF","","","none","—","","Turner has the etymon but lists only B. oṛiyā / uṛiyā",[
 ("J","উড়ে","exact","no","—","No result (either encoding)","—",""),
 ("T","ōḍra","default","yes","entry 2549 ōḍra","Lists B. oṛiyā, uṛiyā 'an inhabitant of Orissa'; not this form","not stated for this form","form not listed")]),
]
with open(f"{OUT}/extraction.csv","w",encoding="utf-8",newline="") as f:
    w=csv.writer(f); w.writerow("item_id,lang,lemma,sense,label,pathway,mia_form,evidence_strength,extractor_confidence,flags,notes".split(","))
    for r in I: w.writerow(r[:11])
with open(f"{OUT}/source_checks.csv","w",encoding="utf-8",newline="") as f:
    w=csv.writer(f); w.writerow("item_id,lang,lemma,source,query_url,found,entry_ref,route_evidence,route_asserted,loan_mark".split(","))
    for r in I:
        for s,q,mode,found,ref,ev,route,lm in r[11]:
            w.writerow([r[0],r[1],r[2],APP[s][0],url(s,q,mode) if q else "—",found,ref,ev,route,lm])
from collections import Counter
print(len(I), Counter(r[4] for r in I), sum(len(r[11]) for r in I))
