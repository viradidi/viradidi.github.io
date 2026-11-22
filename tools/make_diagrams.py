#!/usr/bin/env python3
"""Generates fallback architecture diagrams from each repository's documented components.
They use the same filenames as the originals, so copying the originals over them replaces them."""
import html, os
OUT=os.path.join(os.path.dirname(__file__),'..','assets','architecture')
COL={'src':('#e8f1ff','#3973ac'),'ing':('#fff0d9','#c27b22'),'sto':('#e1f5e8','#37885a'),'prc':('#eee5ff','#8055bd'),'srv':('#ffe8ec','#b8435a'),'ctl':('#f2f2f4','#86868b')}
def esc(s): return html.escape(s)
def diagram(fn,title,lanes,notes,flow=None):
    # lanes: list of (lane title, [(label,kind)...])
    cw,ch,gx,gy,pad,top=190,54,44,18,30,86
    n=len(lanes); maxr=max(len(l[1]) for l in lanes)
    W=pad*2+n*cw+(n-1)*gx; H=top+maxr*(ch+gy)+84
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">',
    f'<title id="t">{esc(title)}</title><desc id="d">{esc(notes)}</desc>',
    '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#6e6e73"/></marker></defs>',
    f'<rect width="{W}" height="{H}" fill="#fff"/>',
    f'<text x="{pad}" y="34" font-family="Helvetica,Arial,sans-serif" font-size="20" font-weight="700" fill="#1d1d1f">{esc(title)}</text>',
    f'<text x="{pad}" y="56" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="#6e6e73">Diagram generated from the repository README components. Replace with the original file when available.</text>']
    pos={}
    for i,(lt,items) in enumerate(lanes):
        x=pad+i*(cw+gx)
        s.append(f'<text x="{x}" y="{top-8}" font-family="Helvetica,Arial,sans-serif" font-size="13" font-weight="600" fill="#424245">{esc(lt)}</text>')
        s.append(f'<line x1="{x}" y1="{top-2}" x2="{x+cw}" y2="{top-2}" stroke="#d2d2d7"/>')
        for j,(lab,k) in enumerate(items):
            y=top+8+j*(ch+gy); f,st=COL[k]
            s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="8" fill="{f}" stroke="{st}" stroke-width="1.5"/>')
            words=lab.split(' '); lines=[];cur=''
            for w in words:
                if len(cur+' '+w)>24 and cur: lines.append(cur);cur=w
                else: cur=(cur+' '+w).strip()
            lines.append(cur)
            y0=y+ch/2-(len(lines)-1)*8+4
            for q,l in enumerate(lines):
                s.append(f'<text x="{x+cw/2}" y="{y0+q*16}" text-anchor="middle" font-family="Helvetica,Arial,sans-serif" font-size="13" fill="#1d1d1f">{esc(l)}</text>')
            pos[lab]=(x,y)
    # lane-to-lane arrows (middle of lane to middle of next)
    for i in range(n-1):
        a=lanes[i][1]; b=lanes[i+1][1]
        ya=top+8+(len(a)*(ch+gy)-gy)/2; yb=top+8+(len(b)*(ch+gy)-gy)/2
        x1=pad+i*(cw+gx)+cw; x2=x1+gx
        s.append(f'<path d="M{x1} {ya} C{x1+gx/2} {ya} {x1+gx/2} {yb} {x2-2} {yb}" fill="none" stroke="#6e6e73" stroke-width="1.6" marker-end="url(#a)"/>')
    s.append(f'<text x="{pad}" y="{H-24}" font-family="Helvetica,Arial,sans-serif" font-size="12" fill="#6e6e73">{esc(notes)}</text></svg>')
    open(os.path.join(OUT,fn),'w',encoding='utf-8').write('\n'.join(s))

D=diagram
D('uber-eats-architecture.svg','Uber Eats: multi-source Azure batch platform',[
 ('Source systems',[('REST API (FastAPI)','src'),('CSV files','src'),('SQL database','src')]),
 ('Orchestration',[('ADF API pipeline','ing'),('ADF CSV pipeline','ing'),('ADF SQL incremental pipeline','ing'),('Metadata and control config','ctl')]),
 ('Storage',[('ADLS Gen2 landing (Bronze)','sto'),('Azure Key Vault (secrets)','ctl')]),
 ('Processing',[('Azure Databricks','prc'),('Silver notebooks (PySpark)','prc')]),
 ('Serving boundary',[('Silver tables','sto')])],
 'The implemented serving boundary is Silver. No Gold or reporting layer is shown or claimed.')
D('novacart-overview.svg','NovaCart: incremental retail lakehouse, overview',[
 ('Source',[('Azure SQL retail source','src')]),
 ('Access',[('Lakehouse Federation (Unity Catalog)','ing')]),
 ('Bronze',[('Raw change-aware ingest (Delta)','sto')]),
 ('Silver',[('Cleaned entities (Delta MERGE)','prc')]),
 ('Gold',[('Dimensions incl. SCD Type 2','srv'),('Facts and analytical models','srv')])],
 'Orchestrated as a Databricks Jobs workflow, with a processing-state control table.')
D('novacart-detailed.svg','NovaCart: incremental processing detail',[
 ('Control',[('Control table (watermarks)','ctl'),('Run state and status','ctl')]),
 ('Extract',[('Read watermark','ing'),('Query changed rows (timestamp or key)','src')]),
 ('Bronze',[('Append changed rows (Delta)','sto')]),
 ('Silver',[('Deduplicate and validate','prc'),('Delta MERGE upsert','prc')]),
 ('Gold',[('SCD Type 2 dimension MERGE','srv'),('Fact and analytical tables','srv')]),
 ('Commit',[('Advance watermark on success','ctl')])],
 'Watermarks advance only after the downstream steps succeed, so a failed run can be repeated.')
D('healthgrid-architecture-overview.svg','HealthGrid: metadata-driven Azure platform',[
 ('Sources',[('Five configured sources (synthetic)','src')]),
 ('Control plane',[('Azure SQL metadata and audit tables','ctl'),('FULL, APPEND or MERGE load type','ctl')]),
 ('Orchestration',[('Azure Data Factory pipelines','ing')]),
 ('Landing',[('ADLS Gen2 landing and file manifest','sto')]),
 ('Databricks',[('Bronze (raw, audited)','prc'),('Silver (standardised, validated)','prc'),('Gold (analytical)','srv')])],
 'Timestamp watermarks are not source CDC. Dataset is synthetic. Not a live clinical system.')
D('flowbridge-technical-architecture.svg','FlowBridge: event-driven supply chain on Snowflake',[
 ('Source',[('Azure Blob Storage','src'),('Event notifications','src')]),
 ('Ingest',[('Snowpipe auto-ingest','ing')]),
 ('Bronze',[('Raw tables and Streams','sto')]),
 ('Process',[('Tasks and stored procedures','prc'),('Validation and error handling','prc')]),
 ('Silver / Gold',[('Silver clean tables','prc'),('Gold dimensional model, Dynamic Tables','srv')]),
 ('Serve',[('Secure views and RBAC','ctl'),('Streamlit dashboard','srv')])],
 'Implemented in SQL on Snowflake. dbt is not part of this implementation.')
D('atlasflow-architecture.svg','AtlasFlow: real-time logistics control tower',[
 ('Source',[('PostgreSQL (logical replication)','src')]),
 ('Capture',[('Debezium CDC','ing')]),
 ('Transport',[('Apache Kafka topics','ing')]),
 ('Stream processing',[('Flink SQL: Bronze','prc'),('Flink SQL: Silver','prc'),('Flink SQL: Gold','prc')]),
 ('Storage',[('Apache Iceberg tables','sto')]),
 ('Serve',[('Trino','srv'),('Apache Superset','srv')])],
 'Runs locally with Docker Compose on synthetic data. Not a hosted production service.')
D('cfpb-consumer-complaint-analytics.svg','CFPB Consumer Complaint Analytics: Microsoft Fabric',[
 ('Source',[('Kaggle API','src')]),
 ('Ingestion',[('Fabric ingestion pipeline','ing')]),
 ('Bronze',[('Raw CSV in Lakehouse','sto')]),
 ('Silver',[('PySpark profiling, validation, cleaning','prc'),('Silver: cleaned complaints','sto'),('Quarantine for investigation','ctl')]),
 ('Gold',[('SQL stored procedure','prc'),('Fact and dimension tables (Warehouse)','srv')]),
 ('Reporting',[('Semantic model and DAX','srv'),('Power BI report','srv')]),
 ('Delivery',[('End-to-end pipeline orchestration','ing'),('Deployment pipelines DEV to PROD','ing')])],
 'Silver 896,931 + quarantine 7,052 = 903,983 source records. Promotion is manual, not Git-triggered CI/CD.')
