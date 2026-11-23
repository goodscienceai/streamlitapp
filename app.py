import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title='Metadata Studio', page_icon='◈', layout='wide', initial_sidebar_state='collapsed')

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
:root {--ink:#151515;--muted:#66645f;--paper:#faf9f6;--surface:#fff;--line:#e6e3df;--soft:#f0eeeb;}
html,body,[class*="css"],[data-testid="stApp"] {font-family:'DM Sans',Arial,sans-serif!important;color:var(--ink)!important;}
.stApp,[data-testid="stAppViewContainer"] {background:var(--paper)!important;}
.block-container {max-width:1660px;padding-top:1.2rem;padding-bottom:3rem;}
section[data-testid="stSidebar"] {background:#f7f6f3!important;border-right:1px solid var(--line)!important;}
h1,h2,h3 {font-family:'DM Sans',Arial,sans-serif!important;letter-spacing:-.052em!important;color:#111!important;}
h1 {font-size:3rem!important;font-weight:800!important;line-height:1.1!important;margin-top:1.5rem!important;}
h3 {font-size:1.3rem!important;font-weight:750!important;}
p,label {color:#302f2c;}
[data-testid="stCaptionContainer"],.small {color:var(--muted)!important;}
.stButton>button {border:1px solid #dedbd7!important;border-radius:13px!important;background:#fff!important;color:#1a1a1a!important;font-weight:650!important;box-shadow:none!important;min-height:43px;}
.stButton>button:hover {background:#f0eeeb!important;border-color:#a7a39d!important;}
.stButton>button[kind="primary"] {background:#171717!important;border-color:#171717!important;color:#fff!important;}
.stButton>button[kind="primary"]:hover {background:#383838!important;}
[data-testid="stVerticalBlockBorderWrapper"] {border:1px solid var(--line)!important;border-radius:17px!important;background:#fff!important;box-shadow:none!important;}
.stTabs [data-baseweb="tab-list"] {gap:20px;border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"] {color:#5b5955!important;font-weight:650!important;border-radius:12px 12px 0 0!important;}
.stTabs [aria-selected="true"] {color:#111!important;}
.stTabs [data-baseweb="tab-highlight"] {background:#171717!important;height:2px!important;}
[data-baseweb="input"],[data-baseweb="select"],textarea {border-radius:12px!important;border-color:#dcd9d4!important;background:#fff!important;}
[data-testid="stDataFrame"] {border:1px solid var(--line);border-radius:12px;overflow:hidden;}
hr {border-color:var(--line)!important;}
.chip {display:inline-block;background:#eeece8;color:#292824;border:1px solid #e6e3de;border-radius:999px;padding:5px 12px;font-size:12px;font-weight:650;}
.node {border:1px solid #dcd9d4;border-radius:14px;overflow:hidden;background:#fff;min-height:260px;}
.node-head {background:#f0eeeb;padding:15px;font-weight:750;border-bottom:1px solid #e6e3df;}
.node-row {padding:11px 13px;border-bottom:1px solid #f0eeeb;font-size:13px;}
.mapping-arrow {text-align:center;font-size:27px;margin-top:125px;color:#262626;}
.brandbar {display:flex;align-items:center;gap:13px;border-bottom:1px solid var(--line);padding:8px 0 20px;font-size:22px;font-weight:800;letter-spacing:-.04em;}
.brandmark {font-size:25px;border:2px solid #111;border-radius:9px;padding:1px 7px;}
[data-testid="stRadio"] [role="radiogroup"] {gap:12px;}
[data-testid="stRadio"] [role="radiogroup"] label {border-radius:100px;padding:5px 12px;background:#f0eeeb;}
</style>''', unsafe_allow_html=True)

DEFAULT = [
 {'name':'Customer','domain':'Finance','status':'Completed','owner':'A. Sharma','version':'2.1','description':'Business model for customer identity, contact and KYC details.','updated':'23 Nov 2026, 14:20','attributes':[('Customer ID','String','CUSTOMER_ID','VARCHAR(64)'),('Customer Name','String','CUST_NAME','VARCHAR(200)'),('Customer Type','String','CUST_TYPE_CD','VARCHAR(30)'),('Address','String','ADDRESS_LINE1','VARCHAR(255)'),('Date of Birth','Date','DATE_OF_BIRTH','DATE')]},
 {'name':'Account','domain':'Finance','status':'In Progress','owner':'M. Kulkarni','version':'1.4','description':'Account identifiers, types and balances.','updated':'23 Nov 2026, 11:05','attributes':[('Account ID','String','ACCOUNT_ID','VARCHAR(64)'),('Account Type','String','ACCOUNT_TYPE_CD','VARCHAR(30)'),('Balance','Decimal','BALANCE_AMT','DECIMAL(18,2)')]},
 {'name':'Transaction','domain':'Payments','status':'Completed','owner':'R. Iyer','version':'1.2','description':'Payment transaction metadata.','updated':'22 Nov 2026, 18:32','attributes':[('Transaction ID','String','TRANSACTION_ID','VARCHAR(64)'),('Amount','Decimal','AMOUNT','DECIMAL(18,2)'),('Transaction Date','Date','TRANSACTION_DT','DATE')]},
 {'name':'Product','domain':'Reference','status':'Completed','owner':'S. Desai','version':'1.0','description':'Reference product catalog.','updated':'21 Nov 2026, 16:10','attributes':[('Product ID','String','PRODUCT_ID','VARCHAR(64)'),('Product Name','String','PRODUCT_NAME','VARCHAR(200)')]},
 {'name':'Party','domain':'Finance','status':'Failed','owner':'P. Verma','version':'0.9','description':'Party and legal entity metadata.','updated':'21 Nov 2026, 09:47','attributes':[('Party ID','String','PARTY_ID','VARCHAR(64)'),('Party Name','String','PARTY_NAME','VARCHAR(200)')]},
]
if 'models' not in st.session_state: st.session_state.models=DEFAULT
if 'selected' not in st.session_state: st.session_state.selected='Customer'
if 'history' not in st.session_state: st.session_state.history=[]

st.markdown('<div class="brandbar"><span class="brandmark">⬡</span> Metadata Studio</div>', unsafe_allow_html=True)
section=st.radio('Workspace',['Models','Conversions','Settings'],horizontal=True,label_visibility='collapsed')

st.title('Data Models' if section=='Models' else section)
st.caption('Manage business and physical data models and run BDM to PDM conversions.')

if section=='Settings':
 st.subheader('Workspace settings')
 st.text_input('Environment',value='Development',disabled=True)
 st.info('Demo application: changes are stored in Streamlit session state only. Connect a database for persistence.')
 st.stop()

if section=='Conversions':
 st.subheader('Conversion history')
 if st.session_state.history: st.dataframe(pd.DataFrame(st.session_state.history),use_container_width=True,hide_index=True)
 else: st.info('No conversions have been run in this session.')
 st.stop()

tab_bdm,tab_pdm,tab_conv=st.tabs(['BDM Models','PDM Models','Conversions'])
with tab_bdm:
 toolbar=st.columns([3,1.5,1.5,1.5])
 with toolbar[0]: query=st.text_input('Search models',placeholder='Search models...',label_visibility='collapsed')
 with toolbar[1]: domain=st.selectbox('Domain',['All']+sorted({m['domain'] for m in st.session_state.models}),label_visibility='collapsed')
 with toolbar[2]: status=st.selectbox('Status',['All','Completed','In Progress','Failed'],label_visibility='collapsed')
 with toolbar[3]:
  with st.popover('＋ New Model',use_container_width=True):
   with st.form('new_model'):
    new_name=st.text_input('Model name')
    new_domain=st.text_input('Domain',value='Finance')
    new_owner=st.text_input('Owner')
    if st.form_submit_button('Create',type='primary'):
     if new_name.strip() and not any(m['name']==new_name.strip() for m in st.session_state.models):
      st.session_state.models.append({'name':new_name.strip(),'domain':new_domain,'status':'In Progress','owner':new_owner,'version':'1.0','description':'','updated':datetime.now().strftime('%d %b %Y, %H:%M'),'attributes':[]})
      st.session_state.selected=new_name.strip();st.rerun()
     else: st.error('Enter a unique model name.')

 filtered=[m for m in st.session_state.models if query.lower() in m['name'].lower() and (domain=='All' or m['domain']==domain) and (status=='All' or m['status']==status)]
 left,center,right=st.columns([1.05,2.2,1.65],gap='small')
 with left:
  with st.container(border=True):
   st.markdown('**Model** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Status**')
   st.divider()
   for m in filtered:
    prefix='● ' if m['name']==st.session_state.selected else '◇ '
    if st.button(f"{prefix}{m['name']}  ·  {m['status']}",key='model_'+m['name'],use_container_width=True):
     st.session_state.selected=m['name'];st.rerun()
   if not filtered: st.caption('No models match the filters.')
 selected=next((m for m in st.session_state.models if m['name']==st.session_state.selected),st.session_state.models[0])
 with center:
  with st.container(border=True):
   st.markdown(f"**↔ BDM → PDM ({selected['name']})**")
   st.caption('Visual attribute mapping')
   a,b,c=st.columns([1,0.18,1],gap='small')
   with a:
    rows=''.join(f'<div class="node-row">{x[0]}</div>' for x in selected['attributes']) or '<div class="node-row">No attributes</div>'
    st.markdown(f'<div class="node"><div class="node-head">◇ BDM · {selected["name"]}</div>{rows}</div>',unsafe_allow_html=True)
   with b: st.markdown('<div class="mapping-arrow">→</div>',unsafe_allow_html=True)
   with c:
    rows=''.join(f'<div class="node-row">{x[2]}</div>' for x in selected['attributes']) or '<div class="node-row">Not generated</div>'
    st.markdown(f'<div class="node"><div class="node-head">▤ PDM · DIM_{selected["name"].upper()}</div>{rows}</div>',unsafe_allow_html=True)
   st.caption('Illustrative mapping preview; conversion rules can be integrated with your agents.')
 with right:
  with st.container(border=True):
   st.markdown(f"### {selected['name']}")
   st.markdown(f"<span class='chip'>{selected['status']}</span> &nbsp; <span class='small'>BDM Model</span>",unsafe_allow_html=True)
   details,attrs,mapping=st.tabs(['Details','Attributes','Mapping'])
   with details:
    with st.form('details_'+selected['name']):
     name=st.text_input('Model Name',value=selected['name'])
     dom=st.text_input('Domain',value=selected['domain'])
     desc=st.text_area('Description',value=selected['description'],height=90)
     owner=st.text_input('Owner',value=selected['owner'])
     st.caption(f"Version: v{selected['version']}  ·  Updated: {selected['updated']}")
     if st.form_submit_button('Save Changes',type='primary'):
      if name.strip() and (name==selected['name'] or not any(m['name']==name for m in st.session_state.models)):
       selected.update(name=name.strip(),domain=dom,description=desc,owner=owner,updated=datetime.now().strftime('%d %b %Y, %H:%M'))
       st.session_state.selected=name.strip();st.rerun()
      else: st.error('Model name must be unique and nonempty.')
   with attrs:
    df=pd.DataFrame(selected['attributes'],columns=['BDM Attribute','Business Type','PDM Column','Physical Type'])
    edited=st.data_editor(df,num_rows='dynamic',hide_index=True,use_container_width=True,key='attrs_'+selected['name'])
    if st.button('Save Attributes',key='saveattrs_'+selected['name']):
     selected['attributes']=[tuple('' if pd.isna(v) else str(v) for v in row) for row in edited.itertuples(index=False,name=None)]
     selected['updated']=datetime.now().strftime('%d %b %Y, %H:%M');st.rerun()
   with mapping:
    st.caption('Business to physical attribute mapping')
    if selected['attributes']:
     for source,typ,target,physical in selected['attributes']: st.markdown(f'`{source}` → `{target}`  ·  {physical}')
    else: st.caption('Add attributes to create mappings.')
   if st.button('▶ Convert to PDM',type='primary',use_container_width=True,key='convert_'+selected['name']):
    if not selected['attributes']: st.error('Add at least one attribute before conversion.')
    else:
     selected['status']='Completed'
     selected['updated']=datetime.now().strftime('%d %b %Y, %H:%M')
     st.session_state.history.insert(0,{'Model':selected['name'],'Status':'Completed','Attributes':len(selected['attributes']),'Time':selected['updated']})
     st.success('Demo conversion completed. Connect your conversion agent to generate actual PDM artifacts.')

with tab_pdm:
 st.subheader('Physical Data Models')
 st.dataframe(pd.DataFrame([{'PDM Name':'DIM_'+m['name'].upper(),'Domain':m['domain'],'Status':m['status'],'Columns':len(m['attributes'])} for m in st.session_state.models if m['status']=='Completed']),hide_index=True,use_container_width=True)
with tab_conv:
 st.subheader('Recent conversions')
 if st.session_state.history: st.dataframe(pd.DataFrame(st.session_state.history),hide_index=True,use_container_width=True)
 else: st.info('No conversions in this session. Select a BDM model and choose Convert to PDM.')
