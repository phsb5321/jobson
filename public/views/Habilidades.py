# Screen for 🛠️ Habilidades
import streamlit as st
import pandas as pd
import altair as alt
from modules.formater import Title
from modules.importer import DataImport
from config import Config
import utils as utl

def load_view():

    # Import data
    jobs_all = DataImport().fetch_and_clean_data()


    # Dictionary for skills and tools mapping, in order to have a correct naming
    keywords_skills = {
        'airflow': 'Airflow', 'alteryx': 'Alteryx', 'asp.net': 'ASP.NET', 'atlassian': 'Atlassian', 
        'excel': 'Excel', 'power_bi': 'Power BI', 'tableau': 'Tableau', 'srss': 'SRSS', 'word': 'Word', 
        'unix': 'Unix', 'vue': 'Vue', 'jquery': 'jQuery', 'linux/unix': 'Linux / Unix', 'seaborn': 'Seaborn', 
        'microstrategy': 'MicroStrategy', 'spss': 'SPSS', 'visio': 'Visio', 'gdpr': 'GDPR', 'ssrs': 'SSRS', 
        'spreadsheet': 'Spreadsheet', 'aws': 'AWS', 'hadoop': 'Hadoop', 'ssis': 'SSIS', 'linux': 'Linux', 
        'sap': 'SAP', 'powerpoint': 'PowerPoint', 'sharepoint': 'SharePoint', 'redshift': 'Redshift', 
        'snowflake': 'Snowflake', 'qlik': 'Qlik', 'cognos': 'Cognos', 'pandas': 'Pandas', 'spark': 'Spark', 'outlook': 'Outlook'
    }

    keywords_programming = {
        'sql' : 'SQL', 'python' : 'Python', 'r' : 'R', 'c':'C', 'c#':'C#', 'javascript' : 'JavaScript', 'js':'JS', 'java':'Java', 
        'scala':'Scala', 'sas' : 'SAS', 'matlab': 'MATLAB', 'c++' : 'C++', 'c/c++' : 'C / C++', 'perl' : 'Perl','go' : 'Go',
        'typescript' : 'TypeScript','bash':'Bash','html' : 'HTML','css' : 'CSS','php' : 'PHP','powershell' : 'Powershell',
        'rust' : 'Rust', 'kotlin' : 'Kotlin','ruby' : 'Ruby','dart' : 'Dart','assembly' :'Assembly',
        'swift' : 'Swift','vba' : 'VBA','lua' : 'Lua','groovy' : 'Groovy','delphi' : 'Delphi','objective-c' : 'Objective-C',
        'haskell' : 'Haskell','elixir' : 'Elixir','julia' : 'Julia','clojure': 'Clojure','solidity' : 'Solidity',
        'lisp' : 'Lisp','f#':'F#','fortran' : 'Fortran','erlang' : 'Erlang','apl' : 'APL','cobol' : 'COBOL',
        'ocaml': 'OCaml','crystal':'Crystal','javascript/typescript' : 'JavaScript / TypeScript','golang':'Golang',
        'nosql': 'NoSQL', 'mongodb' : 'MongoDB','t-sql' :'Transact-SQL', 'no-sql' : 'No-SQL','visual_basic' : 'Visual Basic',
        'pascal':'Pascal', 'mongo' : 'Mongo', 'pl/sql' : 'PL/SQL','sass' :'Sass', 'vb.net' : 'VB.NET','mssql' : 'MSSQL',
    }
    
    keywords_databases = {
        'mysql': 'MySQL',
    'mssql': 'MSSQL',
    'sql server': 'SQL Server',
    'sqlserver': 'SQL Server',
    'postgresql': 'PostgreSQL',
    'postgres': 'PostgreSQL',
    'sqlite': 'SQLite',
    'mongodb': 'MongoDB',
    'redis': 'Redis',
    'mariadb': 'MariaDB',
    'elasticsearch': 'Elasticsearch',
    'firebase': 'Firebase',
    'dynamodb': 'DynamoDB',
    'firestore': 'Firestore',
    'cassandra': 'Cassandra',
    'neo4j': 'Neo4j',
    'db2': 'DB2',
    'couchbase': 'Couchbase',
    'couchdb': 'CouchDB' 
    }
    
    keywords_cloud = {
    'aws': 'AWS',
    'amazon web services': 'Amazon Web Services',
    'azure': 'Azure',
    'google cloud': 'Google Cloud',
    'gcp': 'GCP',
    'ibm cloud': 'IBM Cloud',
    'oracle cloud': 'Oracle Cloud',
    'alibaba cloud': 'Alibaba Cloud',
    'alibabacloud': 'Alibaba Cloud',
    'alibaba': 'Alibaba',
    'digitalocean': 'DigitalOcean',
    'heroku': 'Heroku',
    'vmware': 'VMware',
    'vm ware': 'VMware',
    'vm-ware': 'VMware',
    'vmware cloud': 'VMware Cloud',
    'vm ware cloud': 'VMware Cloud',
    'vm-ware cloud': 'VMware Cloud',
    'vmwarecloud': 'VMware Cloud',
    'red hat': 'Red Hat',
    'redhat': 'Red Hat',
    'redhat cloud': 'Red Hat Cloud',
    'red hat cloud': 'Red Hat Cloud',
    'red-hat cloud': 'Red Hat Cloud',
    'redhatcloud': 'Red Hat Cloud',
    'red-hat cloud': 'Red Hat Cloud',
    'salesforce': 'Salesforce',
    'salesforce cloud': 'Salesforce Cloud',
    'salesforcecloud': 'Salesforce Cloud',
    'ibmcloud': 'IBM Cloud',
    'ibm-cloud': 'IBM Cloud',
    'oraclecloud': 'Oracle Cloud',
    'oracle-cloud': 'Oracle Cloud',
    'alibaba-cloud': 'Alibaba Cloud',
    'digital ocean': 'DigitalOcean',
    'digital-ocean': 'DigitalOcean',
    'digitalocean cloud': 'DigitalOcean Cloud',
    'digital ocean cloud': 'DigitalOcean Cloud',
    'digital-ocean cloud': 'DigitalOcean Cloud',
    'digitaloceancloud': 'DigitalOcean Cloud',
    'heroku cloud': 'Heroku Cloud',
    'herokucloud': 'Heroku Cloud',
    'openstack': 'OpenStack',
    'watson': 'Watson',
    'colocation': 'Colocation',
    'aurora': 'Aurora',
    'snowflake': 'Snowflake',
    'bigquery': 'BigQuery',
    'redshif': 'Redshift',  # Correcting typo
    'ovh': 'OVH',
    'linode': 'Linode',
    'managedhosting': 'Managed Hosting',
    'firebase': 'Firebase'
}

    
    keywords_libraries = {
    'pandas': 'Pandas', 'numpy': 'NumPy', 'scipy': 'SciPy', 'matplotlib': 'Matplotlib', 'seaborn': 'Seaborn',
    'plotly': 'Plotly', 'bokeh': 'Bokeh', 'altair': 'Altair', 'ggplot': 'GGplot', 'shiny': 'Shiny', 'd3': 'D3',
    'leaflet': 'Leaflet', 'keras': 'Keras', 'tensorflow': 'TensorFlow', 'pytorch': 'PyTorch', 'scikit-learn': 'Scikit-Learn',
    'xgboost': 'XGBoost', 'lightgbm': 'LightGBM', 'catboost': 'CatBoost', 'nltk': 'NLTK', 'spacy': 'spaCy', 'gensim': 'Gensim',
    'fastai': 'FastAI', 'caret': 'Caret', 'mlr': 'MLR', 'mlr3': 'MLR3', 'mlr3proba': 'MLR3 Proba', 'mlr3learners': 'MLR3 Learners',
    'mlr3tuning': 'MLR3 Tuning', 'mlr3pipelines': 'MLR3 Pipelines', 'mlr3misc': 'MLR3 Misc', 'mlr3filters': 'MLR3 Filters',
    'mlr3data': 'MLR3 Data', 'mlr3dbm': 'MLR3 DBM', 'mlr3cluster': 'MLR3 Cluster', 'mlr3c': 'MLR3C', 'jupyter': 'Jupyter',
    'theano': 'Theano', 'openCV': 'OpenCV', 'pyspark': 'PySpark', 'nlpack': 'NLPack', 'chainer': 'Chainer', 'fann': 'FANN',
    'shogun': 'Shogun', 'dlib': 'DLib', 'mxnet': 'MXNet', '.net': '.NET', 'kafka': 'Kafka', 'electron': 'Electron',
    'ionic': 'Ionic', 'xamarin': 'Xamarin', 'cordova': 'Cordova', 'dplyr': 'Dplyr', 'gtx': 'GTX', 'capacitor': 'Capacitor',
    'airflow': 'Airflow', 'nlr': 'NLR'
}

    
    keywords_webframeworks = {
    'node-js': 'Node.js', 'vue': 'Vue', 'vue.js': 'Vue.js', 'ember.js': 'Ember.js', 'emberjs': 'Ember.js', 'react': 'React',
    'react.js': 'React.js', 'angular': 'Angular', 'angular.js': 'Angular.js', 'angularjs': 'Angular.js', 'backbone.js': 'Backbone.js',
    'backbonejs': 'Backbone.js', 'express.js': 'Express.js', 'expressjs': 'Express.js', 'meteor.js': 'Meteor.js', 'meteorjs': 'Meteor.js',
    'next.js': 'Next.js', 'nextjs': 'Next.js', 'nuxt.js': 'Nuxt.js', 'nuxtjs': 'Nuxt.js', 'svelte': 'Svelte', 'svelte.js': 'Svelte.js',
    'sveltejs': 'Svelte.js', 'aurelia': 'Aurelia', 'aurelia.js': 'Aurelia.js', 'aureliajs': 'Aurelia.js', 'polymer': 'Polymer',
    'polymer.js': 'Polymer.js', 'polymerjs': 'Polymer.js', 'knockout.js': 'Knockout.js', 'knockoutjs': 'Knockout.js', 'riot.js': 'Riot.js',
    'riotjs': 'Riot.js', 'mithril': 'Mithril', 'mithril.js': 'Mithril.js', 'mithriljs': 'Mithril.js', 'preact': 'Preact', 'preact.js': 'Preact.js',
    'preactjs': 'Preact.js', 'inferno': 'Inferno', 'inferno.js': 'Inferno.js', 'infernojs': 'Inferno.js', 'hyperapp': 'Hyperapp',
    'hyperapp.js': 'Hyperapp.js', 'hyperappjs': 'Hyperapp.js', 'stimulus': 'Stimulus', 'stimulus.js': 'Stimulus.js', 'stimulusjs': 'Stimulus.js',
    'stimulus-reflex': 'Stimulus Reflex', 'stimulusreflex': 'Stimulus Reflex', 'stimulus_reflex': 'Stimulus Reflex', 'stimulus-reflex.js': 'Stimulus Reflex.js',
    'stimulusreflex.js': 'Stimulus Reflex.js', 'stimulus_reflex.js': 'Stimulus Reflex.js', 'stimulusreflexjs': 'Stimulus Reflex.js',
    'stimulus_reflexjs': 'Stimulus Reflex.js', 'sapper': 'Sapper', 'sapper.js': 'Sapper.js', 'sapperjs': 'Sapper.js',
    'ruby': 'Ruby', 'rubyonrails': 'Ruby on Rails', 'svelte': 'Svelte', 'blazor': 'Blazor', 'play framework': 'Play Framework',
    'demo': 'Demo', 'laravel': 'Laravel', 'flask': 'Flask', 'jquery': 'jQuery', 'fastapi': 'FastAPI'
}

    
    keywords_os = {
        'unix','linux', 'windows', 'macos', 'ios', 'android', 'ubuntu', 'debian', 'centos', 'fedora', 'redhat', 'suse', 'solaris', 'freebsd', 'openbsd', 'netbsd', 'aix', 'hp-ux', 'irix', 'os/2', 'os2', 'os2/warp', 'os2warp', 'os/2warp', 'os2warp', 'os/2 warp', 'os2 warp',
        'arch'
    }
    
    keywords_analyst_tools = {
        'excel', 'power_bi', 'tableau', 'qlik', 'alteryx', 'airflow', 'looker', 'superset', 'metabase', 'redash', 'mode', 'domo',
        'cognos', 'dax', 'datarobot', 'qlik', 'sap','powerpoint', 'spreadsheets'
    }
    

    
    # Skill sort, count, and filter list data
    def agg_skill_data(jobs_df):
        keywords_all = {**keywords_skills, **keywords_programming, **keywords_databases, **keywords_cloud, **keywords_libraries, **keywords_webframeworks}
        for index, row in jobs_df.iterrows():
            for i, token in enumerate(row['description_tokens']):
                if token.lower() in keywords_all:
                    row['description_tokens'][i] = keywords_all[token.lower()]
            jobs_df.at[index, 'description_tokens'] = row['description_tokens']
        skill_data = pd.DataFrame(jobs_df.description_tokens.sum()).value_counts().rename_axis('keywords').reset_index(name='counts')
        skill_data = skill_data[skill_data.keywords != '']
        skill_data['percentage'] = skill_data.counts / len(jobs_df)
        return skill_data


    

    skill_count = agg_skill_data(jobs_all)


    skill_type = ["Habilidades por popularidade", "Habilidades por pagamento"]
    skill_choice = st.radio("Tipo de gráfico:", skill_type, horizontal=True)
    # Top page build
    if(skill_choice == skill_type[0]):
        st.markdown("## 🛠️ Habilidades mais requisitadas")

        col1, col2, col3, col4 = st.columns(4)

        option = st.selectbox(
             'Emprego:',
            ['Todos os empregos'] + list(jobs_all['title'].unique())
        )

        # Filter jobs_all DataFrame based on the selected title
        if option == 'Todos os empregos':
            selected_job_data = jobs_all  # Show data for all job titles
        else:
            selected_job_data = jobs_all[jobs_all['title'] == option]
        
            
        keyword_list = ["Todos", "Linguagem", "Banco de Dados", "Cloud", "Bibliotecas", "Frameworks"] 
        keyword_choice = st.radio('Habilidade:', keyword_list, horizontal = True) # label_visibility="collapsed"
        
        # Skill list for slicer... NOT USED
        select_all = "Select All"
        skills = list(skill_count.keywords)
        skills.insert(0, select_all)

        # Number skill selctor for slider
        skill_dict = {"Top 10": 10, "Top 20": 20, "All 🥴" : len(skill_count)}
        top_n_choice = st.radio("Data Skills:", list(skill_dict.keys()))
        
        # Skill Filters - top n and languages
        skill_all_time = agg_skill_data(selected_job_data)
        
        skill_filter = skill_dict[top_n_choice]
        if keyword_choice == keyword_list[1]:
            skill_all_time = skill_all_time[skill_all_time.keywords.isin(list(keywords_programming.values()))]
        if keyword_choice == keyword_list[2]:
            skill_all_time = skill_all_time[skill_all_time.keywords.isin(list(keywords_databases.values()))]  
        if keyword_choice == keyword_list[3]:
            skill_all_time = skill_all_time[skill_all_time.keywords.isin(list(keywords_cloud.values()))]
        if keyword_choice == keyword_list[4]:
            skill_all_time = skill_all_time[skill_all_time.keywords.isin(list(keywords_libraries.values()))]
        if keyword_choice == keyword_list[5]:
            skill_all_time = skill_all_time[skill_all_time.keywords.isin(list(keywords_webframeworks.values()))]                
        skill_all_time = skill_all_time.head(skill_filter)
        skill_all_time_list = list(skill_all_time.keywords)



        # All time line chart
        selector = alt.selection_single(encodings=['x', 'y'])
        all_time_chart = alt.Chart(skill_all_time).mark_bar(
            cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10    
        ).encode(
            x=alt.X('keywords', sort=None, title="", axis=alt.Axis(labelFontSize=20) ),
            y=alt.Y('percentage', title="Probabilidade de estar em um Anúncio", axis=alt.Axis(format='%', labelFontSize=14, titleFontSize=14)),
            color=alt.condition(selector, 'percentage', alt.value('lightgray'), legend=None),
            tooltip=["keywords", alt.Tooltip("percentage", format=".1%")]
        ).add_selection(
            selector
        ).configure_view(
            strokeWidth=0
        )


    
        st.altair_chart(all_time_chart, use_container_width=True)
    


if __name__ == "__main__":
    load_view()
