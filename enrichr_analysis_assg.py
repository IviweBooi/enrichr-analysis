import os
import requests

# Ensure the enrichr_results directory exists - this is where you have results
results_dir = 'enrichr_results'
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Load genes from a file - you will have create a file that contains a list of up genes -- one gene per row of the file 
with open('High_tbx3_genes.txt', 'r') as file:
    genes_str = file.read()

# print(genes_str)

# List of databases to iterate over
databases = [
    'Achilles_fitness_decrease',
    'Achilles_fitness_increase',
    'ChEA_2022',
    'ClinVar_2019',
    'Drug_Perturbations_from_GEO_2014',
    'Drug_Perturbations_from_GEO_down',
    'Drug_Perturbations_from_GEO_up',
    'GO_Biological_Process_2023',
    'GO_Cellular_Component_2023',
    'GO_Molecular_Function_2023',
    'MSigDB_Hallmark_2020',
    'GTEx_Tissues_V8_2023',
    'GWAS_Catalog_2023',
    'IDG_Drug_Targets_2022',
    'KEA_2015',
    'KEGG_2021_Human',
    'LINCS_L1000_Chem_Pert_Consensus_Sigs',
    'LINCS_L1000_Chem_Pert_down',
    'LINCS_L1000_Chem_Pert_up',
    'MGI_Mammalian_Phenotype_Level_4_2021',
    'OMIM_Expanded',
    'PhenGenI_Association_2021',
    'PheWeb_2019',
    'Phosphatase_Substrates_from_DEPOD',
    'PPI_Hub_Proteins',
    'Proteomics_Drug_Atlas_2023',
    'Reactome_2022',
    'UK_Biobank_GWAS_v1',
    'WikiPathways_2019_Mouse'
]

# Enrichr URLs
ENRICHR_URL_ADDLIST = 'https://maayanlab.cloud/Enrichr/addList'
ENRICHR_URL_EXPORT = 'https://maayanlab.cloud/Enrichr/export'

# Submit gene list to Enrichr
description = 'SinkalaGeneList'
payload = {
    'list': (None, genes_str),
    'description': (None, description)
}
response = requests.post(ENRICHR_URL_ADDLIST, files=payload)
if not response.ok:
    raise Exception('Error analyzing gene list')

data = response.json()
user_list_id = data['userListId']
print(f"User List ID: {user_list_id}")

# Download enrichment results for each database
for database in databases:
    filename = f'High TBX3 {database}_table.txt' # CHANGE THE OUTPUT NAME
    file_path = os.path.join(results_dir, filename)
    
    # Construct the export URL with query parameters
    export_url = f"{ENRICHR_URL_EXPORT}?userListId={user_list_id}&filename={filename}&backgroundType={database}"
    
    # Stream download the file
    with requests.get(export_url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Results for {database} saved to {file_path}")
