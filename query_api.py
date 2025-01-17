try:
    import sys
except ImportError:
    import pip
    pip.main(['install', '--user', 'sys'])
    import sys
try:
    import psycopg2
except ImportError:
    import psycopg2
import random
from typing import List
from hashlib import sha256
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel

app = FastAPI()

origins = [
    "*",
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Vote(BaseModel):
    wahlkreis: int
    token: int
    erst: str  # short partei
    zweit: str  # short partei


class BulkVotes(BaseModel):
    wahlkreis: int
    token: int
    list_numbers_first: List[int]
    list_numbers_second: List[int]
    list_votes_first: List[str]
    list_votes_second: List[int]


class VoteErst:
    def __init__(self, wahlkreis, token, erst):
        self.wahlkreis = wahlkreis
        self.token = token
        self.erst = erst


class VoteZweit:
    def __init__(self, wahlkreis, token, zweit):
        self.wahlkreis = wahlkreis
        self.token = token
        self.zweit = zweit


@app.post("/send_bulk_votes")
def add_bulk_votes_call(bulkVotes: BulkVotes):
    add_bulk_votes(bulkVotes)
    value = json.dumps({"response": True})
    return HTMLResponse(content=value, status_code=200)


@app.post("/add_vote")
def add_vote_call(vote: Vote):
    add_vote(vote)
    value = json.dumps({"response": True})
    return HTMLResponse(content=value, status_code=200)


@app.get("/query9_high")
async def query9_high_call():
    value = query9_high()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query9_low")
async def query9_low_call():
    value = query9_low()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query8_rich")
async def query8_rich_call():
    value = query8_rich()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query8_poor")
async def query8_poor_call():
    value = query8_poor()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query4_table2017")
async def query4_call2017():
    value = query4_table2017()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query4_table")
async def query4_call():
    value = query4_table()
    return HTMLResponse(content=value, status_code=200)


@app.get("/verify_token/{token}")
async def token_check_return_wahlzettel_call(token):
    value = token_check_return_wahlzettel(token)
    return HTMLResponse(content=value, status_code=200)


@app.get("/query3_wahlbeteiligung2017/{kreis_id}")
async def query3_wahlbeteiligung_call2017(kreis_id: int):
    value = query3_wahlbeteiligung2017(kreis_id)
    return HTMLResponse(content=value, status_code=200)


@app.get("/query3_wahlbeteiligung/{kreis_id}")
async def query3_wahlbeteiligung_call(kreis_id: int):
    value = query3_wahlbeteiligung(kreis_id)
    return HTMLResponse(content=value, status_code=200)


@app.get("/query3_direktkandidaten2017/{kreis_id}")
async def query3_direktkandidaten_call2017(kreis_id: int):
    value = query3_direktkandidaten2017(kreis_id)
    return HTMLResponse(content=value, status_code=200)


@app.get("/query3_direktkandidaten/{kreis_id}")
async def query3_direktkandidaten_call(kreis_id: int):
    value = query3_direktkandidaten(kreis_id)
    return HTMLResponse(content=value, status_code=200)


@app.get("/query3_stimmen_entwicklung/{kreis_id}")
async def query3_stimmen_entwicklung_call(kreis_id: int):
    value = query3_stimmen_entwicklung(kreis_id)
    return HTMLResponse(content=value, status_code=200)


@app.get("/query1_chart2017")
async def query1_chart2017_call():
    value = query1_chart2017()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query1_chart")
async def query1_chart_call():
    value = query1_chart()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query1_table2017")
async def query1_table2017_call():
    value = query1_table2017()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query1_table")
async def query1_table_call():
    value = query1_table()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query2_table")
async def query2_table_call():
    value = query2_table()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query2_table2017")
async def query2_table2017_call():
    value = query2_table2017()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query5_table")
async def query5_table_call():
    value = query5_table()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query6_win2017")
async def query6_win_call2017():
    value = query6_table_win2017()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query6_win")
async def query6_win_call():
    value = query6_table_win()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query6_loser2017")
async def query6_loser_call2017():
    value = query6_table_loser2017()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query6_loser")
async def query6_loser_call():
    value = query6_table_loser()
    return HTMLResponse(content=value, status_code=200)


@app.get("/query7_wahlbeteiligung/{kreis_id}")
async def query7_wahlbeteiligung_call(kreis_id: int):
    value = query7_wahlbeteiligung(kreis_id)
    return HTMLResponse(content=value, status_code=200)


@app.get("/query7_direktkandidaten/{kreis_id}")
async def query7_direktkandidaten_call(kreis_id: int):
    value = query7_direktkandidaten(kreis_id)
    return HTMLResponse(content=value, status_code=200)


@app.get("/query7_stimmen_entwicklung/{kreis_id}")
async def query7_stimmen_entwicklung(kreis_id: int):
    value = query7_stimmen_entwicklung(kreis_id)
    return HTMLResponse(content=value, status_code=200)


@app.get("/gen_token/{kreis}")
async def generate_token(kreis: int):
    value = generate_token(kreis)
    return HTMLResponse(content=value, status_code=200)

"""
db_host = "localhost"
db_port = 5432
db_name = "wahl"
db_user = "postgres"
db_password = "adnan"


# Inkens local test db:
db_host = "localhost"
db_port = 5432
db_name = "postgres"
db_user = "newuser"
db_password = "pw"
"""


with open("db_credentials.txt", "r") as f:
    db_host = f.readline().strip()
    db_port = f.readline().strip()
    db_name = f.readline().strip()
    db_user = f.readline().strip()
    db_password = f.readline().strip()


try:
    sql_con = psycopg2.connect(
        host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cur = sql_con.cursor()
    print("Success")
except:
    print("Fail")


def add_bulk_votes(bulkVotes: BulkVotes):
    for fir in range(0, len(bulkVotes.list_numbers_first)):
        for k in range(0, bulkVotes.list_numbers_first[fir]):
            vote1 = VoteErst(bulkVotes.wahlkreis,
                             bulkVotes.token, bulkVotes.list_votes_first[fir])
            add_vote_erst(vote1)
    for sec in range(0, len(bulkVotes.list_numbers_second)):
        for k in range(0, bulkVotes.list_numbers_second[sec]):
            vote2 = VoteZweit(bulkVotes.wahlkreis, bulkVotes.token,
                              bulkVotes.list_votes_second[sec])
            add_vote_zweit(vote2)

    num_votes = sum(bulkVotes.list_numbers_first)

    ungueltig_erst = bulkVotes.list_numbers_first[0]
    ungueltig_zweit = bulkVotes.list_numbers_second[0]

    ungueltige_bundes_erst = """update bundeslandaggregation
    set ungueltigeerst = ungueltigeerst + {}
    where wahljahr = 2021
    and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})""".format(ungueltig_erst, bulkVotes.wahlkreis)
    cur.execute(ungueltige_bundes_erst)
    sql_con.commit()

    ungueltige_bundes_zweit = """update bundeslandaggregation
    set ungueltigezweit = ungueltigezweit + {}
    where wahljahr = 2021
    and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})""".format(ungueltig_zweit, bulkVotes.wahlkreis)
    cur.execute(ungueltige_bundes_zweit)
    sql_con.commit()

    ungueltige_deutschland_erst = """update DeutschlandAggregation
    set ungueltigeerst = ungueltigeerst + {}
    where wahljahr = 2021""".format(ungueltig_erst)
    cur.execute(ungueltige_deutschland_erst)
    sql_con.commit()

    ungueltige_deutschland_zweit = """update DeutschlandAggregation
    set ungueltigezweit = ungueltigezweit + {}
    where wahljahr = 2021""".format(ungueltig_zweit)
    cur.execute(ungueltige_deutschland_zweit)
    sql_con.commit()

    ungueltige_kreis_erst = """update wahlkreisaggretation
    set ungueltigeerst = ungueltigeerst + {}
    where wahljahr = 2021
    and wahlkreis = {}""".format(ungueltig_erst, bulkVotes.wahlkreis)
    cur.execute(ungueltige_kreis_erst)
    sql_con.commit()

    ungueltige_kreis_zweit = """update wahlkreisaggretation
    set ungueltigezweit = ungueltigezweit + {}
    where wahljahr = 2021
    and wahlkreis = {}""".format(ungueltig_zweit, bulkVotes.wahlkreis)
    cur.execute(ungueltige_kreis_zweit)
    sql_con.commit()

    print(num_votes)
    bundeslandagg = """update bundeslandaggregation
    set anzahlwahlberechtigte = anzahlwahlberechtigte + {}, anzahlwaehlende = anzahlwaehlende + {}, bevoelkerung = bevoelkerung + {}
    where wahljahr = 2021
    and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})""".format(num_votes, num_votes, num_votes, bulkVotes.wahlkreis)
    cur.execute(bundeslandagg)
    sql_con.commit()
    deutschlandagg = """update DeutschlandAggregation
    set anzahlwahlberechtigte = anzahlwahlberechtigte + {}, anzahlwaehlende = anzahlwaehlende + {}, bevoelkerung = bevoelkerung + {}
    where wahljahr = 2021""".format(num_votes, num_votes, num_votes)
    cur.execute(deutschlandagg)
    sql_con.commit()
    wahlkreisagg = """update wahlkreisaggretation
    set anzahlwahlberechtigte = anzahlwahlberechtigte + {}, anzahlwaehlende = anzahlwaehlende + {}
    where wahljahr = 2021
    and wahlkreis = {}""".format(num_votes, num_votes, bulkVotes.wahlkreis)
    cur.execute(wahlkreisagg)

    sql_con.commit()
    update_percent_erst = """with neue_prozente as (
    select ba.bundesland, p.KurzBezeichnung, bsa.anzahlerststimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigeerst) as prozenterst, bsa.anzahlzweitstimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigezweit)as prozentzweit
    from bundeslandaggregation ba, bundeslandstimmenaggregation bsa, partei p
    where ba.wahljahr = 2021
    and ba.wahljahr = bsa.wahljahr
    and ba.bundesland =  (select bundesland from wahlkreis where wahlkreisid = {})
    and ba.bundesland = bsa.bundesland
    and bsa.partei = p.parteiid
    )
    update bundeslandprozenterst
    set prozenterststimmen = np.prozenterst
    from neue_prozente as np
    where np.KurzBezeichnung = bundeslandprozenterst.parteikurz
    and bundeslandprozenterst.bundesland = np.bundesland
    and bundeslandprozenterst.wahljahr = 2021""".format(bulkVotes.wahlkreis)
    cur.execute(update_percent_erst)
    sql_con.commit()
    update_percent_zweit = """with neue_prozente as (
    select ba.bundesland, p.KurzBezeichnung, bsa.anzahlerststimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigeerst) as prozenterst, bsa.anzahlzweitstimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigezweit)as prozentzweit
    from bundeslandaggregation ba, bundeslandstimmenaggregation bsa, partei p
    where ba.wahljahr = 2021
    and ba.wahljahr = bsa.wahljahr
    and ba.bundesland =  (select bundesland from wahlkreis where wahlkreisid = {})
    and ba.bundesland = bsa.bundesland
    and bsa.partei = p.parteiid
    )
    update bundeslandprozentzwei
    set prozentzweitstimmen = np.prozentzweit
    from neue_prozente as np
    where np.KurzBezeichnung = bundeslandprozentzwei.parteikurz
    and bundeslandprozentzwei.bundesland = np.bundesland
    and bundeslandprozentzwei.wahljahr = 2021""".format(bulkVotes.wahlkreis)
    cur.execute(update_percent_zweit)
    sql_con.commit()
    deutsch_prozente = """with neue_prozente as (
    select dsa.partei, dsa.anzahlerststimmen*100.0000/(da.anzahlwaehlende-da.ungueltigeerst) as prozenterst, dsa.anzahlzweitstimmen*100.0000/(da.anzahlwaehlende-da.ungueltigezweit)as prozentzweit
    from DeutschlandAggregation da, deutschlandstimmenaggregation dsa
    where da.wahljahr = 2021
    and da.wahljahr = dsa.wahljahr
    )
    -- update erst und zweit
    update deutschlandstimmenaggregation
    set prozenterststimmen = np.prozenterst, prozentzweitstimmen = np.prozentzweit
    from neue_prozente as np
    where np.partei = deutschlandstimmenaggregation.partei
    and deutschlandstimmenaggregation.wahljahr = 2021"""
    cur.execute(deutsch_prozente)
    sql_con.commit()
    wahlkreis_erst_prozente = """with neue_prozente as (
    select wa.wahlkreis, p.KurzBezeichnung as partei, wsa.anzahlzweitstimmen*100.0000/(wa.anzahlwaehlende-wa.ungueltigezweit)as prozentzweit, wsa.anzahlerststimmen*100.0000/(wa.anzahlwaehlende-wa.ungueltigeerst)as prozenterst
    from wahlkreisaggretation wa, wahlkreisstimmenaggregation wsa, partei p
    where wa.wahljahr = 2021
    and wa.wahljahr = wsa.wahljahr
    and wsa.wahlkreis = wa.wahlkreis
    and wa.wahlkreis = {}
    and wsa.partei = p.parteiid
    )
    -- update erst
    update wahlkreisprozenterst
    set prozenterststimmen = np.prozenterst
    from neue_prozente as np
    where np.partei = wahlkreisprozenterst.parteikurz
    and np.wahlkreis = wahlkreisprozenterst.wahlkreis
    and wahljahr = 2021""".format(bulkVotes.wahlkreis)
    cur.execute(wahlkreis_erst_prozente)
    sql_con.commit()
    wahlkreis_zweit_prozente = """with neue_prozente as (
    select wa.wahlkreis, p.KurzBezeichnung as partei, wsa.anzahlzweitstimmen*100.0000/(wa.anzahlwaehlende-wa.ungueltigezweit)as prozentzweit, wsa.anzahlerststimmen*100.0000/(wa.anzahlwaehlende-wa.ungueltigeerst)as prozenterst
    from wahlkreisaggretation wa, wahlkreisstimmenaggregation wsa, partei p
    where wa.wahljahr = 2021
    and wa.wahljahr = wsa.wahljahr
    and wsa.wahlkreis = wa.wahlkreis
    and wa.wahlkreis = {}
    and wsa.partei = p.parteiid
    )
    update wahlkreisprozentzweit
    set prozentzweitstimmen = np.prozentzweit
    from neue_prozente as np
    where np.partei = wahlkreisprozentzweit.parteikurz
    and np.wahlkreis = wahlkreisprozentzweit.wahlkreis
    and wahljahr = 2021""".format(bulkVotes.wahlkreis)
    cur.execute(wahlkreis_zweit_prozente)
    sql_con.commit()


def generate_token(kreis):
    range_query = """
    select tokenrangemin, tokenrangemax
    from tokenrange
    where wahlkreis = {}
    """.format(kreis)
    cur.execute(range_query)
    range = cur.fetchall()[0]
    mini = range[0]
    maxi = range[1]
    token = random.randrange(mini, maxi)
    hashed_token = sha256(token.to_bytes(8, 'big', signed=False)).hexdigest()
    insert_token_query = """
    INSERT INTO tokens 
        VALUES ('{}', {})
    """.format(hashed_token, kreis)
    cur.execute(insert_token_query)
    sql_con.commit()
    jsony = {"token": token}
    return json.dumps(jsony)


def add_vote_erst(vote: VoteErst):
    wahlkreis = vote.wahlkreis
    erststimme_party = -1
    max1_query = """
    select case when exists (select 1 from erststimmen) then max(erstimmid) else 0 end
    from erststimmen 
    """
    cur.execute(max1_query)
    max1 = cur.fetchall()[0][0]
    if vote.erst == "None":
        erststimme_party = -1
    else:
        erst_party_name = vote.erst.split("_")[2]
        if (erst_party_name == "null"):
            erststimme_party = 48
        else:
            id_query = """
            select parteiid
            from partei 
            where kurzbezeichnung = '{}'
            """.format(erst_party_name)
            cur.execute(id_query)
            erststimme_party = cur.fetchall()[0][0]
    insert_vote1_query = """insert into erststimmen(erstimmid, wahlkreis, partei)values ({}, {}, {})""".format(
        max1 + 1, wahlkreis, erststimme_party)
    cur.execute(insert_vote1_query)
    sql_con.commit()

    bundesland_partei_erst = """update bundeslandstimmenaggregation
    set anzahlerststimmen = anzahlerststimmen + 1
    where wahljahr = 2021
    and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
    and partei = {}""".format(wahlkreis, erststimme_party)
    cur.execute(bundesland_partei_erst)
    sql_con.commit()
    deutschland_partei_erst = """update deutschlandstimmenaggregation
    set anzahlerststimmen = anzahlerststimmen + 1
    where wahljahr = 2021
    and partei = {}""".format(erststimme_party)
    cur.execute(deutschland_partei_erst)
    sql_con.commit()
    wahlkreis_partei_erst = """update wahlkreisstimmenaggregation
    set anzahlerststimmen = anzahlerststimmen + 1
    where wahljahr = 2021
    and wahlkreis = {}
    and partei = {}""".format(wahlkreis, erststimme_party)
    cur.execute(wahlkreis_partei_erst)
    sql_con.commit()


def add_vote_zweit(vote: VoteZweit):
    wahlkreis = vote.wahlkreis
    zweitstimme_party = -1
    max2_query = """
    select case when exists (select 1 from zweitstimmen) then max(zweitstimmid) else 0 end
    from zweitstimmen
    """
    cur.execute(max2_query)
    max2 = cur.fetchall()[0][0]
    zweit_party_num = vote.zweit
    if (zweit_party_num == "None"):
        zweitstimme_party = -1
    else:
        zweitstimme_party = zweit_party_num
    insert_vote2_query = """
    insert into zweitstimmen(zweitstimmid, wahlkreis, partei)
    values ({}, {}, {})
    """.format(max2 + 1, wahlkreis, zweitstimme_party)
    cur.execute(insert_vote2_query)
    sql_con.commit()

    bundesland_partei_zweit = """update bundeslandstimmenaggregation
    set anzahlzweitstimmen = anzahlzweitstimmen + 1
    where wahljahr = 2021
    and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
    and partei = {}""".format(wahlkreis, zweitstimme_party)
    cur.execute(bundesland_partei_zweit)
    sql_con.commit()
    deutschland_partei_zweit = """update deutschlandstimmenaggregation
    set anzahlzweitstimmen = anzahlzweitstimmen + 1
    where wahljahr = 2021
    and partei = {}""".format(zweitstimme_party)
    cur.execute(deutschland_partei_zweit)
    sql_con.commit()
    wahlkreis_partei_zweit = """update wahlkreisstimmenaggregation
    set anzahlzweitstimmen = anzahlzweitstimmen + 1
    where wahljahr = 2021
    and wahlkreis = {}
    and partei = {}""".format(wahlkreis, zweitstimme_party)
    cur.execute(wahlkreis_partei_zweit)
    sql_con.commit()

# erst - first_last_party
# zweit - party number
# if voter chose to not vote, values are None


def add_vote(vote):
    wahlkreis = vote.wahlkreis
    erststimme_party = -1
    zweitstimme_party = -1

    max1_query = """
    select case when exists (select 1 from erststimmen) then max(erstimmid) else 0 end
    from erststimmen 
    """
    cur.execute(max1_query)
    max1 = cur.fetchall()[0][0]

    max2_query = """
    select case when exists (select 1 from zweitstimmen) then max(zweitstimmid) else 0 end
    from zweitstimmen 
    """
    cur.execute(max2_query)
    max2 = cur.fetchall()[0][0]
    if vote.erst == "None":
        erststimme_party = -1
    else:
        erst_party_name = vote.erst.split("_")[2]
        if (erst_party_name == "null"):
            erststimme_party = 48
        else:
            id_query = """
            select parteiid
            from partei 
            where kurzbezeichnung = '{}'
            """.format(erst_party_name)
            cur.execute(id_query)
            erststimme_party = cur.fetchall()[0][0]
    insert_vote1_query = """insert into erststimmen(erstimmid, wahlkreis, partei)values ({}, {}, {})""".format(
        max1 + 1, wahlkreis, erststimme_party)
    cur.execute(insert_vote1_query)
    zweit_party_num = vote.zweit
    if (zweit_party_num == "None"):
        zweitstimme_party = -1
    else:
        zweitstimme_party = zweit_party_num
    insert_vote2_query = """
    insert into zweitstimmen(zweitstimmid, wahlkreis, partei)
    values ({}, {}, {})
    """.format(max2 + 1, wahlkreis, zweitstimme_party)
    cur.execute(insert_vote2_query)
    sql_con.commit()

    bundesland_partei_erst = """update bundeslandstimmenaggregation
    set anzahlerststimmen = anzahlerststimmen + 1
    where wahljahr = 2021
    and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
    and partei = {}""".format(wahlkreis, erststimme_party)
    cur.execute(bundesland_partei_erst)
    sql_con.commit()
    deutschland_partei_erst = """update deutschlandstimmenaggregation
    set anzahlerststimmen = anzahlerststimmen + 1
    where wahljahr = 2021
    and partei = {}""".format(erststimme_party)
    cur.execute(deutschland_partei_erst)
    sql_con.commit()
    wahlkreis_partei_erst = """update wahlkreisstimmenaggregation
    set anzahlerststimmen = anzahlerststimmen + 1
    where wahljahr = 2021
    and wahlkreis = {}
    and partei = {}""".format(wahlkreis, erststimme_party)
    cur.execute(wahlkreis_partei_erst)
    sql_con.commit()

    bundesland_partei_zweit = """update bundeslandstimmenaggregation
    set anzahlzweitstimmen = anzahlzweitstimmen + 1
    where wahljahr = 2021
    and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})
    and partei = {}""".format(wahlkreis, zweitstimme_party)
    cur.execute(bundesland_partei_zweit)
    sql_con.commit()
    deutschland_partei_zweit = """update deutschlandstimmenaggregation
    set anzahlzweitstimmen = anzahlzweitstimmen + 1
    where wahljahr = 2021
    and partei = {}""".format(zweitstimme_party)
    cur.execute(deutschland_partei_zweit)
    sql_con.commit()
    wahlkreis_partei_zweit = """update wahlkreisstimmenaggregation
    set anzahlzweitstimmen = anzahlzweitstimmen + 1
    where wahljahr = 2021
    and wahlkreis = {}
    and partei = {}""".format(wahlkreis, zweitstimme_party)
    cur.execute(wahlkreis_partei_zweit)
    sql_con.commit()

    if (erststimme_party == -1):  # ungueltig 1
        ungueltige_bundes_erst = """update bundeslandaggregation set ungueltigeerst = ungueltigeerst + 1
        where wahljahr = 2021
        and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})""".format(wahlkreis)
        cur.execute(ungueltige_bundes_erst)
        sql_con.commit()
        ungueltige_deutschland_erst = """update DeutschlandAggregation
        set ungueltigeerst = ungueltigeerst + 1
        where wahljahr = 2021"""
        cur.execute(ungueltige_deutschland_erst)
        sql_con.commit()
        ungueltige_kreis_erst = """update wahlkreisaggretation
        set ungueltigeerst = ungueltigeerst + 1
        where wahljahr = 2021
        and wahlkreis = {}""".format(wahlkreis)
        cur.execute(ungueltige_kreis_erst)
        sql_con.commit()
    if (zweitstimme_party == -1):  # ungueltig 2
        ungueltige_bundes_zweit = """update bundeslandaggregation
        set ungueltigezweit = ungueltigezweit + 1
        where wahljahr = 2021
        and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})""".format(wahlkreis)
        cur.execute(ungueltige_bundes_zweit)
        sql_con.commit()
        ungueltige_deutschland_zweit = """update DeutschlandAggregation
        set ungueltigezweit = ungueltigezweit + 1
        where wahljahr = 2021"""
        cur.execute(ungueltige_deutschland_zweit)
        sql_con.commit()
        ungueltige_kreis_zweit = """update wahlkreisaggretation
        set ungueltigezweit = ungueltigezweit + 1
        where wahljahr = 2021
        and wahlkreis = {}""".format(wahlkreis)
        cur.execute(ungueltige_kreis_zweit)
        sql_con.commit()

    bundeslandagg = """update bundeslandaggregation
    set anzahlwahlberechtigte = anzahlwahlberechtigte + 1, anzahlwaehlende = anzahlwaehlende + 1, bevoelkerung = bevoelkerung + 1
    where wahljahr = 2021
    and bundesland = (select bundesland from wahlkreis where wahlkreisid = {})""".format(wahlkreis)
    cur.execute(bundeslandagg)
    sql_con.commit()
    deutschlandagg = """update DeutschlandAggregation
    set anzahlwahlberechtigte = anzahlwahlberechtigte + 1, anzahlwaehlende = anzahlwaehlende + 1, bevoelkerung = bevoelkerung + 1
    where wahljahr = 2021"""
    cur.execute(deutschlandagg)
    sql_con.commit()
    wahlkreisagg = """update wahlkreisaggretation
    set anzahlwahlberechtigte = anzahlwahlberechtigte + 1, anzahlwaehlende = anzahlwaehlende + 1
    where wahljahr = 2021
    and wahlkreis = {}""".format(wahlkreis)
    cur.execute(wahlkreisagg)
    sql_con.commit()
    update_percent_erst = """with neue_prozente as (
    select ba.bundesland, p.KurzBezeichnung, bsa.anzahlerststimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigeerst) as prozenterst, bsa.anzahlzweitstimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigezweit)as prozentzweit
    from bundeslandaggregation ba, bundeslandstimmenaggregation bsa, partei p
    where ba.wahljahr = 2021
    and ba.wahljahr = bsa.wahljahr
    and ba.bundesland =  (select bundesland from wahlkreis where wahlkreisid = {})
    and ba.bundesland = bsa.bundesland
    and bsa.partei = p.parteiid
    )
    update bundeslandprozenterst
    set prozenterststimmen = np.prozenterst
    from neue_prozente as np
    where np.KurzBezeichnung = bundeslandprozenterst.parteikurz
    and bundeslandprozenterst.bundesland = np.bundesland
    and bundeslandprozenterst.wahljahr = 2021""".format(wahlkreis)
    cur.execute(update_percent_erst)
    sql_con.commit()
    update_percent_zweit = """with neue_prozente as (
    select ba.bundesland, p.KurzBezeichnung, bsa.anzahlerststimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigeerst) as prozenterst, bsa.anzahlzweitstimmen*100.0000/(ba.anzahlwaehlende-ba.ungueltigezweit)as prozentzweit
    from bundeslandaggregation ba, bundeslandstimmenaggregation bsa, partei p
    where ba.wahljahr = 2021
    and ba.wahljahr = bsa.wahljahr
    and ba.bundesland =  (select bundesland from wahlkreis where wahlkreisid = {})
    and ba.bundesland = bsa.bundesland
    and bsa.partei = p.parteiid
    )
    update bundeslandprozentzwei
    set prozentzweitstimmen = np.prozentzweit
    from neue_prozente as np
    where np.KurzBezeichnung = bundeslandprozentzwei.parteikurz
    and bundeslandprozentzwei.bundesland = np.bundesland
    and bundeslandprozentzwei.wahljahr = 2021""".format(wahlkreis)
    cur.execute(update_percent_zweit)
    sql_con.commit()
    deutsch_prozente = """with neue_prozente as (
    select dsa.partei, dsa.anzahlerststimmen*100.0000/(da.anzahlwaehlende-da.ungueltigeerst) as prozenterst, dsa.anzahlzweitstimmen*100.0000/(da.anzahlwaehlende-da.ungueltigezweit)as prozentzweit
    from DeutschlandAggregation da, deutschlandstimmenaggregation dsa
    where da.wahljahr = 2021
    and da.wahljahr = dsa.wahljahr
    )
    -- update erst und zweit
    update deutschlandstimmenaggregation
    set prozenterststimmen = np.prozenterst, prozentzweitstimmen = np.prozentzweit
    from neue_prozente as np
    where np.partei = deutschlandstimmenaggregation.partei
    and deutschlandstimmenaggregation.wahljahr = 2021"""
    cur.execute(deutsch_prozente)
    sql_con.commit()
    wahlkreis_erst_prozente = """with neue_prozente as (
    select wa.wahlkreis, p.KurzBezeichnung as partei, wsa.anzahlzweitstimmen*100.0000/(wa.anzahlwaehlende-wa.ungueltigezweit)as prozentzweit, wsa.anzahlerststimmen*100.0000/(wa.anzahlwaehlende-wa.ungueltigeerst)as prozenterst
    from wahlkreisaggretation wa, wahlkreisstimmenaggregation wsa, partei p
    where wa.wahljahr = 2021
    and wa.wahljahr = wsa.wahljahr
    and wsa.wahlkreis = wa.wahlkreis
    and wa.wahlkreis = {}
    and wsa.partei = p.parteiid
    )
    -- update erst
    update wahlkreisprozenterst
    set prozenterststimmen = np.prozenterst
    from neue_prozente as np
    where np.partei = wahlkreisprozenterst.parteikurz
    and np.wahlkreis = wahlkreisprozenterst.wahlkreis
    and wahljahr = 2021""".format(wahlkreis)
    cur.execute(wahlkreis_erst_prozente)
    sql_con.commit()
    wahlkreis_zweit_prozente = """with neue_prozente as (
    select wa.wahlkreis, p.KurzBezeichnung as partei, wsa.anzahlzweitstimmen*100.0000/(wa.anzahlwaehlende-wa.ungueltigezweit)as prozentzweit, wsa.anzahlerststimmen*100.0000/(wa.anzahlwaehlende-wa.ungueltigeerst)as prozenterst
    from wahlkreisaggretation wa, wahlkreisstimmenaggregation wsa, partei p
    where wa.wahljahr = 2021
    and wa.wahljahr = wsa.wahljahr
    and wsa.wahlkreis = wa.wahlkreis
    and wa.wahlkreis = {}
    and wsa.partei = p.parteiid
    )
    update wahlkreisprozentzweit
    set prozentzweitstimmen = np.prozentzweit
    from neue_prozente as np
    where np.partei = wahlkreisprozentzweit.parteikurz
    and np.wahlkreis = wahlkreisprozentzweit.wahlkreis
    and wahljahr = 2021""".format(wahlkreis)
    cur.execute(wahlkreis_zweit_prozente)
    sql_con.commit()


# validate token, return json
# isValid, wahlkreis, erstimmenzettel, zweitstimmenzettel
def token_check_return_wahlzettel(token):
    jsony = {"isValid": False, "wahlkreis": 0,
             "erstimmenzettel": [], "zweitstimmenzettel": []}
    if (not str(token).isdigit()):
        jsony = {"isValid": False, "wahlkreis": 0,
                 "erstimmenzettel": [], "zweitstimmenzettel": []}
        return json.dumps(jsony)
    hashed_token = sha256(int(token).to_bytes(
        8, 'big', signed=False)).hexdigest()

    if (len(str(token)) == 16):  # Admin token
        check_admin_token_query = """
        select COUNT(*) from adminTokens where token = '{}'
        """.format(hashed_token)
        cur.execute(check_admin_token_query)
        admin_token_legit = cur.fetchall()[0][0]
        if not admin_token_legit:
            print("Invalid Admin token")
            jsony = {"isValid": False, "wahlkreis": 0,
                     "erstimmenzettel": [], "zweitstimmenzettel": []}
            return json.dumps(jsony)
        else:
            admin_wahlkreis_query = """select wahlkreis from adminTokens where token = '{}'""".format(
                hashed_token)
            cur.execute(admin_wahlkreis_query)
            wahlkreis_admin = cur.fetchall()[0][0]
            zweitstimmenzettel_admin = zweitstimmen_data(wahlkreis_admin)
            erstimmenzettel_admin = erststimmen_data(wahlkreis_admin)
            jsony = {"isValid": "Admin", "wahlkreis": wahlkreis_admin,
                     "erstimmenzettel": erstimmenzettel_admin, "zweitstimmenzettel": zweitstimmenzettel_admin}
            return json.dumps(jsony)

    check_token_query = """
    select COUNT(*) from tokens where token = '{}'
    """.format(hashed_token)
    cur.execute(check_token_query)
    record_exists = cur.fetchall()[0][0]
    if not record_exists:
        print("Token not valid.")
        jsony = {"isValid": False, "wahlkreis": 0,
                 "erstimmenzettel": [], "zweitstimmenzettel": []}
        return json.dumps(jsony)
    else:
        wahlkreis_query = """
        select wahlkreis
        from tokenrange
        where tokenrangemin < {}
        and tokenrangemax > {}
        """.format(token, token)
        cur.execute(wahlkreis_query)
        wahlkreis = cur.fetchall()[0][0]
        zweitstimmenzettel = zweitstimmen_data(wahlkreis)
        erstimmenzettel = erststimmen_data(wahlkreis)
        delete_token_query = """
        DELETE FROM tokens
        WHERE token = '{}'
        """.format(hashed_token)
        cur.execute(delete_token_query)
        sql_con.commit()
        jsony = {"isValid": True, "wahlkreis": wahlkreis,
                 "erstimmenzettel": erstimmenzettel, "zweitstimmenzettel": zweitstimmenzettel}
        return json.dumps(jsony)


def query1_chart2017():
    jsony = {"CSU": 46, "CDU": 200, "DIE LINKE": 69,
             "FDP": 80, "SPD": 153, "GR\u00dcNE": 67, "AfD": 94}
    return json.dumps(jsony)


def query1_chart():
    cur.execute("""SELECT p.KurzBezeichnung, s.sitze FROM sitzverteilungbundestag s, partei p
WHERE s.partei = p.parteiid""")

    party = []
    performance = []
    mobile_records = cur.fetchall()
    for i in mobile_records:
        party.append(i[0])
        performance.append(int(i[1]))
    jsony = dict(zip(party, performance))
    return json.dumps(jsony)


def query1_table2017():
    str_table = """<table><tr><th>Partei</th><th>Sitze</th></tr><tr><td>CSU</td><td>46</td></tr><tr><td>CDU</td><td>200</td></tr><tr><td>DIE LINKE</td><td>69</td></tr><tr><td>FDP</td><td>80</td></tr><tr><td>SPD</td><td>153</td></tr><tr><td>GR\u00dcNE</td><td>67</td></tr><tr><td>AfD</td><td>94</td></tr><tr><td></table>"""
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query1_table():

    cur.execute("""SELECT p.KurzBezeichnung, s.sitze FROM sitzverteilungbundestag s, partei p
    WHERE s.partei = p.parteiid""")

    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '<th>Sitze</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + \
            str(i[0]) + '</td><td>' + str(i[1]) + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query2_table2017():
    cur.execute("""with wahlkreis_max as (
    select wahlkreis, max(prozenterststimmen) as maxi
    from wahlkreisprozenterst
    where wahljahr = 2017
    group by wahlkreis
),
direktmandate_wahlkreis as (
    select w.wahlkreis, w.parteikurz
    from wahlkreis_max b, wahlkreisprozenterst w
    where b.wahlkreis = w.wahlkreis 
    and b.maxi = w.prozenterststimmen
),
direktmandate as(
    select k.kandidatid, k.firstname, k.lastname, k.beruf, dw.parteikurz as partei
    from direktmandate_wahlkreis dw, direktkandidaten dk, kandidaten k, partei p
    where dw.wahlkreis = dk.wahlkreis
    and dk.kandidatid = k.kandidatid
    and p.KurzBezeichnung = dw.parteikurz
    and p.parteiid = k.partei
    and k.wahljahr = 2017
),
-- Teil für Listenmandate
-- anzahl sitze pro partei pro bundesland minus die direktmandate, die schon verbraucht wurden
sitze_fuer_liste as(
    select b.partei, b.bundesland, (s.sitze-b.direktmandate) as listensitze
    from sitzverteilungparteienprobundesland2017 s, bundeslandstimmenaggregation b 
    where b.wahljahr = 2017
    and s.partei = b.partei
    and s.bundesland = b.bundesland
),
-- rausloeschen derer aus listenkandidaten, die schon per direktmandat in den BT kommen
liste_ohne_direktmandate as(
    select *
    from listenkandidaten lk
    where lk.kandidatid not in (select kandidatid from direktmandate)
),
-- kandidaten sortieren, um spaeter nur die top X herauszufiltern
reihennummern as(
  select ld.kandidatid, sl.partei, ld.bundesland, ROW_NUMBER() OVER(PARTITION BY sl.partei, sl.bundesland ORDER BY ld.listenplatz ASC) AS row_number
  from liste_ohne_direktmandate ld, sitze_fuer_liste sl, kandidaten k
  where ld.kandidatid = k.kandidatid
  and sl.bundesland = ld.bundesland
  and sl.partei = k.partei
  and k.wahljahr = 2017
),
-- kandidaten, die einen sitz bekommen herausfiltern
listenkandidaten as(
    select r.kandidatid, sl.partei, sl.bundesland
    from sitze_fuer_liste sl, reihennummern r
    where sl.partei = r.partei
    and sl.bundesland = r.bundesland
    and r.row_number <= sl.listensitze
)
-- direktkandidaten und listenkandidaten vereinigen
select * from direktmandate
union
select k.kandidatid, k.firstname, k.lastname, k.beruf, p.KurzBezeichnung as partei
from listenkandidaten l, kandidaten k, partei p
where l.kandidatid = k.kandidatid
and k.wahljahr = 2017
and p.parteiid = k.partei""")

    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Vorname</th>'
    str_table = str_table + '<th>Nachname</th>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + \
            str(i[1]) + '</td><td>' + str(i[2]) + \
            '</td><td>' + str(i[4]) + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query2_table():

    cur.execute("""with wahlkreis_max as (
    select wahlkreis, max(prozenterststimmen) as maxi
    from wahlkreisprozenterst
    where wahljahr = 2021
    group by wahlkreis
),
direktmandate_wahlkreis as (
    select w.wahlkreis, w.parteikurz
    from wahlkreis_max b, wahlkreisprozenterst w
    where b.wahlkreis = w.wahlkreis 
    and b.maxi = w.prozenterststimmen
),
direktmandate as(
    select k.kandidatid, k.firstname, k.lastname, k.beruf, dw.parteikurz as partei
    from direktmandate_wahlkreis dw, direktkandidaten dk, kandidaten k, partei p
    where dw.wahlkreis = dk.wahlkreis
    and dk.kandidatid = k.kandidatid
    and p.KurzBezeichnung = dw.parteikurz
    and p.parteiid = k.partei
    and k.wahljahr = 2021
),
-- Teil für Listenmandate
-- anzahl sitze pro partei pro bundesland minus die direktmandate, die schon verbraucht wurden
sitze_fuer_liste as(
    select b.partei, b.bundesland, (s.sitze-b.direktmandate) as listensitze
    from sitzverteilungparteienprobundesland s, bundeslandstimmenaggregation b 
    where b.wahljahr = 2021
    and s.partei = b.partei
    and s.bundesland = b.bundesland
),
-- rausloeschen derer aus listenkandidaten, die schon per direktmandat in den BT kommen
liste_ohne_direktmandate as(
    select *
    from listenkandidaten lk
    where lk.kandidatid not in (select kandidatid from direktmandate)
),
-- kandidaten sortieren, um spaeter nur die top X herauszufiltern
reihennummern as(
  select ld.kandidatid, sl.partei, ld.bundesland, ROW_NUMBER() OVER(PARTITION BY sl.partei, sl.bundesland ORDER BY ld.listenplatz ASC) AS row_number
  from liste_ohne_direktmandate ld, sitze_fuer_liste sl, kandidaten k
  where ld.kandidatid = k.kandidatid
  and sl.bundesland = ld.bundesland
  and sl.partei = k.partei
  and k.wahljahr = 2021
),
-- kandidaten, die einen sitz bekommen herausfiltern
listenkandidaten as (select r.kandidatid, sl.partei, sl.bundesland
from sitze_fuer_liste sl, reihennummern r
where sl.partei = r.partei
and sl.bundesland = r.bundesland
and r.row_number <= sl.listensitze)
select * from direktmandate
union
select k.kandidatid, k.firstname, k.lastname, k.beruf, p.KurzBezeichnung as partei
from listenkandidaten l, kandidaten k, partei p
where l.kandidatid = k.kandidatid
and k.wahljahr = 2021
and p.parteiid = k.partei""")

    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Vorname</th>'
    str_table = str_table + '<th>Nachname</th>'
    str_table = str_table + '<th>Beruf</th>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + str(i[1]) + '</td><td>' + str(
            i[2]) + '</td><td>' + str(i[3]) + '</td><td>' + str(i[4]) + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query4_table2017():
    cur.execute("""with erststimmensieger as (
  select we.wahlkreis, we.wahljahr, we.parteikurz as erststimmensieger
  from wahlkreisprozenterst we
  where we.wahljahr = 2017
  and not exists                        
          (select *                    
          from wahlkreisprozenterst we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2017
          and we2.prozenterststimmen > we.prozenterststimmen    
          )
  ),
  zweitstimmensieger as(
    select we.wahlkreis, we.wahljahr, we.parteikurz as zweitstimmensieger
    from wahlkreisprozentzweit we
    where we.wahljahr = 2017
    and not exists                        
          (select *                    
          from wahlkreisprozentzweit we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2017
          and we2.prozentzweitstimmen > we.prozentzweitstimmen    
          )
  )
  select w.wahlkreisname,e.wahljahr,e.erststimmensieger,z.zweitstimmensieger
  from erststimmensieger e, zweitstimmensieger z, wahlkreis w
  where e.wahlkreis = z.wahlkreis AND e.wahlkreis = w.wahlkreisid""")

    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Wahlkreisname</th>'
    str_table = str_table + '<th>Wahljahr</th>'
    str_table = str_table + '<th>Erststimmensieger</th>'
    str_table = str_table + '<th>Zweitstimmensieger</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + str(i[0]) + '</td><td>' + str(
            i[1]) + '</td><td>' + str(i[2]) + '</td><td>' + str(i[3]) + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query4_table():

    cur.execute("""with erststimmensieger as (
  select we.wahlkreis, we.wahljahr, we.parteikurz as erststimmensieger
  from wahlkreisprozenterst we
  where we.wahljahr = 2021
  and not exists                        
          (select *                    
          from wahlkreisprozenterst we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2021
          and we2.prozenterststimmen > we.prozenterststimmen    
          )
  ),
  zweitstimmensieger as(
    select we.wahlkreis, we.wahljahr, we.parteikurz as zweitstimmensieger
    from wahlkreisprozentzweit we
    where we.wahljahr = 2021
    and not exists                        
          (select *                    
          from wahlkreisprozentzweit we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2021
          and we2.prozentzweitstimmen > we.prozentzweitstimmen    
          )
  )
  select w.wahlkreisname,e.wahljahr,e.erststimmensieger,z.zweitstimmensieger
  from erststimmensieger e, zweitstimmensieger z, wahlkreis w
  where e.wahlkreis = z.wahlkreis AND e.wahlkreis = w.wahlkreisid""")

    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Wahlkreisname</th>'
    str_table = str_table + '<th>Wahljahr</th>'
    str_table = str_table + '<th>Erststimmensieger</th>'
    str_table = str_table + '<th>Zweitstimmensieger</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + str(i[0]) + '</td><td>' + str(
            i[1]) + '</td><td>' + str(i[2]) + '</td><td>' + str(i[3]) + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query3_wahlbeteiligung2017(kreis):
    cur.execute("""select a.wahlkreis, w.wahlkreisname, (1.00*AnzahlWaehlende)/anzahlwahlberechtigte as wahlbeteiligung, wahljahr
        from wahlkreisaggretation as a, wahlkreis as w
        WHERE wahljahr = 2017 AND a.wahlkreis = w.wahlkreisid""")
    data = cur.fetchall()
    result = 0.0
    for i in data:
        if (int(i[0]) == int(kreis)):
            result = i[2] * 100
    stringy = '<p> ' + str(float("{:.3f}".format(result))) + " %" + ' </p>'
    jsony = {"data": stringy}
    return json.dumps(jsony)


def query3_wahlbeteiligung(kreis):
    cur.execute("""select a.wahlkreis, w.wahlkreisname, (1.00*AnzahlWaehlende)/anzahlwahlberechtigte as wahlbeteiligung, wahljahr
        from wahlkreisaggretation as a, wahlkreis as w
        WHERE wahljahr = 2021 AND a.wahlkreis = w.wahlkreisid""")
    data = cur.fetchall()
    result = 0.0
    for i in data:
        if (int(i[0]) == int(kreis)):
            result = i[2] * 100
    stringy = '<p> ' + str(float("{:.3f}".format(result))) + " %" + ' </p>'
    jsony = {"data": stringy}
    return json.dumps(jsony)


def query5_table():
    cur.execute("""select bundesland, b.bundeslandname, p.kurzbezeichnung, direktmandate-sitzkontingente  as ueberhangsmandate
from vorlaufigesitzverteilungparteienprobundesland as v, bundesland as b, partei as p
where sitzkontingente < direktmandate
and b.bundeslandid = v.bundesland
and partei = p.parteiid
ORDER BY v.bundesland""")
    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Bundesland</th>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '<th>Überhangsmandate</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + \
            str(i[1]) + '</td><td>' + str(i[2]) + \
            '</td><td>' + str(i[3]) + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query3_direktkandidaten2017(kreis):
    cur.execute("""with erststimmensieger as (
  select we.wahlkreis, we.wahljahr, we.parteikurz as erststimmensieger, we.wahljahr
  from wahlkreisprozenterst we
  where we.wahljahr = 2017
  and not exists                        
          (select *                    
          from wahlkreisprozenterst we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2017
          and we2.prozenterststimmen > we.prozenterststimmen    
          )
)
select e.wahlkreis,wk.wahlkreisname, k.firstname, k.lastname, e.erststimmensieger, k.wahljahr
from erststimmensieger e, direktkandidaten dk, kandidaten k, partei p, wahlkreis wk
where e.erststimmensieger = p.KurzBezeichnung
and p.parteiid = k.partei
and wk.wahlkreisid = e.wahlkreis
and k.kandidatid = dk.kandidatid
and dk.wahlkreis = e.wahlkreis
and k.wahljahr = 2017""")
    data = cur.fetchall()
    stringy = ''
    for i in data:
        if (int(i[0]) == int(kreis)):
            stringy = '<p> ' + str(i[2]) + '   ' + str(i[3]) + \
                ',   ' + str(i[4]) + ' </p>'
    jsony = {"data": stringy}
    return json.dumps(jsony)


def query3_direktkandidaten(kreis):
    cur.execute("""with erststimmensieger as (
  select we.wahlkreis, we.wahljahr, we.parteikurz as erststimmensieger, we.wahljahr
  from wahlkreisprozenterst we
  where we.wahljahr = 2021
  and not exists                        
          (select *                    
          from wahlkreisprozenterst we2            
          where we.wahlkreis = we2.wahlkreis  
          and we2.wahljahr = 2021
          and we2.prozenterststimmen > we.prozenterststimmen    
          )
)
select e.wahlkreis,wk.wahlkreisname, k.firstname, k.lastname, e.erststimmensieger, k.wahljahr
from erststimmensieger e, direktkandidaten dk, kandidaten k, partei p, wahlkreis wk
where e.erststimmensieger = p.KurzBezeichnung
and p.parteiid = k.partei
and wk.wahlkreisid = e.wahlkreis
and k.kandidatid = dk.kandidatid
and dk.wahlkreis = e.wahlkreis
and k.wahljahr = 2021""")
    data = cur.fetchall()
    stringy = ''
    for i in data:
        if (int(i[0]) == int(kreis)):
            stringy = '<p> ' + str(i[2]) + '   ' + str(i[3]) + \
                ',   ' + str(i[4]) + ' </p>'
    jsony = {"data": stringy}
    return json.dumps(jsony)


def query3_stimmen_entwicklung(kreis):
    cur.execute("""with vorjahr as (
    select w.wahlkreis, pz.parteikurz, w.anzahlzweitstimmen, pz.prozentzweitstimmen
    from wahlkreisprozentzweit pz, wahlkreisstimmenaggregation w, partei p
    where pz.wahljahr = 2017
    and w.wahljahr = 2017
    and pz.wahlkreis = w.wahlkreis
    and w.partei = p.parteiid
    and p.KurzBezeichnung = pz.parteikurz
)
select w.wahlkreis, pz.parteikurz, w.anzahlzweitstimmen, pz.prozentzweitstimmen, w.anzahlzweitstimmen-v.anzahlzweitstimmen as stimmendifferenz, pz.prozentzweitstimmen-v.prozentzweitstimmen as prozentdifferenz
from wahlkreisprozentzweit pz, wahlkreisstimmenaggregation w, partei p, vorjahr v
where pz.wahljahr = 2021
and w.wahljahr = 2021
and pz.wahlkreis = w.wahlkreis
and w.partei = p.parteiid
and p.KurzBezeichnung = pz.parteikurz
and w.wahlkreis = v.wahlkreis
and p.KurzBezeichnung = v.parteikurz
order by pz.prozentzweitstimmen desc""")
    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Partei </th>'
    str_table = str_table + '<th>Stimmen (absolut) </th>'
    str_table = str_table + '<th>Stimmen (relativ) </th>'
    str_table = str_table + '<th>Differenz zu Vorwahl (absolut) </th>'
    str_table = str_table + '<th>Differenz zu Vorwahl (relativ)</th>'
    str_table = str_table + '</tr>'
    for i in data:
        if (int(i[0]) == int(kreis)):
            str_table = str_table + '<tr>'
            str_table = str_table + '<td>' + str(i[1]) + '</td><td>' + str(i[2]) + '</td><td>' + str(float("{:.3f}".format(
                i[3]))) + '%' + '</td><td>' + str(i[4]) + '</td><td>' + str(float("{:.3f}".format(i[5]))) + '%' + '</td>'
            str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query6_table_win2017():
    cur.execute("""with sieger as(
    select *
    from wahlkreisprozenterst w1
    where w1.wahljahr = 2017
    and not exists (select * from wahlkreisprozenterst w2 
                    where w2.wahljahr = 2017 
                    and w1.wahlkreis = w2.wahlkreis 
                    and w2.prozenterststimmen > w1.prozenterststimmen)
),
-- filtere zweite
wahlkreisprozenterst_ohne_sieger as(
    select * from wahlkreisprozenterst
    EXCEPT
    select * from sieger    
),
zweite_sieger as(
    select *
    from wahlkreisprozenterst_ohne_sieger w1
    where 
    w1.wahljahr = 2017
    and not exists (select * from wahlkreisprozenterst_ohne_sieger w2 
                    where w2.wahljahr = 2017 
                    and w1.wahlkreis = w2.wahlkreis 
                    and w2.prozenterststimmen > w1.prozenterststimmen)    
), 
--bilde differenz zwischen stimmen
differenz as (
  select s.wahljahr, s.wahlkreis, s.parteikurz, s.prozenterststimmen-zs.prozenterststimmen as differenz, ROW_NUMBER() OVER(PARTITION BY s.parteikurz ORDER BY s.prozenterststimmen-zs.prozenterststimmen ASC) AS row_number
  from sieger s, zweite_sieger zs
  where s.wahlkreis = zs.wahlkreis
)
-- waehle die 10 knappsten abstaende
select k.wahljahr, di.wahlkreis, wk.wahlkreisname, di.parteikurz, di.differenz, di.row_number, k.kandidatid, k.firstname, k.lastname
from differenz di, kandidaten k, direktkandidaten dk, partei p, wahlkreis as wk
where row_number <= 10
and di.parteikurz = p.KurzBezeichnung
and p.parteiid = k.partei
and k.wahljahr = 2017
and wk.wahlkreisid = di.wahlkreis
and k.kandidatid = dk.kandidatid
and di.wahlkreis = dk.wahlkreis""")
    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Wahlkreis</th>'
    str_table = str_table + '<th>Vorname</th>'
    str_table = str_table + '<th>Nachname</th>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '<th>Differenz</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + str(i[2]) + '</td><td>' + str(i[7]) + '</td><td>' + str(
            i[8]) + '</td><td>' + str(i[3]) + '</td><td>' + str(float("{:.3f}".format(i[4]))) + '%' + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query6_table_win():
    cur.execute("""with sieger as(
    select *
    from wahlkreisprozenterst w1
    where w1.wahljahr = 2021
    and not exists (select * from wahlkreisprozenterst w2 
                    where w2.wahljahr = 2021 
                    and w1.wahlkreis = w2.wahlkreis 
                    and w2.prozenterststimmen > w1.prozenterststimmen)
),
-- filtere zweite
wahlkreisprozenterst_ohne_sieger as(
    select * from wahlkreisprozenterst
    EXCEPT
    select * from sieger    
),
zweite_sieger as(
    select *
    from wahlkreisprozenterst_ohne_sieger w1
    where 
    w1.wahljahr = 2021
    and not exists (select * from wahlkreisprozenterst_ohne_sieger w2 
                    where w2.wahljahr = 2021 
                    and w1.wahlkreis = w2.wahlkreis 
                    and w2.prozenterststimmen > w1.prozenterststimmen)    
), 
--bilde differenz zwischen stimmen
differenz as (
  select s.wahljahr, s.wahlkreis, s.parteikurz, s.prozenterststimmen-zs.prozenterststimmen as differenz, ROW_NUMBER() OVER(PARTITION BY s.parteikurz ORDER BY s.prozenterststimmen-zs.prozenterststimmen ASC) AS row_number
  from sieger s, zweite_sieger zs
  where s.wahlkreis = zs.wahlkreis
)
-- waehle die 10 knappsten abstaende
select k.wahljahr, di.wahlkreis, wk.wahlkreisname, di.parteikurz, di.differenz, di.row_number, k.kandidatid, k.firstname, k.lastname
from differenz di, kandidaten k, direktkandidaten dk, partei p, wahlkreis as wk
where row_number <= 10
and di.parteikurz = p.KurzBezeichnung
and p.parteiid = k.partei
and k.wahljahr = 2021
and wk.wahlkreisid = di.wahlkreis
and k.kandidatid = dk.kandidatid
and di.wahlkreis = dk.wahlkreis""")
    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Wahlkreis</th>'
    str_table = str_table + '<th>Vorname</th>'
    str_table = str_table + '<th>Nachname</th>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '<th>Differenz</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + str(i[2]) + '</td><td>' + str(i[7]) + '</td><td>' + str(
            i[8]) + '</td><td>' + str(i[3]) + '</td><td>' + str(float("{:.3f}".format(i[4]))) + "%" + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query6_table_loser2017():
    cur.execute("""with sieger as(
    select *
    from wahlkreisprozenterst w1
    where w1.wahljahr = 2017
    and not exists (select * from wahlkreisprozenterst w2 
                    where w2.wahljahr = 2017 
                    and w1.wahlkreis = w2.wahlkreis 
                    and w2.prozenterststimmen > w1.prozenterststimmen)
),
-- suche fuer jede partei wahlkreis, in dem sie angetreten ist
angetreten_in as (select p.kurzbezeichnung as parteikurz, dk.wahlkreis
from direktkandidaten dk, kandidaten k, partei p
where dk.kandidatid = k.kandidatid
and k.partei = p.parteiid
and k.wahljahr = 2017
),
-- differenz zwischen gewinner und parteien
differenz as(
    select w.wahljahr, w.wahlkreis, w.parteikurz, s.prozenterststimmen-w.prozenterststimmen as differenz
    from wahlkreisprozenterst w, sieger s
    where w.wahljahr = 2017
    and s.wahljahr = 2017
    and w.parteikurz not in (select parteikurz from sieger) 
    and w.wahlkreis = s.wahlkreis
    and exists (select * from angetreten_in a where a.parteikurz = w.parteikurz and w.wahlkreis = a.wahlkreis)
),
-- suche fuer jede partei wahlkreis mit kleinster differenz
kleinste_differenz as (select d1.wahljahr, d1.parteikurz, d1.wahlkreis, d1.differenz
from differenz d1
where not exists (
    select *
    from differenz d2
    where d1.parteikurz = d2.parteikurz
    and d2.differenz < d1.differenz
     )
)
select k.wahljahr, kd.wahlkreis, wk.wahlkreisname, kd.parteikurz, kd.differenz, k.kandidatid, k.firstname, k.lastname
from kleinste_differenz kd, kandidaten k, direktkandidaten dk, partei p, wahlkreis as wk
where kd.parteikurz = p.KurzBezeichnung
and p.parteiid = k.partei
and k.wahljahr = 2017
and wk.wahlkreisid = kd.wahlkreis
and k.kandidatid = dk.kandidatid
and kd.wahlkreis = dk.wahlkreis""")
    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Wahlkreis</th>'
    str_table = str_table + '<th>Vorname</th>'
    str_table = str_table + '<th>Nachname</th>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '<th>Differenz</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + str(i[2]) + '</td><td>' + str(i[6]) + '</td><td>' + str(
            i[7]) + '</td><td>' + str(i[3]) + '</td><td>' + str(float("{:.3f}".format(i[4]))) + "%" + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query6_table_loser():
    cur.execute("""with sieger as(
    select *
    from wahlkreisprozenterst w1
    where w1.wahljahr = 2021
    and not exists (select * from wahlkreisprozenterst w2 
                    where w2.wahljahr = 2021 
                    and w1.wahlkreis = w2.wahlkreis 
                    and w2.prozenterststimmen > w1.prozenterststimmen)
),
-- suche fuer jede partei wahlkreis, in dem sie angetreten ist
angetreten_in as (select p.kurzbezeichnung as parteikurz, dk.wahlkreis
from direktkandidaten dk, kandidaten k, partei p
where dk.kandidatid = k.kandidatid
and k.partei = p.parteiid
and k.wahljahr = 2021
),
-- differenz zwischen gewinner und parteien
differenz as(
    select w.wahljahr, w.wahlkreis, w.parteikurz, s.prozenterststimmen-w.prozenterststimmen as differenz
    from wahlkreisprozenterst w, sieger s
    where w.wahljahr = 2021
    and s.wahljahr = 2021
    and w.parteikurz not in (select parteikurz from sieger) 
    and w.wahlkreis = s.wahlkreis
    and exists (select * from angetreten_in a where a.parteikurz = w.parteikurz and w.wahlkreis = a.wahlkreis)
),
-- suche fuer jede partei wahlkreis mit kleinster differenz
kleinste_differenz as (select d1.wahljahr, d1.parteikurz, d1.wahlkreis, d1.differenz
from differenz d1
where not exists (
    select *
    from differenz d2
    where d1.parteikurz = d2.parteikurz
    and d2.differenz < d1.differenz
     )
)
select k.wahljahr, kd.wahlkreis, wk.wahlkreisname, kd.parteikurz, kd.differenz, k.kandidatid, k.firstname, k.lastname
from kleinste_differenz kd, kandidaten k, direktkandidaten dk, partei p, wahlkreis as wk
where kd.parteikurz = p.KurzBezeichnung
and p.parteiid = k.partei
and k.wahljahr = 2021
and wk.wahlkreisid = kd.wahlkreis
and k.kandidatid = dk.kandidatid
and kd.wahlkreis = dk.wahlkreis""")
    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Wahlkreis</th>'
    str_table = str_table + '<th>Vorname</th>'
    str_table = str_table + '<th>Nachname</th>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '<th>Differenz</th>'
    str_table = str_table + '</tr>'
    for i in data:
        str_table = str_table + '<tr>'
        str_table = str_table + '<td>' + str(i[2]) + '</td><td>' + str(i[6]) + '</td><td>' + str(
            i[7]) + '</td><td>' + str(i[3]) + '</td><td>' + str(float("{:.3f}".format(i[4]))) + "%" + '</td>'
        str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query7_wahlbeteiligung(kreis):
    cur.execute("""with anzahlwahlberechtigte as (select anzahlwahlberechtigte, wahlkreis from wahlkreisaggretation where wahljahr = 2021 and wahlkreis = {}),
wahlende as 
    (select count(*) as wahlende
    from anzahlwahlberechtigte a, zweitstimmen zw
    where zw.wahlkreis = {})
select wahlkreis, (1.0*wahlende)/anzahlwahlberechtigte as wahlbeteiligung
from anzahlwahlberechtigte, wahlende""".format(kreis, kreis))
    data = cur.fetchall()
    result = 0.0
    for i in data:
        if (int(i[0]) == int(kreis)):
            result = i[1]*100
    stringy = '<p> ' + str(float("{:.3f}".format(result))) + " %" + ' </p>'
    jsony = {"data": stringy}
    return json.dumps(jsony)


def query7_direktkandidaten(kreis):
    cur.execute("""with stimmen_pro_partei as (
  select partei, count(*) as stimmen
  from erststimmen
  where wahlkreis = {}
  group by partei
)
select dk.wahlkreis, k.kandidatid, k.firstname, k.lastname, s.partei, k.wahljahr, p.kurzbezeichnung
from stimmen_pro_partei s, direktkandidaten dk, kandidaten k, partei p
where stimmen = (select max(stimmen) from stimmen_pro_partei)
and s.partei = k.partei
and k.wahljahr= 2021
and k.kandidatid = dk.kandidatid
and p.parteiid = s.partei
and dk.wahlkreis = {}""".format(kreis, kreis))
    data = cur.fetchall()
    stringy = ''
    for i in data:
        if (int(i[0]) == int(kreis)):
            stringy = '<p> ' + str(i[2]) + '   ' + str(i[3]) + \
                ',   ' + str(i[6]) + ' </p>'
    jsony = {"data": stringy}
    return json.dumps(jsony)


def query7_stimmen_entwicklung(kreis):
    cur.execute("""with stimmen_gesamt as(
    select count(*) - (select count(*) from zweitstimmen where wahlkreis = {} and partei = -1)  as stimmen_gesamt
    from zweitstimmen
    where wahlkreis = {}
),
    stimmen_pro_partei as(
    select partei, count(*) as stimmen_pro_partei
    from zweitstimmen
    where wahlkreis = {}
    group by partei
)
select {} as wahlkreis, wk.wahlkreisname, p.kurzbezeichnung, partei, stimmen_pro_partei, (1.00*stimmen_pro_partei)/stimmen_gesamt as stimmen_prozentual
from stimmen_pro_partei, stimmen_gesamt, partei p, wahlkreis wk
WHERE partei = p.parteiid
and wk.wahlkreisid = {}
and p.parteiid != -1
order by stimmen_prozentual desc""".format(kreis, kreis, kreis, kreis, kreis))
    data = cur.fetchall()
    str_table = '<table>'
    str_table = str_table + '<tr>'
    str_table = str_table + '<th>Partei</th>'
    str_table = str_table + '<th>Stimmen (absolut)</th>'
    str_table = str_table + '<th>Stimmen (relativ)</th>'
    str_table = str_table + '</tr>'
    for i in data:
        if (int(i[0]) == int(kreis)):
            str_table = str_table + '<tr>'
            str_table = str_table + '<td>' + str(i[2]) + '</td><td>' + str(
                i[4]) + '</td><td>' + str(float("{:.3f}".format(i[5]*100))) + '%' + '</td>'
            str_table = str_table + '</tr>'
    str_table = str_table + ' </table>'
    jsony = {"data": str_table}
    return json.dumps(jsony)


def query8_rich():
    cur.execute("""with ten_richest as (SELECT s.wahlkreis, w.wahlkreisname, s.einkommenprivatehaushalte as ein FROM strukturdaten s,
    wahlkreis w where w.wahlkreisid = s.wahlkreis
    ORDER BY ein DESC
    LIMIT 10),
    ten_poorest as (SELECT s.wahlkreis, w.wahlkreisname, s.einkommenprivatehaushalte as ein FROM strukturdaten s, wahlkreis w 
    where w.wahlkreisid = s.wahlkreis
    ORDER BY ein ASC
    LIMIT 10),

    -- CDU/CSU Union average richest
    cdu_csu_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
                            GROUP BY parteikurz),
    -- SPD average richest
    spd_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'SPD') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- fdp average richest
    fdp_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'FDP') AND wahljahr = 2021
                        GROUP BY parteikurz),
	-- Die Linke
    linke_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'DIE LINKE') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- grüne average richest
    grune_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- AfD average richest
    afd_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'AfD') AND wahljahr = 2021
                        GROUP BY parteikurz),
	-- SSW
	ssw_average_rich as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_richest)
    AND (parteikurz = 'SSW') AND wahljahr = 2021
                        GROUP BY parteikurz),

                        
    rich_total as (					  
    SELECT parteikurz, avg, 'rich' as category FROM cdu_csu_average_rich UNION 
    SELECT parteikurz, avg, 'rich' as category FROM spd_average_rich UNION
    SELECT parteikurz, avg, 'rich' as category FROM fdp_average_rich UNION
    SELECT parteikurz, avg, 'rich' as category FROM grune_average_rich UNION
    SELECT parteikurz, avg, 'rich' as category FROM afd_average_rich UNION
	SELECT parteikurz, avg, 'rich' as category FROM linke_average_rich UNION
	SELECT parteikurz, avg, 'rich' as category FROM ssw_average_rich)

    SELECT * FROM rich_total ORDER BY parteikurz""")

    mobile_records = cur.fetchall()
    party = []
    results = []
    total = 0
    for i in mobile_records:
        party.append(i[0])
        results.append(int(i[1]))
        total += int(i[1])
    jso = dict(zip(party, results))
    return json.dumps(jso)


def query8_poor():

    cur.execute("""with ten_richest as (SELECT s.wahlkreis, w.wahlkreisname, s.einkommenprivatehaushalte as ein FROM strukturdaten s,
    wahlkreis w where w.wahlkreisid = s.wahlkreis
    ORDER BY ein DESC
    LIMIT 10),
    ten_poorest as (SELECT s.wahlkreis, w.wahlkreisname, s.einkommenprivatehaushalte as ein FROM strukturdaten s,
    wahlkreis w where w.wahlkreisid = s.wahlkreis
    ORDER BY ein ASC
    LIMIT 10),
    cdu_csu_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
                            GROUP BY parteikurz),
    -- SPD average poorest
    spd_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'SPD') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- fdp average poorest
    fdp_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'FDP') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- grüne average poorest
    grune_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
                        GROUP BY parteikurz),
    -- AfD average poorest
    afd_average_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'AfD') AND wahljahr = 2021
                        GROUP BY parteikurz),
	-- Die Linke
	linke_avg_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'DIE LINKE') AND wahljahr = 2021
                        GROUP BY parteikurz),
	-- SSW
	ssw_avg_poor as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
    WHERE WahlKreis IN
    (SELECT wahlkreis FROM ten_poorest)
    AND (parteikurz = 'SSW') AND wahljahr = 2021
                        GROUP BY parteikurz),
                        
    poor_total as (
    SELECT parteikurz, avg, 'poor' as category FROM cdu_csu_average_poor UNION 
    SELECT parteikurz, avg, 'poor' as category FROM spd_average_poor UNION
    SELECT parteikurz, avg, 'poor' as category FROM fdp_average_poor UNION
    SELECT parteikurz, avg, 'poor' as category FROM grune_average_poor UNION
    SELECT parteikurz, avg, 'poor' as category FROM afd_average_poor UNION
	SELECT parteikurz, avg, 'poor' as category FROM linke_avg_poor UNION
	SELECT parteikurz, avg, 'poor' as category FROM ssw_avg_poor)
    
    SELECT * FROM poor_total ORDER BY parteikurz""")

    mobile_records = cur.fetchall()
    party = []
    results = []
    total = 0
    for i in mobile_records:
        party.append(i[0])
        results.append(int(i[1]))
        total += i[1]
    jso = dict(zip(party, results))
    return json.dumps(jso)


def query9_high():
    cur.execute("""with ten_most_educated as (SELECT s.wahlkreis, w.wahlkreisname, s.bildung as ein FROM strukturdaten s,
    wahlkreis w where w.wahlkreisid = s.wahlkreis
ORDER BY ein DESC
LIMIT 10),
ten_least_educated as (SELECT s.wahlkreis, w.wahlkreisname, s.bildung as ein FROM strukturdaten s,
    wahlkreis w where w.wahlkreisid = s.wahlkreis
ORDER BY ein ASC
LIMIT 10),

-- CDU/CSU Union average most_educated
cdu_csu_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
						GROUP BY parteikurz),
-- SPD average most_educated
spd_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'SPD') AND wahljahr = 2021
					GROUP BY parteikurz),
-- fdp average most_educated
fdp_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'FDP') AND wahljahr = 2021
					GROUP BY parteikurz),
-- grüne average most_educated
grune_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
					  GROUP BY parteikurz),
-- AfD average most_educated
afd_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'AfD') AND wahljahr = 2021
					GROUP BY parteikurz),
linke_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'DIE LINKE') AND wahljahr = 2021
					GROUP BY parteikurz),					
ssw_average_most_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_most_educated)
AND (parteikurz = 'SSW') AND wahljahr = 2021
					GROUP BY parteikurz),
					  
most_educated_total as (
SELECT parteikurz, avg, 'high' as category FROM afd_average_most_educated UNION 					  
SELECT parteikurz, avg, 'high' as category FROM cdu_csu_average_most_educated UNION 
SELECT parteikurz, avg, 'high' as category FROM spd_average_most_educated UNION
SELECT parteikurz, avg, 'high' as category FROM fdp_average_most_educated UNION
SELECT parteikurz, avg, 'high' as category FROM grune_average_most_educated UNION
SELECT parteikurz, avg, 'high' as category FROM grune_average_most_educated UNION
SELECT parteikurz, avg, 'high' as category FROM linke_average_most_educated UNION
SELECT parteikurz, avg, 'high' as category FROM ssw_average_most_educated)


SELECT * FROM most_educated_total ORDER BY parteikurz""")

    mobile_records = cur.fetchall()
    party = []
    results = []
    total = 0
    for i in mobile_records:
        party.append(i[0])
        results.append(int(i[1]))
        total += i[1]
    jso = dict(zip(party, results))
    return json.dumps(jso)


def query9_low():
    cur.execute("""with ten_most_educated as (SELECT s.wahlkreis, w.wahlkreisname, s.bildung as ein FROM strukturdaten s,
    wahlkreis w where w.wahlkreisid = s.wahlkreis
ORDER BY ein DESC
LIMIT 10),
ten_least_educated as (SELECT s.wahlkreis, w.wahlkreisname, s.bildung as ein FROM strukturdaten s,
    wahlkreis w where w.wahlkreisid = s.wahlkreis
ORDER BY ein ASC
LIMIT 10),
cdu_csu_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'CDU' OR parteikurz = 'CSU') AND wahljahr = 2021
						GROUP BY parteikurz),
-- SPD average least educated
spd_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'SPD') AND wahljahr = 2021
					GROUP BY parteikurz),
-- fdp average least educated
fdp_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'FDP') AND wahljahr = 2021
					GROUP BY parteikurz),
-- grüne average least educated
grune_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'GRÜNE') AND wahljahr = 2021
					  GROUP BY parteikurz),
-- AfD average least educated
afd_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'AfD') AND wahljahr = 2021
					  GROUP BY parteikurz),
linke_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'DIE LINKE') AND wahljahr = 2021
					  GROUP BY parteikurz),
ssw_average_least_educated as (SELECT parteikurz, avg(prozentzweitstimmen) FROM WahlKreisProzentZweit
WHERE WahlKreis IN
(SELECT wahlkreis FROM ten_least_educated)
AND (parteikurz = 'SSW') AND wahljahr = 2021
					  GROUP BY parteikurz),
					  
least_educated_total as (
SELECT parteikurz, avg, 'low' as category FROM cdu_csu_average_least_educated UNION 
SELECT parteikurz, avg, 'low' as category FROM spd_average_least_educated UNION
SELECT parteikurz, avg, 'low' as category FROM fdp_average_least_educated UNION
SELECT parteikurz, avg, 'low' as category FROM grune_average_least_educated UNION
SELECT parteikurz, avg, 'low' as category FROM linke_average_least_educated UNION	
SELECT parteikurz, avg, 'low' as category FROM ssw_average_least_educated UNION
SELECT parteikurz, avg, 'low' as category FROM afd_average_least_educated)


SELECT * FROM least_educated_total ORDER BY parteikurz""")
    mobile_records = cur.fetchall()
    party = []
    results = []
    total = 0
    for i in mobile_records:
        party.append(i[0])
        results.append(int(i[1]))
        total += i[1]
    jso = dict(zip(party, results))
    return json.dumps(jso)


# Output: list of tuples inlcuding strings (firstname, lastname, job, parteikurz, parteilang)
# if candidate does not have a party parteikurz and parteilang are None
def erststimmen_data(wahlkreisid):
    dirketkandidaten_query = """
    select k.firstname, k.lastname, k.beruf, p.kurzbezeichnung, p.bezeichnung
    from direktkandidaten dk, kandidaten k 
    left outer join partei p on k.partei = p.parteiid
    where k.wahljahr = 2021
    and dk.wahlkreis = {}
    and dk.kandidatid = k.kandidatid
    """.format(wahlkreisid)
    cur.execute(dirketkandidaten_query)
    direktkandidaten = cur.fetchall()
    return direktkandidaten


# Output:list of lists containing parteiid, parteikurz, parteilang, list of tuples containg names of first five list candidates
def zweitstimmen_data(wahlkreisid):
    angetretene_parteien_query = """
    select distinct p.parteiid, p.kurzbezeichnung, p.bezeichnung
    from listenkandidaten lk, kandidaten k, partei p, wahlkreis w
    where k.wahljahr = 2021
    and w.wahlkreisid = {}
    and w.bundesland = lk.bundesland
    and lk.kandidatid = k.kandidatid
    and k.partei = p.parteiid
    order by p.parteiid asc
    """.format(wahlkreisid)
    cur.execute(angetretene_parteien_query)
    angetretene_parteien = cur.fetchall()

    parteienliste = []
    for partei in angetretene_parteien:
        p = list(partei)
        parteiid = p[0]
        listenkandidaten_query = """
        select concat_ws(' ', k.firstname, k.lastname) as kandidaten
        from listenkandidaten lk, kandidaten k, wahlkreis w
        where k.wahljahr = 2021
        and w.wahlkreisid = {}
        and w.bundesland = lk.bundesland
        and lk.kandidatid = k.kandidatid
        and k.partei = {}
        order by lk.listenplatz asc
        limit 5
        """.format(wahlkreisid, parteiid)
        cur.execute(listenkandidaten_query)
        listenkandidaten = cur.fetchall()
        p.append(listenkandidaten)
        parteienliste.append(p)

    return parteienliste
